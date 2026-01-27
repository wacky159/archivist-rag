# 📚 Archivist-RAG: 基於 LangChain 的個人 Markdown 知識庫

**Archivist-RAG** 是一個專為個人 Markdown 筆記（如 Obsidian, Logseq）設計的 RAG 系統。本專案採用 **業界標準的 LangChain LCEL 架構**，展現高度的可擴展性、可觀察性與生產環境就緒（Production-Ready）的工程設計。

---

## 🌟 核心亮點

* **標題感知切片 (Header-Aware Chunking)**：利用 `MarkdownHeaderTextSplitter` 保持筆記結構，確保 AI 檢索時具備完整的層級上下文。
* **現代 LCEL 架構**：完全使用 LangChain Expression Language 編寫，支援原生異步處理與串流輸出（Streaming）。
* **多查詢檢索 (Multi-Query Retrieval)**：自動將使用者問題擴充為多個維度，解決個人筆記關鍵字不精準的痛點。
* **本地優先**：使用 Ollama (Llama 3.2 + nomic-embed-text)，資料不離開本機，保護個人隱私。
* **完整觀測性**：可選整合 LangSmith，透明化展示 Token 消耗與 Chain 執行鏈路。

---

## 🛠️ 技術棧

* **Orchestration:** LangChain (LCEL)
* **Vector Database:** ChromaDB (Local-first)
* **Embedding Models:** Ollama `nomic-embed-text`
* **LLMs:** Ollama Llama 3.2
* **Interface:** Streamlit

---

## 🏗️ 系統架構

```
┌─────────────────────────────────────────────────────────────────┐
│                        Streamlit UI                              │
└────────────────────────────┬────────────────────────────────────┘
                             │ query
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      RETRIEVAL CHAIN                             │
│  Multi-Query → Vector Search → Contextual Compression            │
└────────────────────────────┬────────────────────────────────────┘
                             │ context
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                      GENERATION                                  │
│  Prompt Template → Ollama Llama 3.2 → Answer with Citations      │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                   INGESTION PIPELINE                             │
│  Scan .md → Header Splitter → Frontmatter → Embed → ChromaDB    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 快速上手

### 前置需求

1. Python 3.9+
2. [Ollama](https://ollama.ai/) 已安裝並運行

### 1. 安裝 Ollama 模型

```bash
ollama pull nomic-embed-text
ollama pull llama3.2
```

### 2. 安裝專案

```bash
git clone https://github.com/your-username/archivist-rag.git
cd archivist-rag
pip install -e .
```

### 3. 設定環境變數（可選）

複製並編輯環境變數：

```bash
cp .env.example .env
```

預設設定：
```env
NOTES_PATH=./sample_notes
CHROMA_PATH=./data/chroma
OLLAMA_BASE_URL=http://localhost:11434
```

### 4. 執行 Ingestion

```bash
python scripts/ingest.py
```

### 5. 啟動對話介面

```bash
streamlit run app.py
```

---

## 📁 專案結構

```
archivist-rag/
├── src/
│   ├── config.py           # 設定管理
│   ├── embeddings.py       # Ollama embeddings
│   ├── ingestion/          # Ingestion pipeline
│   ├── retrieval/          # Retrieval chain
│   └── generation/         # Generation chain
├── scripts/
│   └── ingest.py           # Ingestion CLI
├── sample_notes/           # 範例筆記
├── app.py                  # Streamlit UI
└── data/chroma/            # Vector database
```

---

## 📊 效能評估 (Evaluation)

本專案預計採用 **Ragas** 框架進行基準測試（待完成）：

| 指標 (Metric) | 目標 | 說明 |
| --- | --- | --- |
| **Faithfulness** | > 0.9 | 回答內容忠實於原始筆記，無幻覺。 |
| **Answer Relevancy** | > 0.85 | 回答能精準命中使用者提問的核心。 |
| **Context Precision** | > 0.8 | 檢索到的筆記片段與問題高度相關。 |

---

## 📝 實作心得與工程挑戰

* **挑戰 1：處理破碎的 Markdown 結構**
  * *解決方案*：採用 `MarkdownHeaderTextSplitter` 代替字數切分，避免了程式碼區塊或清單被強行切斷的問題。

* **挑戰 2：檢索噪音過多**
  * *解決方案*：引入了 `Contextual Compression`，在餵給 LLM 之前對檢索結果進行二次精煉。

* **挑戰 3：個人筆記用詞不一致**
  * *解決方案*：使用 `MultiQueryRetriever` 自動生成查詢變體，提升召回率。
