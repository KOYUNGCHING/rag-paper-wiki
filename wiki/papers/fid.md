---
paper_id: fid
title: Leveraging Passage Retrieval with Generative Models for Open Domain Question Answering
status: verified
source_version: arXiv v2
ingested_at: 2026-11-23
verified_at: 2026-11-23
proposal: ../../proposals/fid.md
evidence: ../evidence/fid.json
---

# Fusion-in-Decoder（FiD）

## 基本資料

- **作者**：Gautier Izacard、Edouard Grave
- **版本**：[arXiv:2007.01282v2](https://arxiv.org/abs/2007.01282v2)
- **一句話摘要**：FiD 先分別編碼每個 question-passage pair，再讓同一個 decoder
  attention 所有 passage representations，以可擴展的方式融合多篇檢索證據。
  [FID:fid-c03]

## 快速理解：Introduction 與 Results

### 研究動機

Closed-book generative QA 把知識放在模型參數中，通常需要非常大的 model，訓練與
查詢成本都高。[FID:fid-c01] Retrieval-based QA 雖可取得外部證據，但多篇 passages
可能各自提供部分資訊，如何有效聚合仍是問題。

FiD 採用兩階段流程：先從外部 knowledge source 取得 passages，再讓 generative
seq2seq model 根據 question 與 passages 產生答案。[FID:fid-c02]

### 核心結果

| 問題 | 設定 | 結果 | 解讀 |
| --- | --- | --- | --- |
| FiD 在 NQ 的表現如何？ | Natural Questions test、EM | FiD-large 51.4；FiD-base 48.2；RAG 44.5；DPR 41.5 | 在該完整 system setting 中 FiD 較高，但 model size 與 reader/generator 都不同。[FID:fid-r01] |
| TriviaQA 是否也改善？ | open-domain／hidden test、EM | FiD-large 67.6/80.1；RAG 56.1/68.0 | 兩種 test 必須成對標示。[FID:fid-r02] |
| 更多 passages 是否有幫助？ | 三個 validation curves | 顯示範圍內 EM 隨 passages 增加而上升 | 支援 multi-passage fusion，但不能無限外推。[FID:fid-r03] |
| 少 passages 訓練有何代價？ | 以 100 passages evaluation、dev EM | NQ 37.8→46.5；TriviaQA 58.1→64.7 | 由 5 改為 100 training passages 時表現提高。[FID:fid-r04] |
| 能否用短期 fine-tuning 補救？ | 5-passage initial training、dev EM | NQ 37.8→45.0；TriviaQA 58.1→64.2 | 額外 100-passage fine-tuning 縮小差距。[FID:fid-r05] |

Table 1 是 test results；Figure 3 與 Table 2 使用 validation/development results，
不能把它們混成同一組比較。

## 深入閱讀：Method

### 整體流程

```text
Question + Passage 1 → Encoder ┐
Question + Passage 2 → Encoder ├→ concatenate representations → Decoder → Answer
Question + Passage N → Encoder ┘
```

每個 passage 的 title、text 與 question 組合後，獨立通過 encoder；所有 encoder
outputs 再串接，交給一個 decoder 共同 attention 並生成答案。[FID:fid-c03]

這就是「Fusion-in-Decoder」：passages 在 encoder 階段彼此分離，到 decoder 階段才
共同參與 answer generation。[FID:fid-c05]

### Retriever 與 generator 的分工

FiD 可使用 BM25 或 DPR 取得 support passages；它本身沒有提出新 retriever，貢獻
集中在 generative reader 如何處理多篇 passages。[FID:fid-c06]

Generator 可由 T5 或 BART 初始化，並用 question、title、passage text 組成每個
encoder input。[FID:fid-c07]

### 為什麼較能擴展 passages？

若先把所有 passages 串成一個超長 encoder input，self-attention 會跨整段計算。
FiD 讓 encoder 一次只看單一 passage context，因此計算量隨 passage 數量近似線性
成長；decoder 才看到串接後的全部 representations。[FID:fid-c04]

這降低了 encoder-side multi-passage cost，但不代表 passages 沒有成本。作者仍把
large passage counts 的 efficiency 列為 open problem。[FID:fid-c14]

## Experiments

FiD 的實驗範圍是 open-domain QA：Natural Questions、TriviaQA 與 SQuAD Open，
不是一般性的長文生成或所有 RAG tasks。[FID:fid-c11]

資料集也沒有共用完全相同的 retriever：Natural Questions 與 TriviaQA 使用 DPR，
SQuAD 使用 BM25。[FID:fid-c08] 因此跨 dataset 的差異不能只歸因於 FiD decoder。

Retrieved documents 被切成固定長度、互不重疊的 passages，passage 正是 encoder
獨立處理的 retrieval unit。[FID:fid-c12]

評估使用 normalized Exact Match：生成答案經正規化後，只要符合可接受答案之一就
算正確。[FID:fid-c09] EM 不直接衡量 citation correctness、passage relevance 或
generation faithfulness。

## 對 passage scaling 的解讀

作者將更多 passages 帶來的 performance improvement 解讀為 seq2seq model 能整合
多篇資訊的支持證據。[FID:fid-c13] 這是合理但有範圍的 author interpretation：
曲線顯示輸出改善，並沒有直接觀察 decoder 內部是否真的完成多步證據推理。

## Limitations 與批判性筆記

1. **Retriever 並未 joint-train**：FiD 使用既有 BM25/DPR results；把 retriever 納入
   end-to-end learning 是作者列出的 future work。[FID:fid-c10]
2. **更多 passages 不是免費的**：independent encoding 改善 scaling form，但 GPU
   memory、encoder calls 與 decoder attention 仍會增加。[FID:fid-c04] [FID:fid-c14]
3. **System comparison 包含多個差異**：Table 1 同時混合 model sizes、retrievers、
   training recipes 與 extractive/generative readers，不能只用最高分證明 FiD 架構本身
   是唯一原因。
4. **Dataset scope 有限**：三個 open-domain QA datasets 的結果不能直接外推到
   classification、long-form generation 或所有企業 RAG 場景。[FID:fid-c11]
5. **EM 不等於 evidence quality**：答案剛好符合 reference，不表示使用的 passages
   都相關或輸出具有可追溯來源。[FID:fid-c09]

## 與 DPR、RAG 的關係

DPR 提供 dense retrieval；原始 RAG 把 retrieved documents 當 latent variables 並
marginalize generation probabilities；FiD 則將各 passage 獨立編碼後，讓 decoder
jointly attend 全部 representations。完整比較見
[DPR → RAG → FiD](../comparisons/dpr-rag-fid.md)。

## Related concepts

- [Fusion-in-Decoder](../concepts/fusion-in-decoder.md)
- [Multi-passage fusion](../concepts/multi-passage-fusion.md)
- [Encoder／decoder scaling](../concepts/encoder-decoder-scaling.md)
- [Generator](../concepts/generator.md)
- [Context augmentation](../concepts/context-augmentation.md)

## Source evidence

- [FiD reading proposal](../../proposals/fid.md)
- [FiD structured evidence](../evidence/fid.json)

