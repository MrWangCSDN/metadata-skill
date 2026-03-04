---
name: metadata-composite-types
description: 处理基于 XML 的复合类型元数据文件（*.c_schema.xml）的创建、修改和删除。支持根据领域自动生成 schema 结构、complexType 定义、element 字段，集成 dict-mcp-server 查询字段元数据，处理复合类型间引用。触发场景：创建/修改/删除复合类型、复合对象、c_schema.xml 文件。
---

# 复合类型元数据（c_schema.xml）

处理基于 XML 格式的复合类型元数据文件，文件命名规则：`{SchemaId}.c_schema.xml`。

## 核心工作流

### 模式 1：创建新复合类型文件

触发关键词：「新建」/「创建」+ 复合类型/复合对象

**处理步骤**：

1. **确定 SchemaId** — 全局唯一，同时作为文件名前缀（如 `FtAcctgType`）
2. **确定领域、模块和包路径** — 根据领域映射 resources/beans 模块和包路径（详见 [references/package-module-mapping.md](references/package-module-mapping.md)）
3. **确定文件路径** — 未指定子目录时，默认存放在 `{模块}/src/main/resources/type/` 下；指定子目录时在该目录下创建子目录（详见下方「文件路径规则」）
4. **定义 complexType 列表** — 每个复合对象一个 `complexType`
5. **调用 MCP 查询字段** — 使用 `dict-mcp-server.getDictDefByLongNameList` 批量查询所有 element 的字段元数据
6. **过滤未贯标字段** — MCP 返回 null 的字段**强制不写入 XML**，统一提示（⚠️ 强制规则）
7. **处理复合类型引用字段** — 此类字段不查 MCP，`type` 使用 `{SchemaId}.{ComplexTypeId}` 格式，无 `ref` 属性
8. **生成 XML** — 按标准模板生成（属性单行，同级无空行，子标签缩进 4 空格）
9. **保存文件** — 保存至确定的目标路径，输出文件路径和 package 信息

### 模式 2：修改现有复合类型文件

触发关键词：「修改」+ complexType 名称 / SchemaId

**处理步骤**：

1. **定位文件** — 查找对应 `{SchemaId}.c_schema.xml`
2. **读取原文件** — 保留 `schema` 标签所有属性
3. **调用 MCP** — 查询新增字段的元数据
4. **更新指定 complexType** — 仅修改目标 `complexType` 内的 `element` 列表，不影响其他 complexType
5. **保存** — 保持 XML 格式一致

### 模式 3：删除

触发关键词：「删除」+ complexType 名称 / SchemaId

- 删除整个 `complexType` 节点，或删除指定 `element`
- 若整个文件无 `complexType`，询问是否删除文件

---

## 文件路径规则

> ⛔ **强制决策逻辑**：生成文件前必须先执行以下判断，不得跳过。

### 判断流程

```
用户是否指定子目录？
│
├─ 否（未提及子目录）→ 【默认路径】直接放在 type/ 根目录下
│                       package = 领域基础包（不追加任何子路径）
│
└─ 是（明确说了子目录）→ 【子目录路径】放在 type/{子目录}/ 下
                         package = 领域基础包 + .{子目录用.分隔}
```

### 默认路径（⛔ 未指定子目录时强制使用）

> **用户未提及子目录 → 文件直接创建在 `type/` 根目录，package 不追加任何子路径。**

| 领域 | 文件路径 | schema package |
|------|---------|----------------|
| 存款 | `dept-resources/src/main/resources/type/{SchemaId}.c_schema.xml` | `com.spdb.ccbs.dept.resources.type` |
| 贷款 | `loan-resources/src/main/resources/type/{SchemaId}.c_schema.xml` | `com.spdb.ccbs.loan.resources.type` |
| 结算 | `sett-resources/src/main/resources/type/{SchemaId}.c_schema.xml` | `com.spdb.ccbs.sett.resources.type` |
| 平台公共 | `comm-resources/src/main/resources/type/{SchemaId}.c_schema.xml` | `com.spdb.ccbs.comm.resources.type` |

**示例（贷款领域，无子目录）**：
```
文件路径：loan-resources/src/main/resources/type/LoanApplType.c_schema.xml
package： com.spdb.ccbs.loan.resources.type
```

### 指定子目录

> 用户明确指定子目录时，文件创建在 `type/{子目录}/` 下，package **同步追加**子目录。

