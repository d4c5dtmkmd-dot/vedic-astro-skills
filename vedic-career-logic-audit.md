# vedic-career Skill 逻辑漏洞审查

> 审查对象：`/workspace/antigravity/skills/vedic-career/SKILL.md`（三份副本 antigravity / claude-code / codex 同构）
> 审查时间：2026-09-03
> 审查方式：三轮递进式，分别覆盖 SKILL 内部逻辑 / 跨 skill 契约引用 / 版本治理与计算端根因

---

## 第一轮：SKILL 内部逻辑自洽性（10 条）

### 高优先级

**#1 Phase 2 格局扫描方式与 yogas.md / calc 契约直接冲突**（SKILL.md L202, L209, L211）

career 写：
- L202：`格局扫描 → structured_data 预分析·Graha Drishti + 格局判定规则（参考vedic-core/resources/yogas.md；合相=同宫、互视=graha drishti、互溶=parivartana）`
- L209：`贵格(Raja Yoga): 参考预分析宫主表 + Graha Drishti 互视`
- L211：`Vipreet Raja Yoga: 6/8/12宫主互飞`

冲突：
- yogas.md L5-L14 明令：互视 = 双向 mutual（A 照 B 且 B 照 A，calc 已判）——**读「互视对」表**；❌禁自己从 Graha Drishti 表判双向。结构成立一律读 structured_data「结构格局预扫（全格局）」表 active 字段。
- formatter.py 实际输出了「结构格局预扫」「格局关系类 · 互视 / 互溶」两段。
- career 把已"结构下沉"的判定拉回模型自推，既违反 yogas.md，也和本文件 L128 "所有数据从 structured_data.md 读取，不自己计算"自相矛盾。
- VRY 同理：career 写"6/8/12宫主互飞"自推，yogas.md + p1_p12.md 要求读预扫表。

**#2 "紧密相位(<5°)" 与 orb 相位禁令打架**（L277 vs L168）

Phase 1 步骤3 定义"紧密相位 = 同宫合相 / graha drishti 照射，❌不用西占 orb 相位"；但 STEP 1 影响源头优先级③写"紧密相位(<5°)"——`<5°` 是度数 orb 口径。同一文档内同一个词两个定义，模型会顺 `<5°` 滑回已废除的西占相位。

**#3 生态位四类型判据不可操作**（L171-L177）

- "L10关联太阳/木星/9宫"的"关联"（合相？宫主身份？drishti？落宫？）无定义。
- "6宫能量≥10宫"的"能量"（SAV？occupants？宫主强勤？）无定义。
- 直接击穿 L71-73 自己立的铁律"不同用户同样数据→同样结论"。
- 四类型"可复合"却无仲裁规则——木星、土星同时"关联"L10 时权威型与市场型是对立画像，没有优先级。对比：分盘铁律有明确"冲突仲裁：分别呈现"。
- L190-191 商贸细分的"强连/弱连"同样无定义。

### 中优先级

**#4 变现路径无兜底、无优先级**（L220-L223）

强星不连 2/11/8 任何一宫 → 路径 A/B/C 全不触发，无默认分支；同连多宫无取舍规则。路径 C(8宫) 没有 SAV 极端值佐证说明，与 A/B 不对称。

**#5 STEP 4 步骤 C 果实归类覆盖不全**（L295）

名望(1/10)/财富(2/11)/精神(9/12)——D9 L10 落 3/4/5/6/7/8 宫时无规则。

**#6 "格局强 / Phase2高 / D9质检降级"均无阈值**（L273, L292-L293）

- 步骤 A"Phase2高→以格局为主"是终局决策第一杠杆，但"高"没有判据（格局数量？参与星 Shadbala？）。
- STEP 0"D9 质检降级"同样未定义何为降级。
- 关键原则3"格局优先"继承了同一问题。

**#7 "D9数据 10/10准确度"是硬编码断言**（L241）

data_contract.md 校验结果 #11 是逐盘的"D9 公式交叉 ✅/❌"。career 不检查该字段就宣称"公式验证过、10/10 准确"；非 calc 路径或校验❌的盘该断言失真。

**#8 Phase 1 的 10宫 SAV 引用双重问题**（L162）

- L162 写"SAV表"而非 L123 铁规要求的"宫位映射表"，可能诱导读「原始值（按星座）」表。
- 未带 >32/<20 极端值门槛（house_framework 统一规定仅极端值可提及展示）。

**#9 术语漂移**

- L188 "土星/火星/**计都刑克**"——"刑克"是西占 square 语系，体系已废 orb 相位，应统一为 graha drishti 口径。
- L174 用"罗睺"、L188 用"计都"，与其余 skill 统一英文行星名的记法不一致。

**#10 证据清单两处不一致**

- L64 反确认偏误#1 = "L10+AmK+格局+D10+强星+D9验证"。
- L357 关键原则#8 = "L10+AmK+格局+D10+强星"（漏 D9）。
- "唯一依据"清单应严格同源。

