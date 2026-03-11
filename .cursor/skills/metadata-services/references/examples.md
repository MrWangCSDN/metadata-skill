# PBS/PCS 服务完整示例

## 示例 1：创建基础服务（pbs，含子目录）

### 用户输入

```
帮我创建 FtAcctgDeal 福费延账务处理 基础服务，贷款领域，子目录 ft

服务：
ftAcctgDeal 福费延账务处理
  描述：福费延账务处理服务
  输入：币种代码
  输出：利息金额
```

### 接口文件

**模块**：loan-pbs-api
**路径**：`loan-pbs-api/src/main/resources/serviceType/ft/FtAcctgDeal.pbs.xml`

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceType xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="FtAcctgDealPbsSvtp" kind="auto" longname="福费延账务处理" package="com.spdb.ccbs.loan.pbs.api.servicetype.ft" xsi:noNamespaceSchemaLocation="ltts-model.xsd" outbound="false">
    <service id="FtAcctgDealPbs" name="ftAcctgDeal" longname="福费延账务处理">
        <description><![CDATA[福费延账务处理服务]]></description>
        <interface>
            <input packMode="false">
                <field id="crcyCd" type="MBaseType.U_BI_ZHONG_DAI_MA" required="false" multi="false" array="false" longname="币种代码" ref="MDict.C.crcyCd"/>
            </input>
            <output asParm="false" packMode="false">
                <field id="intrstAmt" type="MBaseType.U_JIN_E" required="false" multi="false" array="false" longname="利息金额" ref="MDict.I.intrstAmt"/>
            </output>
        </interface>
    </service>
</serviceType>
```

### 实现文件（用户确认创建时）

**模块**：loan-pbs-impl
**路径**：`loan-pbs-impl/src/main/resources/serviceimpl/ft/FtAcctgDeal.pbsImpl.xml`

```xml
<?xml  version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceImpl xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="FtAcctgDealPbsImpl" longname="福费延账务处理类服务实现" serviceType="FtAcctgDealPbsSvtp" package="com.spdb.ccbs.loan.pbs.impl.serviceimpl.ft" xsi:noNamespaceSchemaLocation="ltts-model.xsd"/>
```

> 创建服务后需询问用户「是否同时创建该服务的实现文件？」，用户确认后才生成上述文件。

---

## 示例 2：创建组合服务（pcs，无子目录）

### 用户输入

```
创建 OrderSubmit 订单提交 组合服务，贷款领域

服务：
submitOrder 提交订单
  输入：客户ID 必输，贷款金额 必输
  输出：申请编号
```

### 接口文件

**模块**：loan-pcs-api
**路径**：`loan-pcs-api/src/main/resources/serviceType/OrderSubmit.pcs.xml`

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceType xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="OrderSubmitPcsSvtp" kind="auto" longname="订单提交" package="com.spdb.ccbs.loan.pcs.api.servicetype" xsi:noNamespaceSchemaLocation="ltts-model.xsd" outbound="false">
    <service id="OrderSubmitPcs" name="submitOrder" longname="提交订单">
        <interface>
            <input packMode="false">
                <field id="custId" type="MBaseType.U_KE_HU_BIAN_HAO" required="true" multi="false" array="false" longname="客户ID" ref="MDict.C.custId"/>
                <field id="loanAmount" type="MBaseType.U_JIN_E" required="true" multi="false" array="false" longname="贷款金额" ref="MDict.L.loanAmount"/>
            </input>
            <output asParm="false" packMode="false">
                <field id="applicationId" type="MBaseType.U_BIAN_HAO" required="false" multi="false" array="false" longname="申请编号" ref="MDict.A.applicationId"/>
            </output>
        </interface>
    </service>
</serviceType>
```

### 实现文件（用户确认创建时）

**模块**：loan-pcs-impl
**路径**：`loan-pcs-impl/src/main/resources/serviceimpl/OrderSubmit.pcsImpl.xml`

```xml
<?xml  version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceImpl xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="OrderSubmitPcsImpl" longname="订单提交类服务实现" serviceType="OrderSubmitPcsSvtp" package="com.spdb.ccbs.loan.pcs.impl.serviceimpl" xsi:noNamespaceSchemaLocation="ltts-model.xsd"/>
```

---

## 示例 3：含复合类型引用的基础服务

### 用户输入

```
创建 GnfeeTrialChecks 保函费用试算校验 基础服务，结算领域，子目录 gnfee

服务：
保函费用试算校验
  输入：[保函费用试算输入]，币种代码
  输出：利息金额
```

### 接口文件

