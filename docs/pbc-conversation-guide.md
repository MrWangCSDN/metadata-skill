# 构件元数据 —— 对话指令指南

本文档为开发人员提供与 AI 对话创建/修改构件（PBC）元数据的标准指令模板。

---

## 前置说明

### 四种构件类型

| 类型 | 中文名 | 接口文件后缀 | 实现文件后缀 | 说明 |
|------|--------|-------------|-------------|------|
| PBCB | 业务构件 | `.pbcb.xml` | `.pbcbImpl.xml` | 承载具体业务逻辑 |
| PBCP | 产品构件 | `.pbcp.xml` | `.pbcpImpl.xml` | 跨业务复用的产品能力 |
| PBCC | 公共构件 | `.pbcc.xml` | `.pbccImpl.xml` | 通用工具能力（**仅 comm 领域**） |
| PBCT | 技术构件 | `.pbct.xml` | `.pbctImpl.xml` | 基础技术能力封装（暂不考虑） |

> 创建新构件时，AI 会**询问**「是否同时创建该构件的实现文件？」；用户确认后才创建实现文件。

### 领域说明

| 领域 | 缩写 | 适用构件类型 |
|------|------|------------|
| 存款 | dept | PBCB / PBCP |
| 贷款 | loan | PBCB / PBCP |
| 结算 | sett | PBCB / PBCP |
| 平台公共 | comm | PBCB / PBCP / **PBCC（仅 comm）** |

### 模块映射

| 构件类型 | 接口模块 | 实现模块 |
|---------|---------|---------|
| PBCB | {领域}-pbcb-api | {领域}-pbcb-impl |
| PBCP | {领域}-pbcp-api | {领域}-pbcp-impl |
| PBCC | comm-pbcc-api | comm-pbcc-impl |

### id 命名规则

- 接口 id = 大驼峰业务名 + 构件类型后缀 + `Svtp`
- 实现 id = 大驼峰业务名 + 构件类型后缀 + `Impl`

| 构件类型 | 接口 id 后缀 | 实现 id 后缀 | 示例 |
|---------|-------------|-------------|------|
| PBCB | `PbcbSvtp` | `PbcbImpl` | `GnfeeTrialChecksPbcbSvtp` / `GnfeeTrialChecksPbcbImpl` |
| PBCP | `PbcpSvtp` | `PbcpImpl` | `IoAcctOpenPbcpSvtp` / `IoAcctOpenPbcpImpl` |
| PBCC | `PbccSvtp` | `PbccImpl` | `CustInfoQryPbccSvtp` / `CustInfoQryPbccImpl` |

### 字段必输说明

- **必输**：`required="true"`
- **非必输**（缺省）：`required="false"`

### 服务描述写法

构件使用 `<service>` 标签，每个构件文件**可包含多个 service**。

```
服务：
{service的id} {service的name} {service中文名}
  描述：{可选描述}
  输入：{字段中文名1} 必输，{字段中文名2}
  输出：{字段中文名1}，{字段中文名2}
```

> - service 的 id 和 name 可省略，AI 根据中文名自动翻译
> - id 为大驼峰 + 构件类型后缀（如 `PbcbSvtp`），name 为小驼峰
> - 描述可选，有则生成 `<description>` 标签，无则不生成

### packMode 说明

- `input` 的 `packMode` 默认 `false`；用户说「**生成对应的输入接口类**」时设为 `true`
- `output` 的 `packMode` 默认 `false`；用户说「**生成对应的输出接口类**」时设为 `true`
- `output` 的 `asParm` 固定 `false`

### 复合类型引用写法

用 `[中文名]` 中括号包裹复合对象名，AI 自动搜索对应复合类型。

| 写法 | 含义 |
|------|------|
| `[保函费用试算输入]` | 复合引用，单值 |
| `[保函费用试算输入]  多值` | 复合引用，multi=true |
| `gnFeeTrialApsInPojo [保函费用试算输入]` | 复合引用，指定英文 id |

### 数组字段写法

```
{数组名}Array {中文名}数组 start
    包含 {字段名}  {中文名}  {必输/非必输}
{数组名}Array {中文名}数组 end
```

---

## 场景 1：创建业务构件（PBCB）

### 指令模板

```
帮我创建 {英文名} {中文名} 业务构件，{领域}领域

服务：
{service中文名}
  输入：{字段}，{字段} 必输
  输出：{字段}
```

