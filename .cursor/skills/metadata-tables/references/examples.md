# 表定义元数据完整示例

## 示例 1：基本表定义（含主键 + 普通字段）

**用户输入**：
```
帮我新建 Loan_acct_table 贷款账户表，贷款领域

字段：
客户编号  主键
账号      主键
账户余额
币种代码  default="CNY"
```

**MCP 查询结果展示**：
```
📋 MCP 字段查询结果：
  ✅ 客户编号  →  id=custId  type=MBaseType.U_KE_HU_BIAN_HAO  ref=MDict.C.custId  dbname=CUST_ID
  ✅ 账号      →  id=acctNo  type=MBaseType.U_ZHANG_HAO  ref=MDict.A.acctNo  dbname=ACCT_NO
  ✅ 账户余额  →  id=acctBal  type=MBaseType.U_JIN_E  ref=MDict.A.acctBal  dbname=ACCT_BAL
  ✅ 币种代码  →  id=crcyCd  type=MBaseType.U_BI_ZHONG_DAI_MA  ref=MDict.C.crcyCd  dbname=CRCY_CD
```

**生成的 XML**：
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="Loan_acct_table" package="com.spdb.ccbs.loan.bcc.tables" longname="贷款账户表" classgen="auto" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <table id="loan_acct_table" name="loan_acct_table" longname="贷款账户表" extension="SysCommFieldTable.kapp_sys_genl_pub_fld">
        <fields>
            <field id="custId" type="MBaseType.U_KE_HU_BIAN_HAO" nullable="false" ref="MDict.C.custId" primarykey="true" final="false" identity="false" allowSubType="true" dbname="CUST_ID"/>
            <field id="acctNo" type="MBaseType.U_ZHANG_HAO" nullable="false" ref="MDict.A.acctNo" primarykey="true" final="false" identity="false" allowSubType="true" dbname="ACCT_NO"/>
            <field id="acctBal" type="MBaseType.U_JIN_E" nullable="true" ref="MDict.A.acctBal" primarykey="false" final="false" identity="false" allowSubType="true" dbname="ACCT_BAL"/>
            <field id="crcyCd" type="MBaseType.U_BI_ZHONG_DAI_MA" nullable="true" ref="MDict.C.crcyCd" primarykey="false" final="false" identity="false" allowSubType="true" default="CNY" dbname="CRCY_CD"/>
        </fields>
    </table>
</schema>
```

**文件路径**：`loan-bcc/src/main/resources/tables/Loan_acct_table.tables.xml`

**关键说明**：
- 主键字段 `primarykey="true"` + `nullable="false"`（强制联动）
- `default="CNY"` 属性仅在用户指定时出现
- 无索引时不生成 `<odbindexes>` 和 `<indexes>` 标签

---

## 示例 2：含 ODB 索引和物理索引

**用户输入**：
```
帮我新建 Loan_acct_table 贷款账户表，贷款领域

字段：
客户编号  主键
账号      主键
账户余额
币种代码  default="CNY"

ODB索引：
selectByCustIdAndAcctNo  unique  客户编号 账号  operate=单记录查询 删除一条记录 单记录更新 单记录查询（带锁）
selectByCustId  index  客户编号  operate=多记录查询 翻页查询

物理索引：
PK_LOAN_ACCT       primarykey  客户编号 账号
IDX_LOAN_ACCT_01   index       客户编号
```

**MCP 查询结果展示**：
```
📋 MCP 字段查询结果：
  ✅ 客户编号  →  id=custId  dbname=CUST_ID
  ✅ 账号      →  id=acctNo  dbname=ACCT_NO
  ✅ 账户余额  →  id=acctBal  dbname=ACCT_BAL
  ✅ 币种代码  →  id=crcyCd  dbname=CRCY_CD