### 附带发现（属 core/reader 层，影响 career 消费）

formatter.py 实际输出的「结构格局预扫」「格局关系类·互视/互溶」「功能身份 primary_role」段，在 data_contract.md 中均未记载——契约文档落后于生成端，下游按契约找字段会扑空。

---

## 第二轮：跨 Skill 契约引用核查（4 条新发现 + 1 处修正）

### 新发现

**#11 Phase 1 的 Shadbala 字段定位错误**（L160）

写"L10 Shadbala → structured_data 预分析·Shadbala排名"，但按 data_contract.md L116-119，Shadbala 在「量化数据」节，不在「预分析」节。"预分析"节只有行星尊贵度 / Graha Drishti / 宫主表。模型按"预分析·Shadbala排名"去找会扑空或串节。

**#12 Phase 1 步骤3 的"互容"无数据源，仍会导向自推**（L168）

步骤3 写"检查…互容(Parivartana) 和紧密相位（读预分析「Graha Drishti」表 + 行星落宫）"。但互溶(parivartana)不在 Graha Drishti 表里——它定义在 structured_data「格局关系类 · 互溶对」表。既然 Phase 2 的互视/互溶该读这张表，Phase 1 的互容却指到 Graha Drishti 表，模型只能自推互换。这和 #1 同根但位置不同（Phase 1 vs Phase 2）。

**#13 Q&A 时机追问缺 core 的"日期失效检查"硬性首步**（L340）

core 的 qa_rules.md L60-63 规定：回答任何时机/运势类问题前，必须先以今天日期重定位 MD/AD/PD，禁止直接采信 structured_data 的"→当前"快照标记。career Q&A #4 只写"查 Dasha 时间轴推演"，未纳入日期失效检查。报告一旦滞后几天，career 的时机回答会用过期快照。（需确认 career 是否继承 core 的 qa_rules——若有意独立，应显式声明；否则是缺口。）

**#14 VRY 的"孤立性判定"整段缺失**（L211）

career 写 VRY"6/8/12宫主互飞"即止。但 p1_p12.md L211-231 明确 VRY 除结构外必须做"孤立性判定"（与吉宫主同宫距离 >10°/5°/1° 三档 → 有效/稀释/失效），并要求 1宫主 Shadbala≥100% 才判"逆境崛起"，否则降级"勉强求生"。career 既违反"读预扫表"，又把强度评估全丢掉了，会误报 VRY。

### 修正第一轮 #8 表述

第一轮 #8 把 Phase 1 的 SAV 问题只说成"未带极端值门槛"。复查发现更准确的是**双重问题**：① L162 写"SAV表"而非 L123 铁规要求的"宫位映射表"；② 未带 >32/<20 极端值门槛。

### 优先级重排

#1（互视自推）> #12（互容同根）> #14（VRY 孤立性）> #2（orb 矛盾）> #11（字段定位）> #13（日期失效首步）> 其余。

---

## 第三轮：版本治理 / 计算端根因 / 数据指针 / 领域准确性 / i18n（8 条新发现）

> 额外动作：跑 parity 脚本、读 rule_index.json、比对 anchored 与 career 副本、grep 计算端注释。

parity 脚本输出：`[OK] 8 skills match across Antigravity, Claude Code, and Codex.` 版本同步良好。

### 最重要新发现

**#15 Phase 3 整段缺失 D9 分盘边界审计**（L240-L254）

house_framework L10-13「分盘输入稳定性先决条件」明令：**任何** D9 落宫/分盘宫主判断都先读 structured_data 分盘边界审计，边界敏感不得沿单点 Lagna 下定论。career 对 D10（L183）、D4（L230）都写了"可信度⚠️→措辞留余地"，唯独以 D9 为主体的 Phase 3（灵魂舞台=D9 第10宫、职业人格=D9 上升、最终果实、Karakamsha 全在 D9 上）**没有任何边界检查步骤**。而 D9 Lagna 恰恰是全部分盘中对出生时间最敏感的（约 13 分钟换座）。且 L241"公式验证过，10/10准确度"把"计算正确性"与"输入稳定性"混为一谈——data_contract 明确这"是两项不同状态"。Phase 3 建立在全场最不稳定的分盘上却唯独不做稳定性检查。

**#16 career #1 冲突的根因在计算端——生态系统级矛盾，不止 career 一处**

- formatter.py L279-281 Graha Drishti 注释："P10/**格局互视**读本表、禁手推"
- data_contract.md L233 Graha Drishti 注释："P10/**格局互视**/rectifier 第3层读本表、禁手推"
- yogas.md L6："❌禁自己从 Graha Drishti 表判双向——读「互视对」表"
- formatter.py L344-350 实际输出独立的「格局关系类·互视/互溶」段

即：**formatter 过时注释、data_contract 过时注释、career 三处指向 Graha Drishti；yogas.md + formatter 新段指向互视对表**。career 是被过时注释误导的受害者。只修 career 不修这两处注释，下一个下游（rectifier/love）还会踩同一个坑。

