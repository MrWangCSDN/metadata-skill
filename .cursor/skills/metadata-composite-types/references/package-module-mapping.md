# 领域到包路径与模块映射

本文档说明复合类型（c_schema.xml）根据业务领域自动确定包路径和模块的规则。

## 核心映射表

| 领域 | resources 包路径 | beans 包路径 | resources 模块 | beans 模块 |
|------|-----------------|-------------|---------------|-----------|
| 存款 | com.spdb.ccbs.dept.resources.type | com.spdb.ccbs.dept.beans.type | dept-resources | dept-beans |
| 贷款 | com.spdb.ccbs.loan.resources.type | com.spdb.ccbs.loan.beans.type | loan-resources | loan-beans |
| 结算 | com.spdb.ccbs.sett.resources.type | com.spdb.ccbs.sett.beans.type | sett-resources | sett-beans |
| 平台公共 | com.spdb.ccbs.comm.resources.type | com.spdb.ccbs.comm.beans.type | comm-resources | comm-beans |

## resources 与 beans 的区别

- **resources**：存放复合类型 XML 定义文件（`.c_schema.xml`），即元数据来源
- **beans**：由 resources 生成的 Java Bean 类，通常由代码生成器产生

创建 `c_schema.xml` 时，`package` 属性填写 **resources** 对应的包路径。

## 文件存放路径规则

### 默认路径（未指定子目录）

文件直接创建在各模块的 `src/main/resources/type/` 根目录下：

```
{xxx-resources}/src/main/resources/type/{SchemaId}.c_schema.xml
```

**四领域默认路径**：

| 领域 | 默认文件路径 | 默认 package |
|------|------------|-------------|
| 存款 | `dept-resources/src/main/resources/type/{SchemaId}.c_schema.xml` | `com.spdb.ccbs.dept.resources.type` |
| 贷款 | `loan-resources/src/main/resources/type/{SchemaId}.c_schema.xml` | `com.spdb.ccbs.loan.resources.type` |
| 结算 | `sett-resources/src/main/resources/type/{SchemaId}.c_schema.xml` | `com.spdb.ccbs.sett.resources.type` |
| 平台公共 | `comm-resources/src/main/resources/type/{SchemaId}.c_schema.xml` | `com.spdb.ccbs.comm.resources.type` |

### 指定子目录

在 `src/main/resources/type/` 下创建子目录，**`package` 属性同步追加子目录**（`/` 转为 `.`）：

```
{xxx-resources}/src/main/resources/type/{子目录}/{SchemaId}.c_schema.xml
package = {领域基础包}.{子目录（用.分隔）}
```

**路径与 package 对应关系**：

| 子目录（路径） | 文件路径示例 | schema package |
|--------------|------------|----------------|
| `ft/repay` | `loan-resources/src/main/resources/type/ft/repay/FtAcctgType.c_schema.xml` | `com.spdb.ccbs.loan.resources.type.ft.repay` |
| `synd` | `loan-resources/src/main/resources/type/synd/SyndAgrmLoanType.c_schema.xml` | `com.spdb.ccbs.loan.resources.type.synd` |
| `cust` | `comm-resources/src/main/resources/type/cust/CustInfoType.c_schema.xml` | `com.spdb.ccbs.comm.resources.type.cust` |
| `acct/query` | `dept-resources/src/main/resources/type/acct/query/AcctQryType.c_schema.xml` | `com.spdb.ccbs.dept.resources.type.acct.query` |

**子目录规则**：
- 文件路径中使用 `/` 分隔（如 `ft/repay`）
- `package` 中使用 `.` 分隔（如 `ft.repay`）
- 子目录不存在时自动创建

## 快速参考

### 如何确定用哪个领域？

根据复合类型所属业务域判断：
- 存款类业务 → `dept`
- 贷款、融资类业务 → `loan`
- 结算、支付类业务 → `sett`
- 跨领域通用、平台工具类 → `comm`

### SchemaId 命名建议

- 大驼峰命名
- 以业务功能 + `Type` 结尾，例如：`FtAcctgType`、`CustInfoType`、`LoanApplType`
- 全局唯一（跨所有领域），创建前在工程内搜索确认无重复
