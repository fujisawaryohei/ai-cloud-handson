# Bedrockで利用可能なモデルプロバイダー

## 概要

Amazon Bedrockは、数百個のトップファウンデーションモデル（FM）へのアクセスを提供し、コードを書き直すことなくモデルを入れ替える柔軟性を備えています。これにより、ニーズの進化に応じてアプリケーションを構築し、革新することができます。

## サポートされているモデルプロバイダー

Bedrockでは、以下の**17個のモデルプロバイダー**がサポートされています：

### 1. **AI21 Labs**
- Jamba 1.5 Large
- Jamba 1.5 Mini

### 2. **Amazon**
テキスト生成、埋め込み、画像生成などの多様なモデルを提供：
- **Amazon Nova** シリーズ：
  - Multimodal Embeddings
  - Nova 2 Lite
  - Nova 2 Sonic
  - Nova Canvas（画像生成）
  - Nova Lite
  - Nova Micro
  - Nova Premier
  - Nova Pro
  - Nova Reel（動画生成）
  - Nova Sonic

- **Amazon Titan** シリーズ：
  - Titan Embeddings G1 - Text
  - Titan Image Generator G1 v2
  - Titan Multimodal Embeddings G1
  - Titan Text Embeddings V2
  - Titan Embeddings G1 - Text v2
  - Titan Text Large

### 3. **Anthropic**
高性能なClaudeシリーズモデル：
- **Claude 4.x:**
  - Claude Opus 4.7
  - Claude Opus 4.6
  - Claude Sonnet 4.6
  - Claude Haiku 4.5
  - Claude Opus 4.5
  - Claude Sonnet 4.5
  - Claude Sonnet 4
  - Claude Opus 4.1

- **Claude 3.x:**
  - Claude 3.5 Haiku
  - Claude 3 Haiku

- **Preview:**
  - Claude Mythos Preview

### 4. **Cohere**
テキスト生成と埋め込みモデル：
- Rerank 3.5
- Command R
- Command R+
- Embed English
- Embed Multilingual
- Embed v4

### 5. **DeepSeek**
高度な推論能力を持つモデル：
- DeepSeek V3.2
- DeepSeek-V3.1
- DeepSeek-R1

### 6. **Google**
Gemmaシリーズモデル：
- Gemma 3 12B IT
- Gemma 3 27B PT
- Gemma 3 4B IT

### 7. **Meta**
Llamaシリーズの大規模言語モデル：
- **Meta 3.x:**
  - Llama 3.3 70B Instruct
  - Llama 3.2 11B Instruct
  - Llama 3.2 1B Instruct
  - Llama 3.2 3B Instruct
  - Llama 3.2 90B Instruct
  - Llama 3.1 405B Instruct
  - Llama 3.1 70B Instruct
  - Llama 3.1 8B Instruct
  - Llama 3 70B Instruct
  - Llama 3 8B Instruct
  - Llama 4 Maverick 17B Instruct
  - Llama 4 Scout 17B Instruct

### 8. **MiniMax**
- MiniMax M2.5
- MiniMax M2.1
- MiniMax M2

### 9. **Mistral AI**
多様な用途に対応したモデル：
- Ministral 14B 3.0
- Devstral 2 123B
- Magistral Small 2509
- Ministral 3 8B
- Ministral 3B
- Mistral 7B Instruct
- Mistral Large
- Mistral Large 3
- Mistral Small
- Mixtral 8x7B Instruct
- Pixtral Large（マルチモーダル）
- Voxtral Mini 3B 2507
- Voxtral Small 24B 2507

### 10. **Moonshot AI**
会話型AI：
- Kimi K2.5
- Kimi K2 Thinking

### 11. **NVIDIA**
高性能推論モデル：
- NVIDIA Nemotron Nano 12B v2 VL BF16
- NVIDIA Nemotron Nano 9B v2
- Nemotron Nano 3 30B
- NVIDIA Nemotron 3 Super 120B

### 12. **OpenAI**
- GPT OSS Safeguard 120B
- GPT OSS Safeguard 20B
- gpt-oss-120b
- gpt-oss-20b

### 13. **Qwen**
多言語対応モデル：
- Qwen3 235B A22B 2507
- Qwen3 32B
- Qwen3 Coder 480B A35B Instruct
- Qwen3 Coder Next
- Qwen3 Next 80B A3B
- Qwen3 VL 235B A22B
- Qwen3-Coder-30B-A3B-Instruct

### 14. **Stability AI**
画像処理・編集モデル：
- Stable Image Conservative Upscale
- Stable Image Control Sketch
- Stable Image Control Structure
- Stable Image Creative Upscale
- Stable Image Erase Object
- Stable Image Fast Upscale
- Stable Image Inpaint
- Stable Image Outpaint
- Stable Image Remove Background
- Stable Image Search and Recolor
- Stable Image Search and Replace
- Stable Image Style Guide
- Stable Image Style Transfer

### 15. **TwelveLabs**
ビデオ/マルチメディア埋め込み：
- Marengo Embed 3.0
- Marengo Embed v2.7
- Pegasus v1.2

### 16. **Writer**
テキスト生成とビジョンモデル：
- Palmyra X4
- Palmyra X5
- Palmyra Vision 7B

### 17. **Z.AI**
- GLM 4.7
- GLM 4.7 Flash
- GLM 5

---

## モデルの能力範囲

Bedrockで利用可能なモデルは、以下のような多様な機能をカバーしています：

- **テキスト生成**：会話型AI、文章作成、コード生成など
- **埋め込み（Embeddings）**：テキストとマルチモーダル埋め込み
- **画像生成**：テキストから画像への生成
- **マルチモーダル処理**：テキスト、画像、動画の処理
- **再ランキング（Reranking）**：検索結果の最適化
- **画像編集**：アップスケーリング、修復、背景除去など

---

## API参考

モデルの一覧を取得するには、`list_foundation_models` APIを使用できます。このAPIは以下のフィルタリングオプションをサポートしています：

- **プロバイダー**：特定のプロバイダーでフィルタリング
- **カスタマイズタイプ**：ファインチューニング、蒸留など
- **出力モダリティ**：テキスト、画像、埋め込みなど
- **推論タイプ**：オンデマンド、プロビジョニング

---

## 出典

- AWS Bedrock Models at a glance: https://docs.aws.amazon.com/bedrock/latest/userguide/model-cards.html