### 版本治理角度

**#17 career 的"逐字受控副本"已漂移，且不受锚定系统管理**

- core SKILL.md L280-282（与 build/anchored 锚点逐字一致）的 SAV 铁规带例句 `"1宫(Sc)SAV=33" "7宫(Ta)SAV=28"` + "→ 用户可拿星座缩写去原始表交叉验证"行。
- career L123-124 例句是 `"10宫(Le)SAV=30" "2宫(Sg)SAV=33"`，且缺交叉验证行。
- build/anchored 只锚定 core 的文件，career/love/synastry 的副本**不在锚定索引里**（grep 确认 rule_index.json 无任何 career 条目）。
- parity 脚本只查三端同 skill 同步，不查跨 skill 受控副本。副本一致性纯靠人肉。
- love L118 同样缺例句。

### 数据指针角度（错位引用集群）

**#18 Vargottama 两处指错位置**

- L217："Vargottama → 从预分析尊贵度读取"
- L247："从预分析读取"
- 但 formatter L262-263 实际输出的预分析尊贵度表只有 5 列，**没有 Vargottama**——它只在 D9 表（formatter L397）。

**#19 焦伤指错位置**

- L218："逆行/焦伤 → 从行星位置读取"
- 行星位置表只有"逆行"列；燃烧在校验结果 6b。
- Phase 1 L186 的 Combust 同样无数据源指引。

（附带：data_contract 定义尊贵度表 7 列（含自然/临时关系），formatter 实际输出 5 列——契约与实现漂移，影响所有读"预分析·尊贵度"的引用。）

### 领域准确性角度

**#20 AmK 无条件列为"强点"，无 D1 强度检查**

- L216 直接把 AmK 列入强点。
- AmK 落陷+弱 Shadbala 时仍是"强点"，且直接进入"强星连接哪个宫→变现路径"判定（L220-223）——弱 AmK 会把变现路径带偏。
- Phase 3 武器压力测试只测 D9，不补 D1 强度。
- Jaimini 里 AmK 是"职务"不是"力量"，方向可看它，"强点/强星"定位需要强度前提。

**#21 STEP 4 示例自相矛盾 + 违反 Shadbala 引用纪律**

- L301 示例引 `"Shadbala 104%"` 作为"正面3/负面0"的推导依据——但按 house_framework 条件，104% 既不满足正面#3（≥120%）也不触发负面#4（<100%），是无关证据。
- 且 data_contract 明令下游引用"以排序和强弱分级为准，**避免引用具体数值**"（PyJHora 有 1-2 rupas 系统偏差，104% 是假精度）。
- SKILL.md 的示范本身在教模型违规。

### i18n 层角度

**#22 ja 层定义了主工作流不存在的 intake**

- 主 SKILL 无任何 intake 步骤，"核心关切"（反确认偏误#4）无采集机制且 user_context.md 被禁读。
- 但 ja-career.md L39-47 有完整 intake 措辞 + "現実の選択肢への当てはめ"渲染节。
- 日文用户被问结构化 intake、被映射到现实选项；中/英文用户无此流程。
- ja 层声明"never changes the workflow"，实际为一个不存在的步骤定义了行为，构成跨语言行为不对称。
- intake 数据的存放位置及其与 user_context.md 禁令的关系也未说明。

### 附带小问题

- career_phase\*.md 的输出目录未定义，而 Q&A 文件指定"工作目录/parts/"——产物位置不对称。
- Phase 3 大量引用 D9 却不像 Phase 1/2 那样内置线 A/线 B 标注指引，仅靠全局铁律兜底。

---

## 三轮汇总优先级

| 级别 | 条目 | 类型 |
|------|------|------|
| **立即修** | #15 D9 边界审计缺失 | 流程漏步 |
| **立即修** | #16+#1+#12 互视/互容口径（含 formatter/data_contract 过时注释） | 根因冲突 |
| **立即修** | #14 VRY 孤立性 | 领域完整性 |
| **应修** | #2 orb 矛盾 | 规则冲突 |
| **应修** | #18/#19/#11 数据指针错位 | 数据契约 |
| **应修** | #21 示例违规 | 示范违规 |
| **应修** | #20 AmK 强度前提 | 领域准确性 |
| **应修** | #13 日期失效首步 | 流程漏步 |
| **建议** | #17 副本纳入锚定 | 版本治理 |
| **建议** | #22/#9 i18n 与术语 | 一致性 |
| **建议** | #3-#6 判据定义 | 可操作性 |
| **建议** | #7/#8/#10 其余 | 契约漂移 |

---

## 修复范围预估

- vedic-career/SKILL.md × 3 份（antigravity / claude-code / codex）
- vedic-calculator/scripts/formatter.py × 1（更新 Graha Drishti 注释）
- vedic-reader/resources/data_contract.md × 1（更新 Graha Drishti 注释 + 补结构格局预扫 / 互视互溶 / 功能身份段）
- 可选：build/anchored/rule_index.json 加入 career 副本锚定
