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

**路径**：`loan-pbs-api/src/main/resources/serviceType/ft/FtAcctgDeal.pbs.xml`

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceType xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="FtAcctgDealPbsSvtp" kind="auto" longname="福费延账务处理" package="com.spdb.ccbs.loan.pbs.api.serviceType.ft" xsi:noNamespaceSchemaLocation="ltts-model.xsd" outbound="false">
    <service id="FtAcctgDealPbsSvtp" name="ftAcctgDeal" longname="福费延账务处理">
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

**路径**：`loan-pbs-impl/src/main/resources/serviceimpl/ft/FtAcctgDeal.pbsImpl.xml`

```xml
<?xml  version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceImpl xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="FtAcctgDealPbsImpl" longname="福费延账务处理类服务实现" serviceType="FtAcctgDealPbsSvtp" package="com.spdb.ccbs.loan.pbs.impl.serviceimpl.ft" xsi:noNamespaceSchemaLocation="ltts-model.xsd"/>
```

> 创建服务后需询问用户「是否同时创建该服务的实现文件？」，用户确认后才生成上述文件。

---

## 示例 2：创建组合服务（pcs）

### 用户输入

```
创建 OrderSubmit 订单提交 组合服务，贷款领域

服务：
submitOrder 提交订单
  输入：客户ID 必输，贷款金额 必输
  输出：申请编号
```

### 接口文件

**路径**：`loan-pcs-api/src/main/resources/serviceType/OrderSubmit.pcs.xml`

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceType xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="OrderSubmitPcsSvtp" kind="auto" longname="订单提交" package="com.spdb.ccbs.loan.pcs.api.serviceType" xsi:noNamespaceSchemaLocation="ltts-model.xsd" outbound="false">
    <service id="OrderSubmitPcsSvtp" name="submitOrder" longname="提交订单">
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

**路径**：`loan-pcs-impl/src/main/resources/serviceimpl/OrderSubmit.pcsImpl.xml`

```xml
<?xml  version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceImpl xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="OrderSubmitPcsImpl" longname="订单提交类服务实现" serviceType="OrderSubmitPcsSvtp" package="com.spdb.ccbs.loan.pcs.impl.serviceimpl" xsi:noNamespaceSchemaLocation="ltts-model.xsd"/>
```

---

## 示例 3：含复合类型引用的基础服务

### 用户输入

```
创建 GnfeeTrialChecks 保函费用试算校验 基础服务，结算领域

服务：
保函费用试算校验
  输入：[保函费用试算输入]，币种代码
  输出：利息金额
```

### 接口文件（input 含复合引用）

```xml
<input packMode="false">
    <field id="gnFeeTrialApsInPojo" type="GnFeeTrialType.GnFeeTrialApsInPojo" required="false" multi="false" longname="保函费用试算输入"/>
    <field id="crcyCd" type="MBaseType.U_BI_ZHONG_DAI_MA" required="false" multi="false" array="false" longname="币种代码" ref="MDict.C.crcyCd"/>
</input>
```

---

## 对话指令速查表

| 场景 | 示例指令 |
|------|----------|
| 创建基础服务 | 「创建 XXX 基础服务」「新建 pbs」 |
| 创建组合服务 | 「创建 XXX 组合服务」「新建 pcs」 |
| 指定子目录 | 「子目录 ft」「放在 ft 下」 |
| 只有中文名 | 仅提供中文名 → 自动翻译为大驼峰 |
| 修改服务 | 「修改 FtAcctgDeal 基础服务」「在 XXX 里加一个服务」 |
| 含复合引用 | 「输入：[保函费用试算输入]，币种代码」 |
| 含数组字段 | 「xxxArray xxx数组 start ... end」 |
| packMode | 「生成对应的输入接口类」→ packMode=true |
| 配套创建实现 | 创建服务后询问「是否同时创建该服务的实现文件？」 |