### 示例 1-A：单服务

```
帮我创建 GnfeeTrialChecks 保函费用试算校验 业务构件，结算领域，子目录 gnfee

服务：
GnfeeTrialChecksPbcbSvtp gnfeeTrialChecks 保函费用试算校验
  描述：保函费用试算校验服务
  输入：[保函费用试算输入]，币种代码
  输出：利息金额
```

### 示例 1-B：多服务

```
帮我创建 IoCpCustAccountQry 客户账户查询业务构件，存款领域

服务1：
QueryCustAcctPbcbSvtp queryCustAcct 查询客户账户
  输入：客户编号 必输
  输出：账号

服务2：
QueryCustBalancePbcbSvtp queryCustBalance 查询客户余额
  输入：账号 必输
  输出：可用余额
```

### 示例 1-C：不指定英文名

```
帮我创建 贷款查询 业务构件，贷款领域

服务：
查询贷款信息
  输入：客户ID 必输
  输出：贷款金额
```

> AI 自动翻译：构件英文名 `LoanQuery`，接口 id = `LoanQueryPbcbSvtp`，service id = `LoanQueryPbcbSvtp`，name = `loanQuery`

### AI 返回格式示例

创建构件后，AI 会先询问：
```
是否同时创建该构件的实现文件？（Y/n）
```

用户确认后：
```
✅ 成功创建业务构件（接口 + 实现）

📁 接口文件: sett-pbcb-api/src/main/resources/serviceType/gnfee/GnfeeTrialChecks.pbcb.xml
📁 实现文件: sett-pbcb-impl/src/main/resources/serviceimpl/gnfee/GnfeeTrialChecks.pbcbImpl.xml
📦 接口 package: com.spdb.ccbs.sett.pbcb.api.serviceType.gnfee
📦 实现 package: com.spdb.ccbs.sett.pbcb.impl.serviceimpl.gnfee
🧩 服务: gnfeeTrialChecks（保函费用试算校验）

📋 MCP 字段查询结果：
  ✅ 币种代码  →  type=MBaseType.U_BI_ZHONG_DAI_MA  ref=MDict.C.crcyCd
  ✅ 利息金额  →  type=MBaseType.U_JIN_E  ref=MDict.I.intrstAmt

🔍 复合对象引用搜索结果：
  ✅ [保函费用试算输入]  →  GnFeeTrialType.GnFeeTrialApsInPojo

✅ 所有字段均已写入 XML
```

---

## 场景 2：创建产品构件（PBCP）

### 指令模板

```
帮我创建 {英文名} {中文名} 产品构件，{领域}领域

服务：
...
```

### 示例

```
帮我创建 IoAcctOpen 开户产品构件，存款领域，子目录 acct

服务：
openNewAcct 新开账户
  输入：客户编号 必输，账户类型 必输
  输出：账号
```

**生成结果**：
- 接口文件：`dept-pbcp-api/src/main/resources/serviceType/acct/IoAcctOpen.pbcp.xml`
- 实现文件：`dept-pbcp-impl/src/main/resources/serviceimpl/acct/IoAcctOpen.pbcpImpl.xml`
- 接口 id：`IoAcctOpenPbcpSvtp`

---

## 场景 3：创建公共构件（PBCC，仅 comm 领域）

### 指令模板

```
帮我创建 {英文名} {中文名} 公共构件

服务：
...
```

> 公共构件无需指定领域，固定为 comm。

### 示例

```
帮我创建 CustInfoQry 客户信息查询 公共构件，子目录 cust

服务：
queryCustInfo 查询客户信息
  输入：客户编号 必输
  输出：客户名称，客户状态
```

**生成结果**：
- 接口文件：`comm-pbcc-api/src/main/resources/serviceType/cust/CustInfoQry.pbcc.xml`
- 实现文件：`comm-pbcc-impl/src/main/resources/serviceimpl/cust/CustInfoQry.pbccImpl.xml`
- 接口 id：`CustInfoQryPbccSvtp`

---

## 场景 4：含复合类型引用的构件

### 指令模板

```
帮我创建 {英文名} {中文名} 业务构件，{领域}领域

服务：
{服务描述}
  输入：[{复合对象中文名}]，{普通字段}
  输出：{字段}
```

### 示例 4-A：自动生成引用 id

