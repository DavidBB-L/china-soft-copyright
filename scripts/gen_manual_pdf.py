#!/usr/bin/env python3
"""软件说明书MD→PDF — 使用Node.js Playwright生成PDF，保证每页≥30行"""
import os, sys, re, subprocess, tempfile, json

# ── 参数解析 ──
DIR = os.environ.get("COPYRIGHT_DIR", os.getcwd())
MD_FILE = sys.argv[1] if len(sys.argv) > 1 else os.environ.get(
    "MD_FILE", os.path.join(DIR, os.environ.get("MANUAL_MD", "软件说明书.md")))
OUTPUT_FILE = sys.argv[2] if len(sys.argv) > 2 else os.environ.get(
    "OUTPUT_FILE", os.path.join(DIR, os.environ.get("MANUAL_PDF", "文档鉴别材料.pdf")))

# ── 读取MD并转HTML ──
with open(MD_FILE, 'r', encoding='utf-8') as f:
    md = f.read()

html_lines = []
for line in md.split('\n'):
    line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    if line.startswith('# '): html_lines.append(f'<h1>{line[2:]}</h1>')
    elif line.startswith('## '): html_lines.append(f'<h2>{line[3:]}</h2>')
    elif line.startswith('### '): html_lines.append(f'<h3>{line[4:]}</h3>')
    elif line.startswith('- **'):
        line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
        html_lines.append(f'<li>{line[2:]}</li>')
    elif line.startswith('- '): html_lines.append(f'<li>{line[2:]}</li>')
    elif line.startswith('> '): html_lines.append(f'<blockquote>{line[2:]}</blockquote>')
    elif line.strip() == '---': html_lines.append('<hr>')
    elif line.strip(): html_lines.append(f'<p>{line}</p>')
    else: html_lines.append('<br>')

# ── 构建HTML（CSS不含@page，边距由Playwright API控制） ──
html = '''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">
<style>
body { font-family: "Noto Sans CJK SC", sans-serif; font-size: 9.8px; line-height: 1.55; color: #000; }
h1 { font-family: "Noto Sans CJK SC", sans-serif; font-size: 13px; text-align: center; margin: 8px 0; }
h2 { font-family: "Noto Sans CJK SC", sans-serif; font-size: 10.5px; margin: 6px 0 4px; border-bottom: 1px solid #333; padding-bottom: 2px; }
h3 { font-family: "Noto Sans CJK SC", sans-serif; font-size: 9.8px; margin: 5px 0 3px; }
p { margin: 2px 0; text-indent: 2em; }
li { margin: 2px 0 2px 1em; }
hr { border: none; border-top: 1px dashed #ccc; margin: 6px 0; }
blockquote { background: #f5f5f5; border-left: 3px solid #999; margin: 5px 0; padding: 5px 8px; font-size: 8.5px; }
strong { font-family: "Noto Sans CJK SC", sans-serif; }
</style></head><body>''' + ''.join(html_lines) + '</body></html>'

# ── 写临时HTML ──
tmp_html = os.path.join(DIR, '_tmp_man.html')
with open(tmp_html, 'w', encoding='utf-8') as f:
    f.write(html)

# ── 生成临时Node.js Playwright脚本 ──
js_code = f'''
const {{ chromium }} = require('playwright');
(async () => {{
  const browser = await chromium.launch({{ headless: true }});
  const page = await browser.newPage();
  await page.goto('file://{os.path.abspath(tmp_html)}', {{ waitUntil: 'networkidle' }});
  await page.pdf({{
    path: '{os.path.abspath(OUTPUT_FILE)}',
    format: 'A4',
    margin: {{
      top: '1.3cm',
      bottom: '1.3cm',
      left: '1.8cm',
      right: '1.8cm'
    }},
    printBackground: true
  }});
  await browser.close();
  console.log('PDF generated successfully');
}})();
'''

tmp_js = os.path.join(DIR, '_tmp_playwright_gen.js')
with open(tmp_js, 'w', encoding='utf-8') as f:
    f.write(js_code)

try:
    result = subprocess.run(['node', tmp_js], capture_output=True, text=True, timeout=120)
    if result.returncode != 0:
        print(f"Playwright错误: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    print(result.stdout.strip())
finally:
    os.remove(tmp_js)
    os.remove(tmp_html)

# ── 验证：每页行数 ──
r = subprocess.run(['pdfinfo', OUTPUT_FILE], capture_output=True, text=True)
total = 0
for line in r.stdout.split('\n'):
    if 'Pages' in line:
        total = int(line.split(':')[1].strip())
        print(f'总页数: {total}')

all_ok = True
for p in range(1, total + 1):
    r2 = subprocess.run(['pdftotext', OUTPUT_FILE, '-', '-f', str(p), '-l', str(p)],
                        capture_output=True, text=True)
    lines = [l for l in r2.stdout.split('\n') if l.strip()]
    ok = len(lines) >= 30
    if not ok: all_ok = False
    print(f'  第{p}页: {len(lines)}行 {"OK" if ok else "NG — 需补充内容或调小字号"}')

print('全部合规' if all_ok else '末页不足30行，需在MD末尾补充内容')
