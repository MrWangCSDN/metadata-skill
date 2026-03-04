# 构件与服务元数据完整示例

## 示例 1：创建 PBCB 基础构件（含 2 个方法）

**用户输入**：
```
帮我创建 LoanQuery 贷款查询 基础构件，贷款领域

方法：
queryLoanInfo 查询贷款信息
  输入：客户ID 必输，贷款编号 必输
  输出：贷款金额，币种代码

queryLoanList 查询贷款列表
  输入：客户ID 必输
  输出：贷款金额
```

**生成的接口文件** — `loan-pbcb-api/src/main/resources/serviceType/LoanQuery.pbcb.xml`：
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceType xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="LoanQueryPbcbSvtp" kind="auto" longname="贷款查询基础构件" package="com.spdb.ccbs.loan.pbcb.api.servicetype" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <method id="queryLoanInfo" longname="查询贷款信息">
        <input packMode="true">
            <field id="custId" type="MBaseType.U_KE_HU_BIAN_HAO" required="true" multi="false" array="false" longname="客户ID" ref="MDict.C.custId"/>
            <field id="loanNo" type="MBaseType.U_DAI_KUAN_BIAN_HAO" required="true" multi="false" array="false" longname="贷款编号" ref="MDict.L.loanNo"/>
        </input>
        <output asParm="true" packMode="true">
            <field id="loanAmount" type="MBaseType.U_JIN_E" required="false" multi="false" array="false" longname="贷款金额" ref="MDict.L.loanAmount"/>
            <field id="crcyCd" type="MBaseType.U_BI_ZHONG_DAI_MA" required="false" multi="false" array="false" longname="币种代码" ref="MDict.C.crcyCd"/>
        </output>
    </method>
    <method id="queryLoanList" longname="查询贷款列表">
        <input packMode="true">
            <field id="custId" type="MBaseType.U_KE_HU_BIAN_HAO" required="true" multi="false" array="false" longname="客户ID" ref="MDict.C.custId"/>
        </input>
        <output asParm="true" packMode="true">
            <field id="loanAmount" type="MBaseType.U_JIN_E" required="false" multi="false" array="false" longname="贷款金额" ref="MDict.L.loanAmount"/>
        </output>
    </method>
</serviceType>
```

**同时生成的实现文件** — `loan-pbcb-impl/src/main/resources/serviceimpl/LoanQuery.pbcbImpl.xml`：
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceImpl xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="LoanQueryPbcbSvtpImpl" kind="auto" longname="贷款查询基础构件实现" package="com.spdb.ccbs.loan.pbcb.impl.serviceimpl" ref="LoanQueryPbcbSvtp" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <method id="queryLoanInfo" longname="查询贷款信息" ref="LoanQueryPbcbSvtp.queryLoanInfo">
    </method>
    <method id="queryLoanList" longname="查询贷款列表" ref="LoanQueryPbcbSvtp.queryLoanList">
    </method>
</serviceImpl>
```

**AI 返回**：
```
✅ 成功创建基础构件（接口 + 实现）

📁 接口文件: loan-pbcb-api/src/main/resources/serviceType/LoanQuery.pbcb.xml
📁 实现文件: loan-pbcb-impl/src/main/resources/serviceimpl/LoanQuery.pbcbImpl.xml
📦 接口 package: com.spdb.ccbs.loan.pbcb.api.servicetype
📦 实现 package: com.spdb.ccbs.loan.pbcb.impl.serviceimpl
🧩 方法: queryLoanInfo、queryLoanList

✅ 所有字段均已写入 XML
```

---

## 示例 2：创建 PBCC 公共构件（领域固定 comm）

**用户输入**：
```
帮我创建 DateUtil 日期工具 公共构件

方法：
formatDate 格式化日期
  输入：日期 必输
  输出：格式化结果
```

**关键说明**：
- PBCC 公共构件领域固定为 comm，无需指定
- id = `DateUtilPbccSvtp`
- 接口模块：`comm-pbcc-api`，实现模块：`comm-pbcc-impl`

---

## 示例 3：创建 PBS 基础服务（含子目录）

**用户输入**：
```
帮我创建 PriceCalc 价格计算 基础服务，贷款领域，子目录 ft

方法：
calcLoanPrice 计算贷款价格
  输入：贷款金额 必输，币种代码
  输出：利息金额，总金额
```

