#!/usr/bin/env python3
"""依「新人訓練 SOP｜PM.xlsx」範本格式，產出平台 PM／遊戲 PM 的三個月培訓表。

用法：python3 build_pm_training.py <範本.xlsx> <輸出.xlsx>
內容來源：docs/SOP-分享版.html（已定案開發流程、Plane 規則、QA 規範、平台／遊戲規格書撰寫規範）。
文案原則：用日常用語、先講重點，不引用流程文件的步驟編號與縮寫，讓沒讀過流程文件的人也看得懂。
範本是工程師版（工作表「技術」），版面沿用，內容改寫為 PM 職責。
要調整培訓內容時，改下方 PLATFORM / GAME 兩個字典後重跑即可。
"""
import math
import sys
from copy import copy

import openpyxl
from openpyxl.styles import Font
from openpyxl.worksheet.datavalidation import DataValidation

TEMPLATE, OUT = sys.argv[1], sys.argv[2]

DARK = "FF243447"   # 範本中已填內容用的深色字（紅字是教學示例，正式內容不用）
NOTE = "FF5C6C78"
DEPT_LIST = '"平台-設計,平台-後端,平台-前端,產品,遊戲-後端,遊戲-前端,遊戲-美術,行銷"'
COLW = {"A": 20.13, "B": 47.63, "C": 43.88, "D": 38.88}

# ───────────────────────── 共用段落 ─────────────────────────
# 寫法原則：每格先講重點；用日常用語，不引用流程文件的步驟編號或專有縮寫，沒讀過流程文件也看得懂。
NOTE_TEXT = ("這份表說明新進 PM 三個月內要學什麼、做到什麼程度才算通過試用期。"
             "米黃底欄位由新人、主管或 HR 填寫；週次從到職日起算，每月回顧依到職日安排。"
             "標【建議】的數字是參考值，請主管與 HR 確認後定案。")

REVIEW_ROWS = [
    ("第 1 個月", "直屬主管＋HR", "適不適應、流程與工具熟不熟、規格書初稿寫得如何、需要什麼協助。"),
    ("第 2 個月", "直屬主管＋HR", "能不能獨立帶一個需求往前走、有沒有把關、跨部門溝通是否順暢。"),
    ("第 3 個月", "直屬主管＋HR＋BC", "對照下方「通過標準」逐項檢視，決定是否通過試用期。"),
]
PRINCIPLE = ("主管每週看一次進度；HR 安排每月回顧與最後考核；新人每週更新進度，需要協助就主動提。",
             "每個階段記錄「已達成／部分達成／未達成」，並附實際成果。",
             "沒達成就寫下原因、怎麼協助、哪天再檢視；若因排程或權限做不到，改用練習需求替代。")

PASS_HEAD = ("通過標準", "要做到什麼", "怎麼確認", "沒做到怎麼辦")
FAIL_HANDLING = "寫下原因與協助方式，約定再檢視日期"

