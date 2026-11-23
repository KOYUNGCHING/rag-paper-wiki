---
comparison_id: dpr-to-rag
status: verified
verified_sources:
  - dpr
  - rag
---

# 從 DPR 到 RAG：由找資料到用資料生成

## 核心差異

| 問題 | DPR | 原始 RAG |
| --- | --- | --- |
| 主要目標 | 從大型 corpus 找到相關 passages。[DPR:dpr-c01] | 將 retrieved passages 提供給 seq2seq generator。[RAG:rag-c10] |
| Retriever | Question／passage dual encoder，以 inner product 排序。[DPR:dpr-c05] | 由 DPR 初始化，使用 dense index 與 MIPS。[RAG:rag-c06] |
| 最終輸出 | Extractive reader 從 passages 找 answer span。[DPR:dpr-c11] | BART 根據 input 與 passage 生成 sequence。[RAG:rag-c07] |
| 外部知識角色 | 被搜尋的 passage collection | 可讀、可替換的 non-parametric memory。[RAG:rag-c02] |
| 訓練重點 | Positive／negative passages 與 dense retriever。[DPR:dpr-c07] | Query encoder 與 generator fine-tuning；document encoder/index 固定。[RAG:rag-c08] |

## 發展關係

```text
DPR：Question → dense retrieval → passages → extractive reader
                         ↓
RAG：Question → dense retrieval → passages → seq2seq generator
```

RAG 沒有取代 DPR 的 retrieval idea，而是把它當作 non-parametric memory access
mechanism，再加入 context augmentation、generation 與 latent-document
marginalization。[RAG:rag-c03]

## 結果不能直接當成純架構比較

Natural Questions test 中，RAG-Sequence 的 Exact Match 為 44.5，DPR 為 41.5。
[RAG:rag-r01] 但兩者的 reader/generator、training objective 與輸出方式不同，因此這個
結果支援「在該設定下 RAG system 較高」，不能單獨證明 generation 永遠優於 extraction。

