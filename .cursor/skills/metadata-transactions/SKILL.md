---
name: metadata-transactions
description: 处理基于 XML 的 flowtran 联机交易元数据模型的创建和修改。支持根据交易码（TC/TD/TG/TY 格式）、输入输出字段自动生成完整的 .flowtrans.xml 文件，包括数组字段处理（fields 标签）、属性接口（property 标签）、复合类型引用（[xxx] 语法）、流程编排（flow 标签，支持编排 pbs 基础服务、pcs 组合服务和方法节点）、dict-mcp-server 服务集成进行字段元数据查询、自动包路径生成和模块路径定位。触发场景：新建/创建/修改 flowtran 联机交易、TC/TD/TG/TY 开头的交易码、.flowtrans.xml 文件操作、流程编排/flow 编排。
---

# Flowtran 联机交易元数据

处理基于 XML 格式的 flowtran 联机交易元数据，支持**创建**和**修改**两种模式。

## 核心工作流

### 模式 1：创建新交易

触发关键词：「新建」/「创建」+ 交易码

**处理步骤**：

1. **获取工作空间绝对路径** — 获取当前打开项目的工作空间根目录绝对路径，**在工作台展示**：`📂 当前工作空间：{绝对路径}`
2. **验证交易码** — 格式 `T+C/D/G/Y+4位数字`（详见 [references/transaction-id-rules.md](references/transaction-id-rules.md)）
3. **确定目标路径** — 根据交易码前缀映射工程、模块和包路径，拼接完整绝对路径：`{工作空间}/{工程}/{模块}/src/main/resources/trans/{子目录}/{交易码}.flowtrans.xml`
4. **检查文件存在性** — 在目标绝对路径下查找 `.flowtrans.xml`，已存在则自动切换为修改模式
5. **处理子目录** — 检查是否指定子目录，追加到包路径和文件路径
6. **调用 MCP 查询字段** — 使用 `dict-mcp-server.getDictDefByLongNameList` 批量查询（详见 [references/mcp-integration.md](references/mcp-integration.md)）
7. **过滤未贯标字段** — MCP 返回 null 的字段**强制不写入 XML**，收集后统一提示用户（⚠️ 强制规则，不可跳过）
8. **处理流程编排**（如有「流程编排：」关键词）— 解析服务节点和方法节点，对服务节点调用 `find_services_ref.py` 脚本搜索，查不到则调用 MCP `queryServiceDetail`，仍查不到则跳过并提示用户
9. **生成 XML** — 仅对已贯标字段生成标签，按标准模板生成（属性单行，标签间无空行，4 空格缩进）；flow 标签位于 interface 之后
10. **保存并反馈** — 使用完整绝对路径保存文件，反馈中展示完整文件路径和被排除的字段/未找到的服务

### 模式 2：修改现有交易

触发关键词：「修改」+ 交易码

**处理步骤**：

1. **定位文件** — 在 `trans` 目录（含子目录）下查找已有 `.flowtrans.xml`
2. **读取原文件** — 保留 `flowtran`/`description`/`interface`/`flow` 标签的所有属性
3. **调用 MCP** — 查询新增字段的元数据
4. **仅覆盖 input/output** — 更新 `interface` 内的 input 和 output 标签内容
5. **处理流程编排**（如有）— 新增或更新 `flow` 标签内容，搜索服务引用
6. **保存** — 其他标签和属性保持不变

---

## 交易码规则

格式：`T + (C/D/G/Y) + 4位数字`（共 6 位，全大写）

| 前缀 | 领域 | 有效范围 | 示例 |
|------|------|---------|------|
| TC | 存款 | TC021–TC999 | TC100 |
| TD | 贷款 | TD001–TD499 | TD250 |
| TG | 结算 | TG001–TG499 | TG350 |
| TY | 平台公共 | TY001–TY999 | TY291 |

- 交易码全局唯一，文件名为 `{交易码}.flowtrans.xml`（注意扩展名是 `.flowtrans.xml`）
- 详细验证规则见 [references/transaction-id-rules.md](references/transaction-id-rules.md)

---

## 文件创建路径规则

> ⛔ **强制规则**：创建 XML 文件时，**必须使用当前工作空间的绝对路径**，不得使用相对路径。

### 路径构成顺序

创建文件前，**必须先获取并展示当前工作空间绝对路径**，然后按以下顺序逐层拼接：

