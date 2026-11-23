---
run_id: 012
operation: slide_outline
source: all
started_at: 2026-11-23T22:51:00+08:00
input_state: wiki_reconciled
status: awaiting_user_approval
---

# Run 012：Milestone B — 教學大綱與 slide-to-Wiki mapping

## Checks before fix

- `validate_wiki.py`：125 claims／5 papers，通過。
- `validate_project.py`：通過，0 mapped slides（`slides-src/outline.md` 不存在）。

## Findings

1. **真實 validator failure**：第一次驗證大綱時回報
   `slide 1: Wiki page ../wiki/index.md is not verified`。`wiki/index.md` 是導覽頁，沒有
   verified front matter，不應作為內容來源。處理方式是從 Slide 1 移除它，保留
   `five-paper-overview.md`；沒有放寬 validator。
2. **時間超出**：初版各張時間合計 12.5 分鐘，超過 10–12 分鐘。縮短 Slides 4、5、8、11，
   合計 11.5 分鐘。
3. Validator 原本只檢查 slide 中的 paper label，不檢查 claim ID 是否存在。已補上。
4. 互動範例與 failure 範例需要示範資料，論文中沒有適合學生的完整小例子。採用虛構城市
   「青嶼市」並寫入 `wiki/concepts/rag-error-attribution.md`，明確標示為虛構教學資料，
   讓 slides 仍可追溯到 Wiki。

## Action taken

- 建立 `slides-src/outline.md`：14 張、11.5 分鐘、47 個不同的 verified claims。
- 在 `rag-error-attribution.md` 加入虛構 chunks K1–K5 與 ground truth。
- `validate_project.py` 新增 slide claim ID 檢查。
- 更新 `slides-src/README.md`。

## Checks after fix

```text
python3 scripts/validate_wiki.py
Wiki validation passed: 125 verified claims, 125 cited claims, 5 paper.

python3 scripts/validate_project.py
Project validation passed: 5 papers in manifest, lifecycle consistent, 14 mapped slides.

python3 scripts/test_validators.py
7/7 fixture cases caught.
```

## Files changed

- `slides-src/outline.md`（新增）
- `slides-src/README.md`
- `wiki/concepts/rag-error-attribution.md`
- `scripts/validate_project.py`
- `logs/runs/012-slide-outline.md`（新增）
