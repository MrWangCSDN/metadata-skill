# 构件与服务模块路径映射

## 领域

| 领域 | 缩写 | 说明 |
|------|------|------|
| 存款 | dept | — |
| 贷款 | loan | — |
| 结算 | sett | — |
| 平台公共 | comm | — |

> PBCC 公共构件**领域固定为 comm**。

---

## PBCB 基础构件

| 项目 | 接口 | 实现 |
|------|------|------|
| 工程 | ccbs-{领域}-impl | ccbs-{领域}-impl |
| 模块 | {领域}-pbcb-api | {领域}-pbcb-impl |
| 路径 | `src/main/resources/serviceType/{子目录}` | `src/main/resources/serviceimpl/{子目录}` |
| 文件 | `{name}.pbcb.xml` | `{name}.pbcbImpl.xml` |
| package | `com.spdb.ccbs.{领域}.pbcb.api.servicetype.{子目录}` | `com.spdb.ccbs.{领域}.pbcb.impl.serviceimpl.{子目录}` |

**示例**（贷款领域，子目录 ft）：

| | 接口 | 实现 |
|--|------|------|
| 模块 | loan-pbcb-api | loan-pbcb-impl |
| 文件 | `src/main/resources/serviceType/ft/LoanQuery.pbcb.xml` | `src/main/resources/serviceimpl/ft/LoanQuery.pbcbImpl.xml` |
| package | `com.spdb.ccbs.loan.pbcb.api.servicetype.ft` | `com.spdb.ccbs.loan.pbcb.impl.serviceimpl.ft` |

---

## PBCP 产品构件

| 项目 | 接口 | 实现 |
|------|------|------|
| 工程 | ccbs-{领域}-impl | ccbs-{领域}-impl |
| 模块 | {领域}-pbcp-api | {领域}-pbcp-impl |
| 路径 | `src/main/resources/serviceType/{子目录}` | `src/main/resources/serviceimpl/{子目录}` |
| 文件 | `{name}.pbcp.xml` | `{name}.pbcpImpl.xml` |
| package | `com.spdb.ccbs.{领域}.pbcp.api.servicetype.{子目录}` | `com.spdb.ccbs.{领域}.pbcp.impl.serviceimpl.{子目录}` |

---

## PBCC 公共构件（仅 comm 领域）

| 项目 | 接口 | 实现 |
|------|------|------|
| 工程 | ccbs-comm-api | ccbs-comm-impl |
| 模块 | comm-pbcc-api | comm-pbcc-impl |
| 路径 | `src/main/resources/serviceType/{子目录}` | `src/main/resources/serviceimpl/{子目录}` |
| 文件 | `{name}.pbcc.xml` | `{name}.pbccImpl.xml` |
| package | `com.spdb.ccbs.comm.pbcc.api.servicetype.{子目录}` | `com.spdb.ccbs.comm.pbcc.impl.serviceimpl.{子目录}` |

---

## PBCT 技术构件

| 项目 | 接口 | 实现 |
|------|------|------|
| 工程 | ccbs-{领域}-impl | ccbs-{领域}-impl |
| 模块 | {领域}-pbct-api | {领域}-pbct-impl |
| 路径 | `src/main/resources/serviceType/{子目录}` | `src/main/resources/serviceimpl/{子目录}` |
| 文件 | `{name}.pbct.xml` | `{name}.pbctImpl.xml` |
| package | `com.spdb.ccbs.{领域}.pbct.api.servicetype.{子目录}` | `com.spdb.ccbs.{领域}.pbct.impl.serviceimpl.{子目录}` |

---

## PBS 基础服务

| 项目 | 接口 | 实现 |
|------|------|------|
| 工程 | ccbs-{领域}-api | ccbs-{领域}-impl |
| 模块 | {领域}-pbs-api | {领域}-pbs-impl |
| 路径 | `src/main/resources/serviceType/{子目录}` | `src/main/resources/serviceimpl/{子目录}` |
| 文件 | `{name}.pbs.xml` | `{name}.pbsImpl.xml` |
| package | `com.spdb.ccbs.{领域}.pbs.api.servicetype.{子目录}` | `com.spdb.ccbs.{领域}.pbs.impl.serviceimpl.{子目录}` |

---

## PCS 组合服务

| 项目 | 接口 | 实现 |
|------|------|------|
| 工程 | ccbs-{领域}-api | ccbs-{领域}-impl |
| 模块 | {领域}-pcs-api | {领域}-pcs-impl |
| 路径 | `src/main/resources/serviceType/{子目录}` | `src/main/resources/serviceimpl/{子目录}` |
| 文件 | `{name}.pcs.xml` | `{name}.pcsImpl.xml` |
| package | `com.spdb.ccbs.{领域}.pcs.api.servicetype.{子目录}` | `com.spdb.ccbs.{领域}.pcs.impl.serviceimpl.{子目录}` |

---

## 快速对照：接口 vs 实现

| 对比项 | 接口 | 实现 |
|--------|------|------|
| 根标签 | `<serviceType>` | `<serviceImpl>` |
| 模块后缀 | `-api` | `-impl` |
| 路径 | `serviceType/` | `serviceimpl/` |
| package 关键词 | `api.servicetype` | `impl.serviceimpl` |
| 文件后缀 | `.pbcb.xml` 等 | `.pbcbImpl.xml` 等 |
| method ref | 无 | 有（`{接口id}.{方法id}`） |

## 子目录规则

- 用户指定子目录 → 追加到路径和 package（`/` 转 `.`）
- 未指定 → 直接在 `serviceType/` 或 `serviceimpl/` 根目录
- **接口和实现的子目录保持一致**
