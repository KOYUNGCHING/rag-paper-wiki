---
concept_id: retriever
status: verified
verified_sources:
  - dpr
  - rag
  - fid
  - self-rag
  - ragchecker
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

FiD 則把 retriever 視為外部模組，依 dataset 使用 DPR 或 BM25，沒有用 answer loss
joint-train retriever。[FID:fid-c06] [FID:fid-c08] 這讓 FiD 可專注 multi-passage reader，
也代表 retrieval error 不會在同一訓練流程中被自動修正。

## Self-RAG：何時啟動 retriever？

Self-RAG 把 retrieval timing 交給 Retrieve token，或用該 token 的 normalized
probability threshold 觸發檢索。[SELF-RAG:self-rag-c09] 實驗預設使用
Contriever-MS MARCO，但部分 tasks 另加 web search 或 GTR-XXL passages。
[SELF-RAG:self-rag-c13] 這表示 adaptive retrieval 與 retriever quality 是兩個不同
問題：模型可以正確決定「現在要找」，仍可能找回不理想的 passages。

目前來源：[DPR paper note](../papers/dpr.md)、[RAG paper note](../papers/rag.md)、
[FiD paper note](../papers/fid.md)、[Self-RAG paper note](../papers/self-rag.md)。

## RAGChecker：細粒度 retrieval diagnosis

RAGChecker 用 claim recall 與 chunk-level context precision 診斷 retriever。
[RAGCHECKER:ragchecker-c09] 實驗中固定 generator、只換 retriever，就能看到 claim recall
與 F1 一起改變。[RAGCHECKER:ragchecker-r05] 詳見
[Retrieval diagnostics](retrieval-diagnostics.md) 與 [RAGChecker paper note](../papers/ragchecker.md)。
