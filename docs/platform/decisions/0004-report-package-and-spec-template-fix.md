# 決策紀錄 0004:報告產出包(簡報/SOP HTML/規格模板)與模板匯入修正

- 日期:2026-08-11
- 決策者:Cooper
- 狀態:已採用

## 背景

SOP 流程主體於決策0003定案後,進入「整理成報告」階段。Cooper 指定報告分三份產出:簡報、SOP md+html、規格文件標準化模板(md,Plane.io可匯入)。討論確認三份文件的分工與格式後動工。

## 決定

### 1. 三份報告產出的分工

- **簡報(Canva)**:對 SOP 的摘要版,用於溝通共識,不含 SOP 沒有的新資訊——避免兩邊之後各自改版導致內容對不上
- **SOP HTML**(`docs/platform/SOP.html`):離線靜態檔案,存 docs/platform/ 供團隊內部翻閱;`docs/platform/SOP.md` 為唯一權威來源(source of truth),HTML 是由 md 轉出的唯讀呈現層,md 有更新時需重新產生 HTML
- **規格文件標準化模板**(`docs/platform/templates/spec-template.md`):md 格式,可直接貼進 Plane.io issue 描述欄,Plane 能完整呈現 markdown 語法與表格

放棄的方案:HTML 版本原本考慮同時做「離線靜態檔案」與「Artifact 線上可分享連結」兩種,Cooper 確認只需要離線靜態檔案,避免兩份 HTML 之後要同步維護。

### 2. Canva 簡報產出流程

採用 Canva MCP 的 `request-outline-review → 使用者審閱 → generate-design-structured → 選候選版本 → create-design-from-candidate` 流程,10張投影片(balanced length),style 用預設 minimalist,未套用品牌套件(brand kit)。Cooper 從4個生成候選中選定版本4,已加入其 Canva 帳號(design id `DAHR_vAwRwg`)。

### 3. 規格文件模板的 Plane.io 匯入問題與修正

**發現的問題**:模板原始版本開頭放了一段 HTML 註解(`<!-- 使用說明... -->`)作為填寫前提示。Cooper 實際貼到 Plane.io 後,Plane 把貼上內容的「第一行」直接當作頁面標題,第一行是 HTML 註解而非規格文件標題,導致頁面標題變成「Untitled」,規格文件標題反而變成內文裡的一個 H1,與預期不符。

**根因**:設計模板時只憑對 markdown 規範的理解推導 Plane.io 會正確忽略 HTML 註解,未實際貼上驗證 Plane 的解析行為(尤其是「用第一行當頁面標題」這個 Plane 特有行為)。此問題已記入 `~/.claude/logs/pitfalls.md`(2026-08-11條目)。

**修正**:
- `docs/platform/templates/spec-template.md`:移除開頭註解區塊,第一行直接是 `# 規格文件:【需求名稱】`,前面不再有任何內容(含註解、空行)
- 新增 `docs/platform/templates/spec-template-使用須知.md`:原本的使用說明搬到這個獨立檔案,只給企劃自己看,不會被複製貼進 Plane.io

放棄的方案:曾考慮把使用說明保留在 `spec-template.md` 內、只是移到檔案更下方(如附錄),但這樣仍要求使用者記得複製時跳過某段,容易再犯同樣的錯;改為完全分離到獨立檔案,結構性避免此問題再發生。

## 影響

- `docs/platform/SOP.html`、`docs/platform/templates/spec-template.md`、`docs/platform/templates/spec-template-使用須知.md`、Canva 簡報為本次新增/修正產出
- 開放問題清單(SOP 第5節)的「規格文件標準化模板」項目已完成,可標記解決