```
帮我创建 GnfeeTrialChecks 保函费用试算校验 业务构件，结算领域

服务：
保函费用试算校验
  输入：[保函费用试算输入]，币种代码
  输出：利息金额
```

> AI 搜索复合类型，找到 `GnFeeTrialType.GnFeeTrialApsInPojo`，自动生成 id = `gnFeeTrialApsInPojo`

### 示例 4-B：指定引用 id

```
帮我创建 GnfeeTrialChecks 保函费用试算校验 业务构件，结算领域

服务：
保函费用试算校验
  输入：gnFeeTrialApsInPojo [保函费用试算输入]，币种代码
  输出：利息金额
```

> `gnFeeTrialApsInPojo` 是用户指定的英文 id，直接使用

### 示例 4-C：多值复合引用

```
帮我创建 LoanBatchQuery 贷款批量查询 业务构件，贷款领域

服务：
批量查询贷款
  输入：[贷款查询输入] 多值 必输
  输出：[贷款查询输出] 多值
```

> 多值引用：`multi="true"`，id 自动加 `List` 后缀（如无用户指定 id）

### AI 返回格式示例（含引用未找到）

```
📋 MCP 字段查询结果：
  ✅ 币种代码  →  type=MBaseType.U_BI_ZHONG_DAI_MA  ref=MDict.C.crcyCd
  ✅ 利息金额  →  type=MBaseType.U_JIN_E  ref=MDict.I.intrstAmt

🔍 复合对象引用搜索结果：
  ✅ [保函费用试算输入]  →  GnFeeTrialType.GnFeeTrialApsInPojo
  ❌ [结算信息输出]       →  未找到匹配的 c_schema.xml，已跳过

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  以下字段未写入 XML，请确认后补充：

【复合对象引用未找到】（需确认 c_schema.xml 是否已创建）：
  1. [结算信息输出]

💡 确认文件已创建后，可重新执行以补充这些字段。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 场景 5：含数组字段的构件

### 指令模板

```
帮我创建 {英文名} {中文名} 业务构件，{领域}领域

服务：
{服务描述}
  输入：
    {普通字段} 必输
    {数组名}Array {中文名}数组 start
        包含 {字段中文名1} 非必输
        包含 {字段中文名2} 必输
    {数组名}Array {中文名}数组 end
  输出：{字段}
```

### 示例

```
帮我创建 ChargeCalc 费用计算 业务构件，贷款领域

服务：
chargeCalc 费用计算
  输入：
    贷款合同号 必输
    chargCdArray 收费代码数组 start
        包含 收费项目编码 非必输
        包含 收费金额     必输
    chargCdArray 收费代码数组 end
  输出：总金额
```

**生成结果**（input 片段）：

```xml
<input packMode="false">
    <field id="loanCntrNo" type="MBaseType.U_HE_TONG_HAO" required="true" multi="false" array="false" longname="贷款合同号" ref="MDict.L.loanCntrNo"/>
    <fields id="chargCdArray" scope="" required="false" multi="true" array="false" longname="收费代码数组">
        <field id="fPrjCd" type="MBaseType.U_SHOU_FEI_XIANG_MU_BIAN_MA" required="false" multi="false" array="false" longname="收费项目编码" ref="MDict.F.fPrjCd"/>
        <field id="chrgAmt" type="MBaseType.U_JIN_E" required="true" multi="false" array="false" longname="收费金额" ref="MDict.C.chrgAmt"/>
    </fields>
</input>
```

---

## 场景 6：在子目录下创建构件

### 指令模板

```
帮我创建 {英文名} {中文名} {构件类型}，{领域}领域，子目录 {子目录}

服务：
...
```

### 示例 6-A：单级子目录

```
帮我创建 FtLoanQuery 福费延查询 业务构件，贷款领域，子目录 ft

服务：
查询福费延信息
  输入：福费延借据编码 必输
  输出：融资业务编码，币种代码
```

**生成结果**：
- 接口文件：`loan-pbcb-api/src/main/resources/serviceType/ft/FtLoanQuery.pbcb.xml`
- 实现文件：`loan-pbcb-impl/src/main/resources/serviceimpl/ft/FtLoanQuery.pbcbImpl.xml`
- 接口 package：`com.spdb.ccbs.loan.pbcb.api.serviceType.ft`
- 实现 package：`com.spdb.ccbs.loan.pbcb.impl.serviceimpl.ft`

### 示例 6-B：多级子目录

```
帮我创建 FtRepayCalc 福费延还款计算 业务构件，贷款领域，子目录 ft/repay

