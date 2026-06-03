# 📄 中国软著申请材料生成 - Hermes Skill

A [Hermes Agent](https://github.com/nousresearch/hermes-agent) skill for generating compliant materials for Chinese software copyright registration (软件著作权登记).

## 功能

- 📝 **申请引导** — 22 个字段逐一确认，避免填错返工
- 💻 **源代码文档** — 自动生成 50 行/页的 .txt 文件（前30+后30 或全部）
- 📄 **软件说明书** — Markdown → PDF，≥30 行/页
- 📋 **申请表指导** — 每个字段的正确填写方式 + 字数限制提示

## Quick Start

```bash
git clone https://github.com/249695811/china-soft-copyright.git ~/.hermes/skills/china-soft-copyright
```

然后告诉你的 Hermes Agent：
- "我要申请软著"
- "帮我准备软著材料"
- "生成源代码文档"

## 工作流程

Agent 会先走引导问答（Step 1-2），确认所有信息后再生成材料（Step 3）：

### Step 1: 基本信息
- 软件全称、英文名、版本号
- 著作权人、开发方式、权利范围
- 首次发表状态

### Step 2: 技术信息
- 源程序量（自动统计 `wc -l`）
- 软件分类、开发完成日期
- 硬件/软件环境、编程语言
- 主要功能（500-1300 字）、技术特点（≤100 字）

### Step 3: 材料生成
1. 源代码文档 (.txt)
2. 软件说明书 (PDF)
3. 申请表填写指导

## 字数限制速查

| 字段 | 限制 |
|------|------|
| 软件全称 | ≤15 字 |
| 主要功能 | 500-1300 字 |
| 技术特点 | ≤100 字 |
| 各环境/领域/目的 | ≤50 字 |

## 文件结构

```
├── SKILL.md                          # 主 skill 文件（申请流程 + 技术细节）
├── scripts/
│   ├── gen_source_doc.py             # 源代码 .txt 生成器（50行/页）
│   ├── gen_manual_pdf.py             # 说明书 MD→PDF 转换器
│   └── convert_to_pdf.py             # 通用 PDF 生成器
├── templates/
│   └── manual-template.md            # 说明书 Markdown 模板
└── references/
    ├── changetale-copyright-prep.md  # 项目实例参考
    └── field-limits.md               # 字数限制详细说明
```

## 常见坑

- **软件全称不能改**：提交后改名等于重新申请
- **重构不影响软著**：改内部代码不影响证书有效性
- **主要功能 500-1300 字是审核重点**：必须与说明书一致
- **技术特点只有 100 字**：提前精炼好
- **2026年3月15日起使用新版申请表**：旧版已废止

## License

MIT
