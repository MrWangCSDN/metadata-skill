# 表定义元数据 —— 对话指令指南

本文档为开发人员提供与 AI 对话创建/修改表定义元数据（`*.tables.xml`）的标准指令模板。

---

## 前置说明

### 领域与模块映射

| 领域 | 模块 | 默认文件路径 | 默认 package |
|------|------|-------------|-------------|
| 存款 | dept-bcc | `dept-bcc/src/main/resources/tables/` | `com.spdb.ccbs.dept.bcc.tables` |
| 贷款 | loan-bcc | `loan-bcc/src/main/resources/tables/` | `com.spdb.ccbs.loan.bcc.tables` |
| 结算 | sett-bcc | `sett-bcc/src/main/resources/tables/` | `com.spdb.ccbs.sett.bcc.tables` |
| 平台公共 | comm-bcc | `comm-bcc/src/main/resources/tables/` | `com.spdb.ccbs.comm.bcc.tables` |

### 字段修饰词说明

| 修饰词 | 含义 | 生成效果 |
|--------|------|---------|
| **主键** | 该字段为主键 | `primarykey="true"` + `nullable="false"`（强制） |
| **非空** | 不允许为空 | `nullable="false"` |
| `default="xxx"` | 指定默认值 | 追加 `default="xxx"` 属性 |
| 无修饰词 | 默认 | `nullable="true"`, `primarykey="false"`, 无 default |

> 「主键」隐含「非空」，无需重复标注。

### ODB 索引写法

```
ODB索引：
{索引id}  unique  {字段中文名1} {字段中文名2}  operate={操作1} {操作2}
{索引id}  index   {字段中文名}  operate={操作1} {操作2}
```

**unique 类型可用操作**：

| 中文 | 对应值 |
|------|--------|
| 单记录查询 | selectOne |
| 删除一条记录 | deleteOne |
| 单记录更新 | updateOne |
| 单记录查询（带锁） | selectOneWithLock |

**index 类型可用操作**：

| 中文 | 对应值 |
|------|--------|
| 查询第一条 | selectFirst |
| 多记录查询 | selectAll |
| 翻页查询 | selectPage |
| 多记录更新 | update |
| 删除多条记录 | delete |
| 游标处理 | selectCursor |
| 带总记录数的翻页查询 | selectPageWithCount |
| 批量更新 | updateBatch |

### 物理索引写法

```
物理索引：
{索引id}  primarykey  {字段中文名1} {字段中文名2}
{索引id}  unique      {字段中文名}
{索引id}  index       {字段中文名1} {字段中文名2}
```

> 物理索引无 operate，type 可选 `primarykey`、`unique`、`index`。

### ODB 索引 vs 物理索引关键区别

| 对比项 | ODB 索引 | 物理索引 |
|--------|---------|---------|
| 索引字段取值 | MCP 返回的 **id**（如 `custId`） | MCP 返回的 **dbname**（如 `CUST_ID`） |
| operate | ✅ 有 | ❌ 无 |
| type 可选值 | unique、index | primarykey、unique、index |

---

## 场景 1：创建新表定义（默认路径）

### 指令模板

```
帮我新建 {SchemaId} {表中文名}，{领域}领域

字段：
{字段中文名}  {主键/非空}  {default="xxx"}
...
```

### 示例 1-A：基本字段（含主键 + 默认值）

```
帮我新建 LoanAcctTable 贷款账户表，贷款领域

字段：
客户编号  主键
账号      主键
账户余额
币种代码  default="CNY"
```

### 示例 1-B：含非空字段

```
帮我新建 CustInfoTable 客户信息表，平台公共领域

字段：
客户编号  主键
客户名称  非空
证件类型
证件号码  非空
```

### 示例 1-C：用户未指定英文名（自动生成）

```
帮我新建 贷款还款流水表，贷款领域

字段：
客户编号  主键
还款日期  非空
还款金额
```

> AI 根据中文翻译自动生成 SchemaId：`LoanRepayFlowTable`

### AI 返回格式示例