服务：
计算还款
  输入：福费延借据编码 必输
  输出：还款金额
```

**生成结果**：
- 接口文件：`loan-pbcb-api/src/main/resources/serviceType/ft/repay/FtRepayCalc.pbcb.xml`
- 实现文件：`loan-pbcb-impl/src/main/resources/serviceimpl/ft/repay/FtRepayCalc.pbcbImpl.xml`
- 接口 package：`com.spdb.ccbs.loan.pbcb.api.serviceType.ft.repay`

---

## 场景 7：packMode 为 true 的构件

### 指令模板

```
帮我创建 {英文名} {中文名} 业务构件，{领域}领域

服务：
{服务描述}
  输入（生成对应的输入接口类）：{字段}
  输出（生成对应的输出接口类）：{字段}
```

### 示例

```
帮我创建 AcctQuery 账户查询 业务构件，存款领域

服务：
查询账户
  输入（生成对应的输入接口类）：客户编号 必输
  输出（生成对应的输出接口类）：账号，可用余额
```

**生成结果**（input/output 标签的 packMode 为 true）：

```xml
<input packMode="true">
    <field id="custId" type="MBaseType.U_KE_HU_BIAN_HAO" required="true" multi="false" array="false" longname="客户编号" ref="MDict.C.custId"/>
</input>
<output asParm="false" packMode="true">
    <field id="acctNo" type="MBaseType.U_ZHANG_HAO" required="false" multi="false" array="false" longname="账号" ref="MDict.A.acctNo"/>
    <field id="avlBal" type="MBaseType.U_JIN_E" required="false" multi="false" array="false" longname="可用余额" ref="MDict.A.avlBal"/>
</output>
```

---

## 场景 8：修改现有构件

### 指令模板（新增服务）

```
修改 {英文名} {构件类型}，新增服务 {服务描述}
```

### 示例 8-A：新增服务

```
修改 GnfeeTrialChecks 业务构件，新增服务：
gnfeeTrialCalc 保函费用试算计算
  输入：[保函费用试算输入]
  输出：保函费用金额
```

> ⚠️ 修改会更新接口文件（新增/修改 service）。若实现文件已存在，其 `serviceType` 引用无需变更；仅当构件 longname 变更时需同步更新实现的 longname。

### 示例 8-B：在原有字段基础上修改

```
修改 GnfeeTrialChecks 业务构件的 gnfeeTrialChecks 服务，输入增加 交易日期（非必输）
```

### AI 返回格式示例

```
✅ 成功修改业务构件（接口 + 实现已同步更新）

📁 接口文件: sett-pbcb-api/src/main/resources/serviceType/gnfee/GnfeeTrialChecks.pbcb.xml
📁 实现文件: sett-pbcb-impl/src/main/resources/serviceimpl/gnfee/GnfeeTrialChecks.pbcbImpl.xml

新增服务:
  🧩 gnfeeTrialCalc（保函费用试算计算）

📋 MCP 字段查询结果：
  ✅ 保函费用金额  →  id=gnFeeAmt  type=MBaseType.U_JIN_E

🔍 复合对象引用搜索结果：
  ✅ [保函费用试算输入]  →  GnFeeTrialType.GnFeeTrialApsInPojo

📌 原有服务保持不变
```

---

## 场景 9：综合场景（多服务 + 子目录 + 复合引用 + 未贯标字段）

```
帮我创建 SettFlowProcess 结算流水处理 业务构件，结算领域，子目录 flow

服务1：
queryFlowList 查询流水列表
  输入：客户编号 必输，交易日期
  输出：交易金额，币种代码

服务2：
processFlow 处理流水
  描述：处理单笔结算流水
  输入：流水号 必输，[结算流水输入] 必输
  输出：处理结果，未知字段
```

### AI 返回（含未贯标提示）

```
✅ 成功创建业务构件（接口 + 实现）

📁 接口文件: sett-pbcb-api/src/main/resources/serviceType/flow/SettFlowProcess.pbcb.xml
📁 实现文件: sett-pbcb-impl/src/main/resources/serviceimpl/flow/SettFlowProcess.pbcbImpl.xml
🗂️  子目录: flow