```
文件路径：{xxx-resources}/src/main/resources/type/{子目录}/{SchemaId}.c_schema.xml
package： {领域基础包}.{子目录（/改为.）}
```

**示例（贷款领域，子目录 `ft/repay`）**：
```
文件路径：loan-resources/src/main/resources/type/ft/repay/FtAcctgType.c_schema.xml
package： com.spdb.ccbs.loan.resources.type.ft.repay
```

**路径转换规则**：文件路径 `/` → package 中的 `.`（如 `ft/repay` → `ft.repay`）

详细映射表见 [references/package-module-mapping.md](references/package-module-mapping.md)

---

## schema 标签属性

| 属性 | 说明 | 固定/来源 |
|------|------|---------|
| `xmlns:xsi` | — | 固定 `http://www.w3.org/2001/XMLSchema-instance` |
| `id` | 文件唯一标识，同文件名前缀 | 用户提供，全局唯一 |
| `package` | Java 包路径 | 根据领域自动映射 |
| `longname` | 复合类型文件中文名 | 用户提供 |
| `classgen` | — | 固定 `auto` |
| `xsi:noNamespaceSchemaLocation` | — | 固定 `ltts-model.xsd` |

---

## complexType 标签属性

| 属性 | 说明 | 默认值 |
|------|------|--------|
| `id` | 对象英文名（生成 Java 类名），文件内唯一 | 用户提供 |
| `longname` | 对象中文名 | 用户提供 |
| `abstract` | — | `false` |
| `dict` | — | `false` |
| `introduct` | — | `false` |
| `localName` | — | `""` |
| `extension` | — | `""` |
| `tags` | — | `""` |

---

## element 字段属性

| 属性 | 来源 | 默认值 |
|------|------|--------|
| `id` | MCP 返回 | — |
| `longname` | MCP 返回 | — |
| `type` | MCP 返回 / 复合类型引用 | — |
| `required` | 用户输入，未指定默认 | `false` |
| `multi` | 用户输入（集合为 true） | `false` |
| `ref` | MCP 返回（复合类型引用字段无 ref） | — |
| `range` | — | `false` |
| `array` | — | `false` |
| `final` | — | `false` |
| `override` | — | `false` |
| `allowSubType` | — | `true` |
| `key` | — | `false` |

> 历史文件中可能出现 `elemment`（拼写差异），新增内容统一使用 `element`。

---

## MCP 服务集成

**服务名**：`dict-mcp-server`  **方法**：`getDictDefByLongNameList`

> ⛔ **强制规则：MCP 返回 null 的字段禁止写入 XML。**
>
> - null 字段不生成任何 `<element>` 标签
> - **查询结果必须在工作台展示**（见下方「查询结果展示规范」）

### 查询结果展示规范

每次调用 MCP 和脚本后，**必须在工作台输出查询过程和结果**，格式如下：

**MCP 查询结果（逐字段展示）**：
```
📋 MCP 字段查询结果：
  ✅ 交易对方行号  →  type=MBaseType.XXX  ref=MDict.X.jyDfhh
  ✅ 币种代码      →  type=MBaseType.U_BI_ZHONG_DAI_MA  ref=MDict.C.crcyCd
  ❌ 钞汇代码      →  未贯标（MCP 返回 null），已跳过
```

**复合对象脚本搜索结果（逐个展示）**：
```
🔍 复合对象引用搜索结果：
  ✅ [保函收到撤销索偿]  →  GuaranteeType.GrntRcvCxlClmPojo
  ❌ [结算信息输出]       →  未找到匹配的 c_schema.xml，已跳过
```

**最终汇总提示（生成 XML 后必须输出）**：
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  以下字段未写入 XML，请确认后补充：

【未贯标字段】（MCP 返回 null，需完成贯标后重新执行）：
  1. 钞汇代码

【复合对象引用未找到】（需确认文件是否已创建）：
  1. [结算信息输出]

💡 完成上述问题后，可重新执行以补充这些字段。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

> 若没有未贯标字段且所有复合对象均找到，则只输出「✅ 所有字段均已写入 XML」，不显示汇总框。

---

## 复合类型引用规则

### 识别方式

> ⛔ **推荐写法**：用 `[中文名]` 中括号包裹复合对象名，简洁直观。旧写法 `（复合对象）` 保持兼容。

