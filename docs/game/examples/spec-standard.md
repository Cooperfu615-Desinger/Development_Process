# 遊戲規格書撰寫規範

> 人類撰寫版遊戲規格書模板：定義章節結構、每章該寫什麼，供企劃、PM、Math、前端、後端、美術與 QA 共同撰寫。標題格式為 `[PROJECT_CODE] 遊戲規格書：<遊戲名稱>`。

| 屬性 | 內容 |
|---|---|
| id | `SF-GAME-000` |
| title | 人類撰寫版遊戲規格書模板 |
| type | `game-spec` |
| reader | `game-spec` |
| lifecycle | `cross-functional-spec` |
| audience | Product、Frontend、Backend、Art、QA |
| status / version / owner / updated | 每次改版更新這四欄，狀態值：draft／...；owner 填實際維護者，updated 填實際日期 |

> **文件定位：**這是給企劃、PM、Math、前端、後端、美術與 QA 閱讀和共同填寫的版本。它與 `GAME_SPEC_TEMPLATE.md` 使用相同章節與欄位，但將填寫規則直接顯示出來。
>
> **交付前請注意：**完成規格書後，請刪除所有「填寫說明」區塊、placeholder 與未完成範例，再交給 Specs Library 或外部協作者。固定的 §1、§2、§3、§4、§9 標題，以及 §2 的粗體數值 labels 不要改名。
>
> **真相來源：**玩法敘事和設計理由寫在本文件；會被 SlotForge 套用的 shared fields 必須與 `exports/slotforge_<project_code>.profile.yaml` 同步。詳細權重與 RTP 拆解應放在 SF-MATH，不要在這裡猜測。

## 0. 版本歷史 (Changelog)

> 記錄本版本改了什麼、修改原因、重要假設與定案。每個影響玩法、數值、資料同步或交付範圍的變更，請附 Source ID 或 Decision ID。

| 版本 | 日期 | 作者 | 主要變更 |
|---|---|---|---|
| 0.1 | YYYY-MM-DD | `<姓名>` | 建立初版 |

**0.1 重要假設與定案**

> 只放會影響實作或交付的假設。請標示「暫定／已確認／待確認／不適用」，並能回查 `docs/SOURCE_REGISTER.md` 或 `docs/DECISION_LOG.md`。

- **版本基準**：
- **盤面**：
- **付費方式**：
- **RTP / Max Win / 波動**：暫定／已確認；來源：`SRC-###`／`DEC-###`。
- **持久化**：若有累積 meter，說明是否採座位制；無則註明不需要。
- **Project Code / Game ID**：暫定／已確認。

## 1. 遊戲基礎定義 (Identity)

> **本章目的：**建立所有團隊共同使用的遊戲身份與盤面基線。**應填內容：**遊戲名稱、Project Code、Game ID、原廠／參考遊戲、主題、盤面規格、連線或付費機制。
>
> **撰寫提醒：**參考遊戲只寫實際參考的玩法、節奏、UI 或題材；不要把原作未驗證的數值直接當成本款遊戲設定。Project Code 和 Game ID 確認後，要同步 frontmatter、profile.project 與輸出檔名。

| 屬性 | 規格內容 | 備註 |
|---|---|---|
| **遊戲名稱** |  |  |
| **原廠／參考遊戲** |  | 只寫實際參考範圍 |
| **Project Code** |  | 內部識別碼 |
| **Game ID** |  | 對應系統 game_type；未知時寫 TBD |
| **主題** |  |  |
| **輪帶規格** |  | 例：5 Reels x 4 Rows |
| **連線機制** |  | 例：Lines / Ways / Scatter Pays / Cluster |

## 2. 數值模型畫像 (Math Profile)

> **本章目的：**提供跨部門使用的數值摘要，不取代 SF-MATH 詳細模型。

