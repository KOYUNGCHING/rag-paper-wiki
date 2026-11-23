---
paper_id: dpr
title: Dense Passage Retrieval for Open-Domain Question Answering
status: verified
source_version: arXiv v3
ingested_at: 2026-11-23
verified_at: 2026-11-23
proposal: ../../proposals/dpr.md
evidence: ../evidence/dpr.json
---

# Dense Passage Retrieval（DPR）

## 基本資料

- **作者**：Vladimir Karpukhin、Barlas Oğuz、Sewon Min、Patrick Lewis、Ledell Wu、
  Sergey Edunov、Danqi Chen、Wen-tau Yih
- **會議**：EMNLP 2020
- **版本**：[arXiv:2004.04906v3](https://arxiv.org/abs/2004.04906v3)
- **一句話摘要**：DPR 說明只要設計好 dual-encoder 與負樣本訓練，dense retriever
  就能在多個 open-domain QA 設定中改善 passage retrieval，並常帶動下游問答表現；
  但這是有條件的作者主張，不代表所有資料集都成立。[DPR:dpr-c04]

## 快速理解：Introduction 與 Results

### 研究動機

Open-domain QA 可以先由檢索器（retriever）從大型語料庫選出少量候選 passages，
再由閱讀器（reader）找答案。Retriever 的工作不是直接回答，而是縮小 reader 必須
檢查的範圍。[DPR:dpr-c01]

傳統 BM25 等 sparse retriever 擅長精確字詞比對；dense representation 則有機會把
字面不同但語意相關的 question 與 passage 拉近。兩者的差異不是「舊方法與新方法」
這麼簡單，而是 lexical matching 與 semantic matching 的能力分布不同。
[DPR:dpr-c02]

### Research gap

當時成功的 dense retrieval 往往使用額外 pretraining。DPR 將問題收斂成：能否只用
question-passage 或 question-answer supervision，搭配簡單架構，訓練出夠強的 dense
retriever？[DPR:dpr-c03]

### 主要結果

| 問題 | 設定 | 結果 | 解讀 |
| --- | --- | --- | --- |
| Dense retrieval 能改善檢索嗎？ | Natural Questions test、Single、Top-20 | DPR 78.4；BM25 59.1 | 在這個明確設定下，DPR 找到含答案 passage 的比例較高。[DPR:dpr-r01] |
| 所有資料集都改善嗎？ | SQuAD test、Single、Top-20 | DPR 63.2；BM25 68.8 | 否。SQuAD 是重要反例。[DPR:dpr-r02] |
| 較好的 retrieval 會改善回答嗎？ | Natural Questions、Single、Exact Match | DPR 41.5；BM25 32.6 | 在 NQ 中，下游問答也改善。[DPR:dpr-r04] |
| 下游改善也沒有例外嗎？ | SQuAD、Single、Exact Match | DPR 29.8；BM25 38.1 | 仍有例外，不能把相關性寫成保證。[DPR:dpr-r05] |

`Top-20 retrieval accuracy` 與 `Exact Match` 是不同指標：前者衡量前 20 個 passages
中是否包含答案，後者衡量系統最後輸出的答案是否完全符合參考答案。

## 深入閱讀：Method

### Dual encoder

DPR 使用兩個獨立的 BERT encoders：question encoder 將問題轉成向量，passage
encoder 將 passage 轉成向量；兩者以 inner product 計算相似度並排序。
[DPR:dpr-c05]

這個分解很重要：passage embeddings 可以事先離線計算並建立 FAISS index；收到
問題時只需計算 question embedding，再搜尋最相近的 passages。[DPR:dpr-c06]

### Training signal

每個問題都有 positive passage，也需要 negatives。In-batch negatives 直接把 batch
中其他問題的 positive passages 當成 negatives，重用計算；最佳設定另外加入 BM25
找出的 hard negative，讓模型學習區分「字詞很像但不含答案」的 passage。
[DPR:dpr-c07]

Table 3 的 Natural Questions development 結果顯示，一組使用 in-batch negatives
與一個 BM25 hard negative 的設定得到 Top-5／20／100 為 65.8／78.0／84.9；這是
特定 ablation 設定，不應寫成所有 DPR 系統的固定表現。[DPR:dpr-r03]

### Passage 與 index

論文把 passage 當作 retrieval unit，而不是一次比較整份文件；實驗使用固定長度、
不重疊的 text blocks，並將文章標題加入 passage。[DPR:dpr-c08] 這個設計對 RAG
很重要，因為 chunk 的邊界會決定 retriever 可以找到什麼內容。

## Experiments 與評估

Top-k retrieval accuracy 的正式定義是：有多少問題能在前 k 個 retrieved passages
中找到至少一段包含答案的 passage。它不是「前 k 段中有幾段正確」。
[DPR:dpr-c09]

Figure 1 支援作者對 sample efficiency 的觀察：在 Natural Questions development
資料上，使用 1,000 個 examples 訓練的 DPR curve 已高於 BM25 curve；但這個圖不能
外推成所有任務只需要相同資料量。[DPR:dpr-r06]

## Limitations 與批判性筆記

1. **不是完整 generative RAG**：本文研究 open-domain extractive QA，答案是
   retrieved passage 中的 span。它為後來 RAG 的 retriever 提供基礎，但本身沒有
   教學簡報中所說的 generator。[DPR:dpr-c11]
2. **效果依資料分布而變**：SQuAD 的 retrieval 與 end-to-end 結果都提醒我們，
   dense retrieval 並非在每個資料集都勝過 BM25。[DPR:dpr-r02] [DPR:dpr-r05]
3. **Dense 與 sparse 各有 failure mode**：質化分析顯示 DPR 擅長 lexical variation
   與 semantic relation，卻可能漏掉罕見但關鍵的片語；BM25 恰好可能保留這種
   exact-match 優勢。[DPR:dpr-c10]
4. **不能跨設定只比最高數字**：Single/Multi、test/development、Top-k/Exact Match
   都是不同條件，Wiki 與簡報必須完整保留。

## 對 RAG Wiki 的貢獻

DPR 支援 RAG 教學中的 retrieval 半邊：

- [檢索器（Retriever）](../concepts/retriever.md)
- [Dense retrieval](../concepts/dense-retrieval.md)
- [Embedding 與相似度](../concepts/embedding.md)
- [Chunk 與 retrieval unit](../concepts/chunk.md)
- [Top-k retrieval evaluation](../concepts/top-k-evaluation.md)

Generator、retriever-generator 聯合建模與生成式任務屬於後續論文，見
[RAG paper note](rag.md) 與 [五篇總覽](../comparisons/five-paper-overview.md)；這些概念不是
DPR 的原始結論。

## Source evidence

- [DPR reading proposal](../../proposals/dpr.md)
- [DPR structured evidence](../evidence/dpr.json)

