---
name: china-soft-copyright
description: Generate compliant materials for Chinese software copyright registration (软著申请) — source code document, software manual PDF, application form guidance.
triggers:
  - User mentions 软著, 软件著作权, 版权登记, 申请材料, 程序鉴别材料, 文档鉴别材料
  - User asks about copyright application forms, source code submission format
  - User needs to prepare PDF documents meeting Chinese copyright office standards
---

# 中国软著申请材料生成

为中国软件著作权登记生成合规的申请材料。**全自动流程**——AI 扫描项目、读代码、生成材料，用户只需确认少量信息。

## 核心理念

用户已经做好了项目，AI 应该自己去看代码、理解功能、生成材料，而不是问用户 22 个问题。

## 全自动工作流程

当用户说"我要申请软著"或"帮我准备软著材料"时，**按以下流程自动执行**：

### Step 1: 扫描项目（自动）

用户给出项目目录后，AI 立即开始扫描：

```bash
# 1. 列出所有源文件
find /path/to/project -type f \( -name "*.py" -o -name "*.js" -o -name "*.ts" \
  -o -name "*.jsx" -o -name "*.tsx" -o -name "*.vue" -o -name "*.html" -o -name "*.css" \
  -o -name "*.java" -o -name "*.go" -o -name "*.rs" -o -name "*.c" -o -name "*.cpp" \
  -o -name "*.swift" -o -name "*.kt" -o -name "*.rb" -o -name "*.php" \) \
  ! -path "*/node_modules/*" ! -path "*/.git/*" ! -path "*/dist/*" ! -path "*/build/*" \
  ! -path "*/__pycache__/*" ! -path "*/vendor/*" ! -path "*/venv/*"

# 2. 统计总行数
find /path/to/project -type f \( -name "*.py" ... \) ! -path "*/node_modules/*" \
  -exec cat {} + | wc -l

# 3. 检查项目配置文件
cat package.json 2>/dev/null    # Node.js 项目
cat requirements.txt 2>/dev/null # Python 项目
cat Cargo.toml 2>/dev/null       # Rust 项目
cat go.mod 2>/dev/null           # Go 项目
cat pom.xml 2>/dev/null          # Java 项目

# 4. 读 README 了解项目
cat README.md 2>/dev/null
```

### Step 2: 理解项目（自动）

AI 读取关键源文件，自动推断：

| 信息 | 推断方式 |
|------|---------|
| 软件全称 | 从 package.json/README 推断，或根据功能描述建议 |
| 版本号 | 从 package.json/git tag 读取，默认 V1.0 |
| 编程语言 | 从文件扩展名统计 |
| 技术栈 | 从 package.json/requirements.txt 等依赖文件读取 |
| 主要功能 | 读 README + 关键源文件，总结功能模块 |
| 技术特点 | 从代码架构、使用的框架/库推断 |
| 源程序量 | `wc -l` 精确统计 |
| 开发/运行环境 | 从依赖文件和代码推断 |
| 面向领域 | 从功能描述推断 |
| 开发目的 | 从 README 和代码注释推断 |

### Step 3: 只问用户必要信息

AI 只问**确实无法从代码推断**的信息，通常只需要：

1. **著作权人** — 必须问（身份证姓名或公司全称）
2. **软件全称** — 如果从代码能推断就建议一个，让用户确认
3. **版本号** — 如果能读到就自动填，否则默认 V1.0
4. **开发完成日期** — 从 git log 最早 commit 建议，让用户确认

**不要问用户已经能从代码推断的信息。**

### Step 4: 生成材料（自动）

信息确认后，自动按顺序生成：

1. **源代码文档** (.txt) — 50行/页，行号+代码
2. **软件说明书** (PDF) — 从代码分析自动生成，≥30行/页
3. **申请表填写指导** — 自动填好所有字段，标注字数限制

### Step 5: 交付

告诉用户输出文件位置，让用户检查确认。

---

## 文档要求速查

| 材料 | 页数规则 | 每页行数 | 格式 |
|------|---------|---------|------|
| 程序鉴别材料 | 源程序>60页→前30+后30页；<60页→全部 | ≥50行/页 | 行号+代码，等宽字体 |
| 文档鉴别材料 | 全文档>60页→前30+后30页；<60页→全部 | ≥30行/页 | 说明书/用户手册/设计文档 |

---

## 代码分析要点

### 读哪些文件

