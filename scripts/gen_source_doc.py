#!/usr/bin/env python3
"""生成软件著作权源代码文档 — 严格50行/页，行号前缀

Configuration via environment variables:
  PROJECT_DIR      (required) Root directory of the source project
  SOURCE_FILES     (required) Comma-separated list of source files relative to PROJECT_DIR
  SOFTWARE_NAME    (required) Software name for the copyright header
  VERSION          (required) Version string (e.g. V1.0)
  AUTHOR           (required) Copyright holder name
  COPYRIGHT_DIR    (required) Output directory for the generated document
  LINES_PER_PAGE   (default 50)  Lines per page
  PAGES_FRONT      (default 30)  Number of front pages to include
  PAGES_BACK       (default 30)  Number of back pages to include
"""
import os
import sys

# Map file extensions to language descriptions
LANG_MAP = {
    ".py":       "Python",
    ".js":       "JavaScript",
    ".ts":       "TypeScript",
    ".jsx":      "React (JSX)",
    ".tsx":      "React (TSX)",
    ".java":     "Java",
    ".c":        "C",
    ".cpp":      "C++",
    ".h":        "C/C++ Header",
    ".cs":       "C#",
    ".go":       "Go",
    ".rs":       "Rust",
    ".rb":       "Ruby",
    ".php":      "PHP",
    ".swift":    "Swift",
    ".kt":       "Kotlin",
    ".scala":    "Scala",
    ".html":     "HTML",
    ".css":      "CSS",
    ".scss":     "SCSS",
    ".less":     "LESS",
    ".vue":      "Vue",
    ".svelte":   "Svelte",
    ".sql":      "SQL",
    ".sh":       "Shell",
    ".bash":     "Bash",
    ".lua":      "Lua",
    ".r":        "R",
    ".m":        "Objective-C",
    ".dart":     "Dart",
    ".ex":       "Elixir",
    ".erl":      "Erlang",
    ".hs":       "Haskell",
    ".ml":       "OCaml",
    ".clj":      "Clojure",
    ".xml":      "XML",
    ".json":     "JSON",
    ".yaml":     "YAML",
    ".yml":      "YAML",
    ".toml":     "TOML",
    ".md":       "Markdown",
    ".txt":      "Text",
}


def _require_env(name: str) -> str:
    """Get a required environment variable or exit with a clear error."""
    val = os.environ.get(name, "").strip()
    if not val:
        print(f"❌ Error: required environment variable {name} is not set.", file=sys.stderr)
        print(f"   Set it before running:  export {name}=<value>", file=sys.stderr)
        sys.exit(1)
    return val


def _int_env(name: str, default: int) -> int:
    """Get an optional integer environment variable with a default."""
    raw = os.environ.get(name, "").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        print(f"⚠️  Warning: {name}={raw!r} is not a valid integer, using default {default}.")
        return default


def derive_languages(file_paths: list[str]) -> str:
    """Derive a human-readable language description from file extensions."""
    ext_set: set[str] = set()
    for fp in file_paths:
        _, ext = os.path.splitext(fp)
        ext = ext.lower()
        if ext:
            ext_set.add(ext)

    langs = []
    for ext in sorted(ext_set):
        name = LANG_MAP.get(ext)
        if name:
            langs.append(name)
        else:
            langs.append(ext.lstrip(".").upper())

    if not langs:
        return "Unknown"
    return " + ".join(langs)


def get_config():
    """Read and return all configuration from environment variables."""
    project_dir = _require_env("PROJECT_DIR")
    source_files_raw = _require_env("SOURCE_FILES")
    software_name = _require_env("SOFTWARE_NAME")
    version = _require_env("VERSION")
    author = _require_env("AUTHOR")
    copyright_dir = _require_env("COPYRIGHT_DIR")
    lines_per_page = _int_env("LINES_PER_PAGE", 50)
    pages_front = _int_env("PAGES_FRONT", 30)
    pages_back = _int_env("PAGES_BACK", 30)

    # Split and strip the comma-separated file list
    source_files = [f.strip() for f in source_files_raw.split(",") if f.strip()]
    if not source_files:
        print("❌ Error: SOURCE_FILES is set but contains no valid file entries.", file=sys.stderr)
        sys.exit(1)

    return {
        "project_dir": project_dir,
        "source_files": source_files,
        "software_name": software_name,
        "version": version,
        "author": author,
        "copyright_dir": copyright_dir,
        "lines_per_page": lines_per_page,
        "pages_front": pages_front,
        "pages_back": pages_back,
    }


