---
concept_id: rag
status: verified
verified_sources:
  - dpr
  - rag
  - self-rag
---

# Retrieval-Augmented Generation（RAG）

RAG 將外部檢索與文字生成結合。原始論文的架構由 query encoder、document index 與
seq2seq generator 組成：先取得 top-k documents，再讓 generator 對 input 與 retrieved
documents 產生的結果進行 marginalization。[RAG:rag-c03]

## 三個教學階段

```text
Retrieve → Augment → Generate
```

- **Retrieve**：使用 dense retriever 找 passages；原始 RAG 由 DPR 初始化。
  [RAG:rag-c06]
- **Augment**：將 retrieved passage 加到原 input，成為 generator 的額外 context。
  [RAG:rag-c07]
- **Generate**：seq2seq model 根據 input 與 context 產生輸出，而非只擷取 passage
  中既有的 span。[RAG:rag-c10]

## 名稱範圍

本頁前三階段先描述 Lewis et al. 的原始 RAG。後來「RAG」常被廣義用來指 retrieval +
generation pipeline，但那些系統不一定使用 BART、latent-document marginalization 或
joint fine-tuning。Self-RAG 就把固定流程改成可重複的 decide、retrieve、generate、
critique loop。[SELF-RAG:self-rag-c05]

「廣義 RAG 包含多種 retrieval-generation architectures」是跨論文整理，標記為
`wiki_synthesis`；不能把原始 RAG 的 method details 套用到所有後續系統。

相關頁面：[Retriever](retriever.md)、[Generator](generator.md)、
[Context augmentation](context-augmentation.md)。