```
{工作空间绝对路径}/{工程}/{模块}/src/main/resources/trans/{子目录}/{交易码}.flowtrans.xml
```

| 层级 | 说明 | 示例 |
|------|------|------|
| 1. 工作空间 | 当前打开项目的根目录绝对路径 | `/Users/xxx/Desktop/myproject` |
| 2. 工程 | 按领域映射的工程目录 | `ccbs-comm-impl` |
| 3. 模块 | 按领域映射的模块目录 | `comm-pbf` |
| 4. 资源路径 | 固定路径 | `src/main/resources/trans` |
| 5. 子目录 | 用户指定时追加，未指定则无 | `chrg` |
| 6. 文件名 | 交易码 + 扩展名 | `TY291.flowtrans.xml` |

### 工程与模块映射

| 前缀 | 领域 | 工程 | 模块 | 包路径 |
|------|------|------|------|--------|
| TC | 存款 | ccbs-dept-impl | dept-pbf | com.spdb.ccbs.dept.pbf.trans |
| TD | 贷款 | ccbs-loan-impl | loan-pbf | com.spdb.ccbs.loan.pbf.trans |
| TG | 结算 | ccbs-sett-impl | sett-pbf | com.spdb.ccbs.sett.pbf.trans |
| TY | 平台公共 | ccbs-comm-impl | comm-pbf | com.spdb.ccbs.comm.pbf.trans |

### 完整路径示例

**无子目录**（TY291，工作空间 = `/Users/xxx/project`）：
```
/Users/xxx/project/ccbs-comm-impl/comm-pbf/src/main/resources/trans/TY291.flowtrans.xml
```

**有子目录 chrg**（TY291，工作空间 = `/Users/xxx/project`）：
```
/Users/xxx/project/ccbs-comm-impl/comm-pbf/src/main/resources/trans/chrg/TY291.flowtrans.xml
```

- `interface package` = `flowtran package` + `.intf`
- 指定子目录时，包路径和文件路径均追加子目录
- 详见 [references/package-module-mapping.md](references/package-module-mapping.md)

---

## MCP 服务集成

**服务名**：`dict-mcp-server`  **方法**：`getDictDefByLongNameList`

- 输入：字段中文名称数组，如 `["国家", "性别"]`
- 输出：`Map<中文名, 字段定义对象 | null>`，`null` 表示未贯标
- **调用时机**：创建或修改时，一次性批量查询所有字段

> ⛔ **强制规则：MCP 返回 null 的字段，禁止写入 XML。**
>
> - null 字段不生成任何 `<field>` 或 `<fields>` 标签
> - 即使数组（fields）中只有部分子字段为 null，整个数组仍按实际贯标字段生成；若数组内所有子字段均为 null，则整个 `<fields>` 标签也不写入
> - 生成完成后，在反馈中列出所有被排除的字段名，提示用户完成贯标后重新执行

详见 [references/mcp-integration.md](references/mcp-integration.md)

---

## 标准 XML 模板

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<flowtran xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="TY291" longname="收费明细文件批量查询" kind="auto" package="com.spdb.ccbs.comm.pbf.trans" txnMode="A" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <description><![CDATA[收费明细文件批量查询]]></description>
    <interface package="com.spdb.ccbs.comm.pbf.trans.intf">
        <input packMode="true">
            <field id="cst" type="MBaseType.U_GUO_JIA" required="false" multi="false" array="false" longname="国家" ref="MDict.C.cst"/>
        </input>
        <output asParm="true" packMode="true">
            <field id="cst" type="MBaseType.U_GUO_JIA" required="false" multi="false" array="false" longname="国家" ref="MDict.C.cst"/>
        </output>
        <property packMode="true">
            <field id="dkCxCkZhSrLst" type="LoanQueryType.DkCxCkZhSrIn" required="true" multi="true" longname="贷款查询存款账号输入列表"/>
            <field id="queryCount" type="MBaseType.U_JI_SHU" required="false" multi="false" array="false" longname="查询笔数" ref="MDict.Q.queryCount"/>
        </property>
    </interface>
    <flow>
        <service mappingToProperty="true" serviceName="IoCpInnerAcctInfoQryPbsSvtp.IoCpInnerAcctInfoQryPbsSvtp" id="IoCpInnerAcctInfoQryPbsSvtp" longname="内部户账户信息查询"/>
        <method method="beforeQryAcctInfo" id="beforeQryAcctInfo" longname="外调存款公共通用记账前处理" desc="外调存款公共通用记账前处理"/>
    </flow>
