---
concept_id: generation-diagnostics
status: verified
verified_sources:
  - ragchecker
---

# Generation diagnostics

RAGChecker 用六個指標描述 generator 如何使用（或誤用）retrieved context。

| 指標 | 計算對象 | 方向 |
| --- | --- | --- |
| Faithfulness | response claims 被任何 chunk 支持的比例 | ↑ |
| Relevant noise sensitivity, NS(I) | 錯誤且來自 relevant chunk 的 claims | ↓ |
| Irrelevant noise sensitivity, NS(II) | 錯誤且來自 irrelevant chunk 的 claims | ↓ |
| Hallucination | 錯誤且沒有任何 chunk 支持的 claims | ↓ |
| Self-knowledge | 正確但沒有任何 chunk 支持的 claims | ↓（若要求完全依賴 context） |
| Context utilization | 被找回的 ground-truth claims 中，回答實際用到的比例 | ↑ |

依據：[RAGCHECKER:ragchecker-c11] [RAGCHECKER:ragchecker-c12]
[RAGCHECKER:ragchecker-c13] [RAGCHECKER:ragchecker-c14]。前五項分母都是全部
response claims。[RAGCHECKER:ragchecker-c15]

## 錯誤 claim 的三分法

一個錯誤 claim 若「出現在含正確資訊的 chunk 裡」，代表 generator 被同一塊中的雜訊
帶偏；若出現在無關 chunk，代表被無關內容帶偏；若任何 chunk 都沒有，才是
hallucination。[RAGCHECKER:ragchecker-c12] 這讓 hallucination 和「錯信 context」被
分開計算。

## 實驗中的觀察

- 每個系統的 NS(I) 都遠高於 NS(II)。[RAGCHECKER:ragchecker-r07]
- 換成較好的 retriever，faithfulness 上升、hallucination 下降
  [RAGCHECKER:ragchecker-r08]，但 NS(I) 也上升。[RAGCHECKER:ragchecker-r09]
- 同一 retriever 下，較大的 Llama3 在這些指標都較好。[RAGCHECKER:ragchecker-r06]
- GPT-4 的 context utilization 較高、NS(I) 較低。[RAGCHECKER:ragchecker-r10]

作者解讀：generators 呈現 chunk-level faithfulness [RAGCHECKER:ragchecker-c24]；
context utilization 與 F1 相關最強（author claim）。[RAGCHECKER:ragchecker-c23]

## 不能一起最大化

作者在 prompt 實驗中觀察到 context utilization 提高時 noise sensitivity 變差，難以同時
改善所有面向。[RAGCHECKER:ragchecker-c28]

相關頁面：[Generator](generator.md)、[Retrieval diagnostics](retrieval-diagnostics.md)、
[Citation quality](citation-quality.md)。
