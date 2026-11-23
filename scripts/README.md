# Deterministic validators

此目錄只放不需 LLM 的可重複檢查程式，例如 manifest、狀態轉換、Markdown
連結、citation ID、未驗證 claim 與 slide-to-Wiki mapping。實作 validator
時不得加入模型 API 或憑證。

目前的 Wiki evidence、citation 與 link 檢查：

```bash
python3 scripts/validate_wiki.py
```

Manifest、lifecycle、概念頁來源宣告與 slide-to-Wiki mapping 檢查：

```bash
python3 scripts/validate_project.py
```

用明確標記為 `test_fixture` 的破壞副本，確認兩個 validators 會失敗：

```bash
python3 scripts/test_validators.py
```

需要 PyYAML（`validate_project.py` 讀取 manifest 與 front matter）。

`validate_project.py` 也會比對 `docs/index.html` 每張 slide 的 Wiki 頁面與 claim IDs 是否
與已核准的 `slides-src/outline.md` 一致。

瀏覽器檢查（鍵盤、按鈕、觸控、互動元件、手機版面、無 JS、reduced motion）：

```bash
pip install playwright && playwright install chromium
python3 scripts/check_slides_browser.py --shots tmp/shots
```
