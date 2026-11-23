---
concept_id: non-parametric-memory
status: verified
verified_sources:
  - rag
---

# Non-parametric memory

原始 RAG 將 Wikipedia passages 的 dense index 稱為 non-parametric memory。知識存在
外部 raw text 與 index 中，而不是只存在 generator parameters。[RAG:rag-c02]

## 主要特性

- 可由 retriever 搜尋。[RAG:rag-c06]
- Raw text 可被人閱讀與修改，讓來源比較容易檢查。[RAG:rag-c12]
- 可以替換 index，更新模型可取得的資訊，而不必重新訓練 generator。
  [RAG:rag-c11]

外部化不等於可信。若 corpus 有錯誤、偏見或缺漏，這些問題仍可能進入 retrieval 與
generation。[RAG:rag-c13]

