---
concept_id: adaptive-retrieval
status: verified
verified_sources:
  - self-rag
---

# Adaptive retrieval

Adaptive retrieval（按需檢索）讓系統依目前 input 與已生成內容決定是否呼叫 retriever，
而不是每次固定取回相同數量的 passages。Self-RAG 用 Retrieve token 表示這個決策，
也允許對其 normalized probability 設定 threshold。[SELF-RAG:self-rag-c09]

## 為什麼需要？

固定檢索可能在需要 factual grounding 的問題上有幫助，但對不需要外部知識的任務，
額外 passages 可能離題並降低輸出品質。[SELF-RAG:self-rag-c01] Self-RAG 因此把
retrieval decision 放進生成 loop。[SELF-RAG:self-rag-c02]

```text
目前 input／output
  → 是否需要外部證據？
  ├─ 否：繼續生成
  └─ 是：retrieve → evaluate → generate
```

## Threshold 的 trade-off

Threshold 越高，模型越不容易觸發 retrieval。Figure 3(c) 顯示 threshold 增加時，
PubHealth 與 PopQA 的 retrieval frequency 都下降，但 accuracy 的反應不同：PopQA
下降較明顯，PubHealth 在顯示範圍內變化較小。[SELF-RAG:self-rag-r07]

因此「少檢索更快」與「保留足夠 evidence」之間沒有單一通用門檻。這是根據
Self-RAG 結果做出的 `wiki_synthesis`；實作時仍需用目標 task 驗證。

相關頁面：[Retriever](retriever.md)、[Reflection tokens](reflection-tokens.md)。