- **RTP：**填寫理論／目標值；若 Base、Free Game、Buy Feature、Ante Bet 不同，分別列出並註明計算基準。
- **Volatility：**填寫 Low／Medium／High 等分類，並說明來源或判定方式。
- **Max Exposure：**區分理論 Max Win、硬性 cap 與模擬觀察最高值，不要混成一個數字。
- **Hit Rate：**先定義「命中」口徑（例如任一贏分或特定 Feature 觸發），再填數值、樣本或分析來源。
- **投注欄位：**標示幣別、coin／total bet 基準、bet 範圍與適用模式。
- **狀態與同步：**每個數值標示暫定／已確認；未經 Math sign-off 不得寫成正式結果。Machine Profile v1 對應 `math.rtp`、`math.volatility`、`math.max_win`、`math.hit_rate`、`math.win_tiers`。詳細權重、Feature trigger 分布、RTP 拆解和模擬條件放 SF-MATH。
- **目標 RTP (Return to Player)：**`暫定／已確認`
- **波動率 (Volatility)：**`暫定／已確認`
- **最大贏分 (Max Exposure)：**`暫定／已確認`
- **命中率 (Hit Rate)：**`暫定／已確認`
- **Bet 範圍 / 每轉 coin 數：**
- **Default Bet：**
- **來源與 sign-off：**見 `docs/SOURCE_REGISTER.md`、`docs/DECISION_LOG.md`。

## 3. 符號與賠付表 (Symbols & Paytable)

> **本章目的：**讓企劃、Math、前端、後端、美術與 QA 使用同一組 symbol ID、名稱、功能和 paytable。**應填內容：**特殊符號、一般符號、角色、賠付線／Ways／Scatter 判定、Jackpot（若有），以及賠率的明確基準。
>
> **撰寫提醒：**每個 symbol 使用穩定 ID；SlotForge ID 要與 profile 的 flat `slotforge.symbols` 一致。未確認的 paytable 數字保留狀態和來源，不要以相似遊戲補值。

**3.1 特殊符號 (Special Symbols)**

| ID | 名稱 | 出現範圍 | 功能 |
|---|---|---|---|
| WILD |  |  |  |
| SCATTER |  |  |  |
| SP1 |  |  |  |

**3.2 一般符號 (Regular Symbols)**

> 在表格前說明賠率是以 total bet、coin 或其他單位計算；若不同模式有不同 paytable，分開標示。

| 符號 | 階 | SlotForge ID | 5連 | 4連 | 3連 |
|---|---|---|---|---|---|
| H1 | High |  |  |  |  |
| L1 | Low |  |  |  |  |

**3.3 角色 (Character)**

> 只描述角色定位、互動與出現時機；若涉及正式 Spine binding，另依 Animation V1 流程處理。

- **主視覺角色：**
- **角色定位與互動：**

**3.4 賠付線 (Pay Line)**

> 說明連線／Ways／Scatter Pays／Cluster 的判定方向、起賠條件、同局多組得獎處理與賠率基準。

- **連線機制：**
- **判定規則：**

**3.5 Jackpot 階梯（若無可刪除）**

| Jackpot | 值（× bet） |
|---|---|
|  |  |

## 4. 遊戲核心邏輯 (Core Mechanics)

> **本章目的：**把玩法寫成前端、後端、Math 和 QA 可以共同驗證的規則。**每個玩法都要寫：**觸發條件、進入流程、盤面／狀態變化、結算、限制、再觸發、退出條件與邊界案例。**分開描述：**Base Game、特殊 Feature、Free Game／Bonus、Buy Feature、Ante Bet，避免把不同模式的權重、成本或結算基準混在一起。
>
> **不要寫成什麼：**本章不是新的 API contract、RNG 實作、完整遊戲 runtime、Animation scenario／sequence 或音效 cue 規格。正式 payload／reconnect／lock 移到 SF-CONTRACT；詳細權重與分布移到 SF-MATH。

**4.1 主遊戲 (Base Game)**

- **盤面 / 線數 / 連線判定：**
- **特殊符號與倍率：**
- **一局生命週期：**

**4.2 特殊玩法 / Feature**

- **觸發條件：**
- **流程：**
- **結算：**
- **邊界案例：**