**生成结果**：
- 接口文件：`loan-pbs-api/src/main/resources/serviceType/ft/PriceCalc.pbs.xml`
- 实现文件：`loan-pbs-impl/src/main/resources/serviceimpl/ft/PriceCalc.pbsImpl.xml`
- 接口 package：`com.spdb.ccbs.loan.pbs.api.servicetype.ft`
- 实现 package：`com.spdb.ccbs.loan.pbs.impl.serviceimpl.ft`
- 接口 id：`PriceCalcPbsSvtp`
- 实现 id：`PriceCalcPbsSvtpImpl`

---

## 示例 4：创建 PCS 组合服务

**用户输入**：
```
帮我创建 OrderSubmit 订单提交 组合服务，贷款领域

方法：
submitOrder 提交订单
  输入：客户ID 必输，贷款金额 必输
  输出：申请编号
```

**生成的接口文件** — `loan-pcs-api/src/main/resources/serviceType/OrderSubmit.pcs.xml`：
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceType xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="OrderSubmitPcsSvtp" kind="auto" longname="订单提交组合服务" package="com.spdb.ccbs.loan.pcs.api.servicetype" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <method id="submitOrder" longname="提交订单">
        <input packMode="true">
            <field id="custId" type="MBaseType.U_KE_HU_BIAN_HAO" required="true" multi="false" array="false" longname="客户ID" ref="MDict.C.custId"/>
            <field id="loanAmount" type="MBaseType.U_JIN_E" required="true" multi="false" array="false" longname="贷款金额" ref="MDict.L.loanAmount"/>
        </input>
        <output asParm="true" packMode="true">
            <field id="applicationId" type="MBaseType.U_BIAN_HAO" required="false" multi="false" array="false" longname="申请编号" ref="MDict.A.applicationId"/>
        </output>
    </method>
</serviceType>
```

**同时生成的实现文件** — `loan-pcs-impl/src/main/resources/serviceimpl/OrderSubmit.pcsImpl.xml`：
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceImpl xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="OrderSubmitPcsSvtpImpl" kind="auto" longname="订单提交组合服务实现" package="com.spdb.ccbs.loan.pcs.impl.serviceimpl" ref="OrderSubmitPcsSvtp" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <method id="submitOrder" longname="提交订单" ref="OrderSubmitPcsSvtp.submitOrder">
    </method>
</serviceImpl>
```

---

## 示例 5：含未贯标字段

**用户输入**：
```
帮我创建 TestQuery 测试查询 基础构件，贷款领域

方法：
queryTest 查询测试
  输入：客户ID 必输，未知字段
  输出：测试结果
```

**工作台展示**：
```
📋 MCP 字段查询结果：
  ✅ 客户ID    →  id=custId  type=MBaseType.U_KE_HU_BIAN_HAO  ref=MDict.C.custId
  ❌ 未知字段  →  未贯标（MCP 返回 null），已跳过
  ❌ 测试结果  →  未贯标（MCP 返回 null），已跳过

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  以下字段未写入 XML，请确认后补充：

【未贯标字段】（MCP 返回 null，需完成贯标后重新执行）：
  1. 未知字段（queryTest 输入）
  2. 测试结果（queryTest 输出）

💡 完成上述问题后，可重新执行以补充。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 示例 6：用户未指定英文名

**用户输入**：
```
帮我创建 贷款还款处理 基础构件，贷款领域

方法：
还款校验
  输入：客户ID 必输
  输出：校验结果
```

**处理**：
- 构件英文名根据中文翻译：`LoanRepayProcess`
- 接口 id：`LoanRepayProcessPbcbSvtp`
- 方法 id 根据中文翻译：`repayCheck`（小驼峰）

---

## 对话指令速查

| 场景 | 指令起始语 |
|------|-----------|
| 创建基础构件 | `帮我创建 {英文名} {中文名} 基础构件，{领域}领域` |
| 创建产品构件 | `帮我创建 {英文名} {中文名} 产品构件，{领域}领域` |
| 创建公共构件 | `帮我创建 {英文名} {中文名} 公共构件`（领域固定 comm） |
| 创建技术构件 | `帮我创建 {英文名} {中文名} 技术构件，{领域}领域` |
| 创建基础服务 | `帮我创建 {英文名} {中文名} 基础服务，{领域}领域` |
| 创建组合服务 | `帮我创建 {英文名} {中文名} 组合服务，{领域}领域` |
| 指定子目录 | 在末尾加：`，子目录 {子目录}` |
| 只有中文名 | 省略英文名，AI 自动翻译生成 |
| 修改构件/服务 | `修改 {英文名} 基础构件/服务，新增方法 {方法描述}` |