**完整语法对照表**（大模型按此表逐行匹配解析）：

```
输入写法                                      → 解析结果
──────────────────────────────────────────────────────────────────
[保函收到撤销索偿]                            → 复合引用，单值，id 自动生成
[保函收到撤销索偿]  多值                      → 复合引用，multi=true，id 末尾加 List
[保函收到撤销索偿]  必输                      → 复合引用，required=true
[保函收到撤销索偿]  多值  必输               → 复合引用，multi=true，required=true，id 末尾加 List
lstXxx [保函收到撤销索偿]                     → 复合引用，id = lstXxx（用户指定，不追加 List）
lstXxx [保函收到撤销索偿]  多值  必输        → 复合引用，id = lstXxx，multi=true，required=true
保函收到撤销索偿（复合对象）                  → 兼容旧写法，等同于 [保函收到撤销索偿]
保函收到撤销索偿（复合对象）  多值            → 兼容旧写法，multi=true
普通字段中文名                                → 普通字段，查 MCP
普通字段中文名  必输                          → 普通字段，查 MCP，required=true
普通字段中文名  多值                          → 普通字段，查 MCP，multi=true
```

> **关键判断**：一行中有 `[...]` 或 `（复合对象）` → 复合引用；否则 → 普通字段。

**解析规则**：`[中文名]` 或 `xxx（复合对象）` 均视为复合类型引用；中括号前若有英文名则作为 `id`，否则按 id 生成规则处理。

### 处理流程

> ⛔ **强制流程：引用复合类型时必须调用 `scripts/find_composite_ref.py` 脚本搜索，不得自行猜测 type 值。**

1. **调用脚本搜索** — 执行 `scripts/find_composite_ref.py` 脚本，传入搜索目录和中文名
2. **解析脚本返回的 JSON** — 从结果中提取 `type`（已组合好的 `{schemaId}.{complexTypeId}`）
3. **找到（`found: true`）** → 使用脚本返回的 `type` 生成 element，**不填写 `ref`**，不查 MCP
4. **未找到（`found: false`）** → **强制不写入 XML**，在反馈中提示「{字段中文名}（复合对象）未找到，已跳过」
5. **多个匹配（`multiple: true`）** → 列出所有候选，询问用户选择哪一个

### 脚本调用方式

> ⛔ **路径规则**：脚本固定在 `.speedstudio` 目录下，必须使用**绝对路径**，第一个参数必须是脚本文件完整路径（以 `find_composite_ref.py` 结尾），**不能**只传目录。Python 命令**只能使用 `python xxx`**，不得使用其他命令。

**脚本绝对路径**：`{工作区根目录}/.speedstudio/skills/metadata-composite-types/scripts/find_composite_ref.py`

**搜索目录绝对路径**：`{工作区根目录}/{模块相对路径}`

```bash
# 按中文名搜索
python "{工作区根目录}/.speedstudio/skills/metadata-composite-types/scripts/find_composite_ref.py" "{工作区根目录}/loan-resources/src/main/resources/type" 保函收到撤销索偿

# 按英文 id 搜索
python "{工作区根目录}/.speedstudio/skills/metadata-composite-types/scripts/find_composite_ref.py" "{工作区根目录}/loan-resources/src/main/resources/type" "" --id ObCstSetl
```

**`<search_dir>` 与领域对应**：

| 领域 | 搜索目录绝对路径 |
|------|----------------|
| 存款 | `{工作区根目录}/dept-resources/src/main/resources/type` |
| 贷款 | `{工作区根目录}/loan-resources/src/main/resources/type` |
| 结算 | `{工作区根目录}/sett-resources/src/main/resources/type` |
| 平台公共 | `{工作区根目录}/comm-resources/src/main/resources/type` |

> 脚本会**递归搜索**子目录。工作区根目录可通过当前打开文件路径推断（如 `D:\code\ccbs-loan-impl`）。

**脚本返回示例**：

```json
// 找到时
{
  "found": true,
  "schemaId": "GuaranteeType",
  "complexTypeId": "GrntRcvCxlClmPojo",
  "filePath": "loan-resources/src/main/resources/type/GuaranteeType.c_schema.xml",
  "type": "GuaranteeType.GrntRcvCxlClmPojo"
}

// 未找到时
{
  "found": false,
  "message": "在 loan-resources/src/main/resources/type 下未找到 longname='保函收到撤销索偿' 的 complexType（共扫描 5 个文件）"
}
```

