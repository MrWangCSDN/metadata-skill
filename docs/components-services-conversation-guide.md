# 构件与服务元数据 —— 对话指令指南

本文档为开发人员提供与 AI 对话创建/修改构件和服务元数据的标准指令模板。

---

## 前置说明

### 构件与服务类型总览

| 类型 | 中文名 | 接口文件 | 实现文件 | 定位 |
|------|--------|---------|---------|------|
| PBCB | 基础构件 | `{name}.pbcb.xml` | `{name}.pbcbImpl.xml` | 承载具体业务逻辑 |
| PBCP | 产品构件 | `{name}.pbcp.xml` | `{name}.pbcpImpl.xml` | 跨业务复用的产品能力 |
| PBCC | 公共构件 | `{name}.pbcc.xml` | `{name}.pbccImpl.xml` | 通用工具能力（仅 comm 领域） |
| PBCT | 技术构件 | `{name}.pbct.xml` | `{name}.pbctImpl.xml` | 基础技术能力封装 |
| PBS | 基础服务 | `{name}.pbs.xml` | `{name}.pbsImpl.xml` | 单一业务能力，供 PCS 调用 |
| PCS | 组合服务 | `{name}.pcs.xml` | `{name}.pcsImpl.xml` | 编排多个构件/服务，面向外部 |

> ⛔ 创建接口文件时**必须同时创建实现文件**，配套生成。

### 领域与模块映射

| 领域 | 缩写 | 适用类型 |
|------|------|---------|
| 存款 | dept | PBCB / PBCP / PBCT / PBS / PCS |
| 贷款 | loan | PBCB / PBCP / PBCT / PBS / PCS |
| 结算 | sett | PBCB / PBCP / PBCT / PBS / PCS |
| 平台公共 | comm | 全部（**PBCC 仅限 comm**） |

### 各类型接口与实现模块

**构件类**：

| 类型 | 接口模块 | 实现模块 |
|------|---------|---------|
| PBCB | {领域}-pbcb-api | {领域}-pbcb-impl |
| PBCP | {领域}-pbcp-api | {领域}-pbcp-impl |
| PBCC | comm-pbcc-api | comm-pbcc-impl |
| PBCT | {领域}-pbct-api | {领域}-pbct-impl |

**服务类**：

| 类型 | 接口模块 | 实现模块 |
|------|---------|---------|
| PBS | {领域}-pbs-api | {领域}-pbs-impl |
| PCS | {领域}-pcs-api | {领域}-pcs-impl |

### 文件路径规则

- 接口文件：`{模块}/src/main/resources/serviceType/{子目录}/{name}.{类型}.xml`
- 实现文件：`{模块}/src/main/resources/serviceimpl/{子目录}/{name}.{类型}Impl.xml`
- 接口和实现的**子目录保持一致**

### id 命名规则

id 由大驼峰业务名 + 类型后缀 + `Svtp` 组成：

| 类型 | id 后缀 | 示例 |
|------|--------|------|
| PBCB | `PbcbSvtp` | `LoanQueryPbcbSvtp` |
| PBCP | `PbcpSvtp` | `ProductCalcPbcpSvtp` |
| PBCC | `PbccSvtp` | `DateUtilPbccSvtp` |
| PBCT | `PbctSvtp` | `CacheManagePbctSvtp` |
| PBS | `PbsSvtp` | `PriceCalcPbsSvtp` |
| PCS | `PcsSvtp` | `OrderSubmitPcsSvtp` |

实现 id = 接口 id + `Impl`（如 `LoanQueryPbcbSvtpImpl`）。

### 方法描述写法

```
方法：
{方法英文名} {方法中文名}
  输入：{字段中文名1} 必输，{字段中文名2}
  输出：{字段中文名1}，{字段中文名2}
```

> 方法英文名小驼峰；未指定英文名则 AI 根据中文自动翻译。

---

## 场景 1：创建基础构件（PBCB）

### 指令模板

```
帮我创建 {英文名} {中文名} 基础构件，{领域}领域

方法：
{方法英文名} {方法中文名}
  输入：{字段} 必输，{字段}
  输出：{字段}
```

### 示例 1-A：单方法

```
帮我创建 LoanQuery 贷款查询 基础构件，贷款领域

方法：
queryLoanInfo 查询贷款信息
  输入：客户ID 必输，贷款编号 必输
  输出：贷款金额，币种代码
```

### 示例 1-B：多方法

```
帮我创建 LoanQuery 贷款查询 基础构件，贷款领域

方法：
queryLoanInfo 查询贷款信息
  输入：客户ID 必输，贷款编号 必输
  输出：贷款金额，币种代码

queryLoanList 查询贷款列表
  输入：客户ID 必输
  输出：贷款金额
```

### 示例 1-C：不指定英文名

```
帮我创建 贷款查询 基础构件，贷款领域

方法：
查询贷款信息
  输入：客户ID 必输
  输出：贷款金额
```

> AI 自动翻译：构件英文名 `LoanQuery`，id = `LoanQueryPbcbSvtp`，方法 id = `queryLoanInfo`

