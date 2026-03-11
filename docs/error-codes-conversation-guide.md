# 错误码元数据 —— 对话指令指南

本文档为开发人员提供与 AI 对话创建/修改错误码元数据（`*.errors.xml`）的标准指令模板。

---

## 前置说明

### 领域与模块映射

| 领域 | resources 模块 | 默认文件路径 |
|------|--------------|-------------|
| 存款 | dept-resources | `dept-resources/src/main/resources/errors/` |
| 贷款 | loan-resources | `loan-resources/src/main/resources/errors/` |
| 结算 | sett-resources | `sett-resources/src/main/resources/errors/` |
| 平台公共 | comm-resources | `comm-resources/src/main/resources/errors/` |

### 参数占位符说明

- 错误信息中使用 `${xxx}` 表示动态参数
- 每个 `${xxx}` 需在错误码下方用 `参数：` 行定义其 id、中文名、类型
- 参数 id 必须与 `${xxx}` 中的 xxx 完全一致

### description 说明

- 描述为可选项，不提供则不生成 `<description>` 标签
- 文件级描述写在模块列表之前
- 模块级描述写在模块名称下方

---

## 场景 1：创建基本错误码（无参数）

### 指令模板

```
帮我创建 {ErrorConfId} {中文名}，{领域}领域

{模块id} {模块中文名}
  {错误码id} {错误信息}
  {错误码id} {错误信息}
```

### 示例

```
帮我创建 SettBaseError 结算基础错误码，结算领域

Pay 支付模块错误码
  E0001 交易金额不能为零！
  E0002 账户状态异常，无法完成交易！
  E0003 币种不匹配！
```

**AI 将生成**：`sett-resources/src/main/resources/errors/SettBaseError.errors.xml`

---

## 场景 2：创建含参数的错误码

### 指令模板

```
帮我创建 {ErrorConfId} {中文名}，{领域}领域

{模块id} {模块中文名}
  {错误码id} {含${参数}的错误信息}
    参数：{参数id} {参数中文名} {参数类型}
  {错误码id} {无参数错误信息}
```

### 示例

```
帮我创建 DeptAcctError 存款账户错误码，存款领域

AcctMgmt 账户管理模块错误码
  E0001 错误描述：[${errDesc}]
    参数：errDesc 错误描述 BaseType.U_LONG_DESC
  E0002 账户${acctNo}的金额${amt}超过限额！
    参数：acctNo 账号 BaseType.U_ZHANG_HAO
    参数：amt 金额 BaseType.U_JIN_E
  E0003 客户${custId}不存在！
    参数：custId 客户编号 BaseType.U_KE_HU_BIAN_HAO
  E0004 账户已冻结，无法操作！
```

**规则**：
- `E0001` 有 1 个参数 `${errDesc}` → 生成 1 个 `<parameter>` 标签
- `E0002` 有 2 个参数 `${acctNo}` 和 `${amt}` → 生成 2 个 `<parameter>` 标签
- `E0003` 有 1 个参数 `${custId}` → 生成 1 个 `<parameter>` 标签
- `E0004` 无参数 → `<error ... />` 自闭合

---

## 场景 3：多模块错误码

### 指令模板

```
帮我创建 {ErrorConfId} {中文名}，{领域}领域

描述：{文件级描述}

{模块1 id} {模块1中文名}
  描述：{模块1描述}
  {错误码条目...}

{模块2 id} {模块2中文名}
  描述：{模块2描述}
  {错误码条目...}
```

### 示例

```
帮我创建 AtLoanError 资产模块错误码，贷款领域

描述：资产模块错误码定义

Colt 抵押物模块错误码
  描述：抵押物模块错误码
  E0000 错误描述：[${chmiaosh}]
    参数：chmiaosh 错误描述 BaseType.U_LONG_DESC
  E00002 资产目前只支持负债结算！

Obsb 表外业务模块错误码
  描述：表外业务模块错误码
  E0000 错误描述：[${chmiaosh}]
    参数：chmiaosh 错误描述 BaseType.U_LONG_DESC
  E00002 资产目前只支持负债结算！
```