**模块**：sett-pbs-api
**路径**：`sett-pbs-api/src/main/resources/serviceType/gnfee/GnfeeTrialChecks.pbs.xml`

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceType xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="GnfeeTrialChecksPbsSvtp" kind="auto" longname="保函费用试算校验" package="com.spdb.ccbs.sett.pbs.api.servicetype.gnfee" xsi:noNamespaceSchemaLocation="ltts-model.xsd" outbound="false">
    <service id="GnfeeTrialChecksPbs" name="gnfeeTrialChecks" longname="保函费用试算校验">
        <interface>
            <input packMode="false">
                <field id="gnFeeTrialApsInPojo" type="GnFeeTrialType.GnFeeTrialApsInPojo" required="false" multi="false" longname="保函费用试算输入"/>
                <field id="crcyCd" type="MBaseType.U_BI_ZHONG_DAI_MA" required="false" multi="false" array="false" longname="币种代码" ref="MDict.C.crcyCd"/>
            </input>
            <output asParm="false" packMode="false">
                <field id="intrstAmt" type="MBaseType.U_JIN_E" required="false" multi="false" array="false" longname="利息金额" ref="MDict.I.intrstAmt"/>
            </output>
        </interface>
    </service>
</serviceType>
```

### 实现文件（用户确认创建时）

**模块**：sett-pbs-impl
**路径**：`sett-pbs-impl/src/main/resources/serviceimpl/gnfee/GnfeeTrialChecks.pbsImpl.xml`

```xml
<?xml  version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceImpl xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="GnfeeTrialChecksPbsImpl" longname="保函费用试算校验类服务实现" serviceType="GnfeeTrialChecksPbsSvtp" package="com.spdb.ccbs.sett.pbs.impl.serviceimpl.gnfee" xsi:noNamespaceSchemaLocation="ltts-model.xsd"/>
```

---

## 示例 4：多 service 的基础服务

### 用户输入

```
创建 IoCpCustAccountQry 客户账户查询 基础服务，存款领域

服务1：
QueryCustAcctPbs queryCustAcct 查询客户账户
  输入：客户编号 必输
  输出：账号

服务2：
QueryCustBalancePbs queryCustBalance 查询客户余额
  输入：账号 必输
  输出：可用余额
```

### 接口文件

**模块**：dept-pbs-api
**路径**：`dept-pbs-api/src/main/resources/serviceType/IoCpCustAccountQry.pbs.xml`

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceType xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="IoCpCustAccountQryPbsSvtp" kind="auto" longname="客户账户查询基础服务" package="com.spdb.ccbs.dept.pbs.api.servicetype" xsi:noNamespaceSchemaLocation="ltts-model.xsd" outbound="false">
    <service id="QueryCustAcctPbs" name="queryCustAcct" longname="查询客户账户">
        <interface>
            <input packMode="false">
                <field id="custId" type="MBaseType.U_KE_HU_BIAN_HAO" required="true" multi="false" array="false" longname="客户编号" ref="MDict.C.custId"/>
            </input>
            <output asParm="false" packMode="false">
                <field id="acctNo" type="MBaseType.U_ZHANG_HAO" required="false" multi="false" array="false" longname="账号" ref="MDict.A.acctNo"/>
            </output>
        </interface>
    </service>
    <service id="QueryCustBalancePbs" name="queryCustBalance" longname="查询客户余额">
        <interface>
            <input packMode="false">
                <field id="acctNo" type="MBaseType.U_ZHANG_HAO" required="true" multi="false" array="false" longname="账号" ref="MDict.A.acctNo"/>
            </input>
            <output asParm="false" packMode="false">
                <field id="avlBal" type="MBaseType.U_JIN_E" required="false" multi="false" array="false" longname="可用余额" ref="MDict.A.avlBal"/>
            </output>
        </interface>
    </service>
</serviceType>
```

### 实现文件（用户确认创建时）

**模块**：dept-pbs-impl
**路径**：`dept-pbs-impl/src/main/resources/serviceimpl/IoCpCustAccountQry.pbsImpl.xml`

```xml
<?xml  version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceImpl xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="IoCpCustAccountQryPbsImpl" longname="客户账户查询基础服务类服务实现" serviceType="IoCpCustAccountQryPbsSvtp" package="com.spdb.ccbs.dept.pbs.impl.serviceimpl" xsi:noNamespaceSchemaLocation="ltts-model.xsd"/>
```

---

## 示例 5：含数组字段的基础服务

### 用户输入

```
创建 ChargeCalc 费用计算 基础服务，贷款领域

服务：
chargeCalc 费用计算
  输入：
    贷款合同号 必输
    chargCdArray 收费代码数组 start
        包含 收费项目编码 非必输
        包含 收费金额     必输
    chargCdArray 收费代码数组 end
  输出：总金额
```

### 接口文件