### id 生成规则

> ⛔ **强制规则：引用复合对象的 id 必须按以下逻辑确定。**

| 用户输入情况 | id 取值 | 示例 |
|------------|---------|------|
| 用户提供了英文字段名 | **直接使用用户提供的英文名** | 输入 `lstObCstSetlOut 结算信息输出（复合对象）` → id = `lstObCstSetlOut` |
| 用户未提供英文字段名 | **根据中文名生成拼音首字母驼峰** | 输入 `保函收到撤销索偿（复合对象）` → id = `grntRcvCxlClmPojo`（参考 complexType id 小驼峰形式）|
| 多值（multi=true）且无英文名 | 生成的 id 末尾追加 `List` | `grntRcvCxlClmPojoList` |
| 多值（multi=true）且有英文名 | 直接使用用户提供的英文名（不自动追加 List） | `lstObCstSetlOut` |

> **说明**：无英文名时，优先参考找到的 complexType 的 `id`，将其首字母改为小写作为引用字段 id（单值）；多值时追加 `List` 后缀。

### longname 规则

- `longname` = 用户输入的中文名（括号前的部分）
- 如 `保函收到撤销索偿（复合对象）` → `longname="保函收到撤销索偿"`
- 如 `lstObCstSetlOut 结算信息输出（复合对象）` → `longname="结算信息输出"`

### multi 属性（单值 vs 多值）

| 描述 | multi 值 | 含义 |
|------|---------|------|
| 未标注「多值」 | `false` | 单个对象 |
| 标注「多值」 | `true` | 对象数组（List） |

普通字段同理：标注「多值」时 `multi="true"`，否则默认 `false`。

### required 属性

| 描述 | required 值 |
|------|------------|
| 未标注「必输」 | `false` |
| 标注「必输」 | `true` |

### element 属性规则

- `type` = 从找到的文件中读取：`{schema标签的id}.{匹配的complexType的id}`
- `id` = 用户提供的英文名；未提供则参考 complexType id 小驼峰（多值追加 List）
- `longname` = 用户输入的中文名（括号前部分）
- `required` = 用户标注「必输」时 `true`，否则 `false`
- `multi` = 用户标注「多值」时 `true`，否则 `false`
- `ref` 属性**不填写**
- 其余属性固定默认值，**所有属性必须在同一行**

```xml
<!-- 单值引用（无英文名，参考 complexType id 生成） -->
<element id="grntRcvCxlClmPojo" longname="保函收到撤销索偿" type="GuaranteeType.GrntRcvCxlClmPojo" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false"/>

<!-- 多值引用（无英文名，追加 List） -->
<element id="grntRcvCxlClmPojoList" longname="保函收到撤销索偿" type="GuaranteeType.GrntRcvCxlClmPojo" required="false" multi="true" range="false" array="false" final="false" override="false" allowSubType="true" key="false"/>

<!-- 用户提供英文名的引用 -->
<element id="lstObCstSetlOut" longname="结算信息输出" type="ObDealTpMgmtType.ObCstSetl" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false"/>
```

### 反馈格式

> 生成 XML 后，必须按「MCP 查询结果展示规范」在工作台输出完整汇总（见上方「查询结果展示规范」）。所有未写入字段（未贯标 + 引用未找到）必须在汇总框中一并提示。

---

## 标准 XML 模板

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="FtAcctgType" package="com.spdb.ccbs.loan.resources.type.ft.repay" longname="福费延还款复合类型" classgen="auto" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <complexType abstract="false" dict="false" id="FtAcctRepayChkInPojo" introduct="false" localName="" longname="福费延还款校验输入" extension="" tags="">
        <element id="fRFTGDueBillCd" longname="福费延借据编码" type="MBaseType.U_DAI_KUAN_JIE_JU_BIAN_MA" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.F.fRFTGDueBillCd"/>
        <element id="fncgBsnID" longname="融资业务编码" type="MBaseType.U_RONG_ZI_YE_WU_BIAN_MA" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.F.fncgBsnID"/>
    </complexType>
    <complexType abstract="false" dict="false" id="FtAcctRepayChkOutPojo" introduct="false" localName="" longname="福费延还款校验输出" extension="" tags="">
        <element id="fRFTGDueBillCd" longname="福费延借据编码" type="MBaseType.U_DAI_KUAN_JIE_JU_BIAN_MA" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.F.fRFTGDueBillCd"/>
        <element id="fncgBsnID" longname="融资业务编码" type="MBaseType.U_RONG_ZI_YE_WU_BIAN_MA" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.F.fncgBsnID"/>
    </complexType>
