---
comparison_id: dpr-rag-fid
status: verified
verified_sources:
  - dpr
  - rag
  - fid
---

# DPR → RAG → FiD：檢索、生成與多篇融合

| 面向 | DPR | 原始 RAG | FiD |
| --- | --- | --- | --- |
| 核心問題 | 如何找到相關 passages？[DPR:dpr-c01] | 如何用外部 passages 支援 seq2seq generation？[RAG:rag-c10] | 如何讓 generator 擴展到大量 passages？[FID:fid-c03] |
| Retriever | Dual encoder + inner product。[DPR:dpr-c05] | 由 DPR 初始化。[RAG:rag-c06] | 使用既有 DPR 或 BM25。[FID:fid-c06] |
| Passage 處理 | 排序並交給 extractive reader。[DPR:dpr-c11] | 對 latent documents 的 generation probabilities marginalize。[RAG:rag-c03] | 各 passage 分開 encode，decoder jointly attend。[FID:fid-c03] |
| Generator | 無；使用 extractive reader | BART seq2seq。[RAG:rag-c07] | T5／BART-style seq2seq reader。[FID:fid-c07] |
| Retriever training | 訓練 dense retriever。[DPR:dpr-c07] | 更新 query encoder、固定 document encoder/index。[RAG:rag-c08] | 不 joint-train retriever。[FID:fid-c10] |

## 教學主線

```text
DPR：找到 evidence
  ↓
RAG：讓 generator 使用 retrieved evidence
  ↓
FiD：讓 generator 同時融合更多 passages
```

## 結果對照的限制

Natural Questions test 的 Table 1 報告 DPR 41.5、RAG 44.5、FiD-base 48.2、FiD-large
51.4 Exact Match。[FID:fid-r01] 這是一條直觀的歷史發展線，但不是乾淨的單變量
ablation：model size、reader/generator、training recipe 與 evidence aggregation 都不同。

