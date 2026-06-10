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
- **2026年3月15日起使用新版申请表**：旧版已废止，新版签章页新增**AI承诺条款+失信惩戒+征信挂钩**（详见 `references/ai-commitment-clause.md`）
- **⚠️ AI承诺条款是签章页的核心变更**：申请人须声明"未使用AI开发编写代码、撰写文档或生成登记申请材料"，手抄失信+征信惩罚条款。这是二元判断——不看比例、不看贡献度
- **⚠️ 材料必须清除所有AIGC痕迹**：AI模型名称（GPT/Claude等）、AI Provider名称、字数标注（如"（57字）"）、过度结构化的bullet point——都会被识别为AI生成。说明书改成开发者口吻，测试部分用叙述体不用对仗工整的列表（详见 `references/aigc-detection.md`）
- **⚠️ AIGC检测不要预设清单**：让检测AI用自己的专业知识判断，不要预先定义"查哪些特征"。预设清单会限制检测范围。推荐用开放式提示词（见 `references/aigc-detection.md` 的检测流程）
- **⚠️ AIGC检测后让AI直接改正**：检测报告发现问题后，可以让检测AI直接修改材料
- **⚠️ 申请表填写指南本身也要过AIGC检测**：AI写的"注意事项"段容易暴露——它会写"XX字段已确认没问题"（AI自检汇报）而不是"提交前核对XX字段"（人类提醒）。字数标注（"76字"、"800字"）、模型名称列举（"不含GPT/Claude"）都是AI自我泄露
- **⚠️ 字数标注是最容易忽略的AIGC痕迹**：申请表字段复制粘贴时，如果工具输出带了"（57字）"这种标注，提交上去就暴露了。**所有字段内容复制到申请表前，必须手动检查有没有残留的字数标注、模型名、括号注释**
- **⚠️ "人工智能软件"标签要慎选**：如果签了AI承诺条款（声明未使用AI），技术特点标签选"人工智能软件"会自相矛盾。软件的核心功能是X、AI只是辅助时，不选这个标签
- **⚠️ 提交后字段改不了**：申请表在线填写后一旦提交，技术特点字段等内容无法修改，只能等审核员打回来再改。复制内容到申请表前**必须逐字段检查**
- **⚠️ 截图描述不要用同一个句式开头**：为每张截图写描述时，AI容易用完全相同的句式（如"上图展示了XXX"）。人类写法是有的截图写详细、有的一句话带过
- **主要功能字段（500-1300字）是审核重点**：必须与说明书内容一致
- **技术特点只有100字**：提前精炼好，别写多了被截断
- **各50字字段别超限**：表单会直接截断，超了不提示
- **软件全称须以"软件/APP/系统/平台"结尾**：以"工具/计算/系列"等结尾的要慎用
- **⚠️ Chromium PDF页底会打印文件路径**：用 `--print-to-pdf` 时 Chromium 默认在每页底部显示 `file:///...` 路径，必须加 `--no-pdf-header-footer`（Chromium 120+）去除
- **⚠️ 写进说明书的每个功能/格式/数字都必须和代码核实**：不能凭印象或"听起来合理"就写。AI会自动填充听起来合理的数字和功能。**不确定的功能宁可不写，也不能编**——少写一个功能不会被驳回，写一个不存在的功能会被视为虚假材料

---

## 提交前检查清单（血泪教训，逐项核对！）

在把任何内容复制到版权中心在线申请表之前：

- [ ] **技术特点字段**：有没有残留字数标注？（如"（57字）"、"（68字）"）→ 删掉
- [ ] **技术特点字段**：开头有没有多出来的分类标签？（如"人工智能软件\n纯XXX..."）→ 只保留技术描述
- [ ] **主要功能字段**：有没有AI模型名？（GPT/Claude等）→ 替换为通用描述
- [ ] **主要功能字段**：有没有工具品牌名？（LM Studio/Ollama等）→ 替换为"本地推理服务"
- [ ] **技术特点标签**：签了AI承诺的话，不要勾选"人工智能软件"
- [ ] **所有字段**：逐字段肉眼扫一遍，确认没有括号注释、AI自检痕迹
- [ ] **截图**：逐张验证，确认展示的是目标功能而非空白/错误页面
- [ ] **说明书**：每个功能描述、格式数量、数字都和代码核对过
- [ ] **说明书**：没有编造不存在的功能/格式
- [ ] **PDF**：用 `--no-pdf-header-footer` 去掉页脚路径

---

