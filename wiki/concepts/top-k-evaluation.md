---
concept_id: top-k-evaluation
status: verified
verified_sources:
  - dpr
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

相關頁面：[Retriever](retriever.md)、[DPR paper note](../papers/dpr.md)。