```
✅ 成功创建表定义

📁 文件位置: loan-bcc/src/main/resources/tables/LoanAcctTable.tables.xml
📦 package:  com.spdb.ccbs.loan.bcc.tables
🏢 所属领域: 贷款领域

📋 MCP 字段查询结果：
  ✅ 客户编号  →  id=custId  type=MBaseType.U_KE_HU_BIAN_HAO  dbname=CUST_ID
  ✅ 账号      →  id=acctNo  type=MBaseType.U_ZHANG_HAO  dbname=ACCT_NO
  ✅ 账户余额  →  id=acctBal  type=MBaseType.U_JIN_E  dbname=ACCT_BAL
  ✅ 币种代码  →  id=crcyCd  type=MBaseType.U_BI_ZHONG_DAI_MA  dbname=CRCY_CD

✅ 所有字段均已写入 XML
```

---

## 场景 2：含 ODB 索引和物理索引

### 指令模板

```
帮我新建 {SchemaId} {表中文名}，{领域}领域

字段：
{字段中文名}  {主键/非空}
...

ODB索引：
{索引id}  {type}  {字段中文名列表}  operate={操作列表}
...

物理索引：
{索引id}  {type}  {字段中文名列表}
...
```

### 示例 2-A：完整索引

```
帮我新建 LoanAcctTable 贷款账户表，贷款领域

字段：
客户编号  主键
账号      主键
账户余额
币种代码  default="CNY"

ODB索引：
selectByCustIdAndAcctNo  unique  客户编号 账号  operate=单记录查询 删除一条记录 单记录更新 单记录查询（带锁）
selectByCustId  index  客户编号  operate=多记录查询 翻页查询

物理索引：
PK_LOAN_ACCT       primarykey  客户编号 账号
IDX_LOAN_ACCT_01   index       客户编号
```

### AI 返回格式示例

```
✅ 成功创建表定义

📁 文件位置: loan-bcc/src/main/resources/tables/LoanAcctTable.tables.xml

📋 MCP 字段查询结果：
  ✅ 客户编号  →  id=custId  dbname=CUST_ID
  ✅ 账号      →  id=acctNo  dbname=ACCT_NO
  ✅ 账户余额  →  id=acctBal  dbname=ACCT_BAL
  ✅ 币种代码  →  id=crcyCd  dbname=CRCY_CD

🗂️  ODB 索引（2个）：
  ✅ selectByCustIdAndAcctNo  unique  fields=custId acctNo
  ✅ selectByCustId           index   fields=custId

📊 物理索引（2个）：
  ✅ PK_LOAN_ACCT       primarykey  fields=CUST_ID ACCT_NO
  ✅ IDX_LOAN_ACCT_01   index       fields=CUST_ID

✅ 所有字段和索引均已写入 XML
```

---

## 场景 3：创建带子目录的表定义

### 指令模板

```
帮我新建 {SchemaId} {表中文名}，{领域}领域，子目录 {子目录}

字段：
{字段中文名}  {主键/非空}
...
```

### 示例 3-A：单级子目录

```
帮我新建 FtAcctTable 福费延账户表，贷款领域，子目录 ft

字段：
福费延借据编码  主键
融资业务编码    非空
币种代码
```

**生成结果**：
- 文件路径：`loan-bcc/src/main/resources/tables/ft/FtAcctTable.tables.xml`
- package：`com.spdb.ccbs.loan.bcc.tables.ft`

### 示例 3-B：多级子目录

```
帮我新建 FtRepayTable 福费延还款表，贷款领域，子目录 ft/repay

字段：
福费延借据编码  主键
还款日期        非空
还款金额
```

**生成结果**：
- 文件路径：`loan-bcc/src/main/resources/tables/ft/repay/FtRepayTable.tables.xml`
- package：`com.spdb.ccbs.loan.bcc.tables.ft.repay`

### AI 返回格式示例

```
✅ 成功创建表定义

📁 文件位置: loan-bcc/src/main/resources/tables/ft/FtAcctTable.tables.xml
📦 package:  com.spdb.ccbs.loan.bcc.tables.ft
🗂️  子目录:   ft
```

---

## 场景 4：修改现有表定义

### 指令模板（新增字段）

```
修改 {SchemaId}，新增字段 {字段中文名} {主键/非空}
```

### 指令模板（新增索引）

```
修改 {SchemaId}，新增 ODB索引 {索引描述}
修改 {SchemaId}，新增 物理索引 {索引描述}
```

### 示例 4-A：新增字段

```
修改 LoanAcctTable，新增字段 开户日期（非空）、账户状态 default="A"
```

