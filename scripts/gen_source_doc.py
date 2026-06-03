#!/usr/bin/env python3
"""生成软件著作权源代码文档 — 严格50行/页，行号前缀"""
import os, sys

WORKSPACE = os.path.expanduser("~/.hermes/workspace/ChangeTale")
# 按需改 OUTPUT_DIR
OUTPUT_DIR = os.environ.get("COPYRIGHT_DIR", "/media/sf_/changetale/copyright")
LINES_PER_PAGE = 50
PAGES_FRONT = 30
PAGES_BACK = 30

# 按需修改文件列表
FILES = [
    ("index.html", "页面结构"),
    ("style.css", "桌面端样式"),
    ("mobile.css", "移动端样式"),
    ("app.js", "前端核心逻辑"),
    ("mobile.js", "移动端交互"),
    ("server.js", "后端服务"),
]

SOFTWARE_NAME = os.environ.get("SOFTWARE_NAME", "章台剧本结构化创作工具")
VERSION = os.environ.get("VERSION", "V1.1")
AUTHOR = os.environ.get("AUTHOR", "梁起珩")

def get_source_lines():
    all_lines = []
    for fname, _ in FILES:
        fpath = os.path.join(WORKSPACE, fname)
        if os.path.exists(fpath):
            with open(fpath, 'r', encoding='utf-8') as f:
                all_lines.extend(f.readlines())
    return all_lines

def generate():
    code_lines = get_source_lines()
    total = len(code_lines)
    total_pages = (total + LINES_PER_PAGE - 1) // LINES_PER_PAGE
    
    front_count = PAGES_FRONT * LINES_PER_PAGE
    back_count = PAGES_BACK * LINES_PER_PAGE
    front_lines = code_lines[:front_count]
    back_lines = code_lines[-back_count:] if total > back_count else code_lines
    
    output = os.path.join(OUTPUT_DIR, f"源代码文档_{SOFTWARE_NAME}_{VERSION}.txt")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    with open(output, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write(f"软件名称：{SOFTWARE_NAME}\n")
        f.write(f"版本号：{VERSION}\n")
        f.write(f"著作权人：{AUTHOR}\n")
        f.write("开发语言：JavaScript (Node.js) + HTML/CSS\n")
        f.write(f"源程序总行数：{total} 行\n")
        f.write(f"源程序总页数：{total_pages} 页（>60页，取前{PAGES_FRONT}页+后{PAGES_BACK}页）\n")
        f.write(f"本文件行数：{len(front_lines) + len(back_lines)} 行（{PAGES_FRONT + PAGES_BACK}页 × {LINES_PER_PAGE}行/页）\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("【前30页源代码】\n\n")
        for page in range(PAGES_FRONT):
            start = page * LINES_PER_PAGE
            chunk = front_lines[start:start + LINES_PER_PAGE]
            for i, line in enumerate(chunk):
                f.write(f"{(start + i + 1):5d} | {line}")
            f.write(f"\n--- 第 {page + 1} 页结束 ---\n\n")
        
        f.write("\n" + "=" * 60 + "\n")
        omitted = total - front_count - back_count
        f.write(f"（第{PAGES_FRONT+1}页至第{total_pages-PAGES_BACK}页省略，共{total_pages-PAGES_FRONT-PAGES_BACK}页，{omitted}行）\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("【后30页源代码】\n\n")
        line_offset = total - back_count + 1
        for page in range(PAGES_BACK):
            start = page * LINES_PER_PAGE
            chunk = back_lines[start:start + LINES_PER_PAGE]
            for i, line in enumerate(chunk):
                f.write(f"{(line_offset + start + i):5d} | {line}")
            f.write(f"\n--- 第 {total_pages - PAGES_BACK + page + 1} 页结束 ---\n\n")
    
    print(f"✅ {output}")
    print(f"   源程序总行数：{total}（{total_pages}页）")
    print(f"   输出：前{PAGES_FRONT}页+后{PAGES_BACK}页，每页{LINES_PER_PAGE}行")
    return output

if __name__ == "__main__":
    generate()
