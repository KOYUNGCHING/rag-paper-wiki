---
concept_id: critique-guided-decoding
status: verified
verified_sources:
  - self-rag
---

# Critique-guided decoding

Critique-guided decoding 使用模型對 critique tokens 的機率來選擇生成候選。Self-RAG
在每個 segment step 對多篇 retrieved passages 平行產生候選，再把 generation
probability 與 IsRel、IsSup、IsUse scores 結合。[SELF-RAG:self-rag-c05]

## Soft score 與 hard constraint

- **Soft score**：調整各 critique type 的權重，改變候選排序。
- **Hard constraint**：直接過濾例如 IsSup = no support 的候選。

兩種方式都不需要重新訓練 generator，但權重與規則是 inference-time
hyperparameters。[SELF-RAG:self-rag-c10]

## 實驗中的作用

50k-data ablation 中，拿掉 IsSup score 後，PopQA 從 45.5 降至 44.1，ASQA string
exact match 從 32.1 降至 30.6。[SELF-RAG:self-rag-r05] 提高 IsSup 權重則讓 ASQA
citation precision 上升、MAUVE 下降。[SELF-RAG:self-rag-r06]

因此 critique-guided decoding 是多目標取捨，而不是把某個權重調高就讓所有品質
指標一起變好。

相關頁面：[Reflection tokens](reflection-tokens.md)、
[Citation quality](citation-quality.md)。
