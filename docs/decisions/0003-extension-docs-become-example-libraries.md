# 決策紀錄 0003(架構層級):領域擴充文件改為範例庫,platform/game SOP.md 封存

- 日期:2026-08-18
- 決策者:Cooper
- 狀態:已採用

## 背景

`docs/core/SOP.md` 定稿後,開始建立平台/遊戲的領域擴充內容。過程中決定用「範例文件庫」取代原本設想的7份擴充文件(見討論紀錄,最終收斂成5份):`docs/core/examples/qa-example.md`、`docs/platform/examples/plane-example.md`、`docs/game/examples/plane-example.md`,以及尚待建立的兩份規格書範例。

這些範例文件建立後,發現舊版 `docs/platform/SOP.md`、`docs/game/SOP.md`(決策0002當時設想的「領域擴充文件」)內容跟核心規範、跟新的範例文件大量重複(角色表、Plane結構圖、狀態對應表都重複兩三處)。

## 考慮過的選項

### 選項 A:精簡 platform/game SOP.md,留下差異對照+常見風險,改寫成「領域擴充總覽」
- 優點:保留 SOP.md 裡有價值但不適合放進範例文件的內容(例如「動效與前端雙軌若漏同步建議每週對一次」這類常見風險判斷,不是填卡範例,是操作智慧)
- 缺點:多維護一層文件,且核心規範+範例文件已經涵蓋大部分內容,這份「總覽」的獨立存在價值降低
- 結果:放棄

### 選項 B:platform/game SOP.md 直接封存(舊文件備份),不再維護;核心規範改成一句話+連結指向範例文件
- 優點:結構最單純——核心規範講規則,範例文件講「長什麼樣子」,不再有第三層「總覽」文件需要維護同步
- 缺點:SOP.md 裡的「常見風險」等操作智慧不會有新的專屬位置存放,只留在被封存的舊文件與 `decisions/` 歷史紀錄裡,之後找起來比較不直覺
- 結果:採用。Cooper 確認「這兩份可以改成舊文件備份就好,後續不會再用到」

## 決定

1. `docs/platform/SOP.md`、`docs/platform/SOP.md.bak`、`docs/platform/SOP.html` 移至 `docs/platform/_archive/`;`docs/game/` 同樣處理。封存檔案開頭加註停用說明,不刪除、可查閱。
2. `docs/core/SOP.md` 裡凡是跟範例文件重複的內容,改成一句話+連結:
   - 第1節文件對照表:`docs/platform/SOP.md`/`docs/game/SOP.md` 列項改為 `docs/platform/examples/`/`docs/game/examples/`
   - 第2節角色專業擴充說明:指向對應領域的 `examples/` 目錄
   - 第7節 Plane 建議層級:平台/遊戲實際拓撲的說明改為連結兩份 `plane-example.md`
   - 第9節 QA 規則:補一句連結 `docs/core/examples/qa-example.md`
3. 新增核心規範第15節「擴充文件」,列出所有範例文件連結,並同步反映在 `docs/core/SOP.html`。
4. `docs/platform/templates/`、`docs/game/templates/` 不受本次決策影響,維持決策0002當時「舊檔保留、核心模板為主」的狀態。

## 影響

- `docs/platform/`、`docs/game/` 資料夾下不再有作用中的 SOP.md,新讀者應直接看 `docs/core/SOP.md` + 對應 `examples/`
- 「常見風險」類操作智慧目前僅存在於封存文件與各領域 `decisions/` 紀錄裡,若後續發現常被查找,可考慮在範例文件裡補充「注意事項」小節
