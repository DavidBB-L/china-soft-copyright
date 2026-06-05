#!/usr/bin/env python3
"""软著材料 PDF 生成器（统一版）
- 程序鉴别材料：Node.js Playwright，精确50行/页 A4
- 文档鉴别材料：Node.js Playwright，9.8px/1.55行高/1.3cm边距

用法:
  python3 convert_to_pdf.py source <txt_file> <output>
  python3 convert_to_pdf.py manual <md_file> <output>
  python3 convert_to_pdf.py all
"""
import json as _json
import os
import re
import subprocess
import sys
import tempfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def _detect_playwright_path():
    """Find the playwright Node.js module path."""
    candidates = [
        os.path.expanduser("~/node_modules/playwright"),
        os.path.expanduser("~/node_modules/playwright-core"),
        "/usr/local/lib/node_modules/playwright",
        "/usr/lib/node_modules/playwright",
    ]
    for p in candidates:
        if os.path.isdir(p):
            return p
    # Fallback: try require resolution via node -e
    try:
        r = subprocess.run(
            ["node", "-e", "console.log(require.resolve('playwright'))"],
            capture_output=True, text=True, timeout=10
        )
        if r.returncode == 0 and r.stdout.strip():
            return os.path.dirname(r.stdout.strip())
    except Exception:
        pass
    print("❌ 未找到 playwright Node.js 模块，请先 npm install playwright")
    sys.exit(1)


PLAYWRIGHT_PATH = _detect_playwright_path()


def _run_node_script(js_code, description="Node.js script"):
    """Write JS to a temp file, run it, clean up, return success."""
    fd, tmp_js = tempfile.mkstemp(suffix=".js", dir=SCRIPT_DIR)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(js_code)
        result = subprocess.run(
            ["node", tmp_js],
            capture_output=True, text=True, timeout=120
        )
        if result.returncode != 0:
            print(f"❌ {description} 失败:\n{result.stderr}")
            return False
        if result.stdout.strip():
            print(result.stdout.strip())
        return True
    finally:
        if os.path.exists(tmp_js):
            os.remove(tmp_js)


def gen_source_pdf(txt_file, output_file):
    """生成源代码 PDF，精确 50 行/页，通过 Node.js Playwright 渲染。

    Args:
        txt_file: gen_source_doc.py 生成的 .txt 文件路径
        output_file: 输出 PDF 文件路径
    Returns:
        True 成功 / False 失败
    """
    txt_file = os.path.abspath(txt_file)
    output_file = os.path.abspath(output_file)
    pw = _json.dumps(PLAYWRIGHT_PATH)
    txt_js = _json.dumps(txt_file)
    out_js = _json.dumps(output_file)

    js = f"""\
const {{ chromium }} = require({pw});
const fs = require('fs');
const path = require('path');

const txt = fs.readFileSync({txt_js}, 'utf-8');

const hi = txt.indexOf('【前30页源代码】');
const fs_ = txt.indexOf('\\n', hi) + 1;
const om = txt.indexOf('（第');
const bs = txt.indexOf('\\n', txt.indexOf('【后30页源代码】')) + 1;
const hdr = txt.substring(0, hi);
const fl = txt.substring(fs_, om).replace(/\\n--- 第 \\d+ 页结束.*?\\n/g, '\\n').split('\\n').filter(l => l.includes('|'));
const bl = txt.substring(bs).replace(/\\n--- 第 \\d+ 页结束.*?\\n/g, '\\n').split('\\n').filter(l => l.includes('|'));

const L = 50;
let html = '<!DOCTYPE html><html><head><meta charset="UTF-8"><style>';
html += 'body{{margin:0;padding:0}}';
html += 'pre{{font-family:"Courier New",monospace;font-size:8.5px;line-height:1.18;margin:0;padding:0;border:0;white-space:pre}}';
html += '.pb{{page-break-before:always}}';
html += '</style></head><body>';
const e = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
html += '<pre>' + e(hdr) + '</pre>';

function add(lines) {{
    let c = '', f = true;
    for (let i = 0; i < lines.length; i += L) {{
        const ch = lines.slice(i, Math.min(i + L, lines.length));
        if (!ch.length) break;
        c += '<pre' + (f ? '' : ' class="pb"') + '>' + e(ch.join('\\n')) + '</pre>\\n';
        f = false;
    }}
    return c;
}}
html += add(fl);
html += '<div class="pb" style="text-align:center;padding-top:45%;font-size:14px;">（中间省略）</div>';
html += add(bl);
html += '</body></html>';

const outPath = {out_js};
const tmp = path.join(path.dirname(outPath), '_tmp_source.html');
fs.writeFileSync(tmp, html);

(async () => {{
    const b = await chromium.launch({{ headless: true }});
    const p = await b.newPage();
    await p.goto('file://' + tmp, {{ waitUntil: 'networkidle' }});
    await p.pdf({{
        path: outPath,
        format: 'A4',
        margin: {{ top: '0.5cm', bottom: '0.5cm', left: '0.5cm', right: '0.5cm' }}
    }});
    await b.close();
    fs.unlinkSync(tmp);
    console.log('✅ ' + path.basename(outPath) + ' (' + Math.round(fs.statSync(outPath).size / 1024) + 'KB)');
}})();
"""
    return _run_node_script(js, "源代码 PDF 生成")


