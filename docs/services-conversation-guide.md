# 服务元数据 —— 对话指令指南

本文档为开发人员提供与 AI 对话创建/修改服务（PBS/PCS）元数据的标准指令模板。

---

## 前置说明

### 两种服务类型

| 类型 | 中文名 | 接口文件后缀 | 实现文件后缀 | 说明 |
|------|--------|-------------|-------------|------|
| PBS | 基础服务 | `.pbs.xml` | `.pbsImpl.xml` | 单一业务能力，供 PCS 调用 |
| PCS | 组合服务 | `.pcs.xml` | `.pcsImpl.xml` | 编排多个构件/服务，面向外部 |

> 创建新服务时，AI 会**询问**「是否同时创建该服务的实现文件？」；用户确认后才创建实现文件。

### 领域说明

| 领域 | 缩写 | 适用服务类型 |
|------|------|------------|
| 存款 | dept | PBS / PCS |
| 贷款 | loan | PBS / PCS |
| 结算 | sett | PBS / PCS |
| 平台公共 | comm | PBS / PCS |

### 模块映射（必须严格遵守）

| 文件类型 | 模块名格式 |
|---------|-----------|
| 服务（接口） | `{领域}-{服务类型}-api` |
| 服务实现 | `{领域}-{服务类型}-impl` |

**领域**：dept、loan、sett、comm
**服务类型**：pbs、pcs

| 领域 | 服务类型 | 接口模块 | 实现模块 |
|------|---------|---------|---------|
| dept | pbs | dept-pbs-api | dept-pbs-impl |
| dept | pcs | dept-pcs-api | dept-pcs-impl |
| loan | pbs | loan-pbs-api | loan-pbs-impl |
| loan | pcs | loan-pcs-api | loan-pcs-impl |
| sett | pbs | sett-pbs-api | sett-pbs-impl |
| sett | pcs | sett-pcs-api | sett-pcs-impl |
| comm | pbs | comm-pbs-api | comm-pbs-impl |
| comm | pcs | comm-pcs-api | comm-pcs-impl |

### id 命名规则

- 接口 id = 大驼峰业务名 + 服务类型后缀 + `Svtp`
- 实现 id = 大驼峰业务名 + 服务类型后缀 + `Impl`

| 服务类型 | 接口 id 后缀 | 实现 id 后缀 | 示例 |
|---------|-------------|-------------|------|
| PBS | `PbsSvtp` | `PbsImpl` | `FtAcctgDealPbsSvtp` / `FtAcctgDealPbsImpl` |
| PCS | `PcsSvtp` | `PcsImpl` | `OrderSubmitPcsSvtp` / `OrderSubmitPcsImpl` |

### 字段必输说明

- **必输**：`required="true"`
- **非必输**（缺省）：`required="false"`

### 服务描述写法

```
服务：
{service的id} {service的name} {service中文名}
  描述：{可选描述}
  输入：{字段中文名1} 必输，{字段中文名2}
  输出：{字段中文名1}，{字段中文名2}
```

> - service 的 id 和 name 可省略，AI 根据中文名自动翻译
> - id 为大驼峰 + 服务类型后缀（如 `PbsSvtp`），name 为小驼峰
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

## 场景 1：创建基础服务（PBS）

### 指令模板

```
帮我创建 {英文名} {中文名} 基础服务，{领域}领域

服务：
{service中文名}
  输入：{字段}，{字段} 必输
  输出：{字段}
```

### 示例 1-A：单服务（含子目录）

```
帮我创建 FtAcctgDeal 福费延账务处理 基础服务，贷款领域，子目录 ft

服务：
ftAcctgDeal 福费延账务处理
  描述：福费延账务处理服务
  输入：币种代码
  输出：利息金额
```

### 示例 1-B：多服务

```
帮我创建 IoCpCustAccountQry 客户账户查询基础服务，存款领域

服务1：
QueryCustAcctPbsSvtp queryCustAcct 查询客户账户
  输入：客户编号 必输
  输出：账号

服务2：
QueryCustBalancePbsSvtp queryCustBalance 查询客户余额
  输入：账号 必输
  输出：可用余额
```

### 示例 1-C：不指定英文名

```
帮我创建 价格计算 基础服务，贷款领域

服务：
计算贷款价格
  输入：贷款金额 必输，币种代码
  输出：利息金额
```

> AI 自动翻译：服务英文名 `PriceCalc`，接口 id = `PriceCalcPbsSvtp`，service name = `calcLoanPrice`

### AI 返回格式示例

创建服务后，AI 会先询问：
```
是否同时创建该服务的实现文件？（Y/n）
```

用户确认后：
```
✅ 成功创建基础服务（接口 + 实现）

📁 接口文件: loan-pbs-api/src/main/resources/serviceType/ft/FtAcctgDeal.pbs.xml
📁 实现文件: loan-pbs-impl/src/main/resources/serviceimpl/ft/FtAcctgDeal.pbsImpl.xml
📦 接口 package: com.spdb.ccbs.loan.pbs.api.serviceType.ft
📦 实现 package: com.spdb.ccbs.loan.pbs.impl.serviceimpl.ft
🧩 服务: ftAcctgDeal（福费延账务处理）

📋 MCP 字段查询结果：
  ✅ 币种代码  →  type=MBaseType.U_BI_ZHONG_DAI_MA  ref=MDict.C.crcyCd
  ✅ 利息金额  →  type=MBaseType.U_JIN_E  ref=MDict.I.intrstAmt

✅ 所有字段均已写入 XML
```