### AI 返回格式示例

```
✅ 成功创建基础构件（接口 + 实现）

📁 接口文件: loan-pbcb-api/src/main/resources/serviceType/LoanQuery.pbcb.xml
📁 实现文件: loan-pbcb-impl/src/main/resources/serviceimpl/LoanQuery.pbcbImpl.xml
📦 接口 package: com.spdb.ccbs.loan.pbcb.api.servicetype
📦 实现 package: com.spdb.ccbs.loan.pbcb.impl.serviceimpl
🧩 方法: queryLoanInfo、queryLoanList

📋 MCP 字段查询结果：
  ✅ 客户ID    →  id=custId  type=MBaseType.U_KE_HU_BIAN_HAO
  ✅ 贷款编号  →  id=loanNo  type=MBaseType.U_DAI_KUAN_BIAN_HAO
  ✅ 贷款金额  →  id=loanAmount  type=MBaseType.U_JIN_E
  ✅ 币种代码  →  id=crcyCd  type=MBaseType.U_BI_ZHONG_DAI_MA

✅ 所有字段均已写入 XML
```

---

## 场景 2：创建产品构件（PBCP）

### 指令模板

```
帮我创建 {英文名} {中文名} 产品构件，{领域}领域

方法：
...
```

### 示例

```
帮我创建 ProductCalc 产品计算 产品构件，贷款领域

方法：
calcProduct 计算产品
  输入：产品编号 必输
  输出：利率，期限
```

**生成结果**：
- 接口文件：`loan-pbcp-api/src/main/resources/serviceType/ProductCalc.pbcp.xml`
- 实现文件：`loan-pbcp-impl/src/main/resources/serviceimpl/ProductCalc.pbcpImpl.xml`
- id：`ProductCalcPbcpSvtp`

---

## 场景 3：创建公共构件（PBCC，仅 comm 领域）

### 指令模板

```
帮我创建 {英文名} {中文名} 公共构件

方法：
...
```

> 公共构件无需指定领域，固定为 comm。

### 示例

```
帮我创建 DateUtil 日期工具 公共构件

方法：
formatDate 格式化日期
  输入：日期 必输
  输出：格式化结果
```

**生成结果**：
- 接口文件：`comm-pbcc-api/src/main/resources/serviceType/DateUtil.pbcc.xml`
- 实现文件：`comm-pbcc-impl/src/main/resources/serviceimpl/DateUtil.pbccImpl.xml`
- id：`DateUtilPbccSvtp`

---

## 场景 4：创建基础服务（PBS）

### 指令模板

```
帮我创建 {英文名} {中文名} 基础服务，{领域}领域

方法：
...
```

### 示例

```
帮我创建 PriceCalc 价格计算 基础服务，贷款领域

方法：
calcLoanPrice 计算贷款价格
  输入：贷款金额 必输，币种代码
  输出：利息金额，总金额
```

**生成结果**：
- 接口文件：`loan-pbs-api/src/main/resources/serviceType/PriceCalc.pbs.xml`
- 实现文件：`loan-pbs-impl/src/main/resources/serviceimpl/PriceCalc.pbsImpl.xml`
- id：`PriceCalcPbsSvtp`

---

## 场景 5：创建组合服务（PCS）

### 指令模板

```
帮我创建 {英文名} {中文名} 组合服务，{领域}领域

方法：
...
```

### 示例

```
帮我创建 OrderSubmit 订单提交 组合服务，贷款领域

方法：
submitOrder 提交订单
  输入：客户ID 必输，贷款金额 必输
  输出：申请编号
```

**生成结果**：
- 接口文件：`loan-pcs-api/src/main/resources/serviceType/OrderSubmit.pcs.xml`
- 实现文件：`loan-pcs-impl/src/main/resources/serviceimpl/OrderSubmit.pcsImpl.xml`
- id：`OrderSubmitPcsSvtp`

---

## 场景 6：创建带子目录的构件/服务

### 指令模板

```
帮我创建 {英文名} {中文名} {构件/服务类型}，{领域}领域，子目录 {子目录}

方法：
...
```

### 示例 6-A：单级子目录

```
帮我创建 FtLoanQuery 福费延查询 基础构件，贷款领域，子目录 ft

方法：
queryFtInfo 查询福费延信息
  输入：福费延借据编码 必输
  输出：融资业务编码，币种代码
```

**生成结果**：
- 接口文件：`loan-pbcb-api/src/main/resources/serviceType/ft/FtLoanQuery.pbcb.xml`
- 实现文件：`loan-pbcb-impl/src/main/resources/serviceimpl/ft/FtLoanQuery.pbcbImpl.xml`
- 接口 package：`com.spdb.ccbs.loan.pbcb.api.servicetype.ft`

### 示例 6-B：多级子目录

```
帮我创建 FtRepayCalc 福费延还款计算 基础服务，贷款领域，子目录 ft/repay

方法：
calcRepay 计算还款
  输入：福费延借据编码 必输
  输出：还款金额
```

