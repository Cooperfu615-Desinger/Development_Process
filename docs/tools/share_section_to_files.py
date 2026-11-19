#!/usr/bin/env python3
"""把「SOP-分享版.html」裡的某一個分頁（<section id="...">）拆成獨立的 .md 與 .html。

用途：第二次定案後，把只存在分享版的內容同步回完整版（docs/*/examples/）。
分享版是唯一定稿來源，這支腳本只做「格式轉換」，不改寫任何文字。

用法（從 docs/ 目錄執行）：
  python3 tools/share_section_to_files.py \
      --section ex-platform-spec \
      --out-md  platform/examples/spec-standard.md \
      --out-html platform/examples/spec-standard.html \
      --eyebrow "平台 · 範例文件" \
      --back "../../core/SOP.html"

支援的元素：h3(頁標題)、p、h4、table、ul/ol/li、pre、code、strong、div.callout/.warning/.check。
遇到不支援的標籤會在 stderr 警告，不會靜默吞掉。
換新來源時請先看輸出結果再採用（見 docs/decisions/0006）。
"""
import argparse
import html as htmllib
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

SHARE = Path(__file__).resolve().parent.parent / "SOP-分享版.html"

KNOWN = {"section", "h3", "h4", "p", "span", "table", "colgroup", "col", "thead", "tbody",
         "tr", "th", "td", "ul", "ol", "li", "pre", "code", "strong", "div", "br", "em", "a"}


def extract_section(src: str, sid: str) -> str:
    m = re.search(r'<section id="%s"[^>]*>' % re.escape(sid), src)
    if not m:
        sys.exit(f"找不到 section id={sid}")
    n = re.search(r'<section id="', src[m.end():])
    end = m.end() + (n.start() if n else len(src))
    seg = src[m.end():end]
    return seg[: seg.rfind("</section>")]


