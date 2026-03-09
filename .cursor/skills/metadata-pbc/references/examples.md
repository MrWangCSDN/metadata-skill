# PBC 构件完整示例

## 示例 1：创建业务构件（pbcb，含子目录）

### 用户输入

```
帮我创建 GnfeeTrialChecks 保函费用试算校验 业务构件，结算领域，子目录 gnfee

服务：
GnfeeTrialChecksPbcbSvtp gnfeeTrialChecks 保函费用试算校验
  描述：保函费用试算校验服务
  输入：[保函费用试算输入]，币种代码
  输出：利息金额
```

### 接口文件

**路径**：`sett-pbcb-api/src/main/resources/serviceType/gnfee/GnfeeTrialChecks.pbcb.xml`

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceType xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="GnfeeTrialChecksPbcbSvtp" kind="auto" longname="保函费用试算校验" package="com.spdb.ccbs.sett.pbcb.api.serviceType.gnfee" xsi:noNamespaceSchemaLocation="ltts-model.xsd" outbound="false">
    <service id="GnfeeTrialChecksPbcbSvtp" name="gnfeeTrialChecks" longname="保函费用试算校验">
        <description><![CDATA[保函费用试算校验服务]]></description>
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

**路径**：`sett-pbcb-impl/src/main/resources/serviceimpl/gnfee/GnfeeTrialChecks.pbcbImpl.xml`

```xml
<?xml  version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceImpl xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="GnfeeTrialChecksPbcbImpl" longname="保函费用试算校验类服务实现" serviceType="GnfeeTrialChecksPbcbSvtp" package="com.spdb.ccbs.sett.pbcb.impl.serviceimpl.gnfee" xsi:noNamespaceSchemaLocation="ltts-model.xsd"/>
```

> 创建构件后需询问用户「是否同时创建该构件的实现文件？」，用户确认后才生成上述文件。

---

## 示例 2：多 service 的业务构件（无子目录）

### 用户输入

```
创建 IoCpCustAccountQry 客户账户查询业务构件，存款领域

服务1：
QueryCustAcctPbcbSvtp queryCustAcct 查询客户账户
  输入：客户编号 必输
  输出：账号

服务2：
QueryCustBalancePbcbSvtp queryCustBalance 查询客户余额
  输入：账号 必输
  输出：可用余额
```

### 接口文件

**路径**：`dept-pbcb-api/src/main/resources/serviceType/IoCpCustAccountQry.pbcb.xml`

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceType xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="IoCpCustAccountQryPbcbSvtp" kind="auto" longname="客户账户查询业务构件" package="com.spdb.ccbs.dept.pbcb.api.serviceType" xsi:noNamespaceSchemaLocation="ltts-model.xsd" outbound="false">
    <service id="QueryCustAcctPbcbSvtp" name="queryCustAcct" longname="查询客户账户">
        <interface>
            <input packMode="false">
                <field id="custId" type="MBaseType.U_KE_HU_BIAN_HAO" required="true" multi="false" array="false" longname="客户编号" ref="MDict.C.custId"/>
            </input>
            <output asParm="false" packMode="false">
                <field id="acctNo" type="MBaseType.U_ZHANG_HAO" required="false" multi="false" array="false" longname="账号" ref="MDict.A.acctNo"/>
            </output>
        </interface>
    </service>
    <service id="QueryCustBalancePbcbSvtp" name="queryCustBalance" longname="查询客户余额">
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

**路径**：`dept-pbcb-impl/src/main/resources/serviceimpl/IoCpCustAccountQry.pbcbImpl.xml`

```xml
<?xml  version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceImpl xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="IoCpCustAccountQryPbcbImpl" longname="客户账户查询业务构件类服务实现" serviceType="IoCpCustAccountQryPbcbSvtp" package="com.spdb.ccbs.dept.pbcb.impl.serviceimpl" xsi:noNamespaceSchemaLocation="ltts-model.xsd"/>
```

---

## 示例 3：含数组字段的业务构件

### 用户输入

```
创建 ChargeCalc 费用计算 业务构件，贷款领域

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

**路径**：`loan-pbcb-api/src/main/resources/serviceType/ChargeCalc.pbcb.xml`

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceType xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="ChargeCalcPbcbSvtp" kind="auto" longname="费用计算" package="com.spdb.ccbs.loan.pbcb.api.serviceType" xsi:noNamespaceSchemaLocation="ltts-model.xsd" outbound="false">
    <service id="ChargeCalcPbcbSvtp" name="chargeCalc" longname="费用计算">
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

**路径**：`loan-pbcb-impl/src/main/resources/serviceimpl/ChargeCalc.pbcbImpl.xml`

```xml
<?xml  version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceImpl xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="ChargeCalcPbcbImpl" longname="费用计算类服务实现" serviceType="ChargeCalcPbcbSvtp" package="com.spdb.ccbs.loan.pbcb.impl.serviceimpl" xsi:noNamespaceSchemaLocation="ltts-model.xsd"/>
```

---

## 示例 4：公共构件（pbcc）

### 用户输入

```
创建 CustInfoQry 客户信息查询 公共构件，子目录 cust

服务：
queryCustInfo 查询客户信息
  输入：客户编号 必输
  输出：客户名称，客户状态