# ───────────────────────── 平台 PM ─────────────────────────
PLATFORM = dict(
    sheet="平台PM", title="平台 PM 新人訓練 SOP",
    stages=[
        ("入職第 1 週\n認識流程",
         "・認識平台後台有哪些功能（會員、金流、客服與風控…）\n・了解一個需求從提出到上線，要經過哪些關卡、誰負責什麼\n・開通 Plane（工作單系統）與 Figma（設計稿）帳號\n・旁聽 1 場需求會議",
         "能用自己的話說明「一個需求怎麼走到上線」，並指出 PM 負責哪幾個環節。",
         "口頭說明一次流程；交一份功能地圖筆記。"),
        ("入職第 2 週\n學會接需求",
         "・學 Plane 工作單怎麼開、欄位怎麼填\n・練習接需求：記下提出人的原話與證據、判斷急不急（P0 最急～P3 最不急）、釐清到底要解決什麼問題\n・看客服回報如何轉成需求",
         "能把一筆需求或客服回報，整理成別人一看就懂的工作單。",
         "3 張練習工作單、1 份問題分析；帶訓人員逐張檢查。"),
        ("第 1 個月\n學會寫規格書",
         "・學平台規格書的標準寫法（固定 17 章，每章寫什麼）\n・學需求中途要改時怎麼處理\n・在指導下寫 1 份小型後台頁面（列表或報表）的規格書，請需求方確認",
         "規格書讓設計、開發、QA 都能照著做；沒決定的事有負責人和期限。",
         "規格書初版＋需求方確認紀錄；主管驗收。"),
        ("第 2 個月\n帶需求往前走",
         "・負責 1 個小型真實需求，從規格一路追到開發完成\n・參加技術討論，確認範圍、時程、誰負責什麼\n・開發中規格有疑問或要改，同步更新文件與 Plane\n・交給 QA 測試前，先確認功能符合規格\n・學看測試案例與 Bug 單",
         "需求能順利交到 QA 手上；所有變更都有紀錄，不只留在群組訊息。",
         "工作單紀錄、確認紀錄、1 張練習 Bug 單；主管檢視。"),
        ("第 3 個月\n獨立完成並考核",
         "・帶需求完成驗收、上線，並追蹤上線後狀況\n・練習緊急 Bug 與臨時插單時怎麼取捨，並留下紀錄\n・整理回顧，提出 1 項改善建議\n・成果展示與試用考核",
         "獨立帶完 1 個小型需求（從接需求到上線後回顧），並達到下方「通過標準」。",
         "完整資料（工作單、規格書、測試與驗收紀錄）、回顧、自評；主管＋HR＋BC 考核。"),
    ],
    supplement=("預設內容\n（主管可調整）",
                "Plane、Figma、平台規格書標準寫法、測試與 Bug 單格式、客服回報格式。",
                "練習接需求、寫 1 份小型規格書、帶 1 個真實小需求到上線、做回顧。",
                "規格書完整、工作單填寫正確、變更有紀錄、交付前有確認。"),
    pass_rows=[
        ("懂流程", "能說明需求怎麼走到上線，以及自己負責哪些環節。", "口頭問答或情境題，由主管確認。"),
        ("會接需求", "記下提出人的原話與證據；自己的判斷另外寫；優先順序說得出理由。", "練習工作單與問題分析，抽查合格。"),
        ("會寫規格書", "獨立完成 1 份規格書並經需求方確認；沒決定的事項有負責人和期限。【建議：至少 1 份】", "規格書、需求方確認紀錄。"),
        ("會管工作單", "標題、負責人、日期、驗收條件等欄位填齊；狀態和實際進度一致。", "主管抽查 5 張以上。【建議】"),
        ("會把關品質", "需求有變更就更新規格並留紀錄；交給 QA 前先確認功能符合規格；上線前備好回復方案。", "1 個真實需求的變更與驗收紀錄。"),
        ("會溝通", "要延遲或卡住就主動說；規格不清楚就回頭問，不自己猜；不替技術人員決定做法。", "週進度紀錄、同事回饋。"),
        ("成果展示", "說明做過的需求、取捨過程與學到的事，並提出 1 項改善建議。", "成果簡報、自評；主管＋HR＋BC 確認通過。"),
    ],
    weeks=[
        ("開通帳號；了解需求從提出到上線的流程與各角色分工；認識平台功能；旁聽 1 場需求會議。", "學 Plane，練習接需求。"),
        ("學 Plane 工作單；練習 3 張需求工作單；了解客服回報怎麼轉成需求。", "學平台規格書的寫法。"),
        ("學規格書 17 章各寫什麼；拆解 1 份現有規格書；了解 Figma 畫面狀態標記。", "開始寫小型規格書。"),
        ("寫小型後台頁規格書初版，自己對照檢查表；請需求方確認並記錄結論。", "參加技術討論；安排第 1 月回顧。"),
        ("參加技術討論，確認範圍、時程與分工；替練習需求開好工作單與規格、開發任務。", "追蹤開發，處理規格疑問。"),
        ("追蹤開發進度；回答規格疑問；練習需求變更處理（更新規格與 Plane）；填寫風險表。", "學測試與 Bug 單。"),
        ("學測試案例怎麼對應規格、開發自檢清單、Bug 單格式；檢查案例有沒有涵蓋驗收條件。", "確認功能後送測。"),
        ("確認功能符合規格後交給 QA；追蹤 Bug 修復與重測。", "進行驗收；安排第 2 月回顧。"),
        ("與需求方一起驗收；學習怎麼判斷「可以上線／要退回」；備好回復方案。", "完成上線與追蹤。"),
        ("安排上線；和維運、客服確認監控與通知；上線後觀察使用狀況與回饋。", "練習 Bug 與插單處理。"),
        ("練習緊急 Bug 分級與臨時插單取捨並留紀錄；整理客服回饋；完成回顧。", "整理成果與自評。"),
        ("整理完整資料；寫自評與 1 項改善建議；準備成果展示。", "成果展示與考核。"),
        ("成果展示：說明需求、取捨與學到的事；主管、HR、BC 確認考核結果並記錄。", "依回饋安排後續工作與成長目標。"),
    ],
)

