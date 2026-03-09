# PBS 基础服务 —— 对话指令指南

本文档为开发人员提供与 AI 对话创建/修改 PBS 基础服务元数据的标准指令模板。

> **关键提示**：每条指令以 `学习 metadata-pbs 的 skill，` 开头，确保 AI 正确加载基础服务相关规则。

---

## 前置说明

### PBS 基础服务概述

| 项目 | 说明 |
|------|------|
| 类型 | PBS（基础服务） |
| 定位 | 单一业务能力，供 PCS 组合服务调用 |
| 接口文件 | `{name}.pbs.xml` |
| 实现文件 | `{name}.pbsImpl.xml` |
| id 后缀 | `PbsSvtp`（如 `PriceCalcPbsSvtp`） |
| 实现 id | 接口 id + `Impl`（如 `PriceCalcPbsSvtpImpl`） |

> ⛔ 创建接口文件时**必须同时创建实现文件**，配套生成。

### 领域与模块映射

| 领域 | 接口模块 | 实现模块 |
|------|---------|---------|
| 存款 | dept-pbs-api | dept-pbs-impl |
| 贷款 | loan-pbs-api | loan-pbs-impl |
| 结算 | sett-pbs-api | sett-pbs-impl |
| 平台公共 | comm-pbs-api | comm-pbs-impl |

### 文件路径

- 接口：`{领域}-pbs-api/src/main/resources/serviceType/{子目录}/{name}.pbs.xml`
- 实现：`{领域}-pbs-impl/src/main/resources/serviceimpl/{子目录}/{name}.pbsImpl.xml`

---

## 场景 1：创建基础服务（默认路径）

### 指令模板

```
学习 metadata-pbs 的 skill，完成创建基础服务

帮我创建 {英文名} {中文名} 基础服务，{领域}领域

方法：
{方法英文名} {方法中文名}
  输入：{字段} 必输，{字段}
  输出：{字段}
```

### 示例 1-A：单方法

```
学习 metadata-pbs 的 skill，完成创建基础服务

帮我创建 PriceCalc 价格计算 基础服务，贷款领域

方法：
calcLoanPrice 计算贷款价格
  输入：贷款金额 必输，币种代码
  输出：利息金额，总金额
```

**生成结果**：
- 接口文件：`loan-pbs-api/src/main/resources/serviceType/PriceCalc.pbs.xml`
- 实现文件：`loan-pbs-impl/src/main/resources/serviceimpl/PriceCalc.pbsImpl.xml`
- id：`PriceCalcPbsSvtp`

### 示例 1-B：多方法

```
学习 metadata-pbs 的 skill，完成创建基础服务

帮我创建 LoanApprove 贷款审批 基础服务，贷款领域

方法：
approveLoan 审批贷款
  输入：客户ID 必输，贷款金额 必输
  输出：审批结果，审批意见

queryApproveStatus 查询审批状态
  输入：申请编号 必输
  输出：审批结果
```

### 示例 1-C：不指定英文名

```
学习 metadata-pbs 的 skill，完成创建基础服务

帮我创建 价格计算 基础服务，贷款领域

方法：
计算贷款价格
  输入：贷款金额 必输，币种代码
  输出：利息金额
```

> AI 自动翻译：英文名 `PriceCalc`，id = `PriceCalcPbsSvtp`，方法 id = `calcLoanPrice`

---

## 场景 2：创建带子目录的基础服务

### 指令模板

```
学习 metadata-pbs 的 skill，完成创建带子目录的基础服务

帮我创建 {英文名} {中文名} 基础服务，{领域}领域，子目录 {子目录}

方法：
...
```

### 示例 2-A：单级子目录

```
学习 metadata-pbs 的 skill，完成创建带子目录的基础服务

帮我创建 FtRepayCalc 福费延还款计算 基础服务，贷款领域，子目录 ft

方法：
calcRepay 计算还款
  输入：福费延借据编码 必输
  输出：还款金额
```

**生成结果**：
- 接口文件：`loan-pbs-api/src/main/resources/serviceType/ft/FtRepayCalc.pbs.xml`
- 实现文件：`loan-pbs-impl/src/main/resources/serviceimpl/ft/FtRepayCalc.pbsImpl.xml`
- 接口 package：`com.spdb.ccbs.loan.pbs.api.servicetype.ft`

### 示例 2-B：多级子目录

```
学习 metadata-pbs 的 skill，完成创建带子目录的基础服务

帮我创建 FtRepayQuery 福费延还款查询 基础服务，贷款领域，子目录 ft/repay

方法：
queryRepayInfo 查询还款信息
  输入：福费延借据编码 必输
  输出：还款金额，还款日期
```

**生成结果**：
- 接口 package：`com.spdb.ccbs.loan.pbs.api.servicetype.ft.repay`

---

## 场景 3：修改现有基础服务

### 指令模板

```
学习 metadata-pbs 的 skill，完成修改基础服务新增方法

修改 {英文名} 基础服务，新增方法：
{方法英文名} {方法中文名}
  输入：{字段} 必输，{字段}
  输出：{字段}
```

### 示例

```
学习 metadata-pbs 的 skill，完成修改基础服务新增方法

修改 PriceCalc 基础服务，新增方法：
queryPriceList 查询价格列表
  输入：产品编号 必输
  输出：利率，期限
```

> ⚠️ 修改会同时更新接口文件和实现文件。

---

## 快速指令速查

| 场景 | 指令 |
|------|------|
| 创建基础服务 | `学习 metadata-pbs 的 skill，完成创建基础服务` + 描述 |
| 带子目录 | 在描述末尾加：`，子目录 {子目录}` |
| 只有中文名 | 省略英文名，AI 自动翻译 |
| 修改基础服务 | `学习 metadata-pbs 的 skill，完成修改基础服务新增方法` + 描述 |
| 方法必输字段 | 字段后加 `必输` |
