---
concept_id: citation-quality
status: verified
verified_sources:
  - self-rag
  - ragchecker
---

# Citation quality

Citation quality 不能只用一個分數表示。Self-RAG 在 ASQA 同時評估 citation
precision 與 citation recall，並另外評估 answer correctness 與 fluency。
[SELF-RAG:self-rag-c11]

## Precision 與 recall

- **Citation precision**：已提供的 citations 有多少真正支持對應 claim。
- **Citation recall**：需要 evidence 的 claims 有多少獲得足夠 citation coverage。

Table 2 中，Self-RAG 13B 的 precision／recall 是 70.3／71.3；Ret-ChatGPT 是
65.1／76.6。[SELF-RAG:self-rag-r03] 這個交叉結果顯示「引用較準」與「引用較完整」
可能指向不同系統。

## 與 fluency 的取捨

Figure 3(b) 中，提高 IsSup 權重讓 citation precision 上升，卻讓 MAUVE 下降。
[SELF-RAG:self-rag-r06] 較長、較流暢的回答可能增加沒有完整 evidence support 的
claims；較保守的回答則可能犧牲內容與流暢度。

最後一句是基於該實驗的 `wiki_synthesis`，不是所有 task 的普遍定律。

## 與 RAGChecker faithfulness 的關係

RAGChecker 的 faithfulness 檢查 response claims 是否被 retrieved chunks 支持，但它不評估
citation 標記本身。[RAGCHECKER:ragchecker-c11] 兩者都關心 evidence support，衡量對象不同
（`wiki_synthesis`）。見 [Generation diagnostics](generation-diagnostics.md)。

相關頁面：[Reflection tokens](reflection-tokens.md)、
[Critique-guided decoding](critique-guided-decoding.md)、[Generator](generator.md)。