**生成结果**：
- 接口文件：`loan-pbs-api/src/main/resources/serviceType/ft/repay/FtRepayCalc.pbs.xml`
- 实现文件：`loan-pbs-impl/src/main/resources/serviceimpl/ft/repay/FtRepayCalc.pbsImpl.xml`
- 接口 package：`com.spdb.ccbs.loan.pbs.api.servicetype.ft.repay`

---

## 场景 7：修改现有构件/服务

### 指令模板（新增方法）

```
修改 {英文名} {构件/服务类型}，新增方法 {方法描述}
```

### 示例 7-A：新增方法

```
修改 LoanQuery 基础构件，新增方法：
queryLoanDetail 查询贷款详情
  输入：贷款编号 必输
  输出：贷款金额，还款日期，币种代码
```

> ⚠️ 修改会同时更新接口文件和实现文件，在接口中增加 method，在实现中增加对应的 method（含 ref）。

### AI 返回格式示例

```
✅ 成功修改基础构件（接口 + 实现已同步更新）

📁 接口文件: loan-pbcb-api/src/main/resources/serviceType/LoanQuery.pbcb.xml
📁 实现文件: loan-pbcb-impl/src/main/resources/serviceimpl/LoanQuery.pbcbImpl.xml

新增方法:
  🧩 queryLoanDetail（查询贷款详情）

📋 MCP 字段查询结果：
  ✅ 贷款编号  →  id=loanNo
  ✅ 贷款金额  →  id=loanAmount
  ✅ 还款日期  →  id=repayDate
  ✅ 币种代码  →  id=crcyCd

📌 原有方法保持不变
```

---

## 场景 8：综合场景（多方法 + 子目录 + 未贯标字段）

```
帮我创建 SettFlow 结算流水处理 基础构件，结算领域，子目录 flow

方法：
queryFlowList 查询流水列表
  输入：客户编号 必输，交易日期
  输出：交易金额，币种代码

processFlow 处理流水
  输入：流水号 必输，交易金额 必输
  输出：处理结果，未知字段
```

### AI 返回（含未贯标提示）

```
✅ 成功创建基础构件（接口 + 实现）

📁 接口文件: sett-pbcb-api/src/main/resources/serviceType/flow/SettFlow.pbcb.xml
📁 实现文件: sett-pbcb-impl/src/main/resources/serviceimpl/flow/SettFlow.pbcbImpl.xml
🗂️  子目录: flow

📋 MCP 字段查询结果：
  ✅ 客户编号  →  id=custId
  ✅ 交易日期  →  id=transDate
  ✅ 交易金额  →  id=transAmt
  ✅ 币种代码  →  id=crcyCd
  ✅ 流水号    →  id=flowNo
  ❌ 处理结果  →  未贯标（MCP 返回 null），已跳过
  ❌ 未知字段  →  未贯标（MCP 返回 null），已跳过

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

### ❌ 构件/服务类型写错

| 错误输入 | 原因 | 正确写法 |
|---------|------|---------|
| `帮我创建 xxx 构件` | 未指定具体类型 | `帮我创建 xxx 基础构件` |
| `帮我创建 xxx PBCB` | 应使用中文类型名 | `帮我创建 xxx 基础构件` |

### ❌ PBCC 指定了非 comm 领域

```
❌ 公共构件（PBCC）仅属于平台公共（comm）领域，不能指定其他领域
```

**解决**：公共构件不需要指定领域，直接写 `帮我创建 xxx 公共构件`。

### ❌ 字段未贯标

AI 会提示：
```
❌ 以下字段未贯标，已从 XML 中强制排除：
  1. 未知字段（方法名 输入/输出）

💡 请在 dict-mcp-server 系统完成字段贯标后重新执行
```

**解决**：在 `dict-mcp-server` 字段管理系统中完成贯标后重新执行。

### ❌ 只创建了接口没创建实现

```
❌ 接口和实现必须配套创建

💡 系统会自动同时创建接口文件和实现文件
```

### ❌ 领域填写错误

| 错误输入 | 正确写法 |
|---------|---------|
| `loan` | `贷款领域` |
| `公共领域` | `平台公共领域` |

---

## 快速指令速查

| 场景 | 指令起始语 |
|------|-----------|
| 创建基础构件 | `帮我创建 {英文名} {中文名} 基础构件，{领域}领域` |
| 创建产品构件 | `帮我创建 {英文名} {中文名} 产品构件，{领域}领域` |
| 创建公共构件 | `帮我创建 {英文名} {中文名} 公共构件`（领域固定 comm） |
| 创建技术构件 | `帮我创建 {英文名} {中文名} 技术构件，{领域}领域` |
| 创建基础服务 | `帮我创建 {英文名} {中文名} 基础服务，{领域}领域` |
| 创建组合服务 | `帮我创建 {英文名} {中文名} 组合服务，{领域}领域` |
| 指定子目录 | 在末尾加：`，子目录 {子目录}` |
| 只有中文名 | 省略英文名，AI 自动翻译 |
| 修改（新增方法） | `修改 {英文名} {类型}，新增方法 {描述}` |
| 方法必输字段 | 字段后加 `必输` |