</flowtran>
```

**格式要点**：

| 规则 | 说明 |
|------|------|
| 属性单行 | 所有标签属性必须在一行内，不能换行 |
| 无空行 | 同级标签之间不要有空行 |
| 4空格缩进 | 每层级增加 4 个空格，禁用 Tab |
| kind | 固定为 `"auto"` |
| txnMode | 默认 `A`，只读查询用 `R` |
| output | `asParm="true"` 和 `packMode="true"` 均固定 |
| property | `packMode="true"` 固定；位于 output 之后（如有） |

缩进层级：`flowtran(0)` → `description/interface/flow(4)` → `input/output/property/service/method(8)` → `field(12)` → `fields内field(16)`

完整模板说明见 [references/xml-template.md](references/xml-template.md)

---

## 属性接口（property）

### 触发识别

用户输入中出现「属性接口：」关键词时，表示存在 `property` 标签。

**完整语法对照表**（大模型按此表逐行匹配解析）：

```
属性接口中的输入写法                          → 解析结果
──────────────────────────────────────────────────────────────────
[贷款查询存款账号输入列表]                    → 复合引用（中文检索），单值，id 自动生成，无 array/ref
[DkCxCkZhSrIn]                               → 复合引用（英文检索），单值，id 自动生成，无 array/ref
[贷款查询存款账号输入列表]  多值              → 复合引用，multi=true，id 末尾加 List
[贷款查询存款账号输入列表]  必输              → 复合引用，required=true
[贷款查询存款账号输入列表]  多值  必输        → 复合引用，multi=true，required=true，id 末尾加 List
lstXxx [贷款查询存款账号输入列表]             → 复合引用，id = lstXxx（用户指定，不追加 List）
lstXxx [DkCxCkZhSrIn]                        → 复合引用（英文检索），id = lstXxx
lstXxx [贷款查询存款账号输入列表]  多值  必输 → 复合引用，id = lstXxx，multi=true，required=true
查询笔数                                      → 普通字段，查 MCP，生成含 array/ref 的 field
查询笔数  必输                                → 普通字段，查 MCP，required=true
查询笔数  多值                                → 普通字段，查 MCP，multi=true
```

> **关键判断**：一行中有 `[...]` → 复合引用（中括号内含中文 → 按 longname 检索；纯英文 → 按 complexType id 检索）；否则 → 普通字段（查 MCP，有 array/ref）。

### 字段分类与处理规则

| 字段类型 | 识别方式 | 处理方式 | 生成格式 |
|---------|---------|---------|---------|
| 复合类型引用 | `[xxx]` 中括号（xxx 支持中文或英文） | 优先脚本搜索，查不到回退 MCP | 无 `array`、无 `ref` |
| 普通字段 | 普通中文名 | 调用 MCP 查询 | 同 input/output 格式 |

### 复合类型引用字段（[xxx] 语法）

> ⛔ **强制规则：`[xxx]` 引用必须通过搜索确认存在，不得自行猜测 type。**
>
> ⛔ **强制规则：搜索时必须严格使用 `[]` 中括号内的完整内容作为查询词，禁止对中括号内的内容做任何截取、拆分、翻译或改写。** 例如 `[贷款查询存款账号输入列表]`，查询词必须是 `贷款查询存款账号输入列表` 完整字符串；`[DkCxCkZhSrIn]`，查询词必须是 `DkCxCkZhSrIn` 完整字符串。

**`[xxx]` 支持中文和英文**：
- `[贷款查询存款账号输入列表]` → 中文，按 complexType 的 `longname` 精确匹配完整内容
- `[DkCxCkZhSrIn]` → 英文，按 complexType 的 `id` 精确匹配完整内容

**三步查询，逐步回退**：

1. **优先调用 `find_composite_ref.py` 脚本**（在工作空间下递归遍历所有 `*.c_schema.xml`）：
   ```bash
   python "{工作区根目录}/.speedstudio/skills/metadata-composite-types/scripts/find_composite_ref.py" "{工作区根目录}" 贷款查询存款账号输入列表
   ```
   ```bash
   python "{工作区根目录}/.speedstudio/skills/metadata-composite-types/scripts/find_composite_ref.py" "{工作区根目录}" DkCxCkZhSrIn
   ```
   - ⛔ 脚本参数必须是 `[]` 中括号内的**完整原文**，不得截取或改写
   - 脚本自动判断：包含中文字符 → 按 `longname` 匹配；纯英文 → 按 `complexType id` 匹配
   - 脚本内部已做去重（按 schemaId + complexTypeId）

2. **脚本查询不到时，调用 MCP 服务 `dict-mcp-server.queryComplexDetail`**：
   - ⛔ 输入参数必须是 `[]` 中括号内的**完整原文**，不得截取或改写
   - 返回复合类型定义信息（schemaId、complexTypeId、complexTypeLongname、type 等）
   - MCP 返回的数据同样需要去重（按 schemaId + complexTypeId）

3. **MCP 也查询不到时（⛔ 强制规则）**：
   - **XML 中不写入该 field**，该引用完全跳过
   - **立即在工作台输出**：`❌ [xxx] → 未找到匹配的复合类型，已跳过`
   - **生成 XML 后在汇总提示中统一列出**

**找到唯一匹配时**，生成（无 `array`、无 `ref` 属性）：
```xml
<field id="dkCxCkZhSrLst" type="LoanQueryType.DkCxCkZhSrIn" required="true" multi="true" longname="贷款查询存款账号输入列表"/>
```

**去重后仍有多个匹配时**：在工作台列出所有候选（展示 schemaId、complexTypeId、type），明确告知用户让其选择其中一个，用户选择后再继续生成。

```
🔍 复合对象引用搜索结果（property）：
  ⚠️ [贷款查询存款账号输入列表] → 找到 2 个匹配（已去重），请选择其中一个：
    1. LoanQueryType.DkCxCkZhSrIn（文件：ccbs-loan-impl/.../LoanQueryType.c_schema.xml）
    2. CommQueryType.DkCxCkZhSrIn（文件：ccbs-comm-impl/.../CommQueryType.c_schema.xml）
