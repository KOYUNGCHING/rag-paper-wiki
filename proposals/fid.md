---
paper_id: fid
title: Leveraging Passage Retrieval with Generative Models for Open Domain Question Answering
status: approved
proposal_version: 1
proposed_at: 2026-11-23
approved_at: 2026-11-23
source_version: arXiv v2
source_sha256: f1ee7e927c3fb31beb2146f8c205692a91b40dadd65d80e025c6686e4d430953
---

# FiD 閱讀計畫

這份文件只定義 Fusion-in-Decoder（FiD）的正式 ingest 方向，尚不是 Wiki 內容。
所有方法敘述與結果數字都要在使用者核准後建立 evidence records，才可標記為
`verified`。

## 1. 論文想解決什麼問題？

Open-domain QA 系統可能取得許多 retrieved passages，但如何讓 generative model
有效整合多篇 evidence 並不直觀。若把所有 passages 直接串成一個長 input，encoder
self-attention 的成本會快速增加；若各 passage 完全獨立處理，又難以跨 passage
整合資訊。

FiD 的研究問題是：能否讓 encoder 分別處理每個 question-passage pair，再由 decoder
共同 attention 所有 passage representations，以較可擴展的方式融合多篇證據？

## 2. Introduction 預計保留的重點

1. **Closed-book generation 的成本**：只靠模型參數保存知識，往往需要非常大的
   model，訓練與查詢成本高。
2. **Extractive aggregation 的困難**：多篇 passages 可能各自提供部分 evidence，
   單純抽取 span 不容易整合。
3. **兩階段流程**：先用 BM25 或 DPR 取得 support passages，再由 seq2seq model
   生成答案。
4. **FiD 的核心假設**：generative decoder 可以跨 passages 聚合 evidence，而每篇
   passage 的 encoder 計算保持獨立。
5. **Scaling claim**：作者觀察到增加 retrieved passages 時，FiD 表現持續改善，並
   將此解讀為 generative model 能結合多篇 evidence 的支持證據。

預定證據範圍：PDF pp. 1–2，Section 1 與 Figures 1–2。

## 3. Results 預計保留的重點

### 3.1 適合簡報的核心結果

- **FiD 與前代方法比較**：Table 1 的 Natural Questions test Exact Match 為
  FiD-large 51.4、RAG 44.5、DPR 41.5。這組數字可用來說明多 passage fusion 的潛力，
  但正式引用必須保留 model size、retriever 與 test setting，不能單獨歸因給 decoder。
- **Passage 數量與表現**：Figure 3 顯示 FiD-base 在 Natural Questions、TriviaQA 與
  SQuAD validation curves 上，retrieved passages 增加時 Exact Match 整體上升。
  正式 Wiki 會保留曲線趨勢，不從圖中猜未標示的精確數字。
- **訓練 passages 的成本取捨**：Table 2 顯示以較少 passages 訓練會降低表現，
  再以較多 passages fine-tune 可縮小差距。這適合說明品質與運算成本的 trade-off。

### 3.2 適合 Wiki、未必放入簡報的結果

- Table 1 的 TriviaQA 有 open-domain test 與 hidden test 兩欄，必須完整標示。
- SQuAD Open 使用 validation set 作為 test，不能和其他官方 test results 直接等同。
- Table 2 是 development results，不可與 Table 1 test results 混用。
- 作者以 Natural Questions、TriviaQA、SQuAD 三個資料集觀察 passages 數量效應，
  但這不證明所有 RAG task 都會隨 passages 增加而改善。

預定證據範圍：PDF pp. 3–5，Section 4，Tables 1–2 與 Figure 3。

## 4. Method 預計如何整理？

正式 ingest 時會在 Results 之後補上：

