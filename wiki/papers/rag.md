---
paper_id: rag
title: Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
status: verified
source_version: arXiv v4
ingested_at: 2026-11-23
verified_at: 2026-11-23
proposal: ../../proposals/rag.md
evidence: ../evidence/rag.json
---

# Retrieval-Augmented Generation（RAG）

## 基本資料

- **作者**：Patrick Lewis、Ethan Perez、Aleksandra Piktus、Fabio Petroni、
  Vladimir Karpukhin、Naman Goyal、Heinrich Küttler、Mike Lewis、Wen-tau Yih、
  Tim Rocktäschel、Sebastian Riedel、Douwe Kiela
- **會議**：NeurIPS 2020
- **版本**：[arXiv:2005.11401v4](https://arxiv.org/abs/2005.11401v4)
- **一句話摘要**：原始 RAG 將 DPR retriever、Wikipedia dense index 與 BART
  generator 結合，讓 seq2seq generation 同時利用 parametric 與 non-parametric
  knowledge。[RAG:rag-c03] [RAG:rag-c10]

## 快速理解：Introduction 與 Results

### 研究動機

預訓練語言模型把大量知識儲存在參數中，但這種 [parametric memory](../concepts/parametric-memory.md)
不容易直接更新或檢查，也難以為輸出提供明確 provenance。[RAG:rag-c01]

RAG 的核心提案是加入可檢索的 [non-parametric memory](../concepts/non-parametric-memory.md)：
generator 保留參數內能力，retriever 則從外部文字 index 取得可讀、可替換的內容。
[RAG:rag-c02]

### Research gap

當時的 retrieval-augmented neural models 已能支援 extractive QA，但尚未形成可套用到
一般 seq2seq tasks 的統一 generation recipe。RAG 將 retrieved text 接到 generator，
把 retrieval 從「找出可擷取答案的 passage」延伸成「提供生成所需 context」。
[RAG:rag-c10]

### 核心結果

| 問題 | 設定 | 結果 | 解讀 |
| --- | --- | --- | --- |
| RAG 能改善 open-domain QA 嗎？ | Natural Questions test、Exact Match | RAG-Sequence 44.5；DPR 41.5 | 在此設定中，generation-based RAG 高於 DPR extractive system。[RAG:rag-r01] |
| RAG 能支援 abstractive generation 嗎？ | MS-MARCO test | BART R-L/B-1 38.2/41.6；RAG-Sequence 40.8/44.2 | 在這項 task 的兩個 metrics 上改善。[RAG:rag-r02] |
| 人工評估是否偏好 RAG？ | Jeopardy factuality pairwise assessment | RAG better 42.7%；BART better 7.1%；no majority 20.8% | 有明顯偏好，但不能忽略無共識樣本。[RAG:rag-r03] |
| Learned retrieval 是否重要？ | NQ development、RAG-Sequence | learned 44.0；BM25 replacement 31.8 | 對 NQ 有幫助。[RAG:rag-r04] |
| Dense retrieval 是否總是較好？ | FEVER development | BM25 75.1/91.6；learned 74.5/90.6 | 否；FEVER 是明確例外。[RAG:rag-r05] |

這些結果屬於不同 task、split 與 metric，不能把數字橫向當成單一排行榜。

## 深入閱讀：Method

### 整體流程

```text
input x
  → query encoder
  → MIPS 取得 top-k passages z
  → 將 x 與各 passage 組合
  → seq2seq generator 產生候選輸出
  → 對 latent documents 的生成機率做 marginalization
  → output y
```

Figure 1 將 RAG 拆成 Query Encoder、Document Index 與 Generator。Retriever 先用
MIPS 取得 top-k documents，generator 再條件化於 input 與 documents；documents
被視為 latent variables。[RAG:rag-c03]

### Retriever 與 generator

Retriever 由 DPR 初始化，使用 query/document dense representations 與 MIPS 搜尋
document index。[RAG:rag-c06] Generator 使用 BART-large，把原 input 與 retrieved
content 串接後生成。[RAG:rag-c07]

這使系統形成三段教學結構：

1. **Retrieve**：找出與 input 相關的 passages。
2. **Augment**：把 passages 加入 generator 可見的 context。
3. **Generate**：根據 input 與 retrieved context 產生輸出。

### RAG-Sequence 與 RAG-Token

- **RAG-Sequence**：一個 latent document 支援整個 output sequence，再對 top-k
  documents 的 sequence probabilities 做 marginalization。[RAG:rag-c04]
- **RAG-Token**：每個 generated token 可以由不同 latent document 支援，並在每個
  token step marginalize。[RAG:rag-c05]

兩者不是同名模型的小參數差異，而是 latent-document assumption 與 decoding 都不同。
更多 retrieved documents 也不保證持續改善：Figure 3 中 RAG-Sequence 在顯示的 NQ
範圍內上升，RAG-Token 則到達高點後下降。[RAG:rag-r06]

### Training boundary

論文所稱 joint training 有清楚邊界：下游 fine-tuning 更新 query encoder 與 generator，
但 document encoder 與 document index 維持固定。[RAG:rag-c08] 因此不能說「所有
RAG 元件都 end-to-end 更新」。Retriever 又是由已接受 QA retrieval supervision 的
DPR 初始化，不能說它從零開始、完全無 retrieval supervision。[RAG:rag-c06]

## Experiments

同一套架構被 fine-tune 到 open-domain QA、abstractive QA、Jeopardy question
generation 與 FEVER fact verification，並共用 Wikipedia passage index。
[RAG:rag-c09]

實驗的價值不只是宣稱單一 task 的高分，而是展示 retrieval-conditioned seq2seq
architecture 可以跨生成與分類任務使用。不過，任務使用的 metrics 不同，也包含
有無 gold context、test/dev split 等比較條件。

## Knowledge update

Non-parametric index 可以替換。論文的 hot-swapping experiment 顯示，換成不同時間的
Wikipedia index 會讓模型回答對應時期的資訊，而不必重新訓練 generator。
[RAG:rag-c11]

作者把 raw-text memory 描述為 human-readable 與 human-writable：人可以檢查被取用的
文件，也可以修改或替換 index。[RAG:rag-c12] 但這只表示知識較容易維護，不代表新
index 自動正確。

## Limitations 與批判性筆記

1. **原始 RAG 不是所有現代 RAG**：本文特指 DPR、BART、latent-document
   marginalization 與共同 fine-tuning。今日常見的 prompt pipeline 可能不同。
2. **Factuality 不是保證**：作者在特定 task 中觀察到 RAG 輸出較 factual、specific，
   但 Discussion 仍把如何更有效結合兩種 memory 列為未來工作。[RAG:rag-c14]
3. **Retriever 仍有 task dependence**：NQ ablation 支援 learned retrieval，FEVER
   卻由 BM25 replacement 略勝。[RAG:rag-r04] [RAG:rag-r05]
4. **External source 會傳遞問題**：Wikipedia 或其他知識來源仍可能錯誤、有偏見或
   不完整。[RAG:rag-c13]
5. **更新 index 不等於更新真相**：hot-swapping 只保證模型可取得的 corpus 改變，
   不保證檢索正確、來源可信或生成忠實。
6. **2020 SOTA 不是目前排名**：本文結果只能按當時 baselines、splits 與 metrics
   解讀，不能寫成現在仍是最佳方法。

## 與 DPR 的關係

DPR 解決「如何用 dense vectors 找到 passages」；RAG 直接使用 DPR retriever，進一步
把 passages 交給 seq2seq generator。完整演進見 [從 DPR 到 RAG](../comparisons/dpr-to-rag.md)。

## Related concepts

- [RAG 基本概念](../concepts/rag.md)
- [Parametric memory](../concepts/parametric-memory.md)
- [Non-parametric memory](../concepts/non-parametric-memory.md)
- [Generator](../concepts/generator.md)
- [Context augmentation](../concepts/context-augmentation.md)
- [RAG-Sequence 與 RAG-Token](../concepts/rag-sequence-token.md)
- [Knowledge update](../concepts/knowledge-update.md)

## Source evidence

- [RAG reading proposal](../../proposals/rag.md)
- [RAG structured evidence](../evidence/rag.json)