```

**未找到时的汇总提示**：
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  以下字段未写入 XML，请确认后补充：

【property 复合对象引用未找到】（需确认 c_schema.xml 是否已创建）：
  1. [贷款查询存款账号输入列表]

💡 确认文件已创建后，可重新执行以补充这些字段。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**id 生成规则**（与复合类型 skill 一致）：

| 用户输入 | id 取值 |
|---------|---------|
| 中括号前有英文名（`lstXxx [中文名]`） | 直接使用英文名 |
| 无英文名 | 脚本返回 complexTypeId 首字母改小写 |
| 无英文名 + 多值 | 首字母小写 + `List` 后缀 |

### 普通字段

与 input/output 中普通字段处理完全相同：调用 MCP，生成含 `array="false"` 和 `ref` 的完整 `field` 标签。

### 生成的 property 标签

```xml
<property packMode="true">
    <field id="dkCxCkZhSrLst" type="LoanQueryType.DkCxCkZhSrIn" required="true" multi="true" longname="贷款查询存款账号输入列表"/>
    <field id="dkCxGgZhScLst" type="LoanQueryType.DkCxGgZhSc" required="false" multi="false" longname="贷款查询公共账号输出列表"/>
    <field id="queryCount" type="MBaseType.U_JI_SHU" required="false" multi="false" array="false" longname="查询笔数" ref="MDict.Q.queryCount"/>
    <field id="avlBal" type="MBaseType.U_JIN_E" required="false" multi="false" array="false" longname="可用余额" ref="MDict.A.avlBal"/>