class ToMd(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []          # 區塊（段落/表格等）
        self.buf = ""          # 目前的行內文字
        self.title = ""
        self.in_title = False
        self.skip_span = 0
        self.table = None      # {'rows':[[cell,..]], 'row':None, 'head':bool}
        self.cell = None
        self.lists = []        # 堆疊: ['ul'|'ol', index]
        self.box = None        # 目前 div 類型
        self.pre = None
        self.heading = None
        self.is_lead = False
        self.unknown = set()

    # ---- helpers
    def flush(self, prefix=""):
        t = self.buf.strip()
        self.buf = ""
        if t:
            self.out.append(prefix + t)

    def add(self, s):
        if self.cell is not None:
            self.cell.append(s)
        elif self.pre is not None:
            self.pre.append(s)
        else:
            self.buf += s

    # ---- parser
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class", "") or ""
        if tag not in KNOWN:
            self.unknown.add(tag)
        if tag == "h3":
            self.in_title = True
        elif tag == "span" and "eyebrow" in cls:
            self.skip_span += 1
        elif tag == "h4":
            self.flush()
            self.heading = True
        elif tag == "p":
            self.flush()
            self.is_lead = "lead" in cls
        elif tag == "div":
            self.flush()
            if any(k in cls for k in ("callout", "warning", "check")):
                self.box = "check" if "check" in cls else "box"
        elif tag == "table":
            self.flush()
            self.table = {"rows": [], "row": None, "head": False}
        elif tag == "tr" and self.table is not None:
            self.table["row"] = []
        elif tag in ("th", "td") and self.table is not None:
            self.cell = []
            if tag == "th":
                self.table["head"] = True
        elif tag in ("ul", "ol"):
            self.flush()
            self.lists.append([tag, 0])
        elif tag == "li":
            self.flush()
            self.lists[-1][1] += 1
        elif tag == "pre":
            self.flush()
            self.pre = []
        elif tag == "strong":
            self.add("**")
        elif tag == "code" and self.pre is None:
            self.add("`")
        elif tag == "br":
            self.add("<br>" if self.cell is not None else "\n")

    def handle_endtag(self, tag):
        if tag == "h3":
            self.in_title = False
        elif tag == "span" and self.skip_span:
            self.skip_span -= 1
        elif tag == "h4":
            self.flush("## ")
            self.heading = None
        elif tag == "p":
            if self.is_lead:
                self.flush("> ")
            elif self.box:
                self.flush("> ")
            else:
                self.flush()
            self.is_lead = False
        elif tag == "div":
            if self.box == "check":
                self.flush("- ☐ ")
            elif self.box:
                self.flush("> ")
            self.box = None
        elif tag in ("th", "td") and self.cell is not None:
            txt = "".join(self.cell).strip().replace("|", "\\|").replace("\n", "<br>")
            self.table["row"].append(txt)
            self.cell = None
        elif tag == "tr" and self.table is not None and self.table["row"] is not None:
            self.table["rows"].append(self.table["row"])
            self.table["row"] = None
        elif tag == "table" and self.table is not None:
            rows = self.table["rows"]
            if rows:
                w = len(rows[0])
                lines = ["| " + " | ".join(rows[0]) + " |", "|" + "---|" * w]
                lines += ["| " + " | ".join(r) + " |" for r in rows[1:]]
                self.out.append("\n".join(lines))
            self.table = None
        elif tag == "li":
            kind, idx = self.lists[-1]
            mark = f"{idx}. " if kind == "ol" else "- "
            self.flush("  " * (len(self.lists) - 1) + mark)
        elif tag in ("ul", "ol"):
            self.lists.pop()
            if not self.lists:
                self.out.append("")  # 空行分隔
        elif tag == "pre" and self.pre is not None:
            self.out.append("```\n" + "".join(self.pre).strip("\n") + "\n```")
            self.pre = None
        elif tag == "strong":
            self.add("**")
        elif tag == "code" and self.pre is None:
            self.add("`")

    def handle_data(self, data):
        if self.skip_span:
            return
        if self.in_title:
            self.title += data
            return
        if self.pre is not None:
            self.pre.append(data)
            return
        data = re.sub(r"\s+", " ", data) if self.cell is not None or self.buf or True else data
        self.add(data)


def to_md(seg: str, title_hint: str = ""):
    p = ToMd()
    p.feed(seg)
    p.flush()
    if p.unknown:
        print("警告：未支援的標籤", sorted(p.unknown), file=sys.stderr)
    blocks = [b for b in p.out]
    md = "\n\n".join(b for b in blocks if b != "")
    md = re.sub(r"\n{3,}", "\n\n", md)
    # 連續的列表項目不要被空行拆開
    prev = None
    while prev != md:  # 重複套用，避免相鄰項目因重疊比對而漏掉
        prev = md
        md = re.sub(r"(\n *- [^\n]+)\n\n(?= *- )", r"\1\n", md)
        md = re.sub(r"(\n *\d+\. [^\n]+)\n\n(?= *\d+\. )", r"\1\n", md)
        md = re.sub(r"(\n> [^\n]+)\n\n(?=> )", r"\1\n>\n", md)
    return p.title.strip() or title_hint, md.strip() + "\n"


HTML_HEAD = """<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <style>
    :root {{ --ink:#172033; --muted:#64748b; --line:#dbe3ef; --blue:#2563eb; --blue-soft:#eff6ff; --surface:#fff; --page:#f6f8fc; }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font-family:Inter, "PingFang TC", "Microsoft JhengHei", Arial, sans-serif; color:var(--ink); background:var(--page); line-height:1.65; }}
    main {{ max-width:900px; margin:0 auto; padding:42px 24px 90px; }}
    .back {{ display:inline-block; color:var(--blue); text-decoration:none; font-size:14px; font-weight:700; margin-bottom:18px; }}
    .back:hover {{ text-decoration:underline; }}
    .eyebrow {{ color:var(--blue); font-size:13px; font-weight:800; letter-spacing:.08em; text-transform:uppercase; }}
    h1 {{ font-size:30px; margin:4px 0 8px; line-height:1.25; }}
    h2 {{ font-size:19px; margin:38px 0 12px; padding-bottom:6px; border-bottom:2px solid var(--line); }}
    p {{ margin:8px 0 14px; }}
    .lead {{ color:var(--muted); max-width:780px; }}
    table {{ width:100%; max-width:100%; border-collapse:collapse; background:var(--surface); border:1px solid var(--line); border-radius:10px; overflow:hidden; margin:14px 0 22px; font-size:14px; }}
    th,td {{ border-bottom:1px solid var(--line); padding:11px 12px; vertical-align:top; text-align:left; overflow-wrap:anywhere; }}
    tr:last-child td {{ border-bottom:0; }}
    th {{ background:#f8fafc; font-weight:800; }}
    ul,ol {{ padding-left:22px; }}
    li {{ margin:5px 0; }}
    code {{ background:#eef2f7; padding:2px 5px; border-radius:4px; font-family:ui-monospace,SFMono-Regular,Consolas,monospace; font-size:.9em; }}
    pre {{ white-space:pre-wrap; background:#0f172a; color:#e2e8f0; border-radius:10px; padding:16px; overflow:auto; font-size:13px; }}
    pre code {{ background:transparent; padding:0; }}
    .callout {{ background:var(--blue-soft); border-left:4px solid var(--blue); border-radius:8px; padding:14px 16px; margin:18px 0 28px; }}
    .warning {{ border:1px solid #fed7aa; background:#fff7ed; border-radius:10px; padding:14px 16px; margin:18px 0; }}
    .warning strong {{ color:#9a3412; }}
    .check li {{ list-style:"☐  "; padding-left:3px; }}
    .footer {{ color:var(--muted); font-size:13px; padding-top:24px; margin-top:40px; border-top:1px solid var(--line); }}
    @media (max-width:820px) {{ main{{padding:24px 16px 56px;}} h1{{font-size:25px;}} }}
  </style>
</head>
<body>
  <main>
    <a class="back" href="{back}">← 回核心開發流程規範</a>
    <div class="eyebrow">{eyebrow}</div>
    <h1>{title}</h1>
{body}
    <div class="footer">本文件由 {md_path} 轉換產生。內容如有更新請以該檔案為準。</div>
  </main>
</body>
</html>
"""


def to_html(seg: str, title: str, back: str, eyebrow: str, md_path: str) -> str:
    body = re.sub(r"<h3>.*?</h3>", "", seg, count=1, flags=re.S)
    body = body.replace("<h4>", "<h2>").replace("</h4>", "</h2>")
    # 統一縮排，去掉分享版的 8 格縮排
    body = "\n".join(l[4:] if l.startswith("        ") else l for l in body.strip("\n").splitlines())
    body = "\n".join("    " + l if l.strip() else l for l in body.splitlines())
    return HTML_HEAD.format(title=title, back=back, eyebrow=eyebrow, body=body, md_path=md_path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--section", required=True)
    ap.add_argument("--out-md", required=True)
    ap.add_argument("--out-html", required=True)
    ap.add_argument("--eyebrow", required=True)
    ap.add_argument("--back", default="../../core/SOP.html")
    ap.add_argument("--md-label", help="html 頁尾顯示的 md 路徑，預設為 docs/<out-md>")
    ap.add_argument("--share", default=str(SHARE))
    a = ap.parse_args()

    src = Path(a.share).read_text(encoding="utf-8")
    seg = extract_section(src, a.section)
    title, md = to_md(seg)
    md = f"# {title}\n\n" + md
    for out in (a.out_md, a.out_html):
        if Path(out).exists():
            sys.exit(f"拒絕覆寫既有檔案：{out}（先備份或改檔名）")
    Path(a.out_md).write_text(md, encoding="utf-8")
    label = a.md_label or ("docs/" + a.out_md)
    Path(a.out_html).write_text(to_html(seg, title, a.back, a.eyebrow, label), encoding="utf-8")
    print("OK", a.out_md, a.out_html, "title=", title)


if __name__ == "__main__":
    main()
