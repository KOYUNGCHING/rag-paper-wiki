---
concept_id: chunk
status: verified
verified_sources:
  - dpr
  - rag
  - fid
  - ragchecker
---

# Chunk 與 retrieval unit

Retriever 通常不是把整份長文件當成單一候選，而是搜尋較小的 passages／chunks。
DPR 的實驗將 Wikipedia 文件切成固定長度、彼此不重疊的 text blocks，並附上文章
標題。[DPR:dpr-c08]

## 為什麼 chunk 重要？

Chunk 是 retriever 實際排序的單位。切得太大會混入過多無關內容；切得太小可能
失去回答所需上下文。後兩句是本 Wiki 為教學提出的設計推論，標記為
`wiki_synthesis`，不是 DPR 論文直接比較並證實的普遍結論。

原始 RAG 已把 Wikipedia passage index 共用於多種 knowledge-intensive tasks，並將
retrieved passage 與 input 一起交給 generator。[RAG:rag-c09] [RAG:rag-c07] 這表示
chunk 不只是 retriever 的輸出單位，也會直接影響 generator 能看到的 context。

FiD 同樣使用固定長度、互不重疊的 Wikipedia passages，並把每篇 passage 當作獨立
encoder unit。[FID:fid-c12] 當 retrieved passages 增加時，實驗曲線在觀察範圍內上升，
但 encoder/decoder 成本也增加。[FID:fid-r03]

## RAGChecker：chunk 大小與雜訊

RAGChecker 把 retriever precision 定在 chunk level，因為固定大小 chunk 可能同時含有
相關與無關內容。[RAGCHECKER:ragchecker-c10] 作者觀察較大 chunk 提高 context precision
與 claim recall，而 chunk overlap 影響不大。[RAGCHECKER:ragchecker-c27]
[RAGCHECKER:ragchecker-c29] 預設設定是 300 tokens、overlap 0.2。[RAGCHECKER:ragchecker-c19]

## 術語對照（`wiki_synthesis`）

五篇論文對「檢索單位」用詞不同。本 Wiki 在各論文頁保留原論文用詞，在教學與簡報中統一說
「chunk（檢索片段）」。

| 論文 | 原文用詞 | 來源 |
| --- | --- | --- |
| DPR | passage（固定長度、不重疊 text blocks） | [DPR:dpr-c08] |
| 原始 RAG | document／passage | [RAG:rag-c09] |
| FiD | passage | [FID:fid-c12] |
| Self-RAG | passage | 見 [Self-RAG paper note](../papers/self-rag.md) |
| RAGChecker | chunk（固定 token 數，預設 300 tokens、overlap 0.2） | [RAGCHECKER:ragchecker-c19] |

注意 DPR 與 FiD 的 passages 不重疊，RAGChecker 的預設 chunks 有 0.2 overlap；切分方式不同，
各論文的數字不能直接互比。

相關頁面：[Retriever](retriever.md)、[Embedding](embedding.md)、
[Context augmentation](context-augmentation.md)、[Retrieval diagnostics](retrieval-diagnostics.md)。
