---
paper_id: rag
title: Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
status: approved
proposal_version: 1
proposed_at: 2026-11-23
approved_at: 2026-11-23
source_version: arXiv v4
source_sha256: 23e3249e9a1e75418d82efecab0ea8c4d033b89c93742f63208d47ce01f21233
---

# RAG 原始論文閱讀計畫

這份文件只定義正式 ingest 的閱讀方向，尚不是 Wiki 內容。所有架構敘述、結果
數字與限制，都必須在使用者核准後建立 claim-level evidence 才能標記為 `verified`。

## 1. 論文想解決什麼問題？

大型預訓練語言模型會把知識儲存在參數中，但參數知識不容易直接更新、檢查來源，
也可能產生沒有根據的文字。另一方面，當時結合神經 retriever 的方法多集中在
extractive tasks，尚未形成適用於一般 seq2seq generation 的統一方法。

正式筆記預計聚焦這個研究問題：如何把預訓練 generator 的 parametric memory 與
可檢索、可替換的 non-parametric memory 結合，並在 knowledge-intensive tasks 中
共同 fine-tune？

## 2. Introduction 預計保留的重點

1. **Parametric knowledge 的限制**：難以直接更新、難以提供 provenance，且生成
   內容可能出現 hallucination。
2. **Hybrid memory 的核心想法**：generator 保留參數知識，retriever 則從外部文字
   index 提供可讀、可替換的知識。
3. **RAG 的兩個元件**：DPR-based retriever 負責找 passages；BART-based generator
   以 input 與 retrieved passages 共同生成輸出。
4. **Latent document**：模型將 retrieved document 視為 latent variable，對 top-k
   documents 的生成結果進行 marginalization，而不是只把第一名 passage 當唯一來源。
5. **通用 seq2seq 目標**：相同架構可 fine-tune 到 open-domain QA、abstractive QA、
   question generation 與 fact verification。
6. **可替換外部 index**：non-parametric memory 可以在不重新訓練 generator 的情況下
   更換，但「可更新」不等於「更新後一定正確」。

預定證據範圍：PDF pp. 1–2，Section 1 與 Figure 1。

## 3. Results 預計保留的重點

### 3.1 適合簡報的核心結果

- **Retrieval 加入 generation 後的 QA 結果**：Table 1 的 Natural Questions test
  中，RAG-Sequence Exact Match 為 44.5，DPR 為 41.5。正式引用時必須保留 task、
  test split、model variant 與 Exact Match 指標，不能只寫成「RAG 比 DPR 好 3 分」。
- **External memory 可更新**：Section 4.5 以不同年份 Wikipedia index 示範，輸出會
  隨替換的 non-parametric memory 改變。正式 Wiki 可保留概念結論；由於實驗數字在
  正文而非 Table／Figure，依本專案規則不把該段精確百分比帶入簡報。
- **更多文件不必然一直更好**：Figure 3 顯示不同 RAG variant 與 task 對 retrieved
  document 數量的反應不同；RAG-Token 在 Natural Questions 並非單調改善。

### 3.2 適合 Wiki、視篇幅決定是否放簡報

- **生成任務**：Table 2 比較 BART、RAG-Token 與 RAG-Sequence 在 MS-MARCO、
  Jeopardy question generation 與 FEVER 的不同 metrics。
- **人工評估**：Table 4 的 Jeopardy evaluation 比較 factuality 與 specificity，但
  包含 `both good`、`both poor` 與 `no majority`，不能只挑 `RAG better` 報告。
- **Retrieval ablation**：Table 6 比較 learned retrieval、frozen retriever 與 BM25。
  大多數 task 支援 learned retrieval 的價值，但 FEVER 是 BM25 表現更好的重要例外。
- **Generation examples**：Table 3 可說明 RAG 可能產生更具體內容，也同時保留
  不正確或部分正確標記，避免把少量例子當整體證據。

預定證據範圍：PDF pp. 5–8，Section 4，Tables 1–6 與 Figures 2–3。

## 4. Method 預計如何整理？

正式 ingest 時會在 Results 之後補上：

