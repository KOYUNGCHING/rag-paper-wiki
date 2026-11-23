---
concept_id: context-augmentation
status: verified
verified_sources:
  - rag
---

# Context augmentation

Context augmentation 是把 retrieved passage 與原 input 組合，讓 generator 在產生輸出
時能看到外部資訊。原始 RAG 直接將 input 與 retrieved content 串接給 BART。
[RAG:rag-c07]

Augmentation 是 retrieval 與 generation 之間的橋樑：只建立 index 還不是完整 RAG；
必須把檢索結果帶進 generator 的條件資訊。[RAG:rag-c03]

原始 RAG 會分別對 top-k documents 產生條件機率，再依
[RAG-Sequence／RAG-Token](rag-sequence-token.md) 的方式 marginalize，而不是單純把
所有 passages 無條件合併。[RAG:rag-c04] [RAG:rag-c05]

