---
paper_id: ragchecker
title: "RAGChecker: A Fine-grained Framework for Diagnosing Retrieval-Augmented Generation"
status: proposed
proposal_version: 1
proposed_at: 2026-11-23
approved_at: null
source_version: arXiv v2
source_sha256: 1034bf8f0b909895540e093f2d42d6d81f1dfae51711fcf1b0379dc834c084c2
---

# RAGChecker 閱讀計畫

這份文件只定義 RAGChecker 的正式 ingest 方向，尚不是 Wiki 內容。所有方法敘述與
結果數字都要在使用者核准後建立 evidence records，才可標記為 `verified`。

## 1. 論文想解決什麼問題？

前四篇論文（DPR、RAG、FiD、Self-RAG）主要用 end-to-end task metrics（如 exact
match、accuracy、ROUGE）評估系統。RAGChecker 的研究問題是：當 RAG 回答錯誤或
不完整時，能否用一套可對應人類判斷的細粒度指標，分辨問題來自 retriever 還是
generator，並找出具體的錯誤型態？

作者在 Introduction 指出三個 research gap（PDF p. 1–2）：

1. **Modular complexity**：RAG 由 retriever 與 generator 組成，需要同時評估整體與
   個別模組及其互動。
2. **Metric limitation**：recall@k、MRR 依賴標註 chunks 與固定切分；BLEU、ROUGE
   等 generator metrics 多為 rule-based 或 coarse-grained，難以評估長回答。
3. **Metric reliability**：既有 RAG metrics 與人類判斷的一致性仍少有檢驗。

## 2. Introduction 預計保留的重點

1. **Claim-level entailment**：從 response 與 ground-truth answer 抽取 claims，再檢查
   claims 是否被其他文字 entail，以取代 response-level 評分。
2. **三組指標**：overall metrics（給 user 比較系統）、diagnostic retriever metrics、
   diagnostic generator metrics（給 developer 找錯誤來源）。
3. **與既有框架的區分**：作者主張 RAGAS、TruLens、ARES 只在部分指標細粒度，
   RGB、RECALL、NoMIRACL 只評估特定面向；這是 author claim。
4. **Meta evaluation 與 8 個 RAG systems 的實驗**是主要貢獻。

預定證據範圍：PDF pp. 1–2，Abstract 與 Section 1；Section 2.2 related work
（PDF p. 3）只作為比較框架的背景。

## 3. RAGChecker 如何拆分 retrieval 與 generation errors

Section 3（PDF pp. 3–6）與 Figure 1（PDF p. 4）：

- **Formulation**：RAG = {R, G}；retriever 取 top-k chunks，generator 產生 response。
- **兩種 persona**：user 需要單一數值比較系統；developer 需要定位錯誤原因。錯誤原因
  被分為 retrieval errors（沒取回完整、相關 context）與 generator errors（無法辨認、
  利用 context 中的相關資訊）。
- **兩個元件**：text-to-claim extractor 與 claim-entailment checker。
- **Overall**：claim-level precision、recall、F1（response claims vs. ground-truth claims）。
- **Retriever**：claim recall（ground-truth claims 被 retrieved chunks 涵蓋的比例）；
  context precision 是 **chunk-level**（含任一 ground-truth claim 的 relevant chunks / k）。
- **Generator（六項）**：context utilization、relevant noise sensitivity、irrelevant
  noise sensitivity、hallucination、self-knowledge、faithfulness。關鍵在於：錯誤 claim
  依「是否被 relevant chunk／irrelevant chunk／任何 chunk entail」分成 noise 與
  hallucination；正確 claim 若未被任何 chunk entail，則歸為 self-knowledge。

完整公式在 Appendix B（PDF p. 15），ingest 時會對照 Figure 1 與 Appendix B，避免只
依文字摘要重寫公式。

## 4. Framework、metrics、datasets、baselines 與評估範圍

- **8 個 RAG systems**：2 retrievers（BM25、E5-Mistral）× 4 generators（GPT-4、
  Mixtral-8x7B、Llama3-8B、Llama3-70B）。Section 4.1，PDF p. 6；細節在 Appendix D。
- **Checker 本身也是 LLM**：claim extractor 與 checker 都使用 Llama3-70B，透過
  RefChecker 實作；其驗證在 Appendix G、Table 16（PDF pp. 21, 27）。
- **Benchmark**：4,162 queries、10 domains，由公開 QA datasets 改造；部分 domains 的
  short answers 由 GPT-4 擴寫成 long-form answers（Table 1，PDF p. 7；Appendix A）。
- **Meta evaluation baselines**：TruLens、RAGAS、ARES、CRUD-RAG 共 10 個 metrics，
  另加 BLEU、ROUGE-L、BERTScore（Section 4.2，PDF p. 6；Table 4–5，PDF p. 18）。
- **Human evaluation**：280 個 pairwise instances（10 domains × 28 system pairs），
  每筆兩位 annotators，評 correctness、completeness、overall assessment。

## 5. Results 預計保留的重點

### 5.1 適合簡報的核心結果

- **Meta evaluation（Table 2，PDF p. 7）**：在 correctness、completeness、overall 三面向，
  RAGChecker 與人類偏好的 correlation 高於表中各 baseline 的最佳 metric；但仍低於
  human annotator correlation 上界。數字會逐格標明 Pearson／Spearman 與比較對象，
  例如 overall assessment 的 Pearson 需對照 RAGAS Answer Similarity 與 Human row。