```

**生成的 XML**：
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="Loan_acct_table" package="com.spdb.ccbs.loan.bcc.tables" longname="贷款账户表" classgen="auto" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <table id="loan_acct_table" name="loan_acct_table" longname="贷款账户表" extension="SysCommFieldTable.kapp_sys_genl_pub_fld">
        <fields>
            <field id="custId" type="MBaseType.U_KE_HU_BIAN_HAO" nullable="false" ref="MDict.C.custId" primarykey="true" final="false" identity="false" allowSubType="true" dbname="CUST_ID"/>
            <field id="acctNo" type="MBaseType.U_ZHANG_HAO" nullable="false" ref="MDict.A.acctNo" primarykey="true" final="false" identity="false" allowSubType="true" dbname="ACCT_NO"/>
            <field id="acctBal" type="MBaseType.U_JIN_E" nullable="true" ref="MDict.A.acctBal" primarykey="false" final="false" identity="false" allowSubType="true" dbname="ACCT_BAL"/>
            <field id="crcyCd" type="MBaseType.U_BI_ZHONG_DAI_MA" nullable="true" ref="MDict.C.crcyCd" primarykey="false" final="false" identity="false" allowSubType="true" default="CNY" dbname="CRCY_CD"/>
        </fields>
        <odbindexes>
            <index id="selectByCustIdAndAcctNo" type="unique" fields="custId acctNo" operate="selectOne deleteOne updateOne selectOneWithLock"/>
            <index id="selectByCustId" type="index" fields="custId" operate="selectAll selectPage"/>
        </odbindexes>
        <indexes>
            <index id="PK_LOAN_ACCT" type="primarykey" fields="CUST_ID ACCT_NO"/>
            <index id="IDX_LOAN_ACCT_01" type="index" fields="CUST_ID"/>
        </indexes>
    </table>
</schema>
```

**关键说明**：
- ODB 索引 `fields` 用 MCP 返回的 **id**（如 `custId acctNo`）
- 物理索引 `fields` 用 MCP 返回的 **dbname**（如 `CUST_ID ACCT_NO`）
- ODB 索引有 `operate`，物理索引没有
- 操作中文自动映射为英文：`单记录查询` → `selectOne`

---

## 示例 3：含子目录

**用户输入**：
```
帮我新建 Ft_acct_table 福费延账户表，贷款领域，子目录 ft

字段：
福费延借据编码  主键
融资业务编码    非空
币种代码
```

**生成结果**：
- 文件路径：`loan-bcc/src/main/resources/tables/ft/Ft_acct_table.tables.xml`
- package：`com.spdb.ccbs.loan.bcc.tables.ft`
- table id：`ftAcctTable`

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="Ft_acct_table" package="com.spdb.ccbs.loan.bcc.tables.ft" longname="福费延账户表" classgen="auto" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <table id="ft_acct_table" name="ft_acct_table" longname="福费延账户表" extension="SysCommFieldTable.kapp_sys_genl_pub_fld">
        <fields>
            <field id="fRFTGDueBillCd" type="MBaseType.U_DAI_KUAN_JIE_JU_BIAN_MA" nullable="false" ref="MDict.F.fRFTGDueBillCd" primarykey="true" final="false" identity="false" allowSubType="true" dbname="FRFTG_DUE_BILL_CD"/>
            <field id="fncgBsnID" type="MBaseType.U_RONG_ZI_YE_WU_BIAN_MA" nullable="false" ref="MDict.F.fncgBsnID" primarykey="false" final="false" identity="false" allowSubType="true" dbname="FNCG_BSN_ID"/>
            <field id="crcyCd" type="MBaseType.U_BI_ZHONG_DAI_MA" nullable="true" ref="MDict.C.crcyCd" primarykey="false" final="false" identity="false" allowSubType="true" dbname="CRCY_CD"/>
        </fields>
    </table>
</schema>
```

---

## 示例 4：含未贯标字段

**用户输入**：
```
帮我新建 Cust_info_table 客户信息表，平台公共领域

字段：
客户编号  主键
客户名称  非空
未知字段
```

**MCP 查询结果展示**：
```
📋 MCP 字段查询结果：
  ✅ 客户编号  →  id=custId  type=MBaseType.U_KE_HU_BIAN_HAO  ref=MDict.C.custId  dbname=CUST_ID
  ✅ 客户名称  →  id=custName  type=MBaseType.U_KE_HU_MING_CHENG  ref=MDict.C.custName  dbname=CUST_NAME
  ❌ 未知字段  →  未贯标（MCP 返回 null），已跳过