</property>
```

> property 标签位于 `output` 标签之后（如无 output 则紧接 input 之后）。

---

## 流程编排（flow）

### 概述

`flowtran` 标签下包含 `interface` 标签和 `flow` 标签。`flow` 标签用于流程编排，按顺序编排三种节点类型：

| 节点类型 | 标签 | 说明 |
|---------|------|------|
| pbs 基础服务 | `<service>` | 引用已有的 pbs 服务接口 |
| pcs 组合服务 | `<service>` | 引用已有的 pcs 服务接口 |
| 方法节点 | `<method>` | 自定义方法节点 |

### 触发识别

用户输入中出现「流程编排：」关键词时，表示存在 `flow` 标签。

**自然语言格式**：
```
流程编排：
服务：内部户账户信息查询
服务：获取放款和贷款还款账号对应的模块信息
方法：beforeQryAcctInfo 外调存款公共通用记账前处理
服务：负债账户支取   描述：用于存入支取
方法：第一次记账后处理
```

**解析规则**：
- `服务：{服务中文名}` → service 节点，按服务中文名搜索
- `服务：{服务中文名}   描述：{描述}` → service 节点，附带描述
- `方法：{英文方法名} {中文名称}` → method 节点，用户指定了英文方法名和中文名
- `方法：{中文名称}` → method 节点，未指定英文名，需中文翻译成英文

### 服务节点（service）

#### 搜索服务流程

> ⛔ **强制规则：服务引用必须通过搜索确认存在，不得自行猜测 serviceName 和 id。**

**三步查询，逐步回退**：

1. **优先调用 `find_services_ref.py` 脚本**：
   ```bash
   python "{工作区根目录}/.speedstudio/skills/metadata-services/scripts/find_services_ref.py" "{工作区根目录}" {服务中文名}
   ```
   - 脚本按 `serviceLongname`（中文）精确匹配 service 标签
   - 返回 `serviceTypeId`、`serviceId`、`serviceLongname` 等信息

2. **脚本查询不到时，调用 MCP 服务 `dict-mcp-server.queryServiceDetail`**：
   - 输入：服务中文名称
   - 返回服务定义信息（serviceTypeId、serviceId、serviceLongname 等）

3. **MCP 也查询不到时（⛔ 强制规则）**：
   - **XML 中不写入该 service 标签**
   - **在工作台输出**：`❌ 服务「{服务中文名}」不存在，已跳过`
   - **生成 XML 后在汇总提示中统一列出**

#### service 标签属性

| 属性 | 说明 | 来源 |
|------|------|------|
| `mappingToProperty` | 固定值 | `"true"` |
| `serviceName` | **组装值** `{serviceTypeId}.{serviceId}` | 脚本/MCP 返回的两个字段拼接 |
| `id` | service 标签的 id | 搜索结果的 `serviceId` |
| `longname` | service 标签的 longname | 搜索结果的 `serviceLongname` |

> ⛔ **serviceName 组装规则**：`serviceName` 不是直接取某个字段，而是由 `serviceTypeId` 和 `serviceId` 用 `.` 拼接而成。无论数据来自脚本还是 MCP，都需要组装：`{serviceTypeId}.{serviceId}`。

属性顺序：`mappingToProperty → serviceName → id → longname`

**生成示例**（假设 serviceTypeId=`FtAcctgDealPbsSvtp`，serviceId=`FtAcctgDealPbsSvtp`）：
```xml
<service mappingToProperty="true" serviceName="FtAcctgDealPbsSvtp.FtAcctgDealPbsSvtp" id="FtAcctgDealPbsSvtp" longname="福费延账务处理"/>
```

**多 service 文件示例**（serviceTypeId 和 serviceId 不同时）：
```xml
<service mappingToProperty="true" serviceName="IoCpCustAccountQryPbsSvtp.QueryCustAcctPbsSvtp" id="QueryCustAcctPbsSvtp" longname="查询客户账户"/>
```

#### 多个匹配时

脚本或 MCP 返回多个候选服务时，在工作台列出所有候选，询问用户选择哪一个后再继续生成。

### 方法节点（method）

#### method 标签属性

| 属性 | 说明 | 来源 |
|------|------|------|
| `method` | 方法名 | 用户指定英文名；未指定则将中文翻译成英文小驼峰 |
| `id` | 方法标识 | 与 `method` 属性值一致 |
| `longname` | 方法中文名 | 用户指定 |
| `desc` | 方法描述 | 用户指定描述则使用描述；未指定则与 `longname` 一致 |

属性顺序：`method → id → longname → desc`

**完整语法对照表**：

```
用户输入                                                → 解析结果
──────────────────────────────────────────────────────────────────
方法：beforeQryAcctInfo 外调存款公共通用记账前处理      → method="beforeQryAcctInfo"，longname="外调存款公共通用记账前处理"，desc="外调存款公共通用记账前处理"
方法：第一次记账后处理                                  → method=中文翻译英文，longname="第一次记账后处理"，desc="第一次记账后处理"
方法：doProcess 记账处理   描述：执行核心记账逻辑       → method="doProcess"，longname="记账处理"，desc="执行核心记账逻辑"
```

**生成示例**：
```xml
<method method="beforeQryAcctInfo" id="beforeQryAcctInfo" longname="外调存款公共通用记账前处理" desc="外调存款公共通用记账前处理"/>
```

### 生成的 flow 标签

`flow` 标签位于 `interface` 标签之后，是 `flowtran` 的直接子标签。节点按用户输入的顺序排列。

```xml
<flow>
    <service mappingToProperty="true" serviceName="IoCpInnerAcctInfoQryPbsSvtp.IoCpInnerAcctInfoQryPbsSvtp" id="IoCpInnerAcctInfoQryPbsSvtp" longname="内部户账户信息查询"/>
    <service mappingToProperty="true" serviceName="LoanRepayModInfoQryPbsSvtp.LoanRepayModInfoQryPbsSvtp" id="LoanRepayModInfoQryPbsSvtp" longname="获取放款和贷款还款账号对应的模块信息"/>
    <method method="beforeQryAcctInfo" id="beforeQryAcctInfo" longname="外调存款公共通用记账前处理" desc="外调存款公共通用记账前处理"/>
    <service mappingToProperty="true" serviceName="DebtAcctWithdrawPbsSvtp.DebtAcctWithdrawPbsSvtp" id="DebtAcctWithdrawPbsSvtp" longname="负债账户支取"/>
    <method method="firstPostAcctProcess" id="firstPostAcctProcess" longname="第一次记账后处理" desc="第一次记账后处理"/>
