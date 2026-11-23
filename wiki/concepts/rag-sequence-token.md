---
concept_id: rag-sequence-token
status: verified
verified_sources:
  - rag
  - fid
---

# RAG-Sequence 與 RAG-Token

## RAG-Sequence

同一個 latent document 支援完整 output sequence，模型再對 top-k documents 的
sequence probabilities 做 marginalization。[RAG:rag-c04]

## RAG-Token

每個 token 都可由不同 latent document 支援，因此可以在一段輸出中切換文件來源。
[RAG:rag-c05]

## 為什麼不能混為一談？

兩者的 latent-variable assumption、decoding 與 task performance 不同。Figure 3 也顯示
增加 retrieved documents 對兩者的影響不同，不存在「k 越大一定越好」的共同規則。
[RAG:rag-r06]

## 與 FiD 的差異

FiD 不使用 RAG-Sequence／RAG-Token 的 latent-document marginalization。它先獨立
encode passages，再讓一個 decoder jointly attend 串接後的 representations。
[FID:fid-c03] 兩者都能利用多篇 passages，但 fusion mechanism 不同。

