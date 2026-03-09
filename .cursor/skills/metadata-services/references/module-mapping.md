# PBS/PCS 服务模块路径映射

## 领域

| 领域 | 缩写 |
|------|------|
| 存款 | dept |
| 贷款 | loan |
| 结算 | sett |
| 公共 | comm |

---

## 服务类型

| 服务类型 | 缩写 | 接口文件后缀 | 实现文件后缀 |
|---------|------|-------------|-------------|
| 基础服务 | pbs | `.pbs.xml` | `.pbsImpl.xml` |
| 组合服务 | pcs | `.pcs.xml` | `.pcsImpl.xml` |

---

## PBS / PCS 服务

适用于所有领域（dept/loan/sett/comm）。

| 项目 | 接口 | 实现 |
|------|------|------|
| 工程 | ccbs-{领域}-api | ccbs-{领域}-impl |
| 模块 | {领域}-{服务类型}-api | {领域}-{服务类型}-impl |
| 路径 | `src/main/resources/serviceType/{子目录}` | `src/main/resources/serviceimpl/{子目录}` |
| 文件 | `{name}.{服务类型}.xml` | `{name}.{服务类型}Impl.xml` |
| package | `com.spdb.ccbs.{领域}.{服务类型}.api.serviceType.{子目录}` | `com.spdb.ccbs.{领域}.{服务类型}.impl.serviceimpl.{子目录}` |

**示例 1**（贷款领域 pbs，子目录 ft）：

| | 接口 | 实现 |
|--|------|------|
| 模块 | loan-pbs-api | loan-pbs-impl |
| 文件 | `src/main/resources/serviceType/ft/FtAcctgDeal.pbs.xml` | `src/main/resources/serviceimpl/ft/FtAcctgDeal.pbsImpl.xml` |
| package | `com.spdb.ccbs.loan.pbs.api.serviceType.ft` | `com.spdb.ccbs.loan.pbs.impl.serviceimpl.ft` |

**示例 2**（贷款领域 pcs，无子目录）：

| | 接口 | 实现 |
|--|------|------|
| 模块 | loan-pcs-api | loan-pcs-impl |
| 文件 | `src/main/resources/serviceType/OrderSubmit.pcs.xml` | `src/main/resources/serviceimpl/OrderSubmit.pcsImpl.xml` |
| package | `com.spdb.ccbs.loan.pcs.api.serviceType` | `com.spdb.ccbs.loan.pcs.impl.serviceimpl` |

---

## 快速对照：接口 vs 实现

| 对比项 | 接口 | 实现 |
|--------|------|------|
| 根标签 | `<serviceType>` | `<serviceImpl>` |
| 模块后缀 | `-api` | `-impl` |
| 路径 | `serviceType/` | `serviceimpl/` |
| package 关键词 | `api.serviceType` | `impl.serviceimpl` |
| 文件后缀 | `.{服务类型}.xml` | `.{服务类型}Impl.xml` |
| serviceType id 后缀 | `{Xxx}Svtp` | `{Xxx}Impl` |
| 实现引用 | 无 | `serviceType` 属性引用接口 id |

---

## 子目录规则

- 用户指定子目录 → 追加到路径和 package（`/` 转 `.`）
- 未指定 → 直接在 `serviceType/` 或 `serviceimpl/` 根目录
- **接口和实现的子目录保持一致**
- 子目录可以多级（如 `ft/repay`），package 追加为 `.ft.repay`
