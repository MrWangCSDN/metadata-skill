# PBC 构件模块路径映射

## 领域

| 领域 | 缩写 |
|------|------|
| 存款 | dept |
| 贷款 | loan |
| 结算 | sett |
| 公共 | comm |

---

## 构件类型

| 构件类型 | 缩写 | 接口文件后缀 | 实现文件后缀 |
|---------|------|-------------|-------------|
| 业务构件 | pbcb | `.pbcb.xml` | `.pbcbImpl.xml` |
| 产品构件 | pbcp | `.pbcp.xml` | `.pbcpImpl.xml` |
| 公共构件 | pbcc | `.pbcc.xml` | `.pbccImpl.xml` |
| 技术构件 | pbct | `.pbct.xml` | `.pbctImpl.xml` |

---

## pbcb / pbcp 构件（业务构件/产品构件）

适用于所有领域（dept/loan/sett/comm）。

| 项目 | 接口 | 实现 |
|------|------|------|
| 工程 | ccbs-{领域}-impl | ccbs-{领域}-impl |
| 模块 | {领域}-{构件类型}-api | {领域}-{构件类型}-impl |
| 路径 | `src/main/resources/serviceType/{子目录}` | `src/main/resources/serviceimpl/{子目录}` |
| 文件 | `{name}.{构件类型}.xml` | `{name}.{构件类型}Impl.xml` |
| package | `com.spdb.ccbs.{领域}.{构件类型}.api.serviceType.{子目录}` | `com.spdb.ccbs.{领域}.{构件类型}.impl.serviceimpl.{子目录}` |

**示例 1**（存款领域 pbcb，子目录 acct）：

| | 接口 | 实现 |
|--|------|------|
| 模块 | dept-pbcb-api | dept-pbcb-impl |
| 文件 | `src/main/resources/serviceType/acct/CustAcctOpen.pbcb.xml` | `src/main/resources/serviceimpl/acct/CustAcctOpen.pbcbImpl.xml` |
| package | `com.spdb.ccbs.dept.pbcb.api.serviceType.acct` | `com.spdb.ccbs.dept.pbcb.impl.serviceimpl.acct` |

**示例 2**（贷款领域 pbcb，无子目录）：

| | 接口 | 实现 |
|--|------|------|
| 模块 | loan-pbcb-api | loan-pbcb-impl |
| 文件 | `src/main/resources/serviceType/LoanApply.pbcb.xml` | `src/main/resources/serviceimpl/LoanApply.pbcbImpl.xml` |
| package | `com.spdb.ccbs.loan.pbcb.api.serviceType` | `com.spdb.ccbs.loan.pbcb.impl.serviceimpl` |

**示例 3**（结算领域 pbcp，子目录 gnfee）：

| | 接口 | 实现 |
|--|------|------|
| 模块 | sett-pbcp-api | sett-pbcp-impl |
| 文件 | `src/main/resources/serviceType/gnfee/GnfeeCalc.pbcp.xml` | `src/main/resources/serviceimpl/gnfee/GnfeeCalc.pbcpImpl.xml` |
| package | `com.spdb.ccbs.sett.pbcp.api.serviceType.gnfee` | `com.spdb.ccbs.sett.pbcp.impl.serviceimpl.gnfee` |

---

## pbcc 构件（公共构件）

> ⛔ pbcc 仅存在于公共领域（comm），不适用于其他领域。

| 项目 | 接口 | 实现 |
|------|------|------|
| 工程 | ccbs-comm-api | ccbs-comm-impl |
| 模块 | comm-pbcc-api | comm-pbcc-impl |
| 路径 | `src/main/resources/serviceType/{子目录}` | `src/main/resources/serviceimpl/{子目录}` |
| 文件 | `{name}.pbcc.xml` | `{name}.pbccImpl.xml` |
| package | `com.spdb.ccbs.comm.pbcc.api.serviceType.{子目录}` | `com.spdb.ccbs.comm.pbcc.impl.serviceimpl.{子目录}` |

**示例**（公共领域 pbcc，子目录 cust）：

| | 接口 | 实现 |
|--|------|------|
| 模块 | comm-pbcc-api | comm-pbcc-impl |
| 文件 | `src/main/resources/serviceType/cust/CustInfoQry.pbcc.xml` | `src/main/resources/serviceimpl/cust/CustInfoQry.pbccImpl.xml` |
| package | `com.spdb.ccbs.comm.pbcc.api.serviceType.cust` | `com.spdb.ccbs.comm.pbcc.impl.serviceimpl.cust` |

**示例**（公共领域 pbcc，无子目录）：

| | 接口 | 实现 |
|--|------|------|
| 模块 | comm-pbcc-api | comm-pbcc-impl |
| 文件 | `src/main/resources/serviceType/CustInfoQry.pbcc.xml` | `src/main/resources/serviceimpl/CustInfoQry.pbccImpl.xml` |
| package | `com.spdb.ccbs.comm.pbcc.api.serviceType` | `com.spdb.ccbs.comm.pbcc.impl.serviceimpl` |

---

## 快速对照：接口 vs 实现

| 对比项 | 接口 | 实现 |
|--------|------|------|
| 根标签 | `<serviceType>` | `<serviceImpl>` |
| 模块后缀 | `-api` | `-impl` |
| 路径 | `serviceType/` | `serviceimpl/` |
| package 关键词 | `api.serviceType` | `impl.serviceimpl` |
| 文件后缀 | `.{构件类型}.xml` | `.{构件类型}Impl.xml` |
| serviceType id 后缀 | `{Xxx}Svtp` | `{Xxx}Impl` |
| service ref | 无 | 有（`{接口serviceType.id}.{接口service.id}`） |

---

## 子目录规则

- 用户指定子目录 → 追加到路径和 package（`/` 转 `.`）
- 未指定 → 直接在 `serviceType/` 或 `serviceimpl/` 根目录
- **接口和实现的子目录保持一致**
- 子目录可以多级（如 `ft/repay`），package 追加为 `.ft.repay`
