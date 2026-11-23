---
concept_id: retriever
status: verified
verified_sources:
  - dpr
  - rag
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

原始 RAG 接續這個元件：以 DPR 初始化 retriever，再把 retrieved passages 交給
seq2seq generator。[RAG:rag-c06] [RAG:rag-c10]

## Retriever 是否成功？

可用 [Top-k retrieval accuracy](top-k-evaluation.md) 檢查前 k 個 passages 中是否
至少有一段包含答案。[DPR:dpr-c09] 這與最終答案的 Exact Match 不同，兩層錯誤
必須分開診斷。

## Training boundary

原始 RAG 的 task fine-tuning 會更新 query encoder，但保持 document encoder 與 index
固定。[RAG:rag-c08] 因此「retriever 會訓練」必須進一步說明哪一部分會更新。

目前來源：[DPR paper note](../papers/dpr.md)、[RAG paper note](../papers/rag.md)。FiD、
Self-RAG 與 RAGChecker ingest 後會補上多文件整合、何時檢索及細粒度評估。