def gen_manual_pdf(md_file, output_file):
    """Markdown 说明书 → PDF，通过 Node.js Playwright 渲染。

    使用 Noto Sans CJK SC 字体，9.8px/1.55行高/1.3cm边距。
    无 @page CSS — 边距通过 Playwright API 设置。

    Args:
        md_file: Markdown 文件路径
        output_file: 输出 PDF 文件路径
    Returns:
        True 成功 / False 失败
    """
    md_file = os.path.abspath(md_file)
    output_file = os.path.abspath(output_file)

    with open(md_file, 'r', encoding='utf-8') as f:
        md = f.read()

    # Markdown → HTML (simple inline conversion)
    html_lines = []
    for line in md.split('\n'):
        line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        if line.startswith('# '):
            html_lines.append(f'<h1>{line[2:]}</h1>')
        elif line.startswith('## '):
            html_lines.append(f'<h2>{line[3:]}</h2>')
        elif line.startswith('### '):
            html_lines.append(f'<h3>{line[4:]}</h3>')
        elif line.startswith('- **'):
            line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
            html_lines.append(f'<li>{line[2:]}</li>')
        elif line.startswith('- '):
            html_lines.append(f'<li>{line[2:]}</li>')
        elif line.startswith('> '):
            html_lines.append(f'<blockquote>{line[2:]}</blockquote>')
        elif line.strip() == '---':
            html_lines.append('<hr>')
        elif line.strip():
            html_lines.append(f'<p>{line}</p>')
        else:
            html_lines.append('<br>')

    html_content = '\n'.join(html_lines)
    pw = _json.dumps(PLAYWRIGHT_PATH)
    html_js = _json.dumps(html_content)
    out_js = _json.dumps(output_file)

    # Use Noto Sans CJK SC for Linux compatibility
    # Font size: 9.8px, line-height: 1.55, margin: 1.3cm (set via Playwright API)
    # NO @page CSS — margins handled by Playwright pdf() API
    js = f"""\
const {{ chromium }} = require({pw});
const fs = require('fs');
const path = require('path');

const htmlBody = {html_js};

const html = `<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">
<style>
body {{
    font-family: "Noto Sans CJK SC", "Noto Sans SC", "Source Han Sans SC", "WenQuanYi Micro Hei", sans-serif;
    font-size: 9.8px;
    line-height: 1.55;
    color: #000;
}}
h1 {{
    font-family: "Noto Sans CJK SC", "Noto Sans SC", sans-serif;
    font-size: 13px;
    text-align: center;
    margin: 8px 0;
}}
h2 {{
    font-family: "Noto Sans CJK SC", "Noto Sans SC", sans-serif;
    font-size: 10.5px;
    margin: 6px 0 4px;
    border-bottom: 1px solid #333;
    padding-bottom: 2px;
}}
h3 {{
    font-family: "Noto Sans CJK SC", "Noto Sans SC", sans-serif;
    font-size: 9.8px;
    margin: 5px 0 3px;
}}
p {{ margin: 2px 0; text-indent: 2em; }}
li {{ margin: 2px 0 2px 1em; }}
hr {{ border: none; border-top: 1px dashed #ccc; margin: 6px 0; }}
blockquote {{
    background: #f5f5f5;
    border-left: 3px solid #999;
    margin: 5px 0;
    padding: 5px 8px;
    font-size: 8.5px;
}}
strong {{ font-family: "Noto Sans CJK SC", "Noto Sans SC", sans-serif; }}
</style></head><body>${{htmlBody}}</body></html>`;

const outPath = {out_js};
const tmp = path.join(path.dirname(outPath), '_tmp_manual.html');
fs.writeFileSync(tmp, html, 'utf-8');

(async () => {{
    const b = await chromium.launch({{ headless: true }});
    const p = await b.newPage();
    await p.goto('file://' + tmp, {{ waitUntil: 'networkidle' }});
    // Margins via Playwright API — 1.3cm
    await p.pdf({{
        path: outPath,
        format: 'A4',
        margin: {{
            top: '1.3cm',
            bottom: '1.3cm',
            left: '1.3cm',
            right: '1.3cm'
        }}
    }});
    await b.close();
    fs.unlinkSync(tmp);
    console.log('✅ ' + path.basename(outPath) + ' (' + Math.round(fs.statSync(outPath).size / 1024) + 'KB)');
}})();
"""
    return _run_node_script(js, "文档说明书 PDF 生成")