1. **Retrieval**：使用 BM25 或 DPR；FiD 本身沒有提出新的 retriever。
2. **Input formatting**：每個 passage 的 title 與 text 分別和 question 組合。
3. **Independent encoding**：每個 question-passage pair 獨立通過 T5 encoder。
4. **Representation concatenation**：把所有 passage encoder outputs 串接。
5. **Decoder fusion**：decoder 對完整 concatenated representations 做 attention，
   在 decoder 階段融合 evidence。
6. **Scaling reason**：encoder self-attention 只在單一 passage context 內進行，所以
   隨 passage 數量近似線性增加，而不是對整個 concatenated input 做平方成本的
   self-attention。
7. **Training boundary**：retriever 並未和 FiD generator 一起 end-to-end 學習；
   論文把整合 retriever 列為 future work。

預定證據範圍：PDF pp. 2–3，Section 3 與 Figure 2；限制補充使用 PDF p. 5，
Section 5。

## 5. 對 RAG 教學的用途

FiD 將補上目前 Wiki 缺少的「多 passage context 如何整合」：

- Retriever 找到多篇 passages 後，不一定只選第一篇。
- Encoder 可各自理解 question-passage pair，decoder 再跨 passages 聚合資訊。
- 更多 context 可能帶來更多 evidence，也同時增加運算量與 distractors。
- FiD 與原始 RAG 的 fusion mechanism 不同：原始 RAG 對 latent documents 的
  probabilities 做 marginalization；FiD 把各 passage encoder representations 交給
  同一 decoder 做 joint attention。
- Retrieval 與 generation 可以模組化，但分開訓練也代表 retrieval error 不會由
  generator training 自動修正。

簡報會自行以 HTML／CSS／SVG 重畫 Figure 2 概念，不直接複製論文圖。

## 6. 容易讀錯的圖表與比較

1. **FiD 不是新的 retriever**：它使用 BM25 或 DPR，貢獻重點是 reader/generator
   如何處理多 passages。
2. **不是 joint end-to-end retriever training**：retrieval integration 被列為 future
   work，不能說 FiD 會從答案 loss 自動改善 retriever。
3. **FiD 與 RAG fusion 不同**：兩者都 retrieval + generation，但 evidence aggregation
   mechanism 不同。
4. **Table 1 的 model sizes 不同**：FiD-base、FiD-large、T5-11B、RAG 等參數量與
   training setup 不同；最高分不能只歸因於單一架構差異。
5. **TriviaQA 有兩種 test**：open-domain test 與 hidden test 的數字不可交換。
6. **SQuAD Open 的 split 特殊**：validation 被當作 test，不能直接和其他 test set
   比較。
7. **Figure 3 只支援觀察範圍**：最多顯示到該實驗的 passage 數量，不能外推成
   passages 無限增加都會改善。
8. **Table 2 是 dev set**：不能和 Table 1 的 test scores 混用。
9. **Exact Match 不等於 evidence quality**：答案正確不表示每篇 passage 都相關，
   也不表示模型的生成過程可追溯。
10. **作者的 evidence-fusion 解讀仍是推論**：passage 數量與 performance 一起上升
    支援 aggregation hypothesis，但不是對模型內部推理的直接證明。
11. **SOTA 有時間性**：Table 1 是 2020–2021 年當時的 baselines 與設定。

## 7. 核准後的預定輸出

- `wiki/papers/fid.md`
- FiD claim-level evidence，包含 Figure 2、Table 1、Figure 3、Table 2 locators
- 新增 multi-passage fusion、Fusion-in-Decoder、encoder/decoder scaling 概念頁
- 更新 generator、context augmentation、chunk、top-k evaluation 等既有頁面
- 建立 DPR → RAG → FiD 的跨論文比較與連結
- FiD ingest run log 與 deterministic checks

## 8. 核准結果

使用者在本 proposal 里程碑後指示進行「下一步」，授權正式 ingest。驗證結果記錄於
[`logs/runs/006-fid-ingest.md`](../logs/runs/006-fid-ingest.md)。

