# Tavilyについてのレポート

## 概要
**Tavily（タビリー）**は、大規模言語モデル（LLM）とAIエージェント向けに特化した専門的な検索エンジンです。AI開発者を念頭に設計され、リアルタイムで正確かつ偏りのない情報提供を実現します。

## 主な特徴

### 1. **AI/LLM向けに最適化**
- LLMが外部情報を利用する際に、誤情報（Hallucination）のリスクを抑える
- 正確かつ事実に基づいた検索結果を提供

### 2. **カスタマイズ可能な検索パラメータ**
- 検索深度の調整
- 対象ドメインの指定
- 取得件数の柔軟な設定
- 用途に応じた最適な結果取得が可能̦

### 3. **多言語対応とリアルタイム性**
- リアルタイムで最新情報にアクセス可能
- 複数言語に対応
- API経由での結果取得は数秒以内

### 4. **統合の容易さ**
- Python SDK（tavily-python）の提供
- Node.js対応
- **LangChain**、**LlamaIndex**などの既存フレームワークとの簡単な統合
- AWS Bedrock エージェントなどとも連携可能

## 対応プログラミング言語

### Python
```python
from tavily import TavilyClient

# クライアント生成
tavily_client = TavilyClient(api_key="tvly-YOUR_API_KEY")

# 検索実行
response = tavily_client.search("Who is Leo Messi?")
print(response)
```

### LangChainでの利用
```python
from langchain.retrievers.tavily_search_api import TavilySearchAPIRetriever

retriever = TavilySearchAPIRetriever(k=3)
res = retriever.invoke("LangChainの最新情報を日本語で教えて")
print(res)
```

### Node.js
```javascript
const { tavily } = require('@tavily/core');
const tvly = tavily({ apiKey: "tvly-YOUR_API_KEY" });

tvly.search("Who is Leo Messi?")
    .then(results => console.log(results))
    .catch(err => console.error(err));
```

### cURL
```bash
curl -X POST "https://api.tavily.com/search" \
  -H 'Content-Type: application/json' \
  -H 'Authorization: Bearer tvly-YOUR_API_KEY' \
  -d '{"query": "Who is Leo Messi?"}'
```

## API キーの取得方法

1. **サインアップ**
   - Tavilyの公式サイトにアクセスしてアカウントを作成

2. **API キー取得**
   - アカウント作成後、ダッシュボードからAPI キーを入手

3. **環境変数設定例（Python）**
   ```python
   import getpass
   import os
   
   os.environ["TAVILY_API_KEY"] = getpass.getpass("Enter your Tavily API Key: ")
   ```

## AI フレームワークとの統合例

### LangChain統合
- Tavilyを検索ツールとしてAIエージェントに組み込み
- エージェントのプロンプト内に検索結果をコンテキストとして組み込み
- より最新かつ正確な回答を実現

### AWS Bedrock連携
- Lambda関数内でTavily APIを呼び出し
- Web検索結果をAIエージェントへ返す実装が可能

## サポートと無料プラン

- **公式ドキュメント**: API リファレンス、SDK使用方法、ガイドラインを提供
- **コミュニティサポート**: 
  - メール: support@tavily.com
  - GitHub、LinkedInでのサポート
- **無料プラン**: 試用版から導入を検討可能

## 利用シーン

- AIチャットボットの情報検索機能
- AIエージェントの意思決定支援
- LLMベースのリサーチツール
- リアルタイムデータが必要なAIアプリケーション
- 企業のナレッジシステム構築

## まとめ

Tavilyは、LLMやAIエージェントが最新のWeb情報をリアルタイムで取得するための強力で実用的なツールです。AI開発者向けに最適化された設計により、正確で信頼性の高い検索体験を提供し、様々なAIアプリケーションの開発を支援します。

---
*レポート作成日: 2024年*
