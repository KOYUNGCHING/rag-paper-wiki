---
concept_id: retriever
status: verified
verified_sources:
  - dpr
---

# 檢索器（Retriever）

Retriever 的工作是從大型語料庫選出一小組與問題相關的 passages，讓後續 reader
不必讀完整個 corpus。DPR 論文把 open-domain QA 描述為「先 retrieve、再 read」的
兩階段流程。[DPR:dpr-c01]

## 在系統中的位置

```text
問題 → Retriever → Top-k passages → Reader
```

DPR 本身改善的是 Retriever。它不等於完整回答系統，也不等於 generative RAG；
原論文的答案仍由 extractive reader 從 passage 中擷取。[DPR:dpr-c11]

## Retriever 是否成功？

可用 [Top-k retrieval accuracy](top-k-evaluation.md) 檢查前 k 個 passages 中是否
至少有一段包含答案。[DPR:dpr-c09] 這與最終答案的 Exact Match 不同，兩層錯誤
必須分開診斷。

## 目前來源範圍

目前只由 [DPR paper note](../papers/dpr.md) 驗證。RAG、FiD、Self-RAG 與
RAGChecker ingest 後會補上 retriever 如何與 generator 互動、何時檢索及如何評估。