### 示例 4-B：新增索引

```
修改 LoanAcctTable，新增 ODB索引：
selectByAcctNo  unique  账号  operate=单记录查询 单记录更新
```

> ⚠️ **说明**：修改指令只追加字段/索引，不影响原有内容。

### AI 返回格式示例

```
✅ 成功修改表定义

📁 文件位置: loan-bcc/src/main/resources/tables/LoanAcctTable.tables.xml

新增字段（共 2 个）:
  ✅ openDate（开户日期）- 非空
  ✅ acctSts（账户状态）- default="A"

📌 原有字段和索引保持不变
```

---

## 场景 5：综合场景（字段 + 索引 + 子目录）

```
帮我新建 SettFlowTable 结算流水表，结算领域，子目录 flow

字段：
流水号      主键
客户编号    非空
交易金额
交易日期    非空
币种代码    default="CNY"
交易状态    default="N"

ODB索引：
selectByFlowNo  unique  流水号  operate=单记录查询 单记录更新 删除一条记录 单记录查询（带锁）
selectByCustId  index   客户编号  operate=多记录查询 翻页查询 带总记录数的翻页查询
selectByDate    index   交易日期  operate=多记录查询

物理索引：
PK_SETT_FLOW       primarykey  流水号
IDX_SETT_FLOW_01   index       客户编号
IDX_SETT_FLOW_02   index       交易日期
```

---

## 常见错误与修正

### ❌ SchemaId 重复

```
❌ SchemaId 'LoanAcctTable' 已存在
   文件位置: loan-bcc/src/main/resources/tables/LoanAcctTable.tables.xml
```

**解决**：换一个全局唯一的 SchemaId，或改为修改现有文件。

### ❌ 字段未贯标

AI 会提示：
```
❌ 以下字段未贯标，已从 XML 中强制排除：
  1. 未知字段

💡 请在 dict-mcp-server 系统完成字段贯标后重新执行
```

**解决**：在 `dict-mcp-server` 字段管理系统中完成贯标后重新执行。

### ❌ 索引包含未贯标字段

AI 会提示：
```
❌ 以下索引因包含未贯标字段，未予创建：
  1. selectByAll（ODB索引，包含未贯标字段：未知字段）
  2. PK_TEST（物理索引，包含未贯标字段：未知字段）

💡 完成字段贯标后重新执行
```

**解决**：先完成缺失字段的贯标，再重新创建。

### ❌ 索引 id 未指定

索引 id 必须由用户显式指定，AI 不会自动生成。

```
❌ 索引缺少 id，请指定索引名称后重新执行

💡 正确写法：selectByCustId  index  客户编号  operate=多记录查询
```

### ❌ ODB 索引操作不匹配 type

| type 为 unique 时 | 不能使用 |
|---------|---------|
| selectAll / selectPage 等多记录操作 | ❌ 这些属于 index 类型 |

| type 为 index 时 | 不能使用 |
|---------|---------|
| selectOne / deleteOne 等单记录操作 | ❌ 这些属于 unique 类型 |

### ❌ 领域填写错误

| 错误输入 | 正确写法 |
|---------|---------|
| `loan` | `贷款领域` |
| `公共领域` | `平台公共领域` |

---

## 快速指令速查

| 场景 | 指令起始语 |
|------|-----------|
| 创建新表（默认路径） | `帮我新建 {SchemaId} {中文名}，{领域}领域` |
| 创建带子目录的表 | `帮我新建 {SchemaId} {中文名}，{领域}领域，子目录 {子目录}` |
| 只有中文名 | `帮我新建 {中文名}，{领域}领域`（自动生成英文名） |
| 修改表字段 | `修改 {SchemaId}，新增字段 {字段描述}` |
| 修改表索引 | `修改 {SchemaId}，新增 ODB索引/物理索引 {索引描述}` |
| 主键字段 | 字段行末加 `主键` |
| 非空字段 | 字段行末加 `非空` |
| 默认值 | 字段行末加 `default="xxx"` |
| ODB unique 索引 | `{id}  unique  {字段}  operate={操作}` |
| ODB index 索引 | `{id}  index   {字段}  operate={操作}` |
| 物理主键索引 | `{id}  primarykey  {字段}` |
| 物理普通索引 | `{id}  index       {字段}` |
