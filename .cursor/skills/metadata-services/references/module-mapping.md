# PBS/PCS 服务模块路径映射

> ⛔ **强制规则**：服务必须生成在 `{领域}-{服务类型}-api` 模块，服务实现必须生成在 `{领域}-{服务类型}-impl` 模块。不得使用其他模块名。

---

## 领域与服务类型

**领域**（4 个）：dept（存款）、loan（贷款）、sett（结算）、comm（公共）
**服务类型**（2 个）：pbs（基础服务）、pcs（组合服务）

---

## 模块命名规则（必须严格遵守）

| 文件类型 | 模块名格式 | 格式说明 |
|---------|-----------|---------|
| **服务（接口）** | `{领域}-{服务类型}-api` | 如 loan-pbs-api、sett-pcs-api |
| **服务实现** | `{领域}-{服务类型}-impl` | 如 loan-pbs-impl、sett-pcs-impl |

---

## 完整模块对照表

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

---

## 路径与 package

| 项目 | 接口 | 实现 |
|------|------|------|
| 工程 | ccbs-{领域}-api | ccbs-{领域}-impl |
| 模块 | **{领域}-{服务类型}-api** | **{领域}-{服务类型}-impl** |
| 路径 | `src/main/resources/serviceType/{子目录}` | `src/main/resources/serviceimpl/{子目录}` |
| 文件 | `{name}.{服务类型}.xml` | `{name}.{服务类型}Impl.xml` |
| package | `com.spdb.ccbs.{领域}.{服务类型}.api.servicetype.{子目录}` | `com.spdb.ccbs.{领域}.{服务类型}.impl.serviceimpl.{子目录}` |

---

## 示例 1：贷款领域 pbs，子目录 ft

| | 接口 | 实现 |
|--|------|------|
| 模块 | **loan-pbs-api** | **loan-pbs-impl** |
| 完整路径 | `loan-pbs-api/src/main/resources/serviceType/ft/FtAcctgDeal.pbs.xml` | `loan-pbs-impl/src/main/resources/serviceimpl/ft/FtAcctgDeal.pbsImpl.xml` |
| package | `com.spdb.ccbs.loan.pbs.api.servicetype.ft` | `com.spdb.ccbs.loan.pbs.impl.serviceimpl.ft` |

---

## 示例 2：结算领域 pcs，无子目录

| | 接口 | 实现 |
|--|------|------|
| 模块 | **sett-pcs-api** | **sett-pcs-impl** |
| 完整路径 | `sett-pcs-api/src/main/resources/serviceType/OrderSubmit.pcs.xml` | `sett-pcs-impl/src/main/resources/serviceimpl/OrderSubmit.pcsImpl.xml` |
| package | `com.spdb.ccbs.sett.pcs.api.servicetype` | `com.spdb.ccbs.sett.pcs.impl.serviceimpl` |

---

## 示例 3：存款领域 pbs，无子目录

| | 接口 | 实现 |
|--|------|------|
| 模块 | **dept-pbs-api** | **dept-pbs-impl** |
| 完整路径 | `dept-pbs-api/src/main/resources/serviceType/CustAccountQry.pbs.xml` | `dept-pbs-impl/src/main/resources/serviceimpl/CustAccountQry.pbsImpl.xml` |
| package | `com.spdb.ccbs.dept.pbs.api.servicetype` | `com.spdb.ccbs.dept.pbs.impl.serviceimpl` |

---

## 示例 4：公共领域 pcs，子目录 common

| | 接口 | 实现 |
|--|------|------|
| 模块 | **comm-pcs-api** | **comm-pcs-impl** |
| 完整路径 | `comm-pcs-api/src/main/resources/serviceType/common/CommonQuery.pcs.xml` | `comm-pcs-impl/src/main/resources/serviceimpl/common/CommonQuery.pcsImpl.xml` |
| package | `com.spdb.ccbs.comm.pcs.api.servicetype.common` | `com.spdb.ccbs.comm.pcs.impl.serviceimpl.common` |

---

## 快速对照：接口 vs 实现

| 对比项 | 接口 | 实现 |
|--------|------|------|
| 根标签 | `<serviceType>` | `<serviceImpl>` |
| 模块后缀 | `-api` | `-impl` |
| 路径 | `serviceType/` | `serviceimpl/` |
| package 关键词 | `api.servicetype` | `impl.serviceimpl` |
| 文件后缀 | `.{服务类型}.xml` | `.{服务类型}Impl.xml` |
| id 后缀 | `{Xxx}Svtp` | `{Xxx}Impl` |
| 实现引用 | 无 | `serviceType` 属性引用接口 id |

---

## 子目录规则

- 用户指定子目录 → 追加到路径和 package（`/` 转 `.`）
- 未指定 → 直接在 `serviceType/` 或 `serviceimpl/` 根目录
- **接口和实现的子目录保持一致**
- 子目录可以多级（如 `ft/repay`），package 追加为 `.ft.repay`
