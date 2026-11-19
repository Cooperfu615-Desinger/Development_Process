# Plane Pro 方案六項功能研究報告(Epics / Work Items / Cycles / Modules / Views / Pages)

- 日期:2026-08-26
- 性質:**純事實研究,不含建議**。所有結論均需附官方來源 URL;查不到官方確認的一律標記為「未確認 / 待查」,不代表事實。
- 研究對象:Plane 官方文件(docs.plane.so)、官方行銷頁(plane.so)、官方 blog(plane.so/blog)。第三方部落格/評論站(dev.to、xpay、g2、saasworthy 等)只在搜尋結果中出現過,**未作為結論依據**,凡引用官方頁面得到的內容才寫入本報告。
- 查證方式:每項來自官方頁面的擷取皆為 WebFetch 直接讀取當頁內容並要求逐字引用(quote),非憑記憶轉述。頁面若標示 `<Badge type="info" text="Pro" />` 之類的組件,已在下方以「Pro 徽章」註明其確切掛載的功能名稱。
- 適用範圍:僅涵蓋 **Pro 方案**與其相對於 **Free/Community 方案**的差異;Business、Enterprise Grid 僅在能幫助判斷「這功能是不是至少要 Pro 才有」時順帶提及,不做完整研究。

## 全域參考:Plane 定價頁摘要(六項功能的分層總覽)

