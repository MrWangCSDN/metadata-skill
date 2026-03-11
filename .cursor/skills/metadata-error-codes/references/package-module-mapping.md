# 错误码领域到包路径/模块映射

## 领域映射总表

| 领域 | 缩写 | resources 模块 | 默认文件路径 | 默认 package |
|------|------|--------------|-------------|-------------|
| 存款 | dept | dept-resources | `src/main/resources/errors/` | `com.spdb.ccbs.dept.resources.errors` |
| 贷款 | loan | loan-resources | `src/main/resources/errors/` | `com.spdb.ccbs.loan.resources.errors` |
| 结算 | sett | sett-resources | `src/main/resources/errors/` | `com.spdb.ccbs.sett.resources.errors` |
| 平台公共 | comm | comm-resources | `src/main/resources/errors/` | `com.spdb.ccbs.comm.resources.errors` |

## 子目录规则

| 条件 | 文件路径 | package |
|------|---------|---------|
| 无子目录 | `src/main/resources/errors/{Id}.errors.xml` | `com.spdb.ccbs.{领域}.resources.errors` |
| 有子目录 | `src/main/resources/errors/{子目录}/{Id}.errors.xml` | `com.spdb.ccbs.{领域}.resources.errors.{子目录}` |

> 子目录路径中 `/` 转换为 package 中的 `.`（如 `at/loan` → `at.loan`）。

## 示例

### 贷款领域，无子目录

```
模块：     loan-resources
文件路径： src/main/resources/errors/AtLoanError.errors.xml
package：  com.spdb.ccbs.loan.resources.errors
```

### 结算领域，子目录 gnfee

```
模块：     sett-resources
文件路径： src/main/resources/errors/gnfee/SettGnfeeError.errors.xml
package：  com.spdb.ccbs.sett.resources.errors.gnfee
```

### 公共领域，子目录 auth

```
模块：     comm-resources
文件路径： src/main/resources/errors/auth/CommAuthError.errors.xml
package：  com.spdb.ccbs.comm.resources.errors.auth
```