def get_source_lines(project_dir: str, source_files: list[str]) -> list[str]:
    """Read all source files and return a flat list of lines."""
    all_lines: list[str] = []
    for fname in source_files:
        fpath = os.path.join(project_dir, fname)
        if not os.path.exists(fpath):
            print(f"⚠️  Warning: {fpath} does not exist, skipping.", file=sys.stderr)
            continue
        with open(fpath, "r", encoding="utf-8") as f:
            all_lines.extend(f.readlines())
    return all_lines


def generate():
    cfg = get_config()

    project_dir = cfg["project_dir"]
    source_files = cfg["source_files"]
    software_name = cfg["software_name"]
    version = cfg["version"]
    author = cfg["author"]
    copyright_dir = cfg["copyright_dir"]
    lines_per_page = cfg["lines_per_page"]
    pages_front = cfg["pages_front"]
    pages_back = cfg["pages_back"]

    code_lines = get_source_lines(project_dir, source_files)
    total = len(code_lines)
    if total == 0:
        print("❌ Error: no source code lines found. Check PROJECT_DIR and SOURCE_FILES.", file=sys.stderr)
        sys.exit(1)

    total_pages = (total + lines_per_page - 1) // lines_per_page
    front_count = pages_front * lines_per_page
    back_count = pages_back * lines_per_page
    front_lines = code_lines[:front_count]
    back_lines = code_lines[-back_count:] if total > back_count else code_lines

    # Derive language from actual file extensions
    full_paths = [os.path.join(project_dir, f) for f in source_files]
    language = derive_languages(full_paths)

    output = os.path.join(copyright_dir, f"源代码文档_{software_name}_{version}.txt")
    os.makedirs(copyright_dir, exist_ok=True)

    with open(output, "w", encoding="utf-8") as f:
        f.write("=" * 60 + "\n")
        f.write(f"软件名称：{software_name}\n")
        f.write(f"版本号：{version}\n")
        f.write(f"著作权人：{author}\n")
        f.write(f"开发语言：{language}\n")
        f.write(f"源程序总行数：{total} 行\n")
        f.write(f"源程序总页数：{total_pages} 页（>60页，取前{pages_front}页+后{pages_back}页）\n")
        f.write(f"本文件行数：{len(front_lines) + len(back_lines)} 行（{pages_front + pages_back}页 × {lines_per_page}行/页）\n")
        f.write("=" * 60 + "\n\n")

        f.write(f"【前{pages_front}页源代码】\n\n")
        for page in range(pages_front):
            start = page * lines_per_page
            chunk = front_lines[start:start + lines_per_page]
            if not chunk:
                break
            for i, line in enumerate(chunk):
                f.write(f"{(start + i + 1):5d} | {line}")
            f.write(f"\n--- 第 {page + 1} 页结束 ---\n\n")

        f.write("\n" + "=" * 60 + "\n")
        omitted = total - len(front_lines) - len(back_lines)
        omitted_start = pages_front + 1
        omitted_end = total_pages - pages_back
        omitted_pages = omitted_end - omitted_start + 1
        f.write(f"（第{omitted_start}页至第{omitted_end}页省略，共{omitted_pages}页，{omitted}行）\n")
        f.write("=" * 60 + "\n\n")

        f.write(f"【后{pages_back}页源代码】\n\n")
        line_offset = total - back_count + 1
        for page in range(pages_back):
            start = page * lines_per_page
            chunk = back_lines[start:start + lines_per_page]
            if not chunk:
                break
            for i, line in enumerate(chunk):
                f.write(f"{(line_offset + start + i):5d} | {line}")
            f.write(f"\n--- 第 {total_pages - pages_back + page + 1} 页结束 ---\n\n")

    print(f"✅ {output}")
    print(f"   源程序总行数：{total}（{total_pages}页）")
    print(f"   开发语言：{language}")
    print(f"   输出：前{pages_front}页+后{pages_back}页，每页{lines_per_page}行")
    return output


if __name__ == "__main__":
    generate()