# ───────────────────────── 遊戲 PM ─────────────────────────
GAME = dict(
    sheet="遊戲PM", title="遊戲 PM 新人訓練 SOP",
    stages=[
        ("入職第 1 週\n認識流程",
         "・認識一款遊戲怎麼做出來：企劃數值、美術、音效、前端、後端、QA 各做什麼、誰要等誰\n・了解需求從提出到上線，要經過哪些關卡\n・開通 Plane（工作單系統）帳號\n・試玩 2~3 款現有遊戲",
         "能說明「一款遊戲從規格到上線的順序」，並指出 PM 負責哪幾個環節。",
         "口頭說明一次流程；自己畫一張「誰等誰」的順序圖。"),
        ("入職第 2 週\n學會接需求",
         "・學 Plane 工作單怎麼開：一款遊戲一個模組、部門用標籤區分\n・練習接需求：記下提出人的原話與證據、判斷急不急（P0 最急～P3 最不急）、釐清要解決什麼問題\n・認識常聽到的數值名詞：RTP（長期回報率）、波動、最高贏分、命中率",
         "能把一筆需求整理成別人一看就懂的工作單；能說明各數值名詞的意思（不自行決定數值）。",
         "3 張練習工作單、1 份問題分析、數值名詞筆記。"),
        ("第 1 個月\n學會寫規格書",
         "・學遊戲規格書的標準寫法（固定 15 章，每章寫什麼）\n・數值要註明「暫定」或「已確認」及出處；查不到就寫「未提供」，不自己猜\n・在指導下寫現有遊戲規格書的部分章節，請需求方確認",
         "規格書讓各部門都能照著做；每個數值都有狀態與出處；沒決定的事有負責人和期限。",
         "規格書片段＋需求方確認紀錄；主管驗收。"),
        ("第 2 個月\n帶需求往前走",
         "・負責 1 個小型真實需求（例如現有遊戲的畫面優化或素材調整）\n・把工作分給各部門並排好先後（機率→後端→前端）\n・學三種素材驗收：原畫（完成即可）、動效（動效完成＋前端套好才算）、音效（整批做完再交）\n・交給 QA 前先確認功能符合規格\n・涉及機率或賠付的結論，要附模擬或實測結果",
         "各部門工作單掛對；能說清楚三種素材驗收差在哪；需求能順利交到 QA 手上。",
         "工作單紀錄、先後順序圖、素材清單與 Plane 對照檢查；主管檢視。"),
        ("第 3 個月\n獨立完成並考核",
         "・帶需求完成驗收、上線，並追蹤上線後狀況\n・練習緊急 Bug 與臨時插單時怎麼取捨，記錄被往後推的工作\n・整理回顧，提出 1 項改善建議；了解年度規劃怎麼做\n・成果展示與試用考核",
         "獨立帶完 1 個小型需求（從接需求到上線後回顧），並達到下方「通過標準」。",
         "完整資料（工作單、規格書、測試與驗收紀錄）、回顧、自評；主管＋HR＋BC 考核。"),
    ],
    supplement=("預設內容\n（主管可調整）",
                "Plane、遊戲規格書標準寫法、素材清單（Excel）、測試與 Bug 單格式。",
                "練習接需求、寫部分規格書、帶 1 個真實小需求到上線、做回顧。",
                "規格書數值有狀態與出處、工作單掛對、素材驗收方式正確、交付前有確認。"),
    pass_rows=[
        ("懂流程", "能說明一款遊戲從規格到上線的順序，以及自己負責哪些環節。", "口頭問答或情境題，由主管確認。"),
        ("會接需求", "記下提出人的原話與證據；自己的判斷另外寫；優先順序說得出理由。", "練習工作單與問題分析，抽查合格。"),
        ("會寫規格書", "獨立完成規格書的指定章節並經需求方確認；每個數值都有狀態與出處，不自己補值。【建議：至少 1 個完整區塊】", "規格書、需求方確認紀錄。"),
        ("會管工作單與素材", "模組（哪一款）、標籤（哪個部門）掛對；原畫、動效、音效用正確的驗收方式；素材清單與 Plane 狀態一致。", "主管抽查 5 張以上。【建議】"),
        ("會把關品質", "交給 QA 前先確認功能符合規格；機率與賠付結論附驗證結果；需求有變更就更新規格並留紀錄。", "1 個真實需求的驗收與變更紀錄。"),
        ("會溝通", "要延遲或卡住（例如機率外包還沒交）就主動說；商業數值與取捨交給決策者定，不自己決定。", "週進度紀錄、同事回饋。"),
        ("成果展示", "說明做過的需求、取捨過程與學到的事，並提出 1 項改善建議。", "成果簡報、自評；主管＋HR＋BC 確認通過。"),
    ],
    weeks=[
        ("開通帳號；了解一款遊戲各部門分工與先後順序；了解需求流程；試玩 2~3 款現有遊戲。", "學 Plane，練習接需求。"),
        ("學 Plane（一款遊戲一個模組、部門用標籤）；練習 3 張工作單；認識數值名詞。", "學遊戲規格書的寫法。"),
        ("學規格書 15 章各寫什麼；學數值「暫定／已確認」與出處怎麼標；拆解 1 份現有規格書。", "開始寫規格書章節。"),
        ("寫現有遊戲規格書的部分章節；交付前刪掉填寫說明；請需求方確認並記錄結論。", "拆工作給各部門；安排第 1 月回顧。"),
        ("參加技術討論；依規格把工作分給各部門標籤；排好先後（機率→後端→前端）與時程。", "學素材驗收方式。"),
        ("學原畫、動效、音效三種驗收；練習素材清單（Excel）與 Plane 同步更新。", "學測試與機率驗證。"),
        ("學測試案例、開發自檢清單、Bug 單格式；了解機率驗證結果怎麼交接與留證。", "確認功能後送測。"),
        ("確認功能符合規格後交給 QA；追蹤 Bug 修復與重測。", "進行驗收；安排第 2 月回顧。"),
        ("進行驗收；學習怎麼判斷「可以上線／要退回」；備好回復方案。", "完成上線與追蹤。"),
        ("完成上線工作；和後端、客服確認監控與通知；上線後觀察使用狀況與回饋。", "練習 Bug 與插單處理。"),
        ("練習緊急 Bug 分級與臨時插單取捨（記錄被往後推的工作）；整理客服回饋；完成回顧。", "整理成果與自評。"),
        ("整理完整資料；寫自評與 1 項改善建議；了解年度規劃怎麼做；準備成果展示。", "成果展示與考核。"),
        ("成果展示：說明需求、取捨與學到的事；主管、HR、BC 確認考核結果並記錄。", "依回饋安排後續工作與成長目標。"),
    ],
)

