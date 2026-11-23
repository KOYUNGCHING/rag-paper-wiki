---
run_id: 011
operation: wiki_reconciliation_and_reflection
source: all
started_at: 2026-11-23T22:47:00+08:00
input_state: five_papers_verified
status: awaiting_user_review
---

# Run 011：Milestone A — Wiki reconciliation 與 reflection

## Checks before fix

- `validate_wiki.py`：125 verified claims、125 cited claims、5 papers，通過。
- 只有 `validate_wiki.py`；沒有 manifest、lifecycle 或 slide mapping 的自動檢查。

## Findings

1. **第一次執行新的 `validate_project.py` 就失敗（真實）**：
   - `logs/runs/010-ragchecker-ingest.md: run_id does not match filename`：原因是
     PyYAML 依 YAML 1.1 把 `010` 讀成八進位 8；`008`、`009` 不是合法八進位，所以讀成
     字串而通過。這是 validator 本身的 bug，不是 log 錯誤。
   - `wiki/concepts/rag.md: verified_sources lists ['dpr'] but never cites them`：該頁提到
     「原始 RAG 由 DPR 初始化」，但引用的是 RAG 論文的 `rag-c06`。錯誤宣告自 Run 004
     起存在。
2. **過時內容**：`papers/dpr.md` 仍寫「要等 RAG 論文 ingest 後再補入」；`concepts/chunk.md`
   仍寫「後續 ingest 會檢查 RAG、FiD」。
3. **結構漂移**：`chunk.md`、`citation-quality.md`、`rag.md`、`top-k-evaluation.md` 的
   「相關頁面」行在 Run 010 append 後位於新段落之前。
4. **術語**：檢索單位在五篇中分別稱為 passage／document／chunk；Exact Match（FiD、
   RAG、DPR）與 Self-RAG 的 string exact match 是不同指標，現有頁面已分開描述，未混用。
   Wiki 中未發現跨頁矛盾的定義。
5. **Comparison completeness**：四份比較頁涵蓋 2、3、4、5 篇的累進比較；五篇總覽已在
   Run 010 建立。

## Action taken

- 新增 `scripts/validate_project.py`；修正其 run_id 解析。
- 修正 `concepts/rag.md` 的 `verified_sources`（移除 `dpr`）。
- 改寫 `papers/dpr.md` 與 `concepts/chunk.md` 的過時句。
- 將四頁的「相關頁面」移到頁尾。
- 在 `concepts/chunk.md` 新增術語對照表（`wiki_synthesis`）。
- 新增 `scripts/test_validators.py`（test_fixture，7 案例）。
- 依實際 runs 重寫 `graph/workflow.md`。
- 撰寫 `logs/reflection.md`。
- 更新 `README.md`、`scripts/README.md`。

## Checks after fix

```text
python3 scripts/validate_wiki.py
Wiki validation passed: 125 verified claims, 125 cited claims, 5 paper.

python3 scripts/validate_project.py
Project validation passed: 5 papers in manifest, lifecycle consistent, 0 mapped slides.

python3 scripts/test_validators.py
7/7 fixture cases caught.
```

## Files changed

- `scripts/validate_project.py`（新增）
- `scripts/test_validators.py`（新增）
- `scripts/README.md`
- `graph/workflow.md`
- `logs/reflection.md`（新增）
- `logs/runs/011-wiki-reconciliation.md`（新增）
- `README.md`
- `wiki/papers/dpr.md`
- `wiki/concepts/rag.md`
- `wiki/concepts/chunk.md`
- `wiki/concepts/citation-quality.md`
- `wiki/concepts/top-k-evaluation.md`