## 支撑文件

- `scripts/gen_source_doc.py` — 源代码 .txt 生成器（50行/页）
- `scripts/gen_manual_pdf.py` — 说明书 MD→PDF 转换器（≥30行/页）
- `scripts/convert_to_pdf.py` — 通用 PDF 生成器（源码+说明书双模式）
- `templates/manual-template.md` — 软件说明书 Markdown 模板
- `references/field-limits.md` — 申请表各字段字数限制速查表
- `references/aigc-detection.md` — AIGC痕迹检测指南（检测流程+已知模式）
- `references/ai-commitment-clause.md` — AI承诺条款详解（2026年3月15日起施行）

## PDF 生成方式

两种方式都可行，按环境选择：

### 方式A: Chromium CLI（推荐，无需Playwright依赖）
```bash
chromium-browser --headless --no-sandbox --disable-gpu \
  --no-pdf-header-footer \
  --print-to-pdf=output.pdf \
  file:///absolute/path/to/input.html
```

⚠️ **必须加 `--no-pdf-header-footer`**：不加的话 Chromium 会在每页底部打印文件的 `file:///...` 路径。这个 flag 在 Chromium 120+ 可用。

### 方式B: Node.js Playwright API
```javascript
const { chromium } = require('playwright');
const browser = await chromium.launch({ headless: true });
const page = await browser.newPage();
await page.goto('file://' + htmlPath, { waitUntil: 'networkidle' });
await page.pdf({
  path: outputPath,
  format: 'A4',
  margin: { top: '0.5cm', bottom: '0.5cm', left: '0.5cm', right: '0.5cm' }
});
```

### 行数验证
```bash
# 源码PDF：统计含 '|' 的行（行号前缀）
pdftotext output.pdf - -f $PAGE -l $PAGE | grep -c '|'
# 说明书PDF：统计非空行
pdftotext output.pdf - -f $PAGE -l $PAGE | wc -l
```
⚠️ pdftotext 可能比肉眼少计1-2行，以实际 PDF 页面目视为准。版权中心审核员看的是视觉效果，不是跑脚本数行数。

### 说明书含截图时的处理原则

⚠️ **用户偏好：图片清晰 > 每页行数达标**。宁可图片大一点、清晰可读，也不要缩成看不清的缩图。

### 图片+行数的物理约束（必读）

A4纸 + 9.8px字体 + 1.55行高 → 每页约51行（含空白）。一张**全宽截图**（1440×900）约占用35行的垂直空间 → 同页只剩~16行文字 → **物理上不可能凑够30行**。这是硬约束，不是调参能解决的。

### 推荐做法（按图片数量选择策略）

**方案A：少截图（2-3张），全宽居中** — 最简单，最稳
1. 只放2-3张最关键的截图（主界面、核心功能），其余用文字描述
2. 图片 `max-width:100%; height:auto;` 居中显示
3. 图片前后各写3-5句描述段落，补偿行数

**方案B：多截图（5-8张），float环绕** — 图片小但能看到
1. 图片 `max-width:45%; float:right; margin:2px 0 4px 6px;` 让文字环绕
2. 每张图前后写5-8句描述（环绕后文字行数显著增加）
3. 用 `<!-- PAGEBREAK -->` 标记 + 脚本识别，在有图的小节前强制分页

**方案C：图片放附录** — 正文最稳
1. 正文纯文字描述，轻松每页30+行
2. 截图单独放一个"附录：界面截图"章节，每张图一页，标注图号

### 不要做的事

- ❌ 把图片缩到 `max-height:80px`（看不清，白放）
- ❌ 放8张全宽截图然后靠加文字凑30行（物理上不可能）
- ❌ 用 `page-break-before:always` 在每个图片容器上（每张图独占一页开头，同页文字只有3-10行，反而更不达标）
- ❌ 多张图不做分页控制（会堆在同一页，行数崩盘）

### 调研政策时的坑

- **官方公告 ≠ 实际申请表**: ccopyright.com.cn 的公告可能只提大方向（如"诚信制度"），具体条款（如AI承诺）在实际申请表模板里。调研政策变化时**必须看实际申请表或已提交的材料**，不能只看官网新闻稿
- **ccopyright.com.cn 文章正文是图片渲染**: 浏览器 DOM/accessibility tree 不含正文，必须 `browser_vision` 截图读取
- **自媒体解读 ≠ 官方原文**: 代办机构和行业自媒体经常夸大政策，以版权保护中心官网和实际表格为准
