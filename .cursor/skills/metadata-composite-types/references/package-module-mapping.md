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

## 子包路径

复合类型通常按功能模块组织子包，直接追加到领域基础包后：

```
com.spdb.ccbs.loan.resources.type.ft.repay
                                  ↑   ↑
                              功能域 子模块
```

**示例**：

| SchemaId | 领域 | 完整 package |
|---------|------|-------------|
| FtAcctgType | 贷款（福费延） | com.spdb.ccbs.loan.resources.type.ft.repay |
| SyndAgrmLoanType | 贷款（银团） | com.spdb.ccbs.loan.resources.type.synd |
| CustInfoType | 平台公共 | com.spdb.ccbs.comm.resources.type.cust |

## 文件存放路径

```
{模块}/src/main/resources/type/{子路径}/{SchemaId}.c_schema.xml
```

**示例**：
```
loan-resources/src/main/resources/type/ft/repay/FtAcctgType.c_schema.xml
comm-resources/src/main/resources/type/cust/CustInfoType.c_schema.xml
```

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