def validate_pdf(pdf_file):
    """验证 PDF 输出（页数、基本信息）。"""
    if not os.path.exists(pdf_file):
        print(f"  ❌ 文件不存在: {pdf_file}")
        return False
    size_kb = os.path.getsize(pdf_file) // 1024
    print(f"  📄 {os.path.basename(pdf_file)}: {size_kb}KB")
    # Try pdfinfo if available
    try:
        r = subprocess.run(["pdfinfo", pdf_file], capture_output=True, text=True, timeout=10)
        if r.returncode == 0:
            for line in r.stdout.split('\n'):
                if 'Pages' in line:
                    pages = line.split(':')[1].strip()
                    print(f"  📖 总页数: {pages}")
    except FileNotFoundError:
        pass  # pdfinfo not installed, skip validation
    except Exception:
        pass
    return True


def main():
    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 convert_to_pdf.py source <txt_file> <output>")
        print("  python3 convert_to_pdf.py manual <md_file> <output>")
        print("  python3 convert_to_pdf.py all")
        sys.exit(1)

    cmd = sys.argv[1]
    project_dir = os.path.dirname(SCRIPT_DIR)  # china-soft-copyright/

    if cmd == "source":
        if len(sys.argv) < 4:
            print("用法: python3 convert_to_pdf.py source <txt_file> <output>")
            sys.exit(1)
        txt_file = sys.argv[2]
        output_file = sys.argv[3]
        print(f"🔧 生成源代码 PDF: {txt_file} → {output_file}")
        ok = gen_source_pdf(txt_file, output_file)
        if ok:
            validate_pdf(output_file)
        sys.exit(0 if ok else 1)

    elif cmd == "manual":
        if len(sys.argv) < 4:
            print("用法: python3 convert_to_pdf.py manual <md_file> <output>")
            sys.exit(1)
        md_file = sys.argv[2]
        output_file = sys.argv[3]
        print(f"🔧 生成文档说明书 PDF: {md_file} → {output_file}")
        ok = gen_manual_pdf(md_file, output_file)
        if ok:
            validate_pdf(output_file)
        sys.exit(0 if ok else 1)

    elif cmd == "all":
        # Default paths — look for expected files in COPYRIGHT_DIR or project dir
        copyright_dir = os.environ.get("COPYRIGHT_DIR", project_dir)
        txt_file = os.environ.get("SOURCE_TXT", os.path.join(copyright_dir, "源代码文档.txt"))
        source_pdf = os.environ.get("SOURCE_PDF", os.path.join(copyright_dir, "程序鉴别材料.pdf"))
        md_file = os.environ.get("MANUAL_MD", os.path.join(copyright_dir, "软件说明书.md"))
        manual_pdf = os.environ.get("MANUAL_PDF", os.path.join(copyright_dir, "文档鉴别材料.pdf"))

        results = []

        # Source PDF
        if os.path.exists(txt_file):
            print(f"🔧 [1/2] 生成源代码 PDF...")
            ok = gen_source_pdf(txt_file, source_pdf)
            results.append(("程序鉴别材料", source_pdf, ok))
            if ok:
                validate_pdf(source_pdf)
        else:
            print(f"⚠️  跳过源代码 PDF — 未找到: {txt_file}")
            results.append(("程序鉴别材料", source_pdf, False))

        # Manual PDF
        if os.path.exists(md_file):
            print(f"🔧 [2/2] 生成文档说明书 PDF...")
            ok = gen_manual_pdf(md_file, manual_pdf)
            results.append(("文档鉴别材料", manual_pdf, ok))
            if ok:
                validate_pdf(manual_pdf)
        else:
            print(f"⚠️  跳过文档说明书 PDF — 未找到: {md_file}")
            results.append(("文档鉴别材料", manual_pdf, False))

        # Summary
        print("\n" + "=" * 50)
        print("📋 生成结果汇总:")
        all_ok = True
        for name, path_, ok in results:
            status = "✅ 成功" if ok else "❌ 失败/跳过"
            print(f"  {name}: {status}")
            if not ok:
                all_ok = False
        if all_ok:
            print("🎉 全部完成！")
        else:
            print("⚠️  部分任务未完成，请检查上方日志")
        sys.exit(0 if all_ok else 1)

    else:
        print(f"❌ 未知命令: {cmd}")
        print("支持的命令: source, manual, all")
        sys.exit(1)


if __name__ == '__main__':
    main()
