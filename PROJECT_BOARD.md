# 📄 china-soft-copyright — 项目说明

> 最后更新：2026-06-03 | 当前版本：v1.0 | 状态：待上传 GitHub 🔄

---

## 一、总览

```
产品：Hermes Agent 中国软著申请材料生成 skill
定位：引导用户填写申请信息 → 生成源代码文档 → 生成说明书 PDF → 填表指导
模式：开源免费（MIT），Hermes Agent 插件
GitHub：待上传
```

---

## 二、目录结构

```
china-soft-copyright/
├── SKILL.md                        # 主 skill 文件（申请流程 + 技术细节）
├── README.md                       # 用户文档
├── scripts/
│   ├── gen_source_doc.py           # 源代码 .txt 生成器（50行/页）
│   ├── gen_manual_pdf.py           # 说明书 MD→PDF 转换器（≥30行/页）
│   └── convert_to_pdf.py           # 通用 PDF 生成器
├── templates/
│   └── manual-template.md          # 说明书 Markdown 模板
└── references/
    ├── changetale-copyright-prep.md # 项目实例参考（章台）
    └── field-limits.md             # 字数限制详细说明
```

---

## 三、版本历史

### v1.0 — 初始发布 ✅ 2026-06-03

- [x] 22 个字段引导问答流程（Step 1 基本信息 + Step 2 技术信息）
- [x] 字数限制速查（主要功能 500-1300 字、技术特点 ≤100 字、各 50 字字段）
- [x] 源代码文档生成器（scripts/gen_source_doc.py，50 行/页）
- [x] 说明书 PDF 生成器（scripts/gen_manual_pdf.py，≥30 行/页）
- [x] 通用 README.md
- [x] .gitignore

---

## 四、待办

- [ ] BB 确认后上传 GitHub
- [ ] 考虑是否需要更多项目实例（目前只有章台）

---

## 五、关键信息

- **2026 年 3 月 15 日新版申请表已启用，旧版废止**
- 主要功能 500-1300 字是审核重点，必须与说明书一致
- 技术特点只有 100 字，提前精炼好
- PDF 生成用 Node.js Playwright API，不用 Chromium CLI
- 自用版有章台实例（references/changetale-copyright-prep.md），通用版已去掉

---

## 六、Agent 交接说明

本项目通用版已完善，等 BB 确认后上传 GitHub。如需扩展：
1. 新增项目实例 → 在 `references/` 下添加，SKILL.md 中引用
2. 修改生成逻辑 → `scripts/gen_source_doc.py` 或 `scripts/gen_manual_pdf.py`
3. 修改申请流程 → `SKILL.md` 的引导问答部分