按优先级读取：
1. `README.md` — 项目概述、功能说明
2. `package.json` / `requirements.txt` / `Cargo.toml` 等 — 依赖和元信息
3. 主入口文件（`index.js`、`main.py`、`app.py` 等）— 核心逻辑
4. 路由/页面文件 — 功能模块
5. 配置文件 — 技术栈细节

### 总结什么

- **功能模块**：按代码结构划分，每个模块 1-2 句话描述
- **技术特点**：使用的框架、架构模式、创新点
- **面向领域**：根据功能推断（教育/医疗/金融/电商/内容创作等）
- **开发目的**：从 README 或代码注释提取

---

## 字数限制速查

| 字段 | 字数限制 | 备注 |
|------|---------|------|
| 软件全称 | 一般15字以内 | 须以"软件/APP/系统/平台"结尾 |
| 软件简称 | 不超过全称长度 | 可不填 |
| 版本号 | 无限制 | 格式：V1.0 或 1.0 |
| 源程序量 | 无限制 | 填精确行数 |
| 开发目的 | 无明确限制 | 1-2句话即可 |
| 面向领域/行业 | 无明确限制 | 简短描述 |
| 主要功能 | **500-1300字** | 需与说明书一致，审核重点 |
| 技术特点 | **≤100字** | 必须精炼，体现独创性 |
| 硬件环境 | 无明确限制 | 简短描述 |
| 软件环境 | 无明确限制 | 简短描述 |
| 编程语言 | 无明确限制 | 列出所有语言 |

⚠️ **2026年3月15日更新**：中国版权保护中心更新了申请表，功能说明部分有扩展，签章环节新增诚信说明要求。旧版申请表已废止。

---

## 脚本使用

### 源代码文档

```bash
export PROJECT_DIR=/path/to/project
export SOURCE_FILES="src/app.py,src/utils.py,src/main.py"
export SOFTWARE_NAME="XXX工具软件"
export VERSION="V1.0"
export AUTHOR="张三"
export COPYRIGHT_DIR=/path/to/output
python3 scripts/gen_source_doc.py
```

### 说明书 PDF

```bash
python3 scripts/gen_manual_pdf.py 软件说明书.md 输出.pdf
```

### 通用 PDF 生成器

```bash
python3 scripts/convert_to_pdf.py source <txt_file> <output>
python3 scripts/convert_to_pdf.py manual <md_file> <output>
python3 scripts/convert_to_pdf.py all
```

---

## 命名策略

软件全称中的领域词选最宽泛的那个——覆盖面越大越好，不要用太窄的词把自己锁死。例如"内容创作"比"短视频"好，"写作工具"比"剧本编辑器"好。名称须以"软件/APP/系统/平台"结尾，以"工具/计算/系列"等结尾的要慎用。

---

## PDF 生成参数

经过多次调试的参数，不要随意改动：

| 类型 | 字体大小 | 行高 | 边距 | 效果 |
|------|---------|------|------|------|
| 源代码 PDF | 8.5px | 1.18 | 0.5cm | 50 行/页 |
| 说明书 PDF | 9.8px | 1.55 | 1.3cm | ≥30 行/页 |

使用 **Node.js Playwright API** 生成 PDF，不要用 Chromium CLI 的 `--print-to-pdf`（会忽略 `@page` CSS 导致行数不可控）。

---

## 常见坑（提前告诉用户）

- **软件全称不能改**：提交后改名等于重新申请
- **版本号不影响保护范围**：V1.1 的软著覆盖后续所有版本
- **重构不影响软著**：改内部代码不改变软件名称+功能形态，证书继续有效
- **源代码文档里的软件名必须跟申请表一致**：差一个字都不行
- **命名选宽泛词**：领域词选覆盖面大的，别用太窄的把自己锁死
- **2026年3月15日起使用新版申请表**：旧版已废止
- **主要功能字段（500-1300字）是审核重点**：必须与说明书内容一致
- **技术特点只有100字**：提前精炼好
- **各50字字段别超限**：表单会直接截断，超了不提示

---

## 支撑文件

- `scripts/gen_source_doc.py` — 源代码 .txt 生成器（50行/页）
- `scripts/gen_manual_pdf.py` — 说明书 MD→PDF 转换器（≥30行/页）
- `scripts/convert_to_pdf.py` — 通用 PDF 生成器（源码+说明书双模式）
- `templates/manual-template.md` — 软件说明书 Markdown 模板
- `references/field-limits.md` — 申请表各字段字数限制速查表