</flow>
```

**缩进层级**：`flowtran(0)` → `flow(4)` → `service/method(8)`

### 搜索结果展示规范

每次搜索后，**必须在工作台输出查询过程和结果**（展示 serviceTypeId 和 serviceId，便于组装 serviceName）：

```
🔍 流程编排服务搜索结果：
  ✅ 内部户账户信息查询  →  serviceTypeId=IoCpInnerAcctInfoQryPbsSvtp, serviceId=IoCpInnerAcctInfoQryPbsSvtp → serviceName=IoCpInnerAcctInfoQryPbsSvtp.IoCpInnerAcctInfoQryPbsSvtp
  ✅ 获取放款和贷款还款账号对应的模块信息  →  serviceTypeId=LoanRepayModInfoQryPbsSvtp, serviceId=LoanRepayModInfoQryPbsSvtp → serviceName=LoanRepayModInfoQryPbsSvtp.LoanRepayModInfoQryPbsSvtp
  ❌ 负债账户支取  →  服务不存在（脚本未找到，MCP 也未找到），已跳过
```

**最终汇总提示**（生成 XML 后必须输出）：
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  以下服务未写入 XML，请确认后补充：

【流程编排服务未找到】（需确认服务是否已创建）：
  1. 负债账户支取

💡 确认服务已创建后，可重新执行以补充这些节点。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 数组字段处理

使用 `<fields>` 标签表示数组/列表类型。

**自然语言格式**：
```
chargCdArray 收费代码数组 start
    包含 fPrjCd   收费项目编码  非必输
    包含 chrgAmt  收费金额     必输
chargCdArray 收费代码数组 end
```

**生成 XML**：
```xml
<fields id="chargCdArray" scope="" required="false" multi="true" array="false" longname="收费代码数组">
    <field id="fPrjCd" type="MBaseType.U_SHOU_FEI_XIANG_MU_BIAN_MA" required="false" multi="false" array="false" longname="收费项目编码" ref="MDict.F.fPrjCd"/>
    <field id="chrgAmt" type="MBaseType.U_JIN_E" required="true" multi="false" array="false" longname="收费金额" ref="MDict.C.chrgAmt"/>