1. **Retriever**：使用 DPR bi-encoder 與 MIPS 取得 top-k passages。
2. **Generator**：使用 BART-large，將 input 與 retrieved passage 串接後生成。
3. **RAG-Sequence**：整個 output sequence 假設由同一個 latent document 支援，
   再對 top-k documents 的 sequence probabilities 做 marginalization。
4. **RAG-Token**：每個 output token 可以依賴不同 latent document，再逐 token
   marginalize。
5. **Training boundary**：fine-tune query encoder 與 generator；document encoder 與
   document index 固定。正式筆記不可把這種設定簡化成所有元件都 end-to-end 更新。
6. **Non-parametric memory**：論文使用固定版本 Wikipedia passages 的 dense index；
   這是該實驗的知識來源，不是所有 RAG 系統的必要限制。
7. **Decoding**：RAG-Token 可使用標準 autoregressive decoding；RAG-Sequence 需要
   專門的 thorough／fast decoding approximation。

預定證據範圍：PDF pp. 2–4，Sections 2–3。

## 5. 對 RAG 教學的用途

這篇論文將成為簡報的核心來源，可支援：

- 為什麼只靠 LLM 參數知識會遇到更新、來源與 hallucination 問題。
- Retrieve → Augment → Generate 的完整概念圖。
- Parametric memory 與 non-parametric memory 的分工。
- Retriever 找到 passages 後，generator 如何把 passages 當額外 context。
- RAG 不是單一模型名稱，而是一種把檢索結果接入生成流程的設計家族；但必須先
  清楚區分「原始論文的特定 RAG 架構」與後來泛稱的 RAG。
- 為什麼 retrieval quality、generation quality 與 final answer correctness 要分開檢查。
- 外部 index 比模型參數容易替換，但來源品質、偏見與過時資訊仍會流入生成結果。

簡報會自行重畫 Figure 1 的概念，不直接複製論文圖片。

## 6. 容易讀錯的表格、術語與比較

1. **原始 RAG 不等於所有現代 RAG**：這篇使用 DPR、BART、latent documents 與
   marginalization；後來常見的 prompt-based pipeline 不一定採用相同訓練方式。
2. **「End-to-end」有邊界**：query encoder 與 generator 會更新，但 document encoder
   與 index 在 fine-tuning 時保持固定。
3. **DPR initialization 含 retrieval supervision**：不能宣稱 retriever 完全沒有接受
   retrieval supervision；只是下游 fine-tuning 沒有直接標註應檢索哪篇文件。
4. **RAG-Sequence 與 RAG-Token 不可混用**：兩者 marginalization 與 decoding 不同，
   各 task 的最佳 variant 也不同。
5. **Table 1 的 TQA 有兩種 test split**：標準 TQA 與 TQA-Wiki 數字不可交換。
6. **Table 2 混合不同 metrics**：BLEU、Q-BLEU、ROUGE-L 與 label accuracy 不能
   橫向當作同一尺度。
7. **Gold access**：Table 2 的部分 SOTA baseline 使用 gold context／evidence，與
   RAG 自行 retrieval 的條件不同。
8. **Table 6 是 development set**：不可和 Table 1／2 的 test results 混在一起。
9. **「更 factual」不是零 hallucination**：結果來自特定 tasks、metrics 與人工評估，
   不能保證所有生成都正確。
10. **Knowledge update 不等於 truth update**：替換 index 能改變模型可取得的資訊，
    但 Wikipedia 或其他來源仍可能錯誤、有偏見或不完整。
11. **SOTA 有時間性**：論文的 state-of-the-art 是 2020 年論文與當時設定下的結果，
    不是目前模型排名。

## 7. 核准後的預定輸出

- `wiki/papers/rag.md`
- 更新既有 retriever、embedding、chunk 與 top-k pages
- 新增 parametric memory、non-parametric memory、generator、context augmentation、
  RAG-Sequence／RAG-Token、knowledge update 等 concept pages
- RAG claim-level evidence，包含 Section／PDF page／Table 或 Figure locator
- 與 DPR 的第一批 cross-paper links
- RAG ingest run log 與 deterministic checks

## 8. 核准結果

使用者在本 proposal 里程碑後指示進行「下一步」，授權正式 ingest。驗證結果記錄於
[`logs/runs/004-rag-ingest.md`](../logs/runs/004-rag-ingest.md)。

