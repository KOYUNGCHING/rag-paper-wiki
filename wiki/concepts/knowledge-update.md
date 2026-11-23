---
concept_id: knowledge-update
status: verified
verified_sources:
  - rag
---

# Knowledge update

RAG 的 non-parametric memory 可以替換。原始論文用不同時期的 Wikipedia index 示範，
模型的 time-specific answers 會隨 index 改變，而不需要重新訓練 generator。
[RAG:rag-c11]

## 能更新什麼？

- 可被 retriever 搜尋的文件集合。
- Generator 在 inference 時可能取得的外部 evidence。
- 人可檢查與修改的 raw-text memory。[RAG:rag-c12]

## 不能保證什麼？

- 新來源一定正確。
- Retriever 一定找對 passage。
- Generator 一定忠實使用 passage。

外部 corpus 仍可能包含錯誤與偏見。[RAG:rag-c13] 因此 knowledge update 必須搭配
source review、retrieval evaluation 與 generation verification；這三項流程分工是
`wiki_synthesis`，會由後續評估論文補強。

