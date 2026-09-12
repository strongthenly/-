# GPT-6 数学建模工作流 · v1.1

从2025A核内调度与2024C磁芯损耗两轮完整真题演练、论文修订和压力验证中提炼。目标是让另一台电脑、另一位使用者也能执行同样的证据与交付标准。技能不保证相同分数、误差或奖项；模型版本、原始数据、验证设计和人工实验条件都会影响结果。

## 五分钟启动

```bash
git clone https://github.com/strongthenly/-.git modeling-workflows
cd modeling-workflows/建模
python tools/workflow.py doctor
```

在 Codex 中以这个 `建模` 文件夹为工作目录打开任务，选择 **GPT-6 Astra**。技能位于 `.agents/skills/gpt6-math-modeling`；Codex从工作目录及其祖先目录发现技能，**从仓库根启动不会向下扫描建模中的技能**。找不到时先检查目录，再重开任务；也可直接让它读取该SKILL.md。

复制下面这段给 Codex（替换路径和范围）：

```text
使用 $gpt6-math-modeling。
原题与附件：<本机可读目录>；工作目录：<新项目目录>。
目标：完成所有问题的分析、建模、真实求解、独立验证、科学图表、LaTeX PDF及题目要求的答案文件。
这是独立真题练习，首稿冻结前不读同题获奖论文或商业解法。
复用已有环境。先核对数据和验收标准；常规可逆实现自行推进，关键语义缺失时说明影响。
每项核心优势给同口径强基线、证据和适用边界。不要为命名制造创新，不用空白凑页数。
生成一版可复核的完整首稿，冻结模型、划分、结果及文件哈希；检查PDF中全部页面。
保存HANDOFF.md，使下一位代理不依赖聊天记忆即可继续。
```

**本仓库的协作边界**：根README把建模、编程和写作分配到不同目录。本包只是流程资源，不自动授予跨角色修改权。本仓库内按建模手运行时输出模型说明、公式、实现接口和验证要求；全链路练习请指定独立新项目目录，或先明确团队分工授权。不要修改他人的src/paper等目录。

## 移植到其他项目或个人环境

```bash
# 创建一个独立练习项目：目录必须不存在
python tools/workflow.py init /path/to/new-project
# 把完整技能复制到该项目；目标同名技能已存在则拒绝覆盖
python tools/workflow.py install /path/to/new-project/.agents/skills
```

Windows把路径替换为例如 `D:/modeling/practice`，有空格须加引号。个人安装可使用自己主目录下的 `.agents/skills`。复制的是整个技能文件夹，包含references和assets，不要只复制SKILL.md。更新时先比较旧版本并备份，脚本不会静默覆盖。无需修改全局Codex配置或放宽沙箱权限。

官方依据（核对日期2026-09-11）：[Codex技能发现和显式调用](https://learn.chatgpt.com/docs/build-skills)、[GPT-6 Astra使用与提示指导](https://developers.openai.com/api/docs/guides/latest-model)。模型由用户所在Codex环境选择，技能不能替账户开通模型，也不会自己切换模型。实际模型ID应记录到运行日志；API实现另按官方文档核对，不把本机模型可用性当作所有账号的事实。

## 目录与阅读顺序

|入口|用途|
|---|---|
|[SKILL.md](.agents/skills/gpt6-math-modeling/SKILL.md)|主技能：任务选择、证据链、收口|
|[调用规范](调用规范.md)|新题、续做、评审、有限额度、三人协作提示词|
|[环境与复现](环境与复现.md)|必须/按需依赖、跨平台LaTeX、迁移限制|
|[演练经验与验收](演练经验与验收.md)|2025A与2024C失败经验、质量判据、回归演练|
|[预测与不确定性](.agents/skills/gpt6-math-modeling/references/prediction.md)|泄漏、外推、响应敏感性、共形与选择|
|[优化与证明](.agents/skills/gpt6-math-modeling/references/optimization.md)|可行性、强基线、下界、精确验证|
|[论文与图表](.agents/skills/gpt6-math-modeling/references/paper.md)|摘要、图型、原生公式、逐页复核|
|[模板迁移](.agents/skills/gpt6-math-modeling/references/template-fidelity.md)|模板规格、章节映射、可编辑公式、目录与跨格式完整性|
|[运行与交接](.agents/skills/gpt6-math-modeling/references/execution.md)|证据账本、冻结、预算和交接|

维护包本身时执行 `python -m unittest discover -s tests -v`。这验证工具行为和包完整性，不等同于盲题生成质量验证。本次发布没有在全新Linux/macOS环境或独立用户账号上完整跑一篇论文。

只发布流程和自写模板，不包含赛方数据、获奖论文、私有运行库、密钥或个人目录。使用者须自行取得合法原题附件。后续论文的公开发布应另外获得明确授权。
