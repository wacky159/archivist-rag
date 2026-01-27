---
tags: [project, rag, langchain]
date: 2024-04-05
status: active
---

# Archivist-RAG 開發日誌

個人知識庫 RAG 系統的開發記錄與決策。

## 專案目標

建立一個能查詢個人 Markdown 筆記的 RAG 系統，支援：
- 自然語言提問
- 來源標註
- 本地優先（Ollama）

## 2024-04-05: 技術選型

### 為什麼選 LangChain LCEL？

考慮過的方案：
1. **LlamaIndex**: 更專注 RAG，但生態系較小
2. **純 OpenAI API**: 彈性高但要自己處理太多
3. **LangChain LCEL**: 平衡彈性與便利性

決定用 LCEL 因為：
- 原生 streaming 支援
- LangSmith 觀測性
- 社群活躍，資源多

### 為什麼選 Ollama？

隱私考量。個人筆記不想上傳到雲端。
選用模型：
- Embedding: `nomic-embed-text`（768 維，效能不錯）
- LLM: `llama3.2`（中文能力可接受）

## 2024-04-10: Chunking 策略

最初用 `RecursiveCharacterTextSplitter`，發現問題：
- Code blocks 被切斷
- 標題上下文丟失

改用 `MarkdownHeaderTextSplitter`：
- 按標題切分，保持結構
- 標題層級存在 metadata

參考 [[python-async]] 的結構測試效果。

## 2024-04-15: Multi-Query 實驗

問題：搜尋「並發」找不到「異步」相關筆記。

解決方案：`MultiQueryRetriever`
- LLM 生成 3-5 個查詢變體
- 合併搜尋結果

效果顯著改善，但延遲增加約 2 秒。

## 2024-04-20: 待辦事項

- [x] 基本 ingestion pipeline
- [x] Multi-query retrieval
- [ ] Contextual compression
- [ ] Streamlit UI
- [ ] 效能優化

## 學到的教訓

1. **先做 E2E，再優化**: 早期太執著於切片完美，應該先通才對
2. **本地模型夠用**: Llama 3.2 比預期好用
3. **Metadata 很重要**: 來源標註依賴 metadata，一開始就要設計好

## 相關資源

- [[system-design]] - 架構設計參考
- [[reading-notes]] - 軟體設計原則
- [[docker-basics]] - 部署考量