**4.3 免費遊戲 / Bonus（若無可刪除）**

- **進場條件：**
- **局數與再觸發：**
- **離場與結算：**

**4.4 商業化機制 / Buy Feature（若無可刪除）**

- **可用狀態：**
- **費用與 bet 基準：**
- **選項與結果：**
- **拒絕／失效條件：**

## 5. 演出流程說明 (Performance Flow)

> **本章目的：**描述玩家看得到的演出先後、狀態承接與共用規範沿用關係。
>
> **撰寫提醒：**清楚指出 Spin、Stop、Feature 進場、Win presentation、Free Game 進出場的先後；不要在這裡創造新的動畫資料模型、時間 cue 或多 Spine 複合規則。

- **Spin / Stop：**沿用現行共用 SPIN 狀態機；本款差異：
- **特殊符號 / Feature 演出：**
- **Bonus / Free Game 進場：**
- **大獎 / Max Win：**
- **Win 分級：**沿用共用 win presentation；本款差異：

## 6. 介面佈局與 UI (Layout & UI)

> **本章目的：**說明沿用的共用 UI，以及本遊戲需要啟用、隱藏或覆寫的部分。**應填內容：**共用介面、enabled／disabled 元素、位置與尺寸覆寫、popup、遊戲專屬元件、素材來源與狀態。
>
> **撰寫提醒：**只有已確認的 SlotForge canonical slot key 才能放入 hidden／enabled 清單；不要把交易、錢包、平台大廳或尚未核准的 runtime 流程寫成本款 UI contract。

- **共用介面：**底部操作列、漢堡選單、Speed、Auto Spin、SPIN、共用 Popup 沿用 SlotForge 共用規範；本文件只描述差異與覆寫。
- **需要啟用的元素：**
- **需要隱藏的元素：**
- **差異／覆寫：**
- **本遊戲特有 UI：**

## 7. 美術清單 (Art Checklist)

> **本章目的：**提供美術交付與 SlotForge asset mapping 的可回查摘要。**每列應填：**Slot Key、用途、規格尺寸、Applicability（required／optional／not_applicable／needs_decision）、canonical filename 與 Source ID。
>
> **撰寫提醒：**正式母檔與大型資產不要放進這個文件型專案；Standard 110 只是版本化 catalog，不代表模板列出的每個 slot 都是 required。

| 類別 | Slot Key | 用途 | 尺寸 | Applicability | 檔名／來源 |
|---|---|---|---|---|---|
| 背景 | `background_main` |  |  | required / optional |  |
| 符號 High | `symbol_h1 ~` |  |  | required / optional |  |
| 符號 Low | `symbol_l1 ~` |  |  | required / optional |  |
| 符號特殊 | `symbol_wild / symbol_scatter / symbol_sp*` |  |  | required / optional |  |
| UI |  |  |  | required / optional |  |

**7.1 Gameinfo HTML 需呈現內容**

> 依序整理 Header → Paytable → Main Game → Free Game / Bonus → Special Features → Jackpot（若有）→ Rules & Compliance（RTP / 波動 / Max Win / 斷線重連）→ Controls。若內容尚未確認，標示來源和待確認事項。

## 8. 前後端資料需求 (Technical & Dev Notes)

> **本章目的：**提供實作團隊的需求摘要，不取代正式 API／event contract。**每列應填：**資料名稱、用途、權威來源、生命週期與狀態。
>
> **撰寫提醒：**前端猜測的 payload 或不存在的 API 不得寫成已確認資料；正式 request／response、error、reconnect、idempotency 和 round lock 另建 SF-CONTRACT。

| 資料 | 說明 | 權威來源 | 狀態 |
|---|---|---|---|
| Spin Result |  | Backend | 待確認 |
| Win Breakdown |  | Backend | 待確認 |
| Feature State |  | Backend | 待確認 |
| Balance |  | Backend | 待確認 |
| Reconnect Snapshot |  | Backend | 待確認 |

## 9. QA 測試清單 (QA Checklist)