# ───────────────────────── 版面工具 ─────────────────────────

def est_lines(text, width):
    """估計文字在欄寬 width 下的行數（全形字算 2 個單位）。"""
    usable = max(width - 2, 1)
    total = 0
    for para in str(text).split("\n"):
        units = sum(2 if ord(ch) > 0x2E80 else 1 for ch in para)
        total += max(1, math.ceil(units / usable))
    return total


def row_height(texts_by_col, minimum=28.5):
    lines = max(est_lines(t, COLW[c]) for c, t in texts_by_col.items() if t)
    return max(minimum, lines * 15.5 + 8)


wb = openpyxl.load_workbook(TEMPLATE)
tpl = wb["技術"]


def snap(row):
    return {c: copy(tpl[f"{c}{row}"]._style) for c in "ABCD"}


S = dict(  # 範本各列樣式快照
    sec_head=snap(13), sec_body=snap(16), stage_label=snap(7), stage_body=snap(7),
    manager=snap(14), review_label=snap(16), principle=snap(19), wk_head=snap(21), wk_body=snap(22),
    title=snap(1), info_label=snap(2), info_val=snap(2), note=snap(5), stage_head=snap(6),
)
CREAM_BODY = snap(14)   # 米黃底（填寫欄位）


def put(ws, row, col, value, style, color=None, bold=None):
    cell = ws[f"{col}{row}"]
    cell.value = value
    cell._style = copy(style)
    if color or bold is not None:
        f = copy(cell.font)
        cell.font = Font(name=f.name, sz=f.sz, b=f.b if bold is None else bold,
                         color=color or f.color)


