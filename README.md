# Development_Process

公司開發流程規範（SOP）文件庫，涵蓋**平台**（會員、金流、後台）與**遊戲**（老虎機、棋牌、迷你遊戲）兩類專案。文件以繁體中文撰寫。

> 本倉庫為**私人倉庫**。對外傳閱的精簡版是公開的單檔網頁，見下方「分享版」。

## 這裡有什麼

| 想看什麼 | 去哪裡 |
|---|---|
| 開發流程全貌（單檔、可直接開啟傳閱） | `docs/SOP-分享版.html` |
| 完整版流程規範（工作版本體） | `docs/core/SOP.md`（網頁版 `docs/core/SOP.html`） |
| 平台／遊戲規格書怎麼寫 | `docs/platform/examples/spec-standard.md`、`docs/game/examples/spec-standard.md` |
| Plane 怎麼開單、填單 | `docs/platform/examples/plane-example.md`、`docs/game/examples/plane-example.md` |
| QA 測試案例、BUG 卡、發布判定怎麼寫 | `docs/core/examples/qa-example.md` |
| 為什麼這樣決定（決策紀錄） | `docs/decisions/`、`docs/core/decisions/`、`docs/platform/decisions/`、`docs/game/decisions/` |
| 平台 PM／遊戲 PM 三個月新人訓練表 | `docs/training/新人訓練SOP-PM.xlsx` |

## 流程規範涵蓋的內容

核心規範（`docs/core/SOP.md`）是所有專案類型共用的部分：

1. **開發流程圖**：需求進件到結案的分流與角色職責。
2. **開發階段各角色職掌**：步驟 0～13，每步的責任人、產出與「可往下走的條件」，以及開始／完成條件（DoR／DoD）。
3. **管理規範**：角色參與矩陣、RACI、風險登錄、需求變更規則。
4. **擴充文件**：
   - 規則：QA 測試規範、客服回應規範、Plane 開立規則、Figma 狀態標記。
   - 範例：QA 工作單、平台 Plane 使用、遊戲 Plane 使用、平台規格書撰寫規範、遊戲規格書撰寫規範。
5. **適用範圍**：各份文件的負責範圍。

平台與遊戲不各自維護一份敘述性 SOP，而是共用核心規範，差異以 `examples/` 裡的範例與撰寫規範呈現（決策見 `docs/decisions/0002`、`0003`）。

## 目錄結構

```
.
├── README.md
├── CLAUDE.md                     專案層的 Claude Code 設定
└── docs/
    ├── SOP-分享版.html            單檔分享版（核心規範 + 全部範例合併）
    ├── SOP工作流程中心.html        早期舊版總覽頁（已被取代，僅留參考）
    ├── core/                     所有專案共用
    │   ├── SOP.md / SOP.html     完整版規範
    │   ├── assets/               流程圖 SVG
    │   ├── examples/             QA 範例
    │   ├── templates/            規格書模板
    │   └── decisions/
    ├── platform/                 平台專屬
    │   ├── examples/             Plane 範例、規格書撰寫規範、規格書填寫範例
    │   ├── templates/  decisions/  _archive/
    ├── game/                     遊戲專屬
    │   ├── examples/             Plane 範例、規格書撰寫規範
    │   ├── decisions/  _archive/
    ├── decisions/                跨領域的決策紀錄（0001～）
    ├── analysis/                 研究與比對報告
    ├── training/                 PM 新人訓練表與產生腳本
    ├── tools/                    維護用腳本
    └── agents/                   Claude Code 技能用的設定說明
```

## 維護方式

**分享版優先**：流程規範有調整時，先只改 `docs/SOP-分享版.html`，等定案（目前稱「第二次定案」）後，再同步回完整版與範例檔。同步時：

- 分享版內容就是定稿來源，完整版文字以它為準。
- 每次改分享版，也要複製到公開倉庫 [`sop-share`](https://github.com/Cooperfu615-Desinger/sop-share) 的 `index.html` 並推送，網頁在 <https://cooperfu615-desinger.github.io/sop-share/>。
- 把分享版的某個分頁拆成獨立檔案，可用 `docs/tools/share_section_to_files.py`（用法見檔頭說明）。
- 同步的做法、比對方式與放棄的方案，見 `docs/decisions/0004`、`0006`。

**決策紀錄**：任何決策與放棄的方案都寫進對應層級的 `decisions/`，格式為「背景、考慮過的選項、結果、待辦」。

**修改既有規格檔前先備份**：本機用 `.bak` 備份（已被 `.gitignore` 排除，不進 git）。

**訓練表**：內容寫在 `docs/training/build_pm_training.py`，改完用腳本重新產生 `.xlsx`（用法見檔頭）。

## 目前狀態（2026-11-19）

- 完整版已對齊分享版（`docs/decisions/0006`）。
- 平台規格書撰寫規範引用的 `GAME_LIST_PRD_SAMPLE.md` 尚未提供，相關欄位標為「待補」。
- 各份文件中標示「open，待公司定案」的項目（例如 RACI 的發布核准人、客服對外回覆時限）仍待公司決定。
- PM 新人訓練表的通過門檻為建議值，待主管與人資確認（`docs/decisions/0005`）。
- 分享版與完整版之間沒有自動同步機制，靠人工比對。

## 注意

- 本倉庫含公司內部資訊（例如 Plane 內部連結、內部範例規格），不要改成公開。
- `docs/platform/examples/spec-example.md` 保留了原始 Plane 內部連結與完整數值，僅供內部參考，未納入分享版。
