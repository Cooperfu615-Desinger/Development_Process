# 決策紀錄 0001(架構層級):docs 依領域拆分為 platform / game

- 日期:2026-08-12
- 決策者:Cooper
- 狀態:已採用

## 背景

原本 `docs/` 下只有博弈平台功能類(會員/金流/後台)的 SOP 一套。Cooper 現在要再整理一份「博弈遊戲開發流程」說明,兩者在關鍵驗證要求上本來就分屬不同軌道——平台 SOP 開頭即明訂「不適用:遊戲邏輯/賠付表/機率模型類專案」。需要決定新文件要用什麼架構放。

## 考慮過的選項

### 選項 A:共用一份骨架,兩領域各自補充差異段落
- 優點:流程共通部分(需求→規格→開發→測試→驗收→交付、Plane.io工作單結構)不用寫兩次
- 缺點:遊戲開發預期會有平台流程完全沒有的關卡(機率/賠付/RTP驗證,可能還有第三方驗證機構送測),差異可能大到「補充段落」撐不住,共用骨架反而讓兩邊改動互相牽動,增加維護成本
- 結果:放棄

### 選項 B:兩個獨立資料夾(`docs/platform/`、`docs/game/`),各自完整複製今天這套結構(SOP.md+html、decisions/、templates/)
- 優點:各自獨立成套,不用跨資料夾拼湊才能看懂一個領域的完整流程;以後其中一邊改動不會誤動到另一邊
- 缺點:若未來真的出現兩邊都要用的共同內容(例如通用角色詞彙表),要事後抽取
- 結果:採用。Cooper 確認方向

## 決定

`docs/` 下依領域分為 `docs/platform/`、`docs/game/`,每個資料夾各自包含 `SOP.md`/`SOP.html`、`decisions/`、`templates/`。原有平台流程全數搬進 `docs/platform/`,內部文件互相引用的路徑已同步更新(`docs/decisions/...` → `docs/platform/decisions/...`,`docs/templates/...` → `docs/platform/templates/...`,`docs/SOP.*` → `docs/platform/SOP.*`)。

資料夾命名採英文(`platform`/`game`),與既有 `decisions/`、`templates/` 命名風格一致,避免路徑編碼問題。此為純技術選擇,不涉及商業判斷。

暫不建立 `docs/shared/`。若後續真的出現兩領域共用的內容,再依實際需要抽取,不預先假設。

本檔案所在的 `docs/decisions/`(根層級)專門存放跨領域/架構層級的決策,與 `docs/platform/decisions/`、`docs/game/decisions/`(各領域內部決策)區分開來。

## 影響

- `docs/platform/` 下的 SOP.md、SOP.html、decisions/0001-0004、templates/ 皆已搬遷並更新內部路徑引用
- `docs/game/decisions/`、`docs/game/templates/` 已建立空資料夾,待遊戲開發流程內容討論後填入
