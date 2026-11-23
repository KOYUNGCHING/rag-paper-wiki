---
concept_id: chunk
status: verified
verified_sources:
  - dpr
  - rag
---

# Chunk 與 retrieval unit

Retriever 通常不是把整份長文件當成單一候選，而是搜尋較小的 passages／chunks。
DPR 的實驗將 Wikipedia 文件切成固定長度、彼此不重疊的 text blocks，並附上文章
標題。[DPR:dpr-c08]

## 為什麼 chunk 重要？

Chunk 是 retriever 實際排序的單位。切得太大會混入過多無關內容；切得太小可能
失去回答所需上下文。後兩句是本 Wiki 為教學提出的設計推論，標記為
`wiki_synthesis`，不是 DPR 論文直接比較並證實的普遍結論。

後續 ingest 會檢查 RAG、FiD 等論文如何使用多個 retrieved passages，再擴充 chunk
與 generator context 的關係。

原始 RAG 已把 Wikipedia passage index 共用於多種 knowledge-intensive tasks，並將
retrieved passage 與 input 一起交給 generator。[RAG:rag-c09] [RAG:rag-c07] 這表示
chunk 不只是 retriever 的輸出單位，也會直接影響 generator 能看到的 context。

相關頁面：[Retriever](retriever.md)、[Embedding](embedding.md)、
[Context augmentation](context-augmentation.md)。

