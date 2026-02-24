# 复合类型元数据完整示例

## 示例 1：基本复合类型创建（含输入输出 Pojo）

**用户输入**：
```
帮我新建 FtAcctgType 福费延还款复合类型，贷款领域，子包 ft/repay

包含以下复合对象：

FtAcctRepayChkInPojo 福费延还款校验输入
  fRFTGDueBillCd  福费延借据编码  非必输
  fncgBsnID       融资业务编码    非必输

FtAcctRepayChkOutPojo 福费延还款校验输出
  fRFTGDueBillCd  福费延借据编码
  fncgBsnID       融资业务编码
```

**生成的 XML**：
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="FtAcctgType" package="com.spdb.ccbs.loan.resources.type.ft.repay" longname="福费延还款复合类型" classgen="auto" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <complexType abstract="false" dict="false" id="FtAcctRepayChkInPojo" introduct="false" localName="" longname="福费延还款校验输入" extension="" tags="">
        <element id="fRFTGDueBillCd" longname="福费延借据编码" type="MBaseType.U_DAI_KUAN_JIE_JU_BIAN_MA" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.F.fRFTGDueBillCd"/>
        <element id="fncgBsnID" longname="融资业务编码" type="MBaseType.U_RONG_ZI_YE_WU_BIAN_MA" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.F.fncgBsnID"/>
    </complexType>
    <complexType abstract="false" dict="false" id="FtAcctRepayChkOutPojo" introduct="false" localName="" longname="福费延还款校验输出" extension="" tags="">
        <element id="fRFTGDueBillCd" longname="福费延借据编码" type="MBaseType.U_DAI_KUAN_JIE_JU_BIAN_MA" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.F.fRFTGDueBillCd"/>
        <element id="fncgBsnID" longname="融资业务编码" type="MBaseType.U_RONG_ZI_YE_WU_BIAN_MA" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.F.fncgBsnID"/>
    </complexType>
</schema>
```

**文件路径**：`loan-resources/src/main/resources/type/ft/repay/FtAcctgType.c_schema.xml`

---

## 示例 2：含复合类型引用字段

**用户输入**：
```
帮我新建 SyndAgrmLoanType 银团贷款协议复合类型，贷款领域，子包 synd

包含以下复合对象：

SyndAgrmLoanQryOutPojo 银团贷款协议查询输出
  custId                  客户ID                  必输
  lstSyndAgrmLoanQryOutPojo  银团贷款出资份额信息  
    引用复合类型 SyndAgrmLoanType.SysdAgrmLoanInfoPojo，对象数组
```

**生成的 XML**：
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="SyndAgrmLoanType" package="com.spdb.ccbs.loan.resources.type.synd" longname="银团贷款协议复合类型" classgen="auto" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <complexType abstract="false" dict="false" id="SyndAgrmLoanQryOutPojo" introduct="false" localName="" longname="银团贷款协议查询输出" extension="" tags="">
        <element id="custId" longname="客户ID" type="MBaseType.U_KE_HU_BIAN_HAO" required="true" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.C.custId"/>
        <element id="lstSyndAgrmLoanQryOutPojo" longname="银团贷款出资份额信息" type="SyndAgrmLoanType.SysdAgrmLoanInfoPojo" required="false" multi="true" range="false" array="false" final="false" override="false" allowSubType="true" key="false"/>
    </complexType>
</schema>
```

**关键点**：
- `lstSyndAgrmLoanQryOutPojo` 是复合类型引用字段，`type` 使用 `SchemaId.ComplexTypeId` 格式
- 无 `ref` 属性
- `multi="true"` 表示这是一个 List（对象数组）

---

## 示例 3：含未贯标字段

**用户输入**：
```
帮我新建 CustInfoType 客户信息复合类型，平台公共领域

CustBaseInfoPojo 客户基础信息
  custId    客户ID    必输
  custName  客户名称  非必输
  unknownField  未知字段  非必输
```