---

## 场景 2：创建组合服务（PCS）

### 指令模板

```
帮我创建 {英文名} {中文名} 组合服务，{领域}领域

服务：
...
```

### 示例

```
帮我创建 OrderSubmit 订单提交 组合服务，贷款领域

服务：
submitOrder 提交订单
  输入：客户ID 必输，贷款金额 必输
  输出：申请编号
```

**生成结果**：
- 接口模块：`loan-pcs-api`
- 实现模块：`loan-pcs-impl`
- 接口文件：`loan-pcs-api/src/main/resources/serviceType/OrderSubmit.pcs.xml`
- 实现文件（用户确认时）：`loan-pcs-impl/src/main/resources/serviceimpl/OrderSubmit.pcsImpl.xml`
- 接口 id：`OrderSubmitPcsSvtp`

---

## 场景 3：含复合类型引用的服务

### 示例

```
帮我创建 GnfeeTrialChecks 保函费用试算校验 基础服务，结算领域，子目录 gnfee

服务：
保函费用试算校验
  输入：[保函费用试算输入]，币种代码
  输出：利息金额
```

> AI 搜索复合类型，找到 `GnFeeTrialType.GnFeeTrialApsInPojo`，自动生成 input 中的复合引用字段

**生成结果**：
- 接口模块：`sett-pbs-api`
- 实现模块：`sett-pbs-impl`

---

## 场景 4：在子目录下创建服务

### 指令模板

```
帮我创建 {英文名} {中文名} {服务类型}，{领域}领域，子目录 {子目录}

服务：
...
```

### 示例

```
帮我创建 FtAcctgDeal 福费延账务处理 基础服务，贷款领域，子目录 ft

服务：
福费延账务处理
  输入：币种代码
  输出：利息金额
```

**生成结果**：
- 接口文件：`loan-pbs-api/src/main/resources/serviceType/ft/FtAcctgDeal.pbs.xml`
- 实现文件（用户确认时）：`loan-pbs-impl/src/main/resources/serviceimpl/ft/FtAcctgDeal.pbsImpl.xml`
- 接口 package：`com.spdb.ccbs.loan.pbs.api.serviceType.ft`
- 实现 package：`com.spdb.ccbs.loan.pbs.impl.serviceimpl.ft`

---

## 场景 5：含数组字段的服务

### 示例

```
创建 ChargeCalc 费用计算 基础服务，贷款领域

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

**生成结果**：
- 接口模块：`loan-pbs-api`
- 实现模块：`loan-pbs-impl`

---

## 场景 6：修改现有服务

### 指令模板（新增服务）

```
修改 {英文名} {服务类型}，新增服务 {服务描述}
```

### 示例

```
修改 FtAcctgDeal 基础服务，新增服务：
ftRepayCalc 福费延还款计算
  输入：[福费延还款输入]
  输出：还款金额
```

> 修改会更新接口文件（新增 service）。若实现文件已存在，其 `serviceType` 引用无需变更；仅当服务 longname 变更时需同步更新实现的 longname。

---

## 常见错误与修正

### ❌ 服务类型未明确指定

| 错误输入 | 正确写法 |
|---------|---------|
| `帮我创建 xxx 服务` | `帮我创建 xxx 基础服务` 或 `帮我创建 xxx 组合服务` |

### ❌ 模块名错误

| 错误 | 正确 |
|------|------|
| 服务生成到其他模块（如 pbcb-api） | 服务必须生成在 `{领域}-{服务类型}-api`（如 loan-pbs-api） |
| 实现生成到其他模块 | 实现必须生成在 `{领域}-{服务类型}-impl`（如 loan-pbs-impl） |

### ❌ 字段未贯标

AI 会提示：
```
❌ 以下字段未贯标，已从 XML 中强制排除
```

**解决**：在 `dict-mcp-server` 字段管理系统中完成字段贯标后，重新执行指令。

### ❌ 复合类型引用未找到

AI 会提示：
```
❌ [xxx] → 未找到匹配的 c_schema.xml，已跳过
```

**解决**：确认对应的 `*.c_schema.xml` 复合类型文件已创建，且 `complexType` 的 `longname` 与中括号内的中文名**完全一致**。

### ❌ 创建时未确认实现文件

创建服务后 AI 会询问「是否同时创建该服务的实现文件？」。若用户选择否，则仅生成接口文件；后续可再次请求创建实现文件。

---

## 快速指令速查

| 场景 | 指令起始语 |
|------|-----------|
| 创建基础服务 | `帮我创建 {英文名} {中文名} 基础服务，{领域}领域` |
| 创建组合服务 | `帮我创建 {英文名} {中文名} 组合服务，{领域}领域` |
| 指定子目录 | 在末尾加：`，子目录 {子目录}` |
| 只有中文名 | 省略英文名，AI 自动翻译 |
| 含复合引用 | 字段行写 `[中文名]`，可加 `多值`/`必输` |
| 含数组字段 | `xxxArray xxx数组 start` ... `xxxArray xxx数组 end` |
| packMode | 输入/输出后加「（生成对应的输入/输出接口类）」 |
| 含描述 | 服务下加 `描述：{描述内容}` |
| 多服务 | 依次写 `服务1：` `服务2：` |
| 修改（新增服务） | `修改 {英文名} {类型}，新增服务 {描述}` |
| 配套创建实现 | 创建服务后 AI 会询问，用户确认 Y 则创建实现文件 |
