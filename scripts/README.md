# Deterministic validators

此目錄只放不需 LLM 的可重複檢查程式，例如 manifest、狀態轉換、Markdown
連結、citation ID、未驗證 claim 與 slide-to-Wiki mapping。實作 validator
時不得加入模型 API 或憑證。

目前的 Wiki evidence、citation 與 link 檢查：

```bash
python3 scripts/validate_wiki.py
```

