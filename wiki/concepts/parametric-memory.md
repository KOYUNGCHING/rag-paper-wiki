---
concept_id: parametric-memory
status: verified
verified_sources:
  - rag
---

# Parametric memory

Parametric memory 指儲存在模型參數中的能力與知識。RAG 論文使用預訓練 BART
generator 作為 parametric component。[RAG:rag-c07]

它的優點是生成能力已被模型學會；限制是知識不容易直接修改、檢查來源或隨外部世界
更新。[RAG:rag-c01]

RAG 並未移除 parametric knowledge，而是讓它與 [non-parametric memory](non-parametric-memory.md)
合作。原始實驗中的 generator 仍可能依靠參數知識完成 retrieved document 沒有完整寫出
的內容，因此不能把 RAG 理解成單純複製文件。

