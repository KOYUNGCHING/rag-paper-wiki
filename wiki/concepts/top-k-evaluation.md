---
concept_id: top-k-evaluation
status: verified
verified_sources:
  - dpr
  - rag
  - fid
  - ragchecker
---

# Top-k retrieval evaluation

Top-k retrieval accuracy 衡量：對多少問題而言，前 k 個 retrieved passages 中至少有
一段包含答案。它不是前 k 段中「正確 passages 所占比例」。[DPR:dpr-c09]

## 與最終答案評估的差異

- **Retrieval accuracy**：需要的證據有沒有被找進候選集合？
- **Exact Match**：系統最後輸出的答案是否符合參考答案？

Natural Questions 的 Single setting 中，DPR 在 Top-20 retrieval accuracy 與
end-to-end Exact Match 都高於 BM25。[DPR:dpr-r01] [DPR:dpr-r04] 這支持兩者可能
相關，但 SQuAD 的反例表示不能把改善寫成無條件保證。[DPR:dpr-r02]
[DPR:dpr-r05]

## 比較數字時必須保留

- dataset 與 split
- k 值
- Single 或 Multi training
- retriever／reader 設定
- metric 名稱

## 在 generation RAG 中的額外影響

原始 RAG 不只用 top-k 作為 retrieval cutoff，也會對 top-k latent documents 的生成
機率做 marginalization。[RAG:rag-c03] 因此增加 k 會同時改變可見 evidence、計算量與
generation distribution。Figure 3 顯示 RAG-Sequence 與 RAG-Token 對 k 的反應不同，
不能假設文件越多越好。[RAG:rag-r06]

FiD 在三個 validation curves 的顯示範圍內，隨 retrieved passages 增加而提高 Exact
Match。[FID:fid-r03] 這和原始 RAG 的 variant-dependent response 不同，顯示 k 的
效果取決於 fusion architecture、task 與運算預算。

## RAGChecker：k 對生成端的影響

RAGChecker 的 Appendix F 觀察到，增加 k 會提高 claim recall 但降低 context precision，
同時 relevant noise sensitivity 上升（author observation）。[RAGCHECKER:ragchecker-c27]
這補充了 DPR／FiD 只看 retrieval accuracy 或 Exact Match 的視角；詳見
[Retrieval diagnostics](retrieval-diagnostics.md)。

相關頁面：[Retriever](retriever.md)、[DPR paper note](../papers/dpr.md)。
