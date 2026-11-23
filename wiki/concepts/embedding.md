---
concept_id: embedding
status: verified
verified_sources:
  - dpr
---

# Embedding 與相似度

Embedding 在這裡是將 question 或 passage 轉成向量的表示方式。DPR 分別使用
question encoder 與 passage encoder，並以兩個向量的 inner product 排序 passages。
[DPR:dpr-c05]

## 為什麼要分成兩個 encoders？

因為相似度可以拆成 question vector 與 passage vector 的運算，所有 passage vectors
可以事先計算與建立 index；每次查詢只需產生新的 question vector。
[DPR:dpr-c06]

## Embedding 不保證什麼？

語意相似度不保證一定抓到答案。DPR 的 Table 7 顯示 dense representation 能處理
部分同義與改寫，也可能漏掉精確而罕見的關鍵詞。[DPR:dpr-c10]

相關頁面：[Dense retrieval](dense-retrieval.md)、[Retriever](retriever.md)。

