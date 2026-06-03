#!/usr/bin/env python3
"""软著材料 PDF 生成器
- 程序鉴别材料：Node.js Playwright，精确50行/页 A4
- 文档鉴别材料：Chromium 渲染 MD→PDF
"""
import os, subprocess, re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# 如果放在 skill 的 scripts/ 下，OUTPUT_DIR 可能需要改为外部路径
OUTPUT_DIR = SCRIPT_DIR


def gen_source_pdf(txt_file, output_file, playwright_path):
    """生成源代码 PDF，精确 50 行/页"""
    node_script = os.path.join(SCRIPT_DIR, '_gen_source_pdf.js')
    
    # 内联 Node 脚本
    js = f"""
const {{ chromium }} = require('{playwright_path}');
const fs = require('fs'), path = require('path');
const txt = fs.readFileSync('{txt_file}', 'utf-8');

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

const tmp = path.join(path.dirname('{txt_file}'), '_tmp.html');
fs.writeFileSync(tmp, html);
(async () => {{
    const b = await chromium.launch({{ headless: true }});
    const p = await b.newPage();
    await p.goto('file://' + tmp, {{ waitUntil: 'networkidle' }});
    await p.pdf({{ path: '{output_file}', format: 'A4', margin: {{ top: '0.5cm', bottom: '0.5cm', left: '0.5cm', right: '0.5cm' }} }});
    await b.close();
    fs.unlinkSync(tmp);
}})();
"""
    with open(node_script, 'w') as f:
        f.write(js)
    
    result = subprocess.run(['node', node_script], capture_output=True, text=True)
    if result.returncode != 0:
        print(f'❌ 失败: {result.stderr}')
        return False
    os.remove(node_script)
    size_kb = os.path.getsize(output_file) // 1024
    print(f'✅ {os.path.basename(output_file)} ({size_kb}KB)')
    return True


def gen_manual_pdf(md_file, output_file):
    """Markdown 说明书 → PDF"""
    with open(md_file, 'r', encoding='utf-8') as f:
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
    
    html = f'''<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8">
<style>
@page {{ margin: 2.5cm 2cm; size: A4; }}
body {{ font-family: "SimSun", serif; font-size: 12px; line-height: 2; color: #000; }}
h1 {{ font-family: "SimHei", sans-serif; font-size: 18px; text-align: center; margin: 20px 0; }}
h2 {{ font-family: "SimHei", sans-serif; font-size: 14px; margin: 16px 0 8px; border-bottom: 1px solid #333; padding-bottom: 4px; }}
h3 {{ font-family: "SimHei", sans-serif; font-size: 12px; margin: 12px 0 6px; }}
p {{ margin: 4px 0; text-indent: 2em; }}
li {{ margin: 3px 0 3px 1em; }}
hr {{ border: none; border-top: 1px dashed #ccc; margin: 12px 0; }}
blockquote {{ background: #f5f5f5; border-left: 3px solid #999; margin: 8px 0; padding: 8px 12px; font-size: 11px; }}
</style></head><body>{''.join(html_lines)}</body></html>'''
    
    tmp = os.path.join(SCRIPT_DIR, '_tmp_man.html')
    with open(tmp, 'w', encoding='utf-8') as f:
        f.write(html)
    
    subprocess.run([
        'chromium-browser', '--headless', '--no-sandbox', '--disable-gpu',
        f'--print-to-pdf={output_file}', f'file://{os.path.abspath(tmp)}'
    ], check=True, timeout=60)
    os.remove(tmp)
    
    size_kb = os.path.getsize(output_file) // 1024
    print(f'✅ {os.path.basename(output_file)} ({size_kb}KB)')
    return True


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("用法: python3 convert_to_pdf.py <source|manual|all>")
        sys.exit(1)
    # 子命令实现略——实际使用时直接调用上面的函数