- **Main results（Table 3，PDF p. 8）**：10 datasets 平均結果。作為簡報 diagnosis 範例
  最有用的比較是：固定 generator、只換 retriever（BM25 → E5-Mistral），可觀察 claim
  recall、context precision 與 overall F1 一起改變；固定 retriever、比較 Llama3-8B 與
  70B，可觀察 generator metrics 的差異。
- **作者的 diagnostic 觀察（Section 4.3，PDF pp. 8–9）**：retriever 品質一致重要、
  context utilization 與 F1 相關較強、relevant noise sensitivity 明顯高於 irrelevant
  noise sensitivity、retriever recall 與 noise sensitivity 之間有 trade-off。這些都要標成
  author claim／observation。

### 5.2 適合 Wiki、未必放入簡報的結果

- **Section 4.4（PDF p. 9）與 Appendix F（PDF pp. 20–25，Figures 6–10）**：調整 top-k、
  chunk size、chunk overlap 與 generation prompt 的影響。Section 4.4 正文直接給出部分
  數字變化，但未在正文說明是哪個 system 或資料平均；ingest 時必須回到 Appendix F 與對應
  Figure 確認設定，確認不了就不寫數字。
- **Per-dataset 結果（Tables 6–15，PDF pp. 23–26）**：只在需要檢查平均值是否掩蓋差異時使用。
- **Figure 4（PDF p. 19）**：RAGChecker 與 RAGAS 的 score distribution 比較。

## 6. 對 RAG 教學的用途

前四篇讓學生知道「如何找 evidence、如何生成、何時找」；RAGChecker 回答「答錯時
怎麼知道是哪裡錯」：

- 從單一 end-to-end 分數進到 **claim-level** 的 correct／incorrect／missing 分類。
- 把同一個錯誤答案拆成「需要的資訊沒被檢索到」（retriever claim recall 低）與「資訊有在
  context 但 generator 沒用或被 noise 帶偏」（context utilization、noise sensitivity）。
- 很適合簡報的 retrieval-failure example：用一個 query 示範錯誤 claim 分別落在 relevant
  chunk、irrelevant chunk 或沒有任何 chunk 支持時，各自對應哪個指標。
- 與 Self-RAG 的連結（預定 `wiki_synthesis`）：Self-RAG 讓模型在生成中預測 relevance／
  support；RAGChecker 則是外部評估框架。兩者都關心 evidence support，但角色不同，不應
  寫成互相驗證。

簡報會用原創 HTML／CSS／SVG 重畫 claim 分類示意，不複製 Figure 1。

## 7. 容易讀錯的比較與風險

1. **Metric direction 不一致**：Table 3 中 NS(I)、NS(II)、hallucination、self-knowledge
   越低越好，其餘越高越好；self-knowledge 低只在「希望完全依賴 context」時才算好。
2. **Context precision 是 chunk-level，claim recall 是 claim-level**：兩者分母不同，不能當
   同一種 precision／recall 解讀。
3. **評估者也是 LLM**：Llama3-70B extractor／checker 的錯誤會進入所有指標；指標不是
   ground truth。
4. **Ground truth 部分由 GPT-4 擴寫**：Finance、Lifestyle、Recreation、Technology、Science、
   Novel 的 long-form answers 由 GPT-4 產生，可能影響 GPT-4 作為 generator 的比較。
5. **「significantly better correlations」**：Table 2 只列 correlation 值；ingest 時需檢查是否
   有統計檢定，否則只能寫「correlation 較高」。
6. **Table 2 只列每個 baseline 的最佳 metric**：完整比較在 Table 5；RAGChecker row 是
   「same metric as human」，與 baseline metrics 的定義不同。
7. **Meta evaluation 樣本有限**：280 pairs，每筆 2 annotators；不能外推為所有 domains 與
   所有 RAG systems 的普遍保證。
8. **Table 3 是 10 datasets 平均**：不同 domain 的 query 數差很多（KIWI 71、Biomedical
   511）；平均值可能掩蓋 per-dataset 差異。
9. **只有 8 個系統、2 種 retrievers**：「retriever matters consistently」等觀察只在這組設定
   成立；「correlates strongly」是作者對 8 個點的觀察，不是因果。
10. **不要和前四篇數字並列**：RAGChecker 的 F1 是 claim-level，與 FiD／RAG 的 exact match
    完全不同，不能放進同一張排行榜。
11. **時間性**：v2（2024-08-17）只反映當時的 GPT-4、Llama3 與 baselines。

## 8. 核准後的預定輸出

- `wiki/papers/ragchecker.md`
- `wiki/evidence/ragchecker.json`，包含 Figure 1、Table 1、Table 2、Table 3，以及確認過的
  Appendix B／F locators
- 新增概念頁（名稱以論文定義為準）：claim-level evaluation／claim entailment、retriever
  diagnostic metrics（claim recall、context precision）、generator diagnostic metrics
  （context utilization、noise sensitivity、hallucination、self-knowledge、faithfulness）、
  RAG meta evaluation
- 更新 retriever、generator、top-k evaluation、chunk、citation quality 等既有頁面
- 五篇論文整體 comparison：DPR → RAG → FiD → Self-RAG → RAGChecker
- `logs/runs/010-ragchecker-ingest.md` 與 deterministic checks