**模块**：loan-pbs-api
**路径**：`loan-pbs-api/src/main/resources/serviceType/ChargeCalc.pbs.xml`

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceType xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="ChargeCalcPbsSvtp" kind="auto" longname="费用计算" package="com.spdb.ccbs.loan.pbs.api.servicetype" xsi:noNamespaceSchemaLocation="ltts-model.xsd" outbound="false">
    <service id="ChargeCalcPbs" name="chargeCalc" longname="费用计算">
        <interface>
            <input packMode="false">
                <field id="loanCntrNo" type="MBaseType.U_HE_TONG_HAO" required="true" multi="false" array="false" longname="贷款合同号" ref="MDict.L.loanCntrNo"/>
                <fields id="chargCdArray" scope="" required="false" multi="true" array="false" longname="收费代码数组">
                    <field id="fPrjCd" type="MBaseType.U_SHOU_FEI_XIANG_MU_BIAN_MA" required="false" multi="false" array="false" longname="收费项目编码" ref="MDict.F.fPrjCd"/>
                    <field id="chrgAmt" type="MBaseType.U_JIN_E" required="true" multi="false" array="false" longname="收费金额" ref="MDict.C.chrgAmt"/>
                </fields>
            </input>
            <output asParm="false" packMode="false">
                <field id="totlAmt" type="MBaseType.U_JIN_E" required="false" multi="false" array="false" longname="总金额" ref="MDict.T.totlAmt"/>
            </output>
        </interface>
    </service>
</serviceType>
```

### 实现文件（用户确认创建时）

**模块**：loan-pbs-impl
**路径**：`loan-pbs-impl/src/main/resources/serviceimpl/ChargeCalc.pbsImpl.xml`

```xml
<?xml  version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceImpl xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="ChargeCalcPbsImpl" longname="费用计算类服务实现" serviceType="ChargeCalcPbsSvtp" package="com.spdb.ccbs.loan.pbs.impl.serviceimpl" xsi:noNamespaceSchemaLocation="ltts-model.xsd"/>
```

---

## 示例 6：用户仅提供中文名

### 用户输入

```
帮我创建一个基础服务，价格计算，贷款领域
```

### 处理逻辑

- 用户仅提供中文名「价格计算」
- 翻译生成英文名：`PriceCalc`（大驼峰）
- 接口 id：`PriceCalcPbsSvtp`
- 实现 id：`PriceCalcPbsImpl`
- 接口模块：`loan-pbs-api`
- 实现模块：`loan-pbs-impl`

---

## 示例 7：含未贯标字段

### 用户输入

```
创建 LoanQuery 贷款查询 基础服务，贷款领域

服务：
queryLoanInfo 查询贷款信息
  输入：贷款合同号 必输，自定义编号
  输出：贷款状态
```

### 说明

假设 MCP 查询结果：
- `贷款合同号` → 已贯标
- `自定义编号` → **未贯标**（MCP 返回 null）
- `贷款状态` → 已贯标

### 接口文件（未贯标字段不写入 XML）

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceType xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="LoanQueryPbsSvtp" kind="auto" longname="贷款查询" package="com.spdb.ccbs.loan.pbs.api.servicetype" xsi:noNamespaceSchemaLocation="ltts-model.xsd" outbound="false">
    <service id="LoanQueryPbs" name="queryLoanInfo" longname="查询贷款信息">
        <interface>
            <input packMode="false">
                <field id="loanCntrNo" type="MBaseType.U_HE_TONG_HAO" required="true" multi="false" array="false" longname="贷款合同号" ref="MDict.L.loanCntrNo"/>
            </input>
            <output asParm="false" packMode="false">
                <field id="loanSts" type="MBaseType.U_ZHUANG_TAI" required="false" multi="false" array="false" longname="贷款状态" ref="MDict.L.loanSts"/>
            </output>
        </interface>
    </service>
</serviceType>
```

### 工作台提示

```
📋 MCP 字段查询结果：
  ✅ 贷款合同号  →  type=MBaseType.U_HE_TONG_HAO  ref=MDict.L.loanCntrNo
  ❌ 自定义编号  →  未贯标（MCP 返回 null），已跳过
  ✅ 贷款状态    →  type=MBaseType.U_ZHUANG_TAI  ref=MDict.L.loanSts

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  以下字段未写入 XML，请确认后补充：

【未贯标字段】（MCP 返回 null，需完成贯标后重新执行）：
  1. 自定义编号

💡 完成上述问题后，可重新执行以补充这些字段。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 对话指令速查表

| 场景 | 示例指令 |
|------|----------|
| 创建基础服务 | 「创建 XXX 基础服务」「新建 pbs」 |
| 创建组合服务 | 「创建 XXX 组合服务」「新建 pcs」 |
| 指定子目录 | 「子目录 ft」「放在 gnfee 下」 |
| 只有中文名 | 仅提供中文名 → 自动翻译为大驼峰 |
| 修改服务 | 「修改 FtAcctgDeal 基础服务」「在 XXX 里加一个服务」 |
| 含复合引用 | 「输入：[保函费用试算输入]，币种代码」 |
| 含数组字段 | 「xxxArray xxx数组 start ... end」 |
| packMode | 「生成对应的输入接口类」→ packMode=true |
| 配套创建实现 | 创建服务后询问「是否同时创建该服务的实现文件？」 |
