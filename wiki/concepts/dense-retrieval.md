---
concept_id: dense-retrieval
status: verified
verified_sources:
  - dpr
---

# Dense retrieval

Dense retrieval 把 question 與 passage 編碼成低維、連續向量，再依向量相似度排序。
DPR 使用分離的 question/passsage encoders，並以 inner product 作為 similarity score。
[DPR:dpr-c05]

## 為什麼不用只做關鍵字比對？

Sparse retriever 擅長 exact lexical match；dense representation 則能捕捉字面不同的
語意關係。[DPR:dpr-c02] 這不是單向取代關係：DPR 的質化分析也顯示 dense method
可能漏掉罕見而關鍵的名稱或片語。[DPR:dpr-c10]

## 如何搜尋？

Passage embeddings 可離線計算並建立 FAISS index；runtime 只需編碼問題並搜尋
鄰近 passages。[DPR:dpr-c06] 因此 dense retrieval 的完整成本同時包含 embedding
計算、index 建立與線上查詢，不能只看單一速度數字。

## 目前來源範圍

目前內容來自 [DPR paper note](../papers/dpr.md)。後續論文可能使用 DPR 作為元件，
不代表它們沿用完全相同的 encoder、training data 或 index 設定。

