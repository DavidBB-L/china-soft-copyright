# 章台 ChangeTale 软著材料准备

著作权人：梁起珩。材料统一放在 `/media/sf_/changetale/copyright/`。

## 触发条件

- 章台版本号升级后
- 新增重要功能后需要更新说明书和截图

## 源代码文档

编辑 `/media/sf_/changetale/copyright/gen_source_doc.py`：
- `files` 数组包含全部 6 个核心源文件：`index.html, style.css, mobile.css, app.js, mobile.js, server.js`
- 运行：`cd /media/sf_/changetale/copyright && python3 gen_source_doc.py`
- 输出：前30页（1500行）+ 后30页（1500行），中间省略

## 软件说明书

编辑 `/media/sf_/changetale/copyright/软件说明书_章台V{版本号}.md`：
- 更新标题和基本信息中的版本号
- 更新代码规模（`wc -l` 获取各文件最新行数）
- 新增功能模块在 `三、功能模块说明` 中追加，标注 `（V{版本号}新增）`
- 软件全称：**章台 Change Tale 剧本结构化创作工具**（"Change Tale" 绝不能丢；用"剧本"不是"短剧"）

## UI 截图清单

新功能截图按序号命名：`{序号}_{功能描述}.png`

现有截图：
- 01_主界面.png
- 02_角色管理.png
- 03_关系图.png
- 04_统计.png
- 05_AI改写.png
- 06_移动端UI预览.png
- 07_冷启动_模板选择.png
- 08_冷启动_输入创意.png

## 最终检查

```bash
ls -1 /media/sf_/changetale/copyright/*.png *.txt *.md *.py
```
确保包含：说明书.md + 源代码文档.txt + gen_source_doc.py + UI截图 ≥ 6张。

## 注意事项

- 6个源文件必须全收（旧版 gen_source_doc.py 只收了 app.js + server.js，已修正）
- 旧版材料保留：覆盖前先 `.bak` 备份
- 著作权人固定：梁起珩
- 文件编码：UTF-8
- 软著提交后版本号锁死，等证书下来再升