</fields>
```

**关键规则**：`id` 必须以 `Array` 结尾，`scope=""` 固定，`multi="true"` 固定，`longname` 以「数组」结尾。

详见 [references/array-fields.md](references/array-fields.md)

---

## 字段属性说明

| 属性 | 来源 | 固定值 |
|------|------|--------|
| `id` | MCP 返回 | — |
| `type` | MCP 返回 | — |
| `required` | 用户输入（必输/非必输），默认 false | — |
| `multi` | — | `false` |
| `array` | — | `false` |
| `longname` | MCP 返回 | — |
| `ref` | MCP 返回（可选） | — |

---

## 执行清单

### 创建流程

- [ ] ⛔ **获取工作空间绝对路径**，展示：`📂 当前工作空间：{绝对路径}`
- [ ] 验证交易码格式（T+C/D/G/Y+4位数字，范围合法）
- [ ] 确定工程、模块和包路径（根据前缀映射）
- [ ] 拼接完整绝对路径：`{工作空间}/{工程}/{模块}/src/main/resources/trans/{子目录}/{交易码}.flowtrans.xml`
- [ ] 检查 `.flowtrans.xml` 是否已存在（存在则切换修改模式）
- [ ] 处理子目录（如有，追加到路径和包名）
- [ ] 识别四类内容：input 输入接口、output 输出接口、property 属性接口、flow 流程编排
- [ ] 调用 `dict-mcp-server.getDictDefByLongNameList` 批量查询所有普通字段（含 property 中的普通字段）
- [ ] **强制过滤**：将 MCP 返回 null 的字段从字段列表中移除，不得写入 XML
- [ ] 处理数组字段（识别 start/end 标记；子字段全为 null 则整个 fields 标签不写入）
- [ ] ⛔ **property 中的复合类型引用**：对每个 `[xxx]`（中文或英文），**优先**调用 `python "{工作区根目录}/.speedstudio/skills/metadata-composite-types/scripts/find_composite_ref.py" "{工作区根目录}" xxx`（脚本在工作空间下递归遍历所有 `*.c_schema.xml`，自动判断中英文）；**脚本未找到** → 调用 MCP `dict-mcp-server.queryComplexDetail` 查询；**找到唯一** → 生成无 array/ref 的 field；**去重后多匹配** → 工作台列出候选，询问用户选择其中一个；**均未找到** → 立即工作台输出 `❌ [xxx] → 未找到...`，XML 中不写入，计入汇总提示
- [ ] ⛔ **流程编排服务搜索**（如有「流程编排：」）：对每个「服务：{中文名}」，先调用 `python "{工作区根目录}/.speedstudio/skills/metadata-services/scripts/find_services_ref.py" "{工作区根目录}" {服务中文名}`；**找到** → 取 serviceTypeId、serviceId、serviceLongname，**组装 serviceName = `{serviceTypeId}.{serviceId}`**，生成 service 标签；**未找到** → 调用 MCP `dict-mcp-server.queryServiceDetail` 查询，同样组装 serviceName；**仍未找到** → 不写入 XML，提示用户「❌ 服务「xxx」不存在」；**多匹配** → 工作台列出候选，询问用户选择其中一个
- [ ] ⛔ **流程编排方法节点**（如有）：解析方法名（用户指定或中文翻译英文）、longname、desc，生成 method 标签
- [ ] 生成 XML（仅已贯标字段，属性单行，无空行，4空格缩进；property 在 output 之后；flow 在 interface 之后）
- [ ] 收集所有被排除字段和未找到的服务，在反馈中统一提示（MCP未贯标 + 复合引用未找到 + 服务未找到）
- [ ] 保存至完整绝对路径：`{工作空间}/{工程}/{模块}/src/main/resources/trans/{子目录}/`
- [ ] 输出反馈摘要

### 修改流程

- [ ] 定位现有 `.flowtrans.xml`（含子目录搜索）
- [ ] 读取并保留 `flowtran`/`description`/`interface`/`flow` 标签属性
- [ ] 调用 MCP 查询新字段；property 中 `[xxx]` 调用脚本搜索
- [ ] 覆盖 `input`、`output`、`property` 标签内容（原文件有 property 则更新，用户新增则追加）
- [ ] 处理流程编排（如有）：新增或更新 `flow` 标签内容，搜索服务引用
- [ ] 保持 XML 格式一致（属性单行，无空行）

---

## 参考资源

- [references/transaction-id-rules.md](references/transaction-id-rules.md) — 交易码验证规则与实现
- [references/package-module-mapping.md](references/package-module-mapping.md) — 包路径和模块映射
- [references/xml-template.md](references/xml-template.md) — XML 模板完整说明
- [references/array-fields.md](references/array-fields.md) — 数组字段处理详解
- [references/mcp-integration.md](references/mcp-integration.md) — MCP 服务集成说明
- [references/error-handling.md](references/error-handling.md) — 错误处理指南
- [references/examples.md](references/examples.md) — 完整示例集