```

**生成的 XML**（未贯标字段跳过）：
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="Cust_info_table" package="com.spdb.ccbs.comm.bcc.tables" longname="客户信息表" classgen="auto" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <table id="cust_info_table" name="cust_info_table" longname="客户信息表" extension="SysCommFieldTable.kapp_sys_genl_pub_fld">
        <fields>
            <field id="custId" type="MBaseType.U_KE_HU_BIAN_HAO" nullable="false" ref="MDict.C.custId" primarykey="true" final="false" identity="false" allowSubType="true" dbname="CUST_ID"/>
            <field id="custName" type="MBaseType.U_KE_HU_MING_CHENG" nullable="false" ref="MDict.C.custName" primarykey="false" final="false" identity="false" allowSubType="true" dbname="CUST_NAME"/>
        </fields>
    </table>
</schema>
```

**汇总提示**：
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  以下字段未写入 XML，请确认后补充：

【未贯标字段】（MCP 返回 null，需完成贯标后重新执行）：
  1. 未知字段

💡 完成上述问题后，可重新执行以补充。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 示例 5：索引包含未贯标字段

**用户输入**：
```
帮我新建 Test_table 测试表，贷款领域

字段：
客户编号  主键
未知字段

ODB索引：
selectByAll  unique  客户编号 未知字段  operate=单记录查询

物理索引：
PK_TEST  primarykey  客户编号 未知字段
```

**工作台展示**：
```
📋 MCP 字段查询结果：
  ✅ 客户编号  →  id=custId  dbname=CUST_ID
  ❌ 未知字段  →  未贯标（MCP 返回 null），已跳过
```

**生成的 XML**（未贯标字段跳过，相关索引不创建）：
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="Test_table" package="com.spdb.ccbs.loan.bcc.tables" longname="测试表" classgen="auto" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <table id="test_table" name="test_table" longname="测试表" extension="SysCommFieldTable.kapp_sys_genl_pub_fld">
        <fields>
            <field id="custId" type="MBaseType.U_KE_HU_BIAN_HAO" nullable="false" ref="MDict.C.custId" primarykey="true" final="false" identity="false" allowSubType="true" dbname="CUST_ID"/>
        </fields>
    </table>
</schema>
```

> 因 `未知字段` 未贯标，索引 `selectByAll` 和 `PK_TEST` 均包含该字段，**整个索引不创建**。

**汇总提示**：
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  以下字段未写入 XML，请确认后补充：

【未贯标字段】（MCP 返回 null，需完成贯标后重新执行）：
  1. 未知字段

【因字段未贯标导致索引未创建】：
  1. selectByAll（ODB索引，包含未贯标字段：未知字段）
  2. PK_TEST（物理索引，包含未贯标字段：未知字段）

💡 完成上述问题后，可重新执行以补充。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 示例 6：用户未指定英文名（自动翻译生成）

**用户输入**：
```
帮我新建 贷款还款流水表，贷款领域

字段：
客户编号  主键
还款日期  非空
还款金额
```

**处理**：
- 用户未指定 SchemaId，根据中文「贷款还款流水表」翻译 → `Loan_repay_flow_table`
- schema id = `Loan_repay_flow_table`，table id = `loan_repay_flow_table`

---

## 对话指令速查

| 场景 | 指令起始语 |
|------|-----------|
| 创建新表（默认路径） | `帮我新建 {SchemaId} {中文名}，{领域}领域` |
| 创建带子目录的表 | `帮我新建 {SchemaId} {中文名}，{领域}领域，子目录 {子目录}` |
| 只有中文名 | `帮我新建 {中文名}，{领域}领域`（自动生成英文名） |
| 修改表字段 | `修改 {SchemaId}，新增字段 {字段描述}` |
| 修改表索引 | `修改 {SchemaId}，新增 ODB索引/物理索引 {索引描述}` |
| 非空字段 | 字段行末加 `非空` |
| 主键字段 | 字段行末加 `主键` |
| 默认值 | 字段行末加 `default="xxx"` |
