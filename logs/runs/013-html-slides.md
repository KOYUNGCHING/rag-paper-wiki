---
run_id: 013
operation: html_slides
source: all
started_at: 2026-11-23T22:54:00+08:00
input_state: outline_approved
status: awaiting_user_review
---

# Run 013：Milestone C — HTML 簡報

## Approval

使用者在 Run 012 大綱後回覆「下一步」，視為核准大綱。

## Checks before fix

- `validate_wiki.py`：125 claims／5 papers，通過。
- `validate_project.py`：14 mapped outline slides，通過；`docs/` 只有 README。
- 使用者本機 shell 沒有 headless browser；瀏覽器測試改在 agent 的雲端環境執行（同一份
  檔案），完成後再寫回 `docs/`。

## Findings

1. **視覺檢查發現（真實）**：手機寬度 390px 時，Slide 3 橫式流程圖被縮小到文字約 7px，
   無法閱讀。自動檢查沒有抓到，因為沒有水平溢出。
2. **測試本身的錯誤（真實）**：把 Slide 14 sources 改為預設收合後，no-JS 測試失敗，原因是
   測試在收合的 `<details>` 內找文字；頁面本身沒有問題。修正為檢查 summary 標籤。
3. 第一次截圖時多張 slide 呈半透明，是截圖時間落在 0.3 秒淡入動畫中；加入等待後正常。
   不是頁面錯誤。
4. 1366×800 桌機下，Slide 13（quiz）比視窗高 46px，可在 slide 內捲動；保留。

## Action taken

- 建立 `docs/index.html`、`docs/styles.css`、`docs/app.js`（原生，無外部依賴）。
- 圖表（DPR Table 2、RAGChecker Table 3）與示意圖皆以 SVG 重畫，figcaption 註明 paper 與
  table；未複製論文圖片。
- Slide 3 加入手機版直式流程圖；Slide 14 sources 預設收合。
- `validate_project.py` 新增 HTML ↔ outline ↔ Wiki 檢查：每張 slide 的 Wiki 頁面集合必須
  與大綱相同，claim IDs 必須與大綱一致且存在。
- `test_validators.py` 新增 2 個 test_fixture 案例（共 9 個）。
- 新增 `scripts/check_slides_browser.py`。
- 更新 `docs/README.md`（預覽、操作、Pages 發布步驟）、`README.md`、`scripts/README.md`、
  `graph/workflow.md`；大綱 front matter 改為 approved。

## Checks after fix

```text
node --check docs/app.js                     # OK
HTML 標籤配對檢查                             # 無未關閉標籤
python3 scripts/validate_wiki.py             # 125 claims／5 papers，通過
python3 scripts/validate_project.py          # 14 outline + 14 HTML slides，通過
python3 scripts/test_validators.py           # 9/9
python3 scripts/check_slides_browser.py      # 27/27
```

瀏覽器檢查涵蓋：14 張 slides；← → Home End、上一張／下一張按鈕、`#5` 深連結；按鈕上按
Space 不換頁；互動範例 4 步、failure 4 情境、quiz 對錯回饋；sources 展開；左右滑動；
390px 手機無水平溢出；無 JS 時全部內容可讀、4 步驟皆顯示、quiz 按鈕隱藏；reduced motion
下 transition 為 0；無 console error。桌機與手機 14 張截圖已人工檢視。

## Files changed

- `docs/index.html`、`docs/styles.css`、`docs/app.js`（新增）
- `docs/README.md`
- `scripts/validate_project.py`、`scripts/test_validators.py`
- `scripts/check_slides_browser.py`（新增）
- `scripts/README.md`、`README.md`、`graph/workflow.md`
- `slides-src/outline.md`、`slides-src/README.md`
- `logs/runs/013-html-slides.md`（新增）