> **本章目的：**把規格轉成可執行的驗收案例。
>
> **撰寫提醒：**每項要能回答「在什麼條件下，預期看到什麼結果，以及要和哪個來源／profile 欄位比對」；不要只寫「功能正常」。

- 盤面尺寸與付費方式正確。
- 所有符號、SlotForge ID 與 paytable 一致。
- 主遊戲特殊機制正確，無贏分與有特殊符號的邊界案例已定義。
- Free Game / Bonus / Buy Feature 觸發、局數、成本與結算正確。
- 最大贏分、RTP、波動與 Hit Rate 的狀態與標示正確。
- UI enabled／disabled、hidden slots 與特有元件和 profile 一致。
- 素材清單命名符合已核准的 canonical naming；缺漏有來源和狀態。
- Google Sheet 連結、gid、CSV export 與摘要可回查。
- Machine Profile 通過 v1 validator，YAML／JSON round-trip 不遺失有效資料。
- GDD 與 profile 的 shared fields 沒有差異。

## 10. 其他題材發想（可選）

> 本章是未來換皮或備選方向，只保留設計想法，不代表已核准需求，也不會自動進入 Machine Profile。

| 符號 | 題材 A | 題材 B |
|---|---|---|
| WILD |  |  |
| SCATTER / SP* |  |  |
| H1~ |  |  |
| L1~ |  |  |
| 視覺風格 |  |  |

## 11. 待確認問題 (Open Questions)

> **本章目的：**集中記錄所有尚未裁決、但會影響 Math、UI、Art、Backend、QA 或 SlotForge 套用的問題。
>
> **撰寫提醒：**每筆使用唯一 Q ID，寫清楚問題、影響範圍、優先度、狀態與對應 Decision ID。尚未裁決的數值或玩法不可只留在聊天紀錄，也不可在 profile 內假裝完成。

| ID | 問題 | 影響範圍 | 優先度 | 狀態 | 對應決策 |
|---|---|---|---|---|---|
| Q-001 |  | Math / UI / Art / Backend / QA | High / Medium / Low | Open | `DEC-###` |

## 12. 後端可自行補的項目（指引）

> 列出需要後端／外包後續產出的範圍；本章不是已完成的 contract 或 math 結果。

- **SF-CONTRACT：**event schema、reconnect 還原、idempotency / round lock。
- **SF-MATH：**符號權重、功能觸發率、RTP 拆解、Max Win 機率與驗證。
- **內容 / 美術：**Gameinfo HTML（依 §7.1）與示意圖清單。
- **SlotForge Machine Profile：**`exports/slotforge_<project_code>.profile.yaml`，只使用現行 v1 contract。

## 13. 音樂音效清單摘要（可選）

> 完整清單以外部 Sheet 或來源檔案為主，本節只保留摘要、用途、觸發情境與來源 ID。目前不會因為此表新增 audio cue contract。

| 類型 | Filename | 用途 | 觸發時機 | 來源 ID | 狀態 |
|---|---|---|---|---|---|
| BGM |  | Base Game BGM | 進入主遊戲 | `SRC-###` | 待確認 |
| BGM |  | Free Game BGM | 進入免費遊戲 | `SRC-###` | 待確認 |
| SFX |  | Spin / Stop | 點擊或停輪 | `SRC-###` | 待確認 |
| SFX |  | Win 報獎 | Small / Big / Mega | `SRC-###` | 待確認 |

## 14. 交付與同步備註

> **本章目的：**交付前確認 GDD、profile、來源、決策與驗證結果已同步。
>
> **交付前必查：**project、template、symbols、math、mechanics、UI／asset shared fields 一致；review checklist 完成；SlotForge 匯入失敗時能依欄位 path 修正且不覆蓋既有專案。

- 本文件最後一次與 profile 同步日期：`YYYY-MM-DD`。
- 對應 profile：`exports/slotforge_<project_code>.profile.yaml`。
- 最新決策：`docs/DECISION_LOG.md`。
- 仍未完成的審查項目：
- SlotForge 實際匯入結果：