📋 MCP 字段查询结果：
  ✅ 客户编号  →  type=MBaseType.U_KE_HU_BIAN_HAO  ref=MDict.C.custId
  ✅ 交易日期  →  type=MBaseType.U_RI_QI  ref=MDict.T.transDate
  ✅ 交易金额  →  type=MBaseType.U_JIN_E  ref=MDict.T.transAmt
  ✅ 币种代码  →  type=MBaseType.U_BI_ZHONG_DAI_MA  ref=MDict.C.crcyCd
  ✅ 流水号    →  type=MBaseType.U_LIU_SHUI_HAO  ref=MDict.F.flowNo
  ❌ 处理结果  →  未贯标（MCP 返回 null），已跳过
  ❌ 未知字段  →  未贯标（MCP 返回 null），已跳过

🔍 复合对象引用搜索结果：
  ✅ [结算流水输入]  →  SettFlowType.SettFlowInPojo

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  以下字段未写入 XML，请确认后补充：

【未贯标字段】（MCP 返回 null，需完成贯标后重新执行）：
  1. 处理结果（processFlow 输出）
  2. 未知字段（processFlow 输出）

💡 完成上述问题后，可重新执行以补充。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 常见错误与修正

### ❌ 构件类型未明确指定

| 错误输入 | 原因 | 正确写法 |
|---------|------|---------|
| `帮我创建 xxx 构件` | 未指定具体类型 | `帮我创建 xxx 业务构件` |
| `帮我创建 xxx PBCB` | 应使用中文类型名 | `帮我创建 xxx 业务构件` |

### ❌ PBCC 指定了非 comm 领域

```
❌ 公共构件（PBCC）仅属于平台公共（comm）领域，不能指定其他领域
```

**解决**：公共构件不需要指定领域，直接写 `帮我创建 xxx 公共构件`。

### ❌ 字段未贯标

AI 会提示：
```
❌ 以下字段未贯标，已从 XML 中强制排除：
  1. 未知字段

💡 请在 dict-mcp-server 系统完成字段贯标后重新执行
```

**解决**：在 `dict-mcp-server` 字段管理系统中完成字段贯标（登记字段英文名、类型、中文名等元数据）后，重新执行指令。

### ❌ 复合类型引用未找到

AI 会提示：
```
❌ [结算信息输出] → 未找到匹配的 c_schema.xml，已跳过
```

**解决**：确认对应的 `*.c_schema.xml` 复合类型文件已创建，且 `complexType` 的 `longname` 与中括号内的中文名**完全一致**，然后重新执行指令。

### ❌ 数组字段格式错误

| 错误 | 正确 |
|------|------|
| `chargCd 收费代码数组 start` | `chargCdArray 收费代码数组 start`（id 必须以 Array 结尾） |
| 只有 start 没有 end | start 和 end 必须成对出现 |
| start 和 end 名称不一致 | 保持名称完全一致 |

### ❌ 创建时未确认实现文件

创建构件后 AI 会询问「是否同时创建该构件的实现文件？」。若用户选择否，则仅生成接口文件；后续可再次请求创建实现文件。

---

## 快速指令速查

| 场景 | 指令起始语 |
|------|-----------|
| 创建业务构件 | `帮我创建 {英文名} {中文名} 业务构件，{领域}领域` |
| 创建产品构件 | `帮我创建 {英文名} {中文名} 产品构件，{领域}领域` |
| 创建公共构件 | `帮我创建 {英文名} {中文名} 公共构件`（领域固定 comm） |
| 指定子目录 | 在末尾加：`，子目录 {子目录}` |
| 只有中文名 | 省略英文名，AI 自动翻译 |
| 含复合引用 | 字段行写 `[中文名]`，可加 `多值`/`必输` |
| 指定引用 id | 字段行写 `英文id [中文名]` |
| 含数组字段 | `xxxArray xxx数组 start` ... `xxxArray xxx数组 end` |
| packMode | 输入/输出后加「（生成对应的输入/输出接口类）」 |
| 含描述 | 服务下加 `描述：{描述内容}` |
| 多服务 | 依次写 `服务1：` `服务2：` |
| 修改（新增服务） | `修改 {英文名} {类型}，新增服务 {描述}` |
| 修改（修改字段） | `修改 {英文名} {类型} 的 {服务名} 服务，输入增加 {字段}` |
| 配套创建实现 | 创建构件后 AI 会询问，用户确认 Y 则创建实现文件 |