def build(spec):
    ws = wb.copy_worksheet(tpl)
    ws.title = spec["sheet"]
    ws.sheet_view.showGridLines = False
    for col, w in COLW.items():
        ws.column_dimensions[col].width = w
    # 清掉範本第 20 列之後（教學示例的週次紀錄）
    for r in range(20, 60):
        for c in "ABCD":
            cell = ws[f"{c}{r}"]
            cell.value = None
            cell._style = copy(tpl["A12"]._style)
    for r in range(20, 60):
        ws.row_dimensions[r].height = 15.75

    ws["A1"] = spec["title"]
    ws["D2"] = "產品"
    put(ws, 5, "B", NOTE_TEXT, S["note"]["B"], color=NOTE)
    ws.row_dimensions[5].height = 43.5

    # 階段表（第 7~11 列）：正式內容改深色字
    for i, (label, a, b, c) in enumerate(spec["stages"]):
        r = 7 + i
        put(ws, r, "A", label, S["stage_label"]["A"])
        for col, txt in zip("BCD", (a, b, c)):
            put(ws, r, col, txt, S["stage_body"][col], color=DARK)
        ws.row_dimensions[r].height = row_height({"B": a, "C": b, "D": c})

    # 主管補充（第 13~14 列）
    for col, txt in zip("ABCD", ("主管補充", "主要技術／工具／產品", "訓練任務", "驗收標準")):
        put(ws, 13, col, txt, S["sec_head"][col])
    sup = spec["supplement"]
    for col, txt in zip("ABCD", sup):
        put(ws, 14, col, txt, S["manager"][col], color=DARK)
    ws.row_dimensions[14].height = row_height(dict(zip("ABCD", sup)))

    # 每月回顧（第 15~19 列）
    for col, txt in zip("ABCD", ("每月回顧", "參與人員", "檢視重點", "會後紀錄")):
        put(ws, 15, col, txt, S["sec_head"][col])
    for i, (m, who, focus) in enumerate(REVIEW_ROWS):
        r = 16 + i
        put(ws, r, "A", m, S["review_label"]["A"])
        put(ws, r, "B", who, S["review_label"]["B"], color=DARK)
        put(ws, r, "C", focus, S["review_label"]["C"], color=DARK)
        put(ws, r, "D", None, CREAM_BODY["D"], color=DARK)
        ws.row_dimensions[r].height = row_height({"C": focus}, 60)
    put(ws, 19, "A", "執行原則", S["principle"]["A"])
    for col, txt in zip("BCD", PRINCIPLE):
        put(ws, 19, col, txt, S["principle"][col])
    ws.row_dimensions[19].height = row_height(dict(zip("BCD", PRINCIPLE)))

    # 試用期通過標準（第 21 列起）
    r = 21
    for col, txt in zip("ABCD", PASS_HEAD):
        put(ws, r, col, txt, S["sec_head"][col])
    ws.row_dimensions[r].height = 28.5
    for item, cond, evid in spec["pass_rows"]:
        r += 1
        put(ws, r, "A", item, S["review_label"]["A"])
        put(ws, r, "B", cond, S["review_label"]["B"], color=DARK)
        put(ws, r, "C", evid, S["review_label"]["C"], color=DARK)
        put(ws, r, "D", FAIL_HANDLING, S["review_label"]["D"], color=DARK)
        ws.row_dimensions[r].height = row_height({"B": cond, "C": evid, "D": FAIL_HANDLING})

    # 週次紀錄
    r += 2
    for col, txt in zip("ABCD", ("週次", "本週任務／完成情形與成果", "問題／協助措施／負責人／期限", "下週目標／再次檢視日")):
        put(ws, r, col, txt, S["wk_head"][col], color="FF24465E")
    ws.row_dimensions[r].height = 28.5
    for i, (task, nxt) in enumerate(spec["weeks"]):
        r += 1
        put(ws, r, "A", f"第{i + 1}週", S["wk_body"]["A"], color=DARK, bold=True)
        put(ws, r, "B", task, S["wk_body"]["B"], color=DARK)
        put(ws, r, "C", None, S["wk_body"]["C"], color=DARK)
        put(ws, r, "D", nxt, S["wk_body"]["D"], color=DARK)
        ws.row_dimensions[r].height = row_height({"B": task, "D": nxt}, 44)

    dv = DataValidation(type="list", formula1=DEPT_LIST, allow_blank=True)
    ws.add_data_validation(dv)
    dv.add("D2")
    return ws


build(PLATFORM)
build(GAME)
del wb["技術"]
wb.save(OUT)
print("saved", OUT)
