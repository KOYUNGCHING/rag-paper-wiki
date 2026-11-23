---
comparison_id: five-paper-overview
status: verified
verified_sources:
  - dpr
  - rag
  - fid
  - self-rag
  - ragchecker
---

# 五篇總覽：從找資料、用資料，到診斷錯誤

本頁延續 [DPR → RAG → FiD → Self-RAG](dpr-rag-fid-self-rag.md)，加入 RAGChecker。
整條發展線是 `wiki_synthesis`，不是宣稱後一篇在所有任務上勝過前一篇。

| 面向 | DPR | 原始 RAG | FiD | Self-RAG | RAGChecker |
| --- | --- | --- | --- | --- | --- |
| 核心問題 | 如何找 passages？[DPR:dpr-c01] | 如何讓 generator 用外部 passages？[RAG:rag-c10] | 如何融合大量 passages？[FID:fid-c03] | 何時找、如何評估 passage／output？[SELF-RAG:self-rag-c02] | 答錯時是 retriever 還是 generator 的問題？[RAGCHECKER:ragchecker-c05] |
| 類型 | Retriever | RAG architecture | Reader／generator architecture | 訓練出的控制機制 | 外部評估框架 |
| 評估單位 | Top-k retrieval accuracy | Task metrics | Exact Match | Task + citation metrics [SELF-RAG:self-rag-c11] | Claims 與 chunks [RAGCHECKER:ragchecker-c03] |

## 教學發展線

```text
DPR         找到 evidence
  ↓
RAG         讓 generator 使用 evidence
  ↓
FiD         融合更多 passages
  ↓
Self-RAG    決定何時找，並在生成中評估 passage 與 output
  ↓
RAGChecker  從外部拆解：錯在檢索，還是錯在生成？
```

## RAGChecker 如何連回前四篇

- **DPR 的 retriever**：RAGChecker 用 claim recall 與 context precision 取代「是否含答案」
  的 top-k 判斷。[RAGCHECKER:ragchecker-c09] 實驗也顯示 dense retriever（E5-Mistral）
  在 8 個系統平均上比 BM25 有較高 claim recall。[RAGCHECKER:ragchecker-r05] 但這不是 DPR
  本身，不能當成 DPR 的再驗證。
- **RAG／FiD 的「給更多 passages」**：FiD 觀察到更多 passages 在其設定下提高 Exact
  Match。[FID:fid-r03] RAGChecker 補上另一面：更多 context 也讓 relevant noise
  sensitivity 上升（author observation）。[RAGCHECKER:ragchecker-c27]
- **Self-RAG 的 IsSup／IsRel**：Self-RAG 讓模型自己預測 support 與 relevance
  [SELF-RAG:self-rag-c04]；RAGChecker 是另一個 LLM 從外部判斷 claim 是否被 chunk 支持。
  [RAGCHECKER:ragchecker-c07] 兩者都不是 ground truth，也不應互相當作驗證。

## 結果比較的邊界

五篇的 datasets、models 與 metrics 都不同；RAGChecker 的 F1 是 claim-level
[RAGCHECKER:ragchecker-c08]，與 FiD 的 Exact Match 不是同一尺度。這張表只比較研究問題
與評估視角，不是排行榜。
