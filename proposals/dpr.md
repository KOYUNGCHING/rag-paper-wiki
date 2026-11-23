---
paper_id: dpr
title: Dense Passage Retrieval for Open-Domain Question Answering
status: approved
proposal_version: 1
proposed_at: 2026-11-23
approved_at: 2026-11-23
source_version: arXiv v3
source_sha256: 3e67fc1a9977715acf722d85f0b7d124b03715e975f6310a4d6c12094190912f
---

# DPR 閱讀計畫

這份文件只定義正式 ingest 的閱讀方向，尚不是 Wiki 內容。以下觀察必須在使用者
核准後重新對照原文，建立 evidence records，才能標記為 `verified`。

## 1. 論文想解決什麼問題？

Open-domain question answering（開放領域問答）通常先由 retriever 從大型語料庫
挑出少量候選 passages，再交給 reader 找答案。當時常見的 TF-IDF／BM25 依賴字詞
重疊，可能無法處理同義詞或改寫；另一方面，dense retrieval 又被認為需要大量標註
或額外 pretraining。

正式筆記預計聚焦這個研究問題：是否能只用既有的 question-passage pairs，搭配
簡單的 dual-encoder 設計，訓練出實用且勝過 BM25 的 dense retriever？

## 2. Introduction 預計保留的重點

1. **Retriever-reader 兩階段架構**：retriever 負責縮小搜尋範圍，reader 才負責
   從候選 passage 擷取答案。
2. **Sparse retrieval 的限制**：BM25 擅長精確關鍵字，但難以直接連結語意相近、
   字面不同的問句與 passage。
3. **當時的 dense retrieval gap**：既有方法通常仰賴昂貴的額外 pretraining；
   DPR 詢問能否以較簡單的 supervised setup 達到更好的結果。
4. **主要貢獻**：以兩個 BERT encoders、inner product、in-batch negatives 與
   BM25 hard negative 組成可擴展的 dense passage retriever。
5. **檢索與下游表現的關係**：論文不只測 passage retrieval，也檢查較好的 retrieval
   是否能轉化為較高的 end-to-end QA accuracy。

預定證據範圍：PDF pp. 1–2，Section 1；背景定義補充使用 PDF p. 2，Section 2。

## 3. Results 預計保留的重點

### 3.1 適合簡報的核心結果

- **DPR 與 BM25 的檢索差異**：Table 2 顯示，在 Single training 的 Natural
  Questions test set，Top-20 retrieval accuracy 為 DPR 78.4、BM25 59.1。
  這組數字適合說明 dense retrieval 的價值，但正式引用時必須同時保留 dataset、
  split、Top-20 與 Single training 條件。
- **Retrieval 對 end-to-end QA 的影響**：Table 4 的 Single setting 中，Natural
  Questions exact match 為 DPR 41.5、BM25 32.6。這可支援「找到較好的 passage
  通常能改善回答」的教學主線，但不能把 exact match 說成 retrieval accuracy。
- **Dense retriever 也會失敗**：Table 7 顯示 DPR 能處理部分語意關聯，卻可能漏掉
 罕見而關鍵的名稱；這適合用於簡報的 retrieval failure 案例。

### 3.2 適合 Wiki、未必放進簡報的技術結果

- Figure 1：sample efficiency，以及作者所述用 1,000 個 training examples 已超過
  BM25 的觀察。
- Table 3：in-batch negatives、batch size 與額外 BM25 hard negative 的影響。
- Section 5.4：dense index 的查詢速度、embedding 計算與建 index 成本之間的取捨。
- Appendix A／B：distant supervision、similarity function 與 loss 的補充比較。

預定證據範圍：PDF pp. 5–8，Sections 5–6；PDF pp. 12–13，Appendices A–D。

## 4. Method 預計如何整理？

正式 ingest 時會在 Results 之後補上：

1. Question encoder 與 passage encoder 的 dual-encoder 架構。
2. 以 dot product 計算 question-passage similarity。
3. 離線預先計算 passage embeddings，並以 FAISS 做 maximum inner product search。
4. Positive passage、random／BM25／gold negatives 的定義。
5. In-batch negative training 如何重用 batch 內的 passages。
6. Wikipedia 切成固定 100-word passages，以及約 2,100 萬 passages 的實驗語料。
7. Retriever 與 reader 分工，避免把 DPR 本身誤寫成完整的生成式 RAG 系統。

預定證據範圍：PDF pp. 2–4，Sections 2–4；reader 補充使用 PDF pp. 7–8，Section 6。

## 5. 對 RAG 教學的用途

DPR 在整體 Wiki 中扮演「如何找到外部資料」的基礎來源，可支援：

- Retriever 為何是 RAG 的第一個關鍵元件。
- Embedding 與 vector similarity 的直覺。
- Passage／chunk 為何要切分，以及 retrieval unit 的意義。
- Passage embeddings 可離線建立 index，而 query embedding 在 runtime 計算。
- Top-k retrieval accuracy 與回答正確率是兩個不同層級的評估。
- Dense 與 sparse retrieval 各自擅長的情境，不能把 dense 說成永遠較好。

DPR 論文研究的是 open-domain extractive QA，不是後來常見的完整 generative RAG。
正式 Wiki 必須把這項範圍限制寫清楚，再由 RAG 論文接續 generator 的角色。

## 6. 容易讀錯的表格與比較

1. **Table 2 的 metric**：Top-k retrieval accuracy 是「多少問題能在前 k 個 passages
   中找到含答案的 passage」，不是前 k 個 passages 中有多少比例是正確 passage。
2. **Single 與 Multi 不可混用**：不同 training data 設定的數字必須分開描述。
3. **Test 與 development set 不可混用**：Table 2 是 test；Table 3 是 Natural
   Questions development set。
4. **SQuAD 是明確例外**：DPR 並非在每個資料集都勝過 BM25，作者也討論了
   lexical overlap 與資料分布偏差。
5. **Retrieval 與 end-to-end 不可混用**：Table 2 是 Top-k retrieval accuracy；
   Table 4 是 QA exact match。
6. **不同 baseline 的前提不同**：ORQA、REALM、BM25 與 DPR 的 pretraining、reader、
   passage 長度與訓練方式不完全相同，不能只拿最高數字宣稱方法全面優勝。
7. **效率數字高度依賴硬體與 index 設定**：Section 5.4 的速度不可直接當作一般
   系統保證。
8. **Table 7 是質化例子**：可用來解釋 failure mode，但不能當作整體勝率證據。

## 7. 核准後的預定輸出

- `wiki/papers/dpr.md`
- 初始 concept pages：dense retrieval、retriever、embedding、chunk、top-k evaluation
- DPR evidence records，包含 Section／PDF page／Table 或 Figure locator
- DPR ingest run log 與 deterministic checks

## 8. 核准結果

使用者已於 2026-11-23 核准本閱讀方向。正式 ingest 與驗證結果記錄於
[`logs/runs/002-dpr-ingest.md`](../logs/runs/002-dpr-ingest.md)。

