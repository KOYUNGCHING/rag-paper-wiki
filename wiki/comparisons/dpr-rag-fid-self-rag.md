---
comparison_id: dpr-rag-fid-self-rag
status: verified
verified_sources:
  - dpr
  - rag
  - fid
  - self-rag
---

# DPR → RAG → FiD → Self-RAG：從檢索到可控制的生成

| 面向 | DPR | 原始 RAG | FiD | Self-RAG |
| --- | --- | --- | --- | --- |
| 核心問題 | 如何找 relevant passages？[DPR:dpr-c01] | 如何讓 seq2seq generator 使用外部 passages？[RAG:rag-c10] | 如何融合大量 passages？[FID:fid-c03] | 如何按需求檢索並評估 passage／output？[SELF-RAG:self-rag-c02] |
| Retrieval timing | 每題先 retrieve | 每題先 retrieve top-k | 每題先取得 passages | 由 Retrieve token／threshold 決定。[SELF-RAG:self-rag-c09] |
| Passage aggregation | 排序後交給 extractive reader。[DPR:dpr-c11] | 對 latent documents marginalize。[RAG:rag-c03] | Independent encoding + decoder joint attention。[FID:fid-c03] | 對 passages 平行產生 segments，再以 critique scores 排序。[SELF-RAG:self-rag-c05] |
| Output model | Extractive reader | BART generator。[RAG:rag-c07] | T5／BART-style generator。[FID:fid-c07] | Llama2 7B／13B generator。[SELF-RAG:self-rag-c12] |
| Evidence assessment | Retrieval accuracy | Task output metrics | Exact Match | IsRel、IsSup、IsUse + task/citation metrics。[SELF-RAG:self-rag-c04] |
| Training boundary | 訓練 dual encoder。[DPR:dpr-c07] | 更新 query encoder 與 generator，index 固定。[RAG:rag-c08] | 不 joint-train retriever。[FID:fid-c10] | Offline critic 建資料；推論不需 critic。[SELF-RAG:self-rag-c17] |

## 教學發展線

```text
DPR       找到 evidence
  ↓
RAG       讓 generator 使用 evidence
  ↓
FiD       融合更多 passages
  ↓
Self-RAG  決定何時找，並評估 passage 與 output
```

這條發展線是 `wiki_synthesis`，用來整理四篇論文各自補上的問題，不表示後一篇在
所有 tasks 或 metrics 都嚴格勝過前一篇。

## Self-RAG 改變了什麼？

Self-RAG 不是用另一個 retriever 取代 DPR，也不是用另一種 FiD architecture。它把
retrieval timing、passage relevance、evidence support 與 response utility 轉成模型可
生成的 control tokens。[SELF-RAG:self-rag-c04]

這讓 RAG pipeline 從固定三階段：

```text
Retrieve → Augment → Generate
```

變成可重複的控制 loop：

```text
Decide → Retrieve → Generate candidates → Critique → Select → Repeat
```

後一個流程是根據 Algorithm 1 的教學性簡化。[SELF-RAG:self-rag-c05]

## 結果比較的邊界

四篇論文的 model family、datasets、retrieval sources、reader/generator 與 metrics 都
不同。Self-RAG Table 2 又同時使用 accuracy、FactScore、ROUGE、MAUVE、citation
precision 與 recall。[SELF-RAG:self-rag-c11] 因此歷史順序可以比較「研究問題如何
擴張」，不能把各篇最高數字排成一條乾淨的 architecture leaderboard。