```

### 接口文件

**路径**：`comm-pbcc-api/src/main/resources/serviceType/cust/CustInfoQry.pbcc.xml`

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceType xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="CustInfoQryPbccSvtp" kind="auto" longname="客户信息查询" package="com.spdb.ccbs.comm.pbcc.api.serviceType.cust" xsi:noNamespaceSchemaLocation="ltts-model.xsd" outbound="false">
    <service id="CustInfoQryPbccSvtp" name="queryCustInfo" longname="查询客户信息">
        <interface>
            <input packMode="false">
                <field id="custId" type="MBaseType.U_KE_HU_BIAN_HAO" required="true" multi="false" array="false" longname="客户编号" ref="MDict.C.custId"/>
            </input>
            <output asParm="false" packMode="false">
                <field id="custName" type="MBaseType.U_KE_HU_MING_CHENG" required="false" multi="false" array="false" longname="客户名称" ref="MDict.C.custName"/>
                <field id="custSts" type="MBaseType.U_ZHUANG_TAI" required="false" multi="false" array="false" longname="客户状态" ref="MDict.C.custSts"/>
            </output>
        </interface>
    </service>
</serviceType>
```

### 实现文件（用户确认创建时）

**路径**：`comm-pbcc-impl/src/main/resources/serviceimpl/cust/CustInfoQry.pbccImpl.xml`

```xml
<?xml  version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceImpl xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="CustInfoQryPbccImpl" longname="客户信息查询类服务实现" serviceType="CustInfoQryPbccSvtp" package="com.spdb.ccbs.comm.pbcc.impl.serviceimpl.cust" xsi:noNamespaceSchemaLocation="ltts-model.xsd"/>
```

---

## 示例 5：含未贯标字段

### 用户输入

```
创建 LoanQuery 贷款查询 业务构件，贷款领域

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
<serviceType xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="LoanQueryPbcbSvtp" kind="auto" longname="贷款查询" package="com.spdb.ccbs.loan.pbcb.api.serviceType" xsi:noNamespaceSchemaLocation="ltts-model.xsd" outbound="false">
    <service id="LoanQueryPbcbSvtp" name="queryLoanInfo" longname="查询贷款信息">
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

## 示例 6：用户仅提供中文名

### 用户输入

```
帮我创建一个业务构件，保函费用试算校验，结算领域
```

### 处理逻辑

- 用户仅提供中文名「保函费用试算校验」
- 翻译生成英文名：`GnfeeTrialChecks`（大驼峰）
- 接口 id：`GnfeeTrialChecksPbcbSvtp`
- 实现 id：`GnfeeTrialChecksPbcbImpl`
- 后续 XML 生成同示例 1

---

## 示例 7：产品构件（pbcp）

### 用户输入

```
创建 IoAcctOpen 开户产品构件，存款领域，子目录 acct

服务：
openNewAcct 新开账户
  输入：客户编号 必输，账户类型 必输
  输出：账号
```

### 接口文件

**路径**：`dept-pbcp-api/src/main/resources/serviceType/acct/IoAcctOpen.pbcp.xml`

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceType xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="IoAcctOpenPbcpSvtp" kind="auto" longname="开户产品构件" package="com.spdb.ccbs.dept.pbcp.api.serviceType.acct" xsi:noNamespaceSchemaLocation="ltts-model.xsd" outbound="false">
    <service id="IoAcctOpenPbcpSvtp" name="openNewAcct" longname="新开账户">
        <interface>
            <input packMode="false">
                <field id="custId" type="MBaseType.U_KE_HU_BIAN_HAO" required="true" multi="false" array="false" longname="客户编号" ref="MDict.C.custId"/>
                <field id="acctTp" type="MBaseType.U_ZHANG_HU_LEI_XING" required="true" multi="false" array="false" longname="账户类型" ref="MDict.A.acctTp"/>
            </input>
            <output asParm="false" packMode="false">
                <field id="acctNo" type="MBaseType.U_ZHANG_HAO" required="false" multi="false" array="false" longname="账号" ref="MDict.A.acctNo"/>
            </output>
        </interface>
    </service>
</serviceType>
```

### 实现文件（用户确认创建时）

**路径**：`dept-pbcp-impl/src/main/resources/serviceimpl/acct/IoAcctOpen.pbcpImpl.xml`

```xml
<?xml  version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceImpl xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="IoAcctOpenPbcpImpl" longname="开户产品构件类服务实现" serviceType="IoAcctOpenPbcpSvtp" package="com.spdb.ccbs.dept.pbcp.impl.serviceimpl.acct" xsi:noNamespaceSchemaLocation="ltts-model.xsd"/>
```

---

## 对话指令速查表

| 场景 | 示例指令 |
|------|----------|
| 创建业务构件 | 「创建 XXX 业务构件」「新建 pbcb」 |
| 创建产品构件 | 「创建 XXX 产品构件」「新建 pbcp」 |
| 创建公共构件 | 「创建 XXX 公共构件」「新建 pbcc」 |
| 指定子目录 | 「子目录 gnfee」「放在 acct 下」 |
| 只有中文名 | 仅提供中文名 → 自动翻译为大驼峰 |
| 修改构件 | 「修改 GnfeeTrialChecks 业务构件」「在 XXX 里加一个服务」 |
| 配套创建实现 | 创建构件后询问「是否同时创建该构件的实现文件？」 |
| 含复合引用 | 「输入：[保函费用试算输入]，币种代码」 |
| 含数组字段 | 「xxxArray xxx数组 start ... end」 |
| packMode | 「生成对应的输入接口类」→ packMode=true |