**AI 将生成**：`loan-resources/src/main/resources/errors/AtLoanError.errors.xml`

---

## 场景 4：含子目录

### 指令模板

```
帮我创建 {ErrorConfId} {中文名}，{领域}领域，子目录 {子目录}

{模块id} {模块中文名}
  {错误码条目...}
```

### 示例

```
帮我创建 CommAuthError 公共认证错误码，公共领域，子目录 auth

Auth 认证模块错误码
  描述：用户认证相关错误码
  E0001 用户名或密码错误！
  E0002 登录超时，请重新登录！
  E0003 无权限访问资源${resId}！
    参数：resId 资源标识 BaseType.U_RESOURCE_ID
```

**AI 将生成**：
- 文件路径：`comm-resources/src/main/resources/errors/auth/CommAuthError.errors.xml`
- package：`com.spdb.ccbs.comm.resources.errors.auth`

---

## 场景 5：仅提供中文名（无英文名）

### 示例

```
帮我创建 贷款还款错误码，贷款领域

Repay 还款模块错误码
  E0001 还款金额不能为零！
  E0002 借据${dueBillCd}已结清！
    参数：dueBillCd 借据编码 BaseType.U_DAI_KUAN_JIE_JU_BIAN_MA
```

**AI 处理**：
- 用户未指定英文名，翻译生成大驼峰：`LoanRepayError`
- errorConf id：`LoanRepayError`
- longname：`贷款还款错误码`

---

## 场景 6：修改现有错误码

### 指令模板

```
修改 {ErrorConfId} 错误码

在 {模块id} 模块下新增：
  {错误码id} {错误信息}
    参数：...
```

### 示例 6-A：新增错误码条目

```
修改 AtLoanError 错误码

在 Colt 模块下新增：
  E00003 抵押物估值${colVal}低于最低要求${minVal}！
    参数：colVal 抵押物估值 BaseType.U_JIN_E
    参数：minVal 最低估值 BaseType.U_JIN_E
```

### 示例 6-B：新增错误码模块

```
修改 AtLoanError 错误码

新增模块：
LoanFee 费用模块错误码
  描述：贷款费用相关错误码
  E0001 费用计算异常！
  E0002 费率${feeRate}超出范围！
    参数：feeRate 费率 BaseType.U_FEI_LV
```

---

## 常见问题

### ❌ 领域填写错误

| 错误输入 | 原因 | 正确写法 |
|---------|------|---------|
| `贷款domain` | 不识别英文 | `贷款领域` |
| `loan` | 不识别英文缩写 | `贷款领域` |
| `公共领域` | 非标准领域名 | `平台公共领域` |

### ❌ 参数 id 与占位符不一致

```
❌ 错误示例：
message="金额${amt}超限"，但参数写了 参数：amount 金额 BaseType.U_JIN_E
```

**注意**：参数 id 必须与 `${xxx}` 中的 `xxx` **完全一致**，上例应写 `参数：amt 金额 BaseType.U_JIN_E`。

### ❌ 遗漏参数定义

如果 message 中有 `${xxx}` 但未在下方提供 `参数：` 行，AI 会提示补充参数信息。

---

## 快速指令速查

| 场景 | 指令起始语 |
|------|-----------|
| 创建新错误码 | `帮我创建 {Id} {中文名}，{领域}领域` |
| 创建带子目录 | `帮我创建 {Id} {中文名}，{领域}领域，子目录 {子目录}` |
| 仅中文名 | `帮我创建 {中文名}，{领域}领域` |
| 修改错误码 | `修改 {Id} 错误码` |
| 新增模块 | `修改 {Id}，新增模块 {模块id} {模块名}` |
| 新增条目 | `修改 {Id}，在 {模块id} 下新增 {错误码}` |
| 含参数 | message 写 `${xxx}`，下方 `参数：xxx 中文名 类型` |
| 含描述 | 文件级 `描述：xxx`，模块级在模块名下写 `描述：xxx` |
