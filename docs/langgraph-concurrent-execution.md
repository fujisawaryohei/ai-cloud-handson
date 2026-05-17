# LangGraph の並列実行と Python 並行処理の仕組み

## 1. `tools_by_name` パターン

### なぜ list ではなく dict にするか

LLM が返す `tool_call` は、呼び出すツールを **文字列の name** で指定する。
実行には **tool オブジェクト本体** が必要なため、name → tool のマッピングが必要になる。

```python
# list のまま → 毎回線形探索 O(n)
for tool in tools:
    if tool.name == tool_call["name"]:
        tool.invoke(...)

# dict に変換 → O(1) で引ける
tools_by_name = {tool.name: tool for tool in tools}
tool = tools_by_name[tool_call["name"]]
```

これは **ディスパッチテーブルパターン** と呼ばれる。
ツールが増えても `use_tool` 側のコードは変えなくてよい（開放閉鎖原則）。

---

## 2. Python の Future

**「まだ完了していない非同期処理の結果を表すオブジェクト」**。

```python
# 通常の関数：呼んだ瞬間にブロック
result = 重い処理()

# Future：呼んだ瞬間に即返る。処理はバックグラウンドで進む
future = 重い処理()
result = future.result()   # ここで完了を待つ
```

### 実行開始と待機のタイミング

| タイミング | 何が起きるか |
|-----------|-------------|
| `use_tool(tool_call)` を呼んだ瞬間 | 実行**開始** + Future を返す |
| `future.result()` を呼んだ瞬間 | 完了を**待つ**（完了済みなら即返る） |

### 並列実行が成立する理由

```python
# ① 全ツールを同時に起動
futureA = use_tool(tool_callA)   # A の実行開始
futureB = use_tool(tool_callB)   # B の実行開始（A と並行）
futureC = use_tool(tool_callC)   # C の実行開始（A,B と並行）

# ② 完了を順番に待つだけ
resultA = futureA.result()
resultB = futureB.result()
resultC = futureC.result()
```

`.result()` のタイミングで実行開始するなら逐次実行になってしまう。
起動時に実行開始するから並列になる。

---

## 3. `@task` デコレータ

`@task` が元の関数を「バックグラウンドで実行して Future を返す関数」に差し替える。

```python
@task
def use_tool(tool_call):
    ...
    return ToolMessage(...)   # 関数自体は ToolMessage を返すが...

future = use_tool(tool_call)   # 呼び出し元が受け取るのは Future<ToolMessage>
result = future.result()       # ここで ToolMessage を取り出す
```

デコレータの仕組み：

```python
# @task は以下と等価
use_tool = task(use_tool)   # 元の関数を受け取り、ラッパーに差し替える
```

---

## 4. LangGraph ランタイムと Python 標準の比較

```
Python 標準                    LangGraph
─────────────────────          ─────────────────────────────────
ThreadPoolExecutor             LangGraph ランタイム
  └─ submit() → Future           └─ @task 呼び出し → Future
     └─ .result() で待つ              └─ .result() で待つ

       ↑ ここまでは同じインターフェース

                                  ├─ チェックポイント連携（MemorySaver）
                                  ├─ interrupt() によるサスペンド・再開
                                  └─ @entrypoint との統合
```

LangGraph は `concurrent.futures` 互換のインターフェースを維持しながら、
エージェント固有の機能（中断・再開・状態保存）を統合している。

---

## 5. GIL（Global Interpreter Lock）

### GIL とは

CPython（標準の Python 実装）が持つ、
**一度に1スレッドしか Python バイトコードを実行させないためのロック機構**。

```
OS レベル      : スレッドは複数存在し、カーネルがスケジューリング
CPython レベル : GIL により Python コード実行は同時に1スレッドのみ
```

OS は GIL を知らない。GIL はあくまで CPython 内部のロック。

### なぜ GIL が存在するか

CPython がオブジェクトの **参照カウント** でメモリ管理しているため。
複数スレッドが同時に参照カウントを書き換えると競合・メモリ破壊が起きるため GIL で保護している。

### I/O 待ち中に GIL が解放される流れ

```
スレッドA が GIL を保持して Python コードを実行
  └─ I/O 発生（HTTP リクエスト送信など）
       ├─ GIL を解放
       ├─ スレッドA は I/O 待ち（CPU は使わない）
       └─ スレッドB が GIL を取得 → Python コードを実行開始
            └─ スレッドA の I/O 完了 → GIL 返還を要求 → スレッドB が解放 → スレッドA が再取得
```

### I/O バウンド vs CPU バウンド

| 種類 | CPU の状態 | GIL | 並列効果 |
|------|-----------|-----|---------|
| I/O バウンド（HTTP, ファイル等） | 遊んでいる（待ち） | 解放される | あり |
| CPU バウンド（純粋な計算） | フル稼働 | 解放されない | なし |

```python
# I/O バウンド（GIL が解放される）
response = requests.get("https://...")   # ネットワーク応答待ち

# CPU バウンド（GIL が解放されない）
result = sum(range(10_000_000))          # CPU がずっと計算
```

### このコードへの当てはめ

| ツール | 内部処理 | 並列効果 |
|--------|---------|---------|
| `TavilySearch` | HTTP リクエスト（I/O） | GIL 解放 → 真の並列 |
| `write_file` | ファイル書き込み（I/O） | GIL 解放 → 真の並列 |

エージェントのツール実行は I/O バウンドがほとんどなので、スレッドベースで十分。
CPU バウンドを並列化したい場合は `ProcessPoolExecutor`（マルチプロセス）が必要。

### Python 3.13 以降

GIL をオプションで無効化できる **"free-threaded Python"** が実験的に導入。
将来的には GIL 撤廃の方向に進んでいる。
