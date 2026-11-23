---
reflection_id: wiki-milestone-a
based_on_runs: [001, 002, 003, 004, 005, 006, 007, 008, 009, 010, 011]
written_at: 2026-11-23
---

# Reflection：五篇 ingest 與 Wiki reconciliation

本文只根據 `logs/runs/001–011` 的實際紀錄撰寫。所有 runs 都在 2026-11-23
21:40–23:00（Asia/Taipei）之間完成。

## 1. 發生過哪些真實 failure？

| Run | 類型 | 內容 | 如何發現 | 修正 |
| --- | --- | --- | --- | --- |
| 002 | Validator | `wiki/evidence/README.md` 的範例 citation 被 parser 當成真的 citation | `validate_wiki.py` 第一次執行 | 改寫範例，不放寬 parser |
| 004→011 | Wiki 資料 | `concepts/rag.md` 宣告 `dpr` 為來源，但只引用 RAG 論文的 claim | Run 011 新增的 `validate_project.py` | 移除錯誤宣告 |
| 011 | Validator 本身 | YAML 1.1 把 `run_id: 010` 讀成八進位 8，而 `008`、`009` 讀成字串 | `validate_project.py` 第一次執行 | 改用原始文字比對 run_id |
| 009 | 環境 | Agent 的兩個執行環境都無法連到 arxiv.org（proxy 403） | 下載失敗 | 使用者在本機下載，hash 照常驗證 |
| 010→011 | Wiki 一致性 | Run 010 用 append 更新概念頁，讓四頁的「相關頁面」行落在新段落之前 | Run 011 人工 + 腳本檢查 | 移到頁尾 |
| 004／006→011 | 過時內容 | `dpr.md`、`chunk.md` 仍寫「等後續 ingest 再補」 | Run 011 grep | 改為連結已完成頁面 |

**沒有任何 proposal 被使用者退回修改**；五次核准都是在 proposal 後回覆「下一步」。
因此本專案的人工審核 loop 實際上只跑了「核准」分支。這是事實紀錄，不代表 proposal
不需要審核。

## 2. 從紀錄看出的模式

**(a) 作者的摘要句常比表格更廣。** 每篇 ingest 都找到至少一個「文字結論 vs 表格」
的範圍差異：

- DPR：Table 2 的 SQuAD 是 BM25 較好（Run 002）。
- 原始 RAG：Table 6 的 FEVER 是 BM25 較好（Run 004）。
- FiD：Table 1 的比較不是單變量 architecture ablation（Run 006）。
- Self-RAG：ASQA citation recall 是 Ret-ChatGPT 較高（Run 008）。
- RAGChecker：Table 2 completeness Spearman、Table 16 noisy-context Non-Fact F1 與作者
  文字不一致（Run 010）。

這說明「以 Table／Figure 為準、作者解讀標成 author claim」這條規則確實有用，不只是
形式要求。

**(b) 實驗設定的差異是最常見的誤讀風險。** 紀錄中反覆出現：dataset split（DPR、
FiD）、訓練規模 50k vs 150k（Self-RAG）、10 datasets 平均 vs 個別 domain
（RAGChecker）、無法追溯設定的數字（RAGChecker Section 4.4，最後選擇不收錄）。

**(c) Validator 只能抓它被設計去抓的東西。** `rag.md` 的錯誤宣告從 Run 004 存在到
Run 011，期間 `validate_wiki.py` 每次都通過，因為它不檢查 front matter 的來源宣告。
同樣地，過時的「待補」句子也沒有規則能抓。

**(d) Append 式更新會累積結構漂移。** Run 008、010 都用「附加新段落」更新既有概念頁，
速度快，但造成段落順序與過時句子問題。

## 3. 這次改了什麼

- 新增 `scripts/validate_project.py`：manifest 欄位、合法 lifecycle、proposal／manifest
  一致性、run log 順序、PDF hash、概念頁來源宣告、slide-to-Wiki mapping。
- 新增 `scripts/test_validators.py`：7 個明確標記為 **test_fixture** 的破壞案例，證明
  兩個 validators 會失敗。這些不是真實事故。
- 在 `concepts/chunk.md` 新增五篇論文的檢索單位術語對照。
- 更新 `graph/workflow.md`，與實際 runs 一致。

## 4. 對後續 milestone 的影響

- 大綱與簡報必須沿用 2(a)、2(b) 的邊界：每個數字附上 dataset／setting，不做跨論文
  排行榜。
- Slide mapping 已有 deterministic 檢查，大綱建立時就會被驗證。
- 仍無法自動檢查的：語意層面的誤讀（例如把 author claim 寫成事實）。這部分仍靠
  人工 review，是目前流程最大的盲點。
