# 领域到包路径与模块映射（表定义）

## 核心映射表

| 领域 | bcc 包路径 | bcc 模块 |
|------|-----------|---------|
| 存款 | `com.spdb.ccbs.dept.bcc.tables` | dept-bcc |
| 贷款 | `com.spdb.ccbs.loan.bcc.tables` | loan-bcc |
| 结算 | `com.spdb.ccbs.sett.bcc.tables` | sett-bcc |
| 平台公共 | `com.spdb.ccbs.comm.bcc.tables` | comm-bcc |

## 工程路径说明

表定义文件存放于 `ccbs-{领域}-impl` 工程下的 `{领域}-bcc` 模块：

```
ccbs-{领域}-impl/
└── {领域}-bcc/
    └── src/main/resources/tables/
        ├── {SchemaId}.tables.xml          ← 默认路径
        └── {子目录}/
            └── {SchemaId}.tables.xml      ← 指定子目录
```

## 默认路径（未指定子目录）

| 领域 | 文件路径 | package |
|------|---------|---------|
| 存款 | `dept-bcc/src/main/resources/tables/{SchemaId}.tables.xml` | `com.spdb.ccbs.dept.bcc.tables` |
| 贷款 | `loan-bcc/src/main/resources/tables/{SchemaId}.tables.xml` | `com.spdb.ccbs.loan.bcc.tables` |
| 结算 | `sett-bcc/src/main/resources/tables/{SchemaId}.tables.xml` | `com.spdb.ccbs.sett.bcc.tables` |
| 平台公共 | `comm-bcc/src/main/resources/tables/{SchemaId}.tables.xml` | `com.spdb.ccbs.comm.bcc.tables` |

## 指定子目录

```
文件路径：{领域}-bcc/src/main/resources/tables/{子目录}/{SchemaId}.tables.xml
package： com.spdb.ccbs.{领域}.bcc.tables.{子目录（/转.）}
```

| 子目录 | 文件路径示例 | package |
|--------|------------|---------|
| `ft` | `loan-bcc/src/main/resources/tables/ft/Ft_acct_table.tables.xml` | `com.spdb.ccbs.loan.bcc.tables.ft` |
| `ft/repay` | `loan-bcc/src/main/resources/tables/ft/repay/Ft_repay_table.tables.xml` | `com.spdb.ccbs.loan.bcc.tables.ft.repay` |
| `cust` | `comm-bcc/src/main/resources/tables/cust/Cust_info_table.tables.xml` | `com.spdb.ccbs.comm.bcc.tables.cust` |

## SchemaId 命名规则

- **蛇形命名法，首字母大写**（如 `Loan_acct_table`、`Cust_info_table`）
- 单词间用下划线 `_` 分隔，仅首字母大写，其余小写
- 全局唯一，创建前在工程内搜索确认无重复

## 如何确定领域？

- 存款类业务 → `dept`
- 贷款、融资类业务 → `loan`
- 结算、支付类业务 → `sett`
- 跨领域通用、平台工具类 → `comm`