**MCP 查询结果**：
```
custId    → ✅ 已贯标
custName  → ✅ 已贯标
unknownField → ❌ 返回 null（未贯标）
```

**生成的 XML**（未贯标字段强制排除）：
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="CustInfoType" package="com.spdb.ccbs.comm.resources.type.cust" longname="客户信息复合类型" classgen="auto" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <complexType abstract="false" dict="false" id="CustBaseInfoPojo" introduct="false" localName="" longname="客户基础信息" extension="" tags="">
        <element id="custId" longname="客户ID" type="MBaseType.U_KE_HU_BIAN_HAO" required="true" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.C.custId"/>
        <element id="custName" longname="客户名称" type="MBaseType.U_KE_HU_MING_CHENG" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.C.custName"/>
    </complexType>
</schema>
```

**AI 反馈**：
```
⚠️  以下字段未贯标，已从 XML 中强制排除（共 1 个）:
  1. unknownField（未知字段）← MCP 返回 null，未写入 XML

✅ 已成功写入字段（共 2 个）:
  - custId (客户ID)
  - custName (客户名称)

📁 文件位置: comm-resources/src/main/resources/type/cust/CustInfoType.c_schema.xml
```

---

## 示例 4：修改现有复合类型

**用户输入**：
```
修改 FtAcctgType 中的 FtAcctRepayChkInPojo，新增字段 applyDate 申请日期（非必输）
```

**处理流程**：
1. 定位 `FtAcctgType.c_schema.xml`
2. 读取原文件，保留 `schema` 标签所有属性
3. 调用 MCP 查询 `申请日期`
4. 仅更新 `FtAcctRepayChkInPojo` 的 `element` 列表，追加新字段
5. `FtAcctRepayChkOutPojo` 保持不变

**修改后**：
```xml
<complexType abstract="false" dict="false" id="FtAcctRepayChkInPojo" introduct="false" localName="" longname="福费延还款校验输入" extension="" tags="">
    <element id="fRFTGDueBillCd" longname="福费延借据编码" type="MBaseType.U_DAI_KUAN_JIE_JU_BIAN_MA" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.F.fRFTGDueBillCd"/>
    <element id="fncgBsnID" longname="融资业务编码" type="MBaseType.U_RONG_ZI_YE_WU_BIAN_MA" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.F.fncgBsnID"/>
    <element id="applyDate" longname="申请日期" type="MBaseType.U_RI_QI" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.A.applyDate"/>
</complexType>
```

---

## 示例 5：多领域示例对比

| 场景 | SchemaId | 领域 | package | 文件路径 |
|------|---------|------|---------|---------|
| 存款账户类型 | DeptAcctType | 存款 | com.spdb.ccbs.dept.resources.type | dept-resources/src/main/resources/type/DeptAcctType.c_schema.xml |
| 贷款申请类型 | LoanApplType | 贷款 | com.spdb.ccbs.loan.resources.type | loan-resources/src/main/resources/type/LoanApplType.c_schema.xml |
| 结算流水类型 | SettFlowType | 结算 | com.spdb.ccbs.sett.resources.type | sett-resources/src/main/resources/type/SettFlowType.c_schema.xml |
| 公共客户类型 | CommCustType | 平台公共 | com.spdb.ccbs.comm.resources.type | comm-resources/src/main/resources/type/CommCustType.c_schema.xml |

---

## 对话指令速查

| 场景 | 指令示例 |
|------|---------|
| 创建新文件 | `帮我新建 {SchemaId} {文件中文名}，{领域}领域` |
| 指定子包 | `帮我新建 {SchemaId} {中文名}，{领域}领域，子包 {子包路径}` |
| 修改某 complexType | `修改 {SchemaId} 中的 {ComplexTypeId}，{新增/删除/修改}字段 {字段描述}` |
| 删除某 complexType | `删除 {SchemaId} 中的 {ComplexTypeId}` |
| 删除整个文件 | `删除复合类型文件 {SchemaId}` |
