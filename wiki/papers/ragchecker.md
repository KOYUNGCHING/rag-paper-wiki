---
paper_id: ragchecker
title: "RAGChecker: A Fine-grained Framework for Diagnosing Retrieval-Augmented Generation"
status: verified
source_version: arXiv v2
ingested_at: 2026-11-23
verified_at: 2026-11-23
proposal: ../../proposals/ragchecker.md
evidence: ../evidence/ragchecker.json
---

# RAGChecker

## 基本資料

- **作者**：Dongyu Ru、Lin Qiu、Xiangkun Hu 等（Amazon AWS AI、上海交通大學、西湖大學）
- **版本**：[arXiv:2408.08067v2](https://arxiv.org/abs/2408.08067v2)（2024-08-17）
- **一句話摘要**：RAGChecker 把 response 與 ground-truth answer 拆成 claims，用
  claim-level entailment 計算 overall、retriever 與 generator 三組指標，讓 RAG 答錯時
  可以追問「是沒找到，還是找到了卻沒用好」。[RAGCHECKER:ragchecker-c03]
  [RAGCHECKER:ragchecker-c05]

## Introduction 與研究動機

作者指出 RAG 評估有兩個難處：RAG 是 retriever 加 generator 的模組化系統，需要同時看
整體與個別模組；而既有指標中，recall@k／MRR 依賴人工標註 chunks 與固定切分，
BLEU／ROUGE 等 generator 指標則太粗，難以評估長回答。[RAGCHECKER:ragchecker-c01]
另外，既有 RAG 指標是否與人類判斷一致，也少有檢驗。[RAGCHECKER:ragchecker-c02]

## Research gap

前四篇（DPR、RAG、FiD、Self-RAG）用 retrieval accuracy、Exact Match 或 task metrics
評估「做得好不好」。作者認為只評 generator 的 benchmarks 看不出生成結果如何受不同
retrieval 行為影響（author claim）。[RAGCHECKER:ragchecker-c31] 作者也主張既有框架如
RAGAS、TruLens、ARES 只在部分指標細粒度（author claim）。[RAGCHECKER:ragchecker-c04]

## Contributions

1. 以 text-to-claim extractor 與 claim-entailment checker 建立 [claim-level
   evaluation](../concepts/claim-level-evaluation.md)。[RAGCHECKER:ragchecker-c07]
2. 定義 [retrieval diagnostics](../concepts/retrieval-diagnostics.md) 與六項
   [generation diagnostics](../concepts/generation-diagnostics.md)，把錯誤分派給模組。
   [RAGCHECKER:ragchecker-c09] [RAGCHECKER:ragchecker-c12]
3. 用 280 組人工 pairwise 偏好做 [meta evaluation](../concepts/rag-meta-evaluation.md)。
   [RAGCHECKER:ragchecker-c20]
4. 在 10 domains 上診斷 8 個 RAG systems，並分析 top-k、chunk size、overlap 與 prompt。
   [RAGCHECKER:ragchecker-c16] [RAGCHECKER:ragchecker-c26]

## Main results

### Meta evaluation：與人類判斷的一致性

在 overall assessment 的 Pearson correlation，RAGChecker 是 61.93，表中最強 baseline
RAGAS Answer Similarity 是 48.31，兩位人類 annotators 之間是 70.09。
[RAGCHECKER:ragchecker-r01] Correctness Pearson 也是 RAGChecker 較高（49.66 vs
41.07）。[RAGCHECKER:ragchecker-r02]

**解讀邊界**：作者文字寫 RAGChecker 在三個面向都有最強 correlation，但 Table 2 的
completeness Spearman 是 RAGAS Answer Similarity 較高（61.35 vs 58.11）。
[RAGCHECKER:ragchecker-r03] 摘要的「significantly better」也沒有在本文找到統計檢定；
本 Wiki 只寫「correlation 較高」。人類上界仍明顯高於所有自動指標。

### 8 個 RAG systems 的平均診斷（Table 3）

- 平均 F1 最高是 E5-Mistral_GPT-4（52.7），最低是 BM25_Llama3-8b（42.1）。
  [RAGCHECKER:ragchecker-r04]
- **換 retriever**：固定 GPT-4，BM25 → E5-Mistral 讓 claim recall 74.0 → 83.5、context
  precision 52.3 → 61.8、F1 50.3 → 52.7。[RAGCHECKER:ragchecker-r05] 每個 generator 的
  faithfulness 都上升、hallucination 都下降。[RAGCHECKER:ragchecker-r08]
- **但 noise 也變多**：同樣的換法讓四個 generators 的 relevant noise sensitivity 全部上升。
  [RAGCHECKER:ragchecker-r09]
- **換 generator 大小**：固定 E5-Mistral，Llama3-70b 比 8b 有較高 F1 與 context
  utilization、較低 noise sensitivity 與 hallucination。[RAGCHECKER:ragchecker-r06]
- **Relevant noise 更難處理**：每一列 NS(I) 都遠高於 NS(II)。[RAGCHECKER:ragchecker-r07]
- GPT-4 的 context utilization 較高、relevant noise sensitivity 較低。
  [RAGCHECKER:ragchecker-r10]

作者對這些數字的解讀（author claims）：context utilization 與 F1 相關較強
[RAGCHECKER:ragchecker-c23]；generators 表現出 chunk-level faithfulness，整塊相信
relevant chunk [RAGCHECKER:ragchecker-c24]；open-source models 較容易盲目相信
context。[RAGCHECKER:ragchecker-c25] 這些是 8 個系統上的觀察，不是因果證明。

平均值會掩蓋 domain 差異：換 retriever 的 claim recall 提升在 Finance 很大（69.4 →
86.3），在 ClapNQ 幾乎沒有（81.1 → 81.5）。[RAGCHECKER:ragchecker-r11]

### RAG 設定調整（Appendix F）

設定：3 個 systems × 3 domains（Writing、Finance、KIWI），調整 k、chunk size、overlap
與 prompt。[RAGCHECKER:ragchecker-c26] 作者觀察：

- 更大的 k 降低 context precision，更大的 chunk 提高它；兩者都提高 claim recall 與
  faithfulness，但 context utilization 變差、relevant noise sensitivity 上升。
  [RAGCHECKER:ragchecker-c27]
- 要求更忠實的 prompt 提高 context utilization，卻讓 noise sensitivity 變差。
  [RAGCHECKER:ragchecker-c28]
- Chunk overlap 影響不大。[RAGCHECKER:ragchecker-c29]

Section 4.4 正文另有幾組數字（例如 k 5 → 20 時的 claim recall），但正文與 Appendix F
都沒說明是哪個 system／domain 或如何平均，Figures 6–10 也只畫 radar 範圍，因此本 Wiki
**不收錄這些數字**。

## Method

- **Formulation**：RAG = {R, G}，retriever 取 top-k chunks，generator 產生 response。
  [RAGCHECKER:ragchecker-c06]
- **Overall**：claim-level precision、recall、F1。[RAGCHECKER:ragchecker-c08]
- **Retriever**：claim recall（claim-level）與 context precision（chunk-level）。
  [RAGCHECKER:ragchecker-c09] 作者選 chunk-level 是因為固定大小 chunk 本來就會混入
  無關內容。[RAGCHECKER:ragchecker-c10]
- **Generator**：faithfulness [RAGCHECKER:ragchecker-c11]；relevant／irrelevant noise
  sensitivity 與 hallucination [RAGCHECKER:ragchecker-c12]；self-knowledge
  [RAGCHECKER:ragchecker-c13]；context utilization。[RAGCHECKER:ragchecker-c14]
  完整公式見 Appendix B。[RAGCHECKER:ragchecker-c15]

## Experiments, datasets, metrics, and baselines

- 8 systems = BM25／E5-Mistral × GPT-4／Mixtral-8x7B／Llama3-8B／Llama3-70B；claim
  extractor 與 checker 都是 Llama3-70B（RefChecker）。[RAGCHECKER:ragchecker-c16]
- 預設 300-token chunks、overlap 0.2、top-20、temperature 0。[RAGCHECKER:ragchecker-c19]
- Benchmark：4,162 queries、10 domains，short answers 轉 long-form。
  [RAGCHECKER:ragchecker-c17] 哪些 domains 由 GPT-4 擴寫，Table 1 與 Figure 2 的說明
  不一致（六個 vs 七個，差在 Writing）。[RAGCHECKER:ragchecker-c18]
- Meta evaluation：280 pairs、每組 2 位 annotators。[RAGCHECKER:ragchecker-c20]
  標註介面會顯示 GPT-4 產生的 critiques。[RAGCHECKER:ragchecker-c21]
- Checker 驗證：Llama3 版 RefChecker 在三種 context settings 的 accuracy 都較高，但
  noisy context 的 Non-Factual F1 略低。[RAGCHECKER:ragchecker-r12]

## Ablations

論文沒有對 RAGChecker 本身做 ablation；Appendix F 是用 RAGChecker 去診斷 RAG
hyper-parameters，已整理在 Main results。

## Limitations

- 作者自述：retriever 指標不如 generator 指標有洞察力；不區分 Neutral 與 Contradiction；
  benchmark 只有英文、純文字且由既有資料改造。[RAGCHECKER:ragchecker-c22]
- 作者也提醒，開發者可能只為這些指標優化。[RAGCHECKER:ragchecker-c30]
- Wiki 補充：評估者本身是 LLM，ground truth 部分由 GPT-4 擴寫，人類標註介面帶有
  GPT-4 critiques；這些都可能影響包含 GPT-4 的比較（`wiki_synthesis`，依據
  [RAGCHECKER:ragchecker-c16] [RAGCHECKER:ragchecker-c18] [RAGCHECKER:ragchecker-c21]）。

## Related Wiki concepts

[Claim-level evaluation](../concepts/claim-level-evaluation.md)、
[Retrieval diagnostics](../concepts/retrieval-diagnostics.md)、
[Generation diagnostics](../concepts/generation-diagnostics.md)、
[RAG error attribution](../concepts/rag-error-attribution.md)、
[RAG meta evaluation](../concepts/rag-meta-evaluation.md)、
[Retriever](../concepts/retriever.md)、[Generator](../concepts/generator.md)、
[Chunk](../concepts/chunk.md)、[Top-k evaluation](../concepts/top-k-evaluation.md)。

## Source evidence

所有 claims 位於 [`wiki/evidence/ragchecker.json`](../evidence/ragchecker.json)。