</schema>
```

**格式强制规则**：

| 规则 | 说明 | 强制等级 |
|------|------|---------|
| ⛔ 属性不换行 | **所有标签**（`schema`、`complexType`、`element`）的属性必须写在同一行，绝对不允许换行 | 强制 |
| ⛔ 同级无空行 | 同级 `element` 之间、同级 `complexType` 之间**不允许有空行** | 强制 |
| ⛔ 禁用 Tab | 只使用空格缩进，禁止任何 Tab 字符 | 强制 |
| 子标签缩进 | 子标签相对父标签缩进 **4 个空格**（`complexType` = 4格，`element` = 8格） | 必须 |
| 自闭合 | `element` 使用 `/>` 自闭合结尾 | 必须 |

每个 `element` 属性顺序：`id → longname → type → required → multi → range → array → final → override → allowSubType → key → [ref]`

完整模板说明见 [references/xml-template.md](references/xml-template.md)

---

## 执行清单

### 创建流程

- [ ] 确认 SchemaId（全局唯一，与文件名前缀一致）
- [ ] 确定领域，映射 resources 模块和基础包路径
- [ ] ⛔ **路径判断**：用户是否指定子目录？
  - 否 → 文件路径 = `{模块}/src/main/resources/type/{SchemaId}.c_schema.xml`，package = 领域基础包（不追加子路径）
  - 是 → 文件路径追加子目录，package 同步追加（`/` 转 `.`）
- [ ] 整理 complexType 列表（每个对象的 id、longname、字段列表）
- [ ] 区分三类字段：普通字段（查 MCP）、复合类型引用字段（搜索 c_schema.xml）、多值字段（multi=true）
- [ ] 调用 `dict-mcp-server.getDictDefByLongNameList` 批量查询普通字段
- [ ] ⛔ **强制过滤**：MCP 返回 null 的字段不写入 XML
- [ ] ⛔ **复合类型引用**：对每个 `[中文名]` 或 `xxx（复合对象）`，调用 `python "{工作区根目录}/.speedstudio/skills/metadata-composite-types/scripts/find_composite_ref.py" "{搜索目录绝对路径}" 中文名`；在工作台展示搜索结果；从返回 JSON 的 `type` 字段取值；找不到则不写入 XML；多个匹配则询问用户
- [ ] ⛔ **引用字段 id 确定**：用户提供英文名 → 直接用；未提供 → 取脚本返回的 `complexTypeId` 首字母小写；多值且无英文名 → 末尾追加 `List`
- [ ] 多值字段：标注「多值」的字段 `multi="true"`，否则 `multi="false"`
- [ ] 生成 XML：⛔ 所有标签属性必须在同一行，不换行；同级标签无空行；子标签缩进 4 空格
- [ ] 保存至确定的目标路径
- [ ] ⛔ **展示查询结果**：在工作台输出 MCP 查询结果（每个字段 ✅/❌）和脚本搜索结果（每个复合引用 ✅/❌）
- [ ] ⛔ **汇总提示**：生成 XML 后，在工作台输出汇总框，列出所有未写入字段（未贯标 + 引用未找到）；若全部写入则输出「✅ 所有字段均已写入 XML」

### 修改流程

- [ ] 定位 `{SchemaId}.c_schema.xml` 文件
- [ ] 读取原文件，保留 `schema` 标签属性
- [ ] 调用 MCP 查询新增字段
- [ ] 仅更新目标 `complexType` 内容，不影响其他 complexType

---

## 参考资源

- [scripts/find_composite_ref.py](scripts/find_composite_ref.py) — 搜索 c_schema.xml 并解析复合类型引用的脚本（⛔ 引用复合对象时必须调用）
- [references/package-module-mapping.md](references/package-module-mapping.md) — 领域到包路径/模块映射
- [references/xml-template.md](references/xml-template.md) — XML 完整模板说明
- [references/examples.md](references/examples.md) — 完整创建/修改/引用示例
