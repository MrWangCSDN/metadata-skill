# PCS 组合服务 —— 对话指令指南

本文档为开发人员提供与 AI 对话创建/修改 PCS 组合服务元数据的标准指令模板。

> **关键提示**：每条指令以 `学习 metadata-pcs 的 skill，` 开头，确保 AI 正确加载组合服务相关规则。

---

## 前置说明

### PCS 组合服务概述

| 项目 | 说明 |
|------|------|
| 类型 | PCS（组合服务） |
| 定位 | 编排多个构件/服务，面向外部提供组合能力 |
| 接口文件 | `{name}.pcs.xml` |
| 实现文件 | `{name}.pcsImpl.xml` |
| id 后缀 | `PcsSvtp`（如 `OrderSubmitPcsSvtp`） |
| 实现 id | 接口 id + `Impl`（如 `OrderSubmitPcsSvtpImpl`） |

> ⛔ 创建接口文件时**必须同时创建实现文件**，配套生成。

### 领域与模块映射

| 领域 | 接口模块 | 实现模块 |
|------|---------|---------|
| 存款 | dept-pcs-api | dept-pcs-impl |
| 贷款 | loan-pcs-api | loan-pcs-impl |
| 结算 | sett-pcs-api | sett-pcs-impl |
| 平台公共 | comm-pcs-api | comm-pcs-impl |

### 文件路径

- 接口：`{领域}-pcs-api/src/main/resources/serviceType/{子目录}/{name}.pcs.xml`
- 实现：`{领域}-pcs-impl/src/main/resources/serviceimpl/{子目录}/{name}.pcsImpl.xml`

---

## 场景 1：创建组合服务（默认路径）

### 指令模板

```
学习 metadata-pcs 的 skill，完成创建组合服务

帮我创建 {英文名} {中文名} 组合服务，{领域}领域

方法：
{方法英文名} {方法中文名}
  输入：{字段} 必输，{字段}
  输出：{字段}
```

### 示例 1-A：单方法

```
学习 metadata-pcs 的 skill，完成创建组合服务

帮我创建 OrderSubmit 订单提交 组合服务，贷款领域

方法：
submitOrder 提交订单
  输入：客户ID 必输，贷款金额 必输
  输出：申请编号
```

**生成结果**：
- 接口文件：`loan-pcs-api/src/main/resources/serviceType/OrderSubmit.pcs.xml`
- 实现文件：`loan-pcs-impl/src/main/resources/serviceimpl/OrderSubmit.pcsImpl.xml`
- id：`OrderSubmitPcsSvtp`

### 示例 1-B：多方法

```
学习 metadata-pcs 的 skill，完成创建组合服务

帮我创建 LoanApply 贷款申请 组合服务，贷款领域

方法：
submitApply 提交申请
  输入：客户ID 必输，贷款金额 必输，贷款期限 必输
  输出：申请编号

queryApply 查询申请
  输入：申请编号 必输
  输出：申请状态，审批意见
```

### 示例 1-C：不指定英文名

```
学习 metadata-pcs 的 skill，完成创建组合服务

帮我创建 订单提交 组合服务，贷款领域

方法：
提交订单
  输入：客户ID 必输，贷款金额 必输
  输出：申请编号
```

> AI 自动翻译：英文名 `OrderSubmit`，id = `OrderSubmitPcsSvtp`，方法 id = `submitOrder`

---

## 场景 2：创建带子目录的组合服务

### 指令模板

```
学习 metadata-pcs 的 skill，完成创建带子目录的组合服务

帮我创建 {英文名} {中文名} 组合服务，{领域}领域，子目录 {子目录}

方法：
...
```

### 示例 2-A：单级子目录

```
学习 metadata-pcs 的 skill，完成创建带子目录的组合服务

帮我创建 FtOrderSubmit 福费延订单提交 组合服务，贷款领域，子目录 ft

方法：
submitFtOrder 提交福费延订单
  输入：客户ID 必输，福费延借据编码 必输
  输出：申请编号
```

**生成结果**：
- 接口文件：`loan-pcs-api/src/main/resources/serviceType/ft/FtOrderSubmit.pcs.xml`
- 实现文件：`loan-pcs-impl/src/main/resources/serviceimpl/ft/FtOrderSubmit.pcsImpl.xml`
- 接口 package：`com.spdb.ccbs.loan.pcs.api.servicetype.ft`

### 示例 2-B：多级子目录

```
学习 metadata-pcs 的 skill，完成创建带子目录的组合服务

帮我创建 FtRepaySubmit 福费延还款提交 组合服务，贷款领域，子目录 ft/repay

方法：
submitRepay 提交还款
  输入：福费延借据编码 必输，还款金额 必输
  输出：还款流水号
```

**生成结果**：
- 接口 package：`com.spdb.ccbs.loan.pcs.api.servicetype.ft.repay`

---

## 场景 3：修改现有组合服务

### 指令模板

```
学习 metadata-pcs 的 skill，完成修改组合服务新增方法

修改 {英文名} 组合服务，新增方法：
{方法英文名} {方法中文名}
  输入：{字段} 必输，{字段}
  输出：{字段}
```

### 示例

```
学习 metadata-pcs 的 skill，完成修改组合服务新增方法

修改 OrderSubmit 组合服务，新增方法：
cancelOrder 取消订单
  输入：申请编号 必输
  输出：取消结果
```

> ⚠️ 修改会同时更新接口文件和实现文件。

---

## 快速指令速查

| 场景 | 指令 |
|------|------|
| 创建组合服务 | `学习 metadata-pcs 的 skill，完成创建组合服务` + 描述 |
| 带子目录 | 在描述末尾加：`，子目录 {子目录}` |
| 只有中文名 | 省略英文名，AI 自动翻译 |
| 修改组合服务 | `学习 metadata-pcs 的 skill，完成修改组合服务新增方法` + 描述 |
| 方法必输字段 | 字段后加 `必输` |