來源:[plane.so/pricing](https://plane.so/pricing)、[plane.so/pro](https://plane.so/pro)

**Free 方案($0/席位/月,上限 12 人)** 明確包含:Projects、Work Items、Comments、Cycles and Modules、Pages(知識庫)、Estimates、List/Board/Calendar/Gantt/Spreadsheet 版面、基本 Views(排序/篩選/顯示)、500 AI credits/席位。

**Pro 方案($6/席位/月)** = Free 的一切,外加(plane.so/pro 頁 FAQ 原文):
> "Everything on Free, plus unlimited seats, custom work item types, epics and initiatives, time tracking, bulk ops, workspace Wiki, published pages and views, active cycles, advanced estimates, teamspaces, and 1,000 AI credits per seat per month."

**重要結構性結論**:六項功能中,**Cycles、Modules、Pages、Views 這四項「功能本身」在 Free 方案就存在**(基礎建立/使用免費);Pro 方案賣的不是「解鎖這四項功能」,而是解鎖這四項功能底下的**特定進階能力**(如下方各節的 Pro 徽章清單)。真正整個功能被鎖在 Pro 之後的,是 **Epics(以及其背後的 Work Item Types 機制)**。這點與團隊原本可能的假設(六項都是「要不要升級才能用」的整包功能)不同,細節見各節。

---

## 1. Epics(史詩)

### 1.1 定義與目的(Plane 官方說法)
- docs.plane.so/core-concepts/issues/epics 原文:"An epic is still the parent layer above individual work items."
- Epic 用於把相關的工作項目群組成更大的工作單位,提供階層式結構來管理複雜專案、拆解大目標。
- 來源:[docs.plane.so/core-concepts/issues/epics](https://docs.plane.so/core-concepts/issues/epics)

### 1.2 重大架構變更(2026-05-26 起,官方 blog)
Plane 官方 blog 明確說明 Epic 已從「獨立、寫死的實體」改為「Work Item Type 的一種」:
> "Epic stops being a fixed, special-cased entity and becomes a work item type you can enable or disable."

變更細節(來源:[plane.so/blog/epics-is-becoming-a-work-item-type-in-plane](https://plane.so/blog/epics-is-becoming-a-work-item-type-in-plane)):
- 側邊欄的獨立「Epics」分頁已移除,Epic 現在活在 Work Items 清單裡,用「類型」篩選。
- 建立表單、詳情頁、批次編輯器、篩選器與一般 Work Item 完全共用同一套。
- 舊資料完整保留:"every comment, every activity log entry, every update, every sub-work item relationship" 都沒有流失。
- **新能力**:Epic 現在可以被加入 Cycle 與 Module("Cycles and modules assignment (previously work-items-only)")——舊版 Epic 做不到這件事,新版可以。
- Epic 也可以被嵌入 Pages 成為「即時同步的參照(live, synced references)」。
- Initiative(不在本次研究範圍內)現在可以接受任何 Work Item Type,不再限定只能掛 Epic。

### 1.3 結構/階層(相對於 Projects、Work Items、Cycles、Modules)
- 啟用 Work Item Types 後,Plane 自動建立兩個預設類型:**Task(層級 0,預設)** 與 **Epic(層級 1,父層)**。
- 子項目(Task 等)透過「Parent」欄位連到 Epic,形成 Epic → Task 的父子關係。
- 來源:[docs.plane.so/work-items/project-work-item-types](https://docs.plane.so/work-items/project-work-item-types)、docs.plane.so/core-concepts/issues/epics
- Epic 本身可否直接掛進 Cycle / Module:依 1.2 的 blog 內容,**可以**(這是本次改版新增的能力),但 Epics 專頁本身沒有進一步描述「Epic 進 Cycle/Module 之後 UI 如何呈現」的細節——**此細節 Plane 文件未具體展開,標記為 not_stated**。

### 1.4 方案分層(Tier gating)—— 明確 Pro-only
- Epics 頁面標題原文帶有徽章:**"Epics `<Badge type="info" text="Pro" />`"**
- 來源:[docs.plane.so/core-concepts/issues/epics](https://docs.plane.so/core-concepts/issues/epics)
- 交叉驗證:Epic 是透過「Work Item Types」機制實現,而 Work Item Types 整個功能頁面標題也帶 Pro 徽章:**"Project Work Item Types `<Badge type="info" text="Pro" />`"**,且原文寫明「Free 方案沒有提到可用 Work Item Types」。
- 來源:[docs.plane.so/work-items/project-work-item-types](https://docs.plane.so/work-items/project-work-item-types)
- 再交叉驗證:plane.so/pro 頁 FAQ 把 "epics and initiatives" 列為 Pro 才有的項目之一(見上方全域摘要引文)。
- **結論:三個獨立官方來源一致,Epics 是 Pro 方案專屬功能,Free 方案完全沒有 Epic。** 這與同份 blog 貼文本身「沒有提到分層限制」形成表面落差——但 blog 的主題是「架構怎麼變」,不是「定價怎麼分」,兩者不衝突,只是關注點不同,已在此註明避免誤讀成矛盾。

### 1.5 最佳實踐(Plane 官方文件所述)
- 官方文件未針對 Epic 提供獨立的「最佳實踐」段落;可參考的操作性指引都寫在 Work Items 總覽頁(見第 2 節)裡,例如「Epic 複製到其他專案時,目的地專案必須也支援 Epic 類型」。

### 1.6 已知限制(Plane 官方文件所述)
- 複製(duplicate)Work Item 時,若原項目是 Epic,目的專案必須支援 Epic 類型,否則無法複製。
- 來源:[docs.plane.so/core-concepts/issues/overview](https://docs.plane.so/core-concepts/issues/overview)
- Epic 與 Cycle/Module 之間的 UI 呈現細節、Epic 是否有專屬的進度計算公式等,官方文件未展開說明——標記 not_stated。

---

## 2. Work Items 工作項目(原 Issues)

### 2.1 定義與目的
> "Work items represent the fundamental unit of work — a task, bug, feature, or any piece of work your team needs to track."
- 來源:[docs.plane.so/core-concepts/issues/overview](https://docs.plane.so/core-concepts/issues/overview)
- Plane 官方確認這是「Issues」的新名稱/新定位:所有工作的最小可指派、可追蹤單位。

### 2.2 結構/階層
- 建立時依專案取得序列 ID(如 PROJ-1)。
- **父子結構**:Work Item 支援建立 Sub-work item,可拆解成更小單位。
- **跨專案子項目**:A 專案的 Work Item 可以當作 B 專案某個 Work Item 的子項目。
- **類型**:標準 Task、Bug、Feature,以及 Epic(需專案啟用 Work Item Types,見第 1 節)。
- 與 Cycles(時間區段)、Modules(功能分組)、Customers/Customer requests、Milestones/releases、自訂屬性皆有連結欄位。
- 來源同上。

### 2.3 方案分層
- Free 方案:核心的建立與管理功能(不含以下三項)。
- Pro 徽章功能(逐字擷取自官方文件):
  1. **Duplicate work items**(複製工作項目,可複製到同專案或跨專案)
  2. **Link pages to work items**(把專案頁面/wiki 文件連結到工作項目)
  3. **Export work items**(匯出成 CSV/JSON)
- 來源:[docs.plane.so/core-concepts/issues/overview](https://docs.plane.so/core-concepts/issues/overview)

### 2.4 最佳實踐(官方文件所述)
- 使用「快速新增」的行內列快速輸入。
- 關閉未完成的工作項目時有草稿自動儲存。
- 設定起訖日期以在 Timeline 產生依賴關係的視覺連接線。
- 發布狀態更新(On Track / At Risk / Off Track)讓 Initiative 彙總看到。
- 用 `@username` 提及來訂閱通知。
- 用「Copy branch name」功能取得標準化分支命名。
- 來源同上。

### 2.5 已知限制
- 已封存(archived)的工作項目若被複製,複製出來的是「啟用中」狀態,不是封存狀態。
- 專案專屬屬性(labels、modules、cycles、estimates)無法跨專案複製轉移。
- Sub-work items 與 customer requests 不會隨複製動作一起複製。
- 刪除的工作項目**無法復原**。
- 自訂屬性值在跨專案複製時會轉成純文字敘述。
- 來源同上。

---

## 3. Cycles 週期

### 3.1 定義與目的
> "A Cycle is a set period of time where your team focuses on completing specific tasks or work items."
> "Each Cycle is flexible, allowing you to prioritize and tackle backlog items at your own pace."
- 定位近似 Agile Sprint,是時間箱型(time-boxed)的工作容器。
- 來源:[docs.plane.so/core-concepts/cycles](https://docs.plane.so/core-concepts/cycles)

### 3.2 結構/階層
- 新專案預設啟用 Cycles,可在 Project Settings > Features 關閉。
- Work Item 可在 Cycle 頁面直接掛,或作為工作項目本身的一個屬性欄位來設定。
- **一個 Work Item 一次只能屬於一個 Cycle**(官方文件明確寫出這條限制)。文件未明確說明「同時屬於一個 Cycle 又屬於一個 Module」是否允許——**此點標記待查(見第 4.2 節的交叉檢核)**。
- Cycle 三種狀態:Active(進行中,無平行 Cycle 設定時通常只能有一個)、Upcoming(未來)、Completed(已結束,不可編輯但可將未完成項目轉移到下一個 Cycle)。
- 來源同上。

### 3.3 方案分層(逐字擷取每個徽章掛載的功能)
| 功能 | 徽章 |
|---|---|
| Manually start and stop cycles(手動啟動/結束週期) | Pro |
| Cycle progress charts(進度圖表) | Pro |
| Active cycles across projects(跨專案查看進行中週期) | Pro |
| Export cycles(匯出週期資料) | Pro |
| Auto-schedule cycles(自動排程週期) | Business |
| Override scheduled cycles(覆寫已排程週期) | Enterprise Grid |
| Parallel cycles(平行週期) | Enterprise Grid |

- 來源:[docs.plane.so/core-concepts/cycles](https://docs.plane.so/core-concepts/cycles)
- **注意**:Cycle 功能本身(建立、加入工作項目、基本追蹤)是 Free 方案就有的(見全域摘要),上表是 Cycle 底下的進階子功能,不是「Cycle 整包」的分層。

### 3.4 最佳實踐(官方文件所述/暗示)
- 自動排程可省去手動設定;手動控制則能貼合團隊實際節奏。
- 進度圖表有助於提早發現排程偏移。
- 來源同上(此段官方文件語氣偏描述性,非條列式最佳實踐,已註明為「暗示」而非逐字最佳實踐清單)。

### 3.5 已知限制
- 預設情況下 Cycle 日期不可重疊。
- 未開啟平行週期時,同一專案只能有一個 Active Cycle。
- 手動結束的 Cycle **無法重新啟動**:"You can't restart a Cycle after it's been manually ended."
- 管理員時區設定與成員個人時區設定之間可能出現時間顯示落差。
- 來源同上。

---

## 4. Modules 模組

### 4.1 定義與目的
> Modules 是 "smaller, focused projects that help users group and organize work items within specific time frames."
- 用途舉例(官方文件原文列舉):追蹤新功能開發進度、管理里程碑(如行銷活動)、代表軟體架構中的離散單位(如微服務)。
- 來源:[docs.plane.so/core-concepts/modules](https://docs.plane.so/core-concepts/modules)

### 4.2 結構/階層
- Module 存在於專案內,可在專案設定中開關。
- **一個 Work Item 可以同時屬於多個 Module**:官方文件明確寫出「a work item can belong to both a Feature module and a Release module simultaneously」。
- **與 Cycle 的關係:官方 Modules 頁面完全沒有提到 Cycle**,沒有明講「一個 Work Item 能否同時屬於一個 Module 又屬於一個 Cycle」。結合第 3.2 節(Cycle 頁面也沒提 Module),**這是一個 Plane 文件沒有明確交代的開放問題**——沒有任何一頁明說「可以」或「不可以」同時掛 Module + Cycle,不應假設答案,需標記 not_stated / 待官方進一步確認或實測驗證。
- Module 狀態:Backlog(預設)、Planned、In Progress、Paused、Completed、Cancelled,共 6 種。
- 進度計算:「Module progress is calculated based on the number of completed work items within the Module.」
- 版面:List、Gallery、Timeline 三種。
- 來源同上。

### 4.3 方案分層
- 官方文件中**唯一**帶徽章的 Module 子功能是 **Export modules(匯出模組資料)= Pro**。
- 來源同上。
- Module 功能本體(建立、加入工作項目、進度追蹤、狀態管理)在 Free 方案即可使用(見全域摘要;文件本文亦未對建立/使用本身標註任何限制)。

### 4.4 最佳實踐(官方文件所述)
- 官方文件未提供獨立的最佳實踐條列段落;操作說明包含:按 `M` 鍵可在專案任何位置快速建立 Module,或從側邊欄 Modules 頁點 Add Module;名稱為必填,描述/狀態/負責人/起訖日期皆可事後補。

### 4.5 已知限制
- 刪除 Module 會移除其進度分析資料,並將所有關聯的工作項目解除連結("removes its progress analytics and de-links all associated work items")。
- 已完成的 Module 可封存以保留歷史資料同時精簡畫面。
- 來源同上。

---

## 5. Views 視圖

### 5.1 定義與目的
> "A View is a saved configuration of filters, layouts, display options, and sorting preferences applied to your work items."
- 文件把 View 比喻為「smart bookmarks」與「lenses」——不改變底層資料,只是換角度觀看同一批工作項目,不會重複建立或搬動資料。
- 用途舉例:讓站立會議聚焦特定切片的工作、為利害關係人建立固定觀察窗、分享會即時更新的篩選結果連結、統一團隊的追蹤方式。
- 來源:[docs.plane.so/core-concepts/views](https://docs.plane.so/core-concepts/views)

### 5.2 結構/階層
- **Project Views**:建立在特定專案內,所有專案成員可見,支援 List / Board / Calendar / Table / Gantt 全部版面。
- **Workspace Views**:建立在工作區層級,所有工作區成員可見,**僅支援 Spreadsheet 版面**;內建 4 個不可刪除的系統預設 View:All Issues、Assigned to Me、Created by Me、Subscribed。
- **Teamspace Views**:綁定特定 Teamspace,而非單一專案或整個工作區。
- 來源同上。

### 5.3 方案分層(逐字擷取每個徽章)
| 功能 | 徽章 | 說明摘要 |
|---|---|---|
| Private view(私人視圖) | Pro | 僅建立者可見,其他成員無法查看或開啟 |
| Lock view(鎖定視圖) | Pro | 建立者可鎖定,防止他人修改篩選、顯示設定、更名 |
| Publish View(發布視圖) | Pro | 專案視圖可產生公開分享連結,免登入 Plane 帳號即可存取 |
| Export View(匯出視圖) | Pro | 匯出成 CSV / XLSX / JSON |

- 來源同上。
- 對照全域摘要:定價頁把「Basic views(排序/篩選/顯示)」列為 Free,「Public + Private views」列為 Pro——與上表一致:**建立公開、可共用的基礎 View 本身是 Free 就有的,只有「私人視圖 / 鎖定 / 發布 / 匯出」這幾項進階能力要 Pro**。

### 5.4 最佳實踐(官方文件所述)
- 文件強調 View 代表「團隊已達成共識的標準做法」,最好用 Lock 功能保存下來,避免被誤改。
- 若未儲存就關閉 View,未儲存的篩選變更會被捨棄,View 會還原到上次儲存的狀態。
- 來源同上。

### 5.5 已知限制
- 匯出反映的是「目前作用中(session 內)的篩選條件」,代表未儲存的臨時修改也會一併被匯出。
- Workspace View 匯出涵蓋所有專案;Project View 匯出僅限單一專案範圍。
- 來源同上。

---

## 6. Pages 頁面

### 6.1 定義與目的
- Pages 是內建於專案中的文件系統,用來「capture and organize project-related information」,取代外部文件工具,可用於會議記錄、技術規格、產品需求文件。
- 來源:[docs.plane.so/core-concepts/pages/overview](https://docs.plane.so/core-concepts/pages/overview)

### 6.2 結構/階層
- 新專案預設啟用 Pages,可在專案設定中開關;Pages 存在於個別專案內,而非工作區層級。
- **與 Work Items 的連結**:
  - 用 `@` 語法提及工作項目,建立互動式連結(此為 **Business** 方案功能,見下方分層表)。
  - 把選取的頁面文字直接轉成工作項目,並保留雙向參照關聯(同樣是 **Business** 方案功能)。
  - 可將工作項目直接嵌入頁面成為內容區塊(此項未見獨立徽章,推測為 Free 可用,但**文件未逐字標註,標記待查**)。
- **Pages 與 Wiki 的關係**:「Move Page」動作可將頁面轉移到「Wiki、Teamspace 或另一個專案」,顯示 Pages 與 Wiki 是不同的組織層級(Wiki 屬工作區層級的知識庫,對照全域摘要中 Pro 方案項目「Workspace Wiki」)。Move Page 本身帶 **Pro** 徽章。
- 來源同上。

### 6.3 方案分層(逐字擷取每個徽章)
| 功能 | 徽章 |
|---|---|
| AI helper(AI 輔助:改寫、摘要、擴寫) | Pro |
| Copy link to block(複製指定區塊的連結) | Pro |
| Move Page(轉移頁面到 Wiki/Teamspace/其他專案) | Pro |
| Publish Page(發布頁面到網路,產生公開連結) | Pro |
| Mention work items(用 `@` 提及工作項目建立連結) | Business |
| Convert selected text to work items(選取文字轉成工作項目) | Business |

- Free 方案:基礎建立、格式化、Markdown 支援、即時多人協作編輯,官方文件未對這些標註任何徽章限制,對照全域摘要(定價頁列「Pages(知識庫)」為 Free 項目),視為 Free 可用。
- 來源同上。

### 6.4 技術能力補充(官方文件所述,非分層限制)
- 16 種以上內容區塊類型(清單、圖片、表格、嵌入等)。
- 完整 Markdown 支援與自動轉換、拖放排序區塊。
- 即時多人協作(彩色游標)、版本歷史(含差異比對與還原)。
- 鎖定/解鎖功能可防止未授權編輯。
- 自動產生目錄;資訊面板顯示字數、字元數、段落數、預估閱讀時間。
- 匯出格式:PDF、Word、Markdown。
- 來源同上。

### 6.5 已知限制
- 私人頁面僅建立者可存取。
- 頁面鎖定是全有全無(防止團隊編輯),**沒有選擇性的細緻權限控制**。
- **巢狀頁面階層(nested page hierarchy)**:Pages 總覽頁**沒有提到**巢狀頁面這件事。但定價頁(全域摘要)把「Nested Pages and Embeds」列為 **Business** 方案功能。**這是一個文件間的落差**:Pages 功能總覽頁完全沒提巢狀結構,只有定價頁單獨提到「Nested Pages and Embeds」屬於 Business——兩份官方頁面對不上,無法確認「巢狀頁面」具體行為與方案門檻的細節,標記為 not_stated / 開放問題,需要 Plane 官方進一步文件或實際登入 Business 帳號測試才能確認。
- 疑難排解文件另提到一個已知問題:透過外部反向代理(reverse proxy)部署時,若未正確設定 WebSocket 的 `Upgrade`、`Connection: upgrade` 標頭,即使頁面設為 Public,Members 也看不到頁面內容。
- 來源同上。

---

## 附錄:開放問題清單(Plane 官方文件未明確交代,不應假設答案)

1. **Module + Cycle 能否同時掛在同一個 Work Item 上?** Cycles 頁與 Modules 頁互相都沒提到對方,兩份文件都沒有正面回答「是」或「否」(見 3.2、4.2 節)。
2. **Epic 進 Cycle/Module 後在 UI 上如何呈現、進度計算方式是否比照一般 Work Item?** Blog 只說「現在支援」,沒有展開細節(見 1.3 節)。
3. **Pages 的巢狀頁面(nested pages)方案門檻與行為**:定價頁說是 Business 功能,但 Pages 功能總覽頁完全沒提這件事,兩份官方頁面內容對不上(見 6.5 節)。
4. **工作項目直接嵌入頁面成為內容區塊**這項能力是否需要付費方案:文件描述了這個功能存在,但沒有像其他 Pages 子功能一樣掛徽章,無法確認是 Free 還是有方案限制(見 6.2 節)。

## 來源清單(依出現順序)

- https://plane.so/pricing
- https://plane.so/pro
- https://docs.plane.so/core-concepts/issues/epics
- https://plane.so/blog/epics-is-becoming-a-work-item-type-in-plane
- https://docs.plane.so/work-items/project-work-item-types
- https://docs.plane.so/core-concepts/issues/overview
- https://docs.plane.so/core-concepts/cycles
- https://docs.plane.so/core-concepts/modules
- https://docs.plane.so/core-concepts/views
- https://docs.plane.so/core-concepts/pages/overview
