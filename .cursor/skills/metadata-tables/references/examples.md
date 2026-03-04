# 表定义元数据完整示例

## 示例 1：只有字段（用户未指定索引）

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
  ✅ 客户编号  →  id=custId  type=MBaseType.U_KE_HU_BIAN_HAO  ref=MDict.C.custId  dbname=cust_id
  ✅ 账号      →  id=acctNo  type=MBaseType.U_ZHANG_HAO  ref=MDict.A.acctNo  dbname=acct_no
  ✅ 账户余额  →  id=acctBal  type=MBaseType.U_JIN_E  ref=MDict.A.acctBal  dbname=acct_bal
  ✅ 币种代码  →  id=crcyCd  type=MBaseType.U_BI_ZHONG_DAI_MA  ref=MDict.C.crcyCd  dbname=crcy_cd
```

**生成的 XML**：
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="Loan_acct_table" package="com.spdb.ccbs.loan.bcc.tables" longname="贷款账户表" classgen="auto" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <table id="loan_acct_table" name="loan_acct_table" longname="贷款账户表" extension="SysCommFieldTable.kapp_sys_genl_pub_fld">
        <fields>
            <field id="custId" type="MBaseType.U_KE_HU_BIAN_HAO" nullable="false" ref="MDict.C.custId" primarykey="true" final="false" identity="false" allowSubType="true" dbname="cust_id"/>
            <field id="acctNo" type="MBaseType.U_ZHANG_HAO" nullable="false" ref="MDict.A.acctNo" primarykey="true" final="false" identity="false" allowSubType="true" dbname="acct_no"/>
            <field id="acctBal" type="MBaseType.U_JIN_E" nullable="true" ref="MDict.A.acctBal" primarykey="false" final="false" identity="false" allowSubType="true" dbname="acct_bal"/>
            <field id="crcyCd" type="MBaseType.U_BI_ZHONG_DAI_MA" nullable="true" ref="MDict.C.crcyCd" primarykey="false" final="false" identity="false" allowSubType="true" default="CNY" dbname="crcy_cd"/>
        </fields>
    </table>
</schema>
```

**文件路径**：`loan-bcc/src/main/resources/tables/Loan_acct_table.tables.xml`

**关键说明**：
- 主键字段 `primarykey="true"` + `nullable="false"`（强制联动）
- `default="CNY"` 属性仅在用户指定时出现
- ⛔ 用户未提及 ODB 索引和物理索引 → **不生成** `<odbindexes>` 和 `<indexes>` 标签

---

## 示例 2：字段 + ODB 索引 + 物理索引（用户全部指定）

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
  ✅ 客户编号  →  id=custId  dbname=cust_id
  ✅ 账号      →  id=acctNo  dbname=acct_no
  ✅ 账户余额  →  id=acctBal  dbname=acct_bal
  ✅ 币种代码  →  id=crcyCd  dbname=crcy_cd
```

**生成的 XML**：
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="Loan_acct_table" package="com.spdb.ccbs.loan.bcc.tables" longname="贷款账户表" classgen="auto" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <table id="loan_acct_table" name="loan_acct_table" longname="贷款账户表" extension="SysCommFieldTable.kapp_sys_genl_pub_fld">
        <fields>
            <field id="custId" type="MBaseType.U_KE_HU_BIAN_HAO" nullable="false" ref="MDict.C.custId" primarykey="true" final="false" identity="false" allowSubType="true" dbname="cust_id"/>
            <field id="acctNo" type="MBaseType.U_ZHANG_HAO" nullable="false" ref="MDict.A.acctNo" primarykey="true" final="false" identity="false" allowSubType="true" dbname="acct_no"/>
            <field id="acctBal" type="MBaseType.U_JIN_E" nullable="true" ref="MDict.A.acctBal" primarykey="false" final="false" identity="false" allowSubType="true" dbname="acct_bal"/>
            <field id="crcyCd" type="MBaseType.U_BI_ZHONG_DAI_MA" nullable="true" ref="MDict.C.crcyCd" primarykey="false" final="false" identity="false" allowSubType="true" default="CNY" dbname="crcy_cd"/>
        </fields>
        <odbindexes>
            <index id="selectByCustIdAndAcctNo" type="unique" fields="custId acctNo" operate="selectOne deleteOne updateOne selectOneWithLock"/>
            <index id="selectByCustId" type="index" fields="custId" operate="selectAll selectPage"/>
        </odbindexes>
        <indexes>
            <index id="PK_LOAN_ACCT" type="primarykey" fields="cust_id acct_no"/>
            <index id="IDX_LOAN_ACCT_01" type="index" fields="cust_id"/>
        </indexes>
    </table>
</schema>
```

**关键说明**：
- 用户同时指定了字段、ODB 索引、物理索引 → 三部分都生成
- ODB 索引 `fields` 用 MCP 返回的 **id**（如 `custId acctNo`）
- 物理索引 `fields` 用 MCP 返回的 **dbname**（如 `cust_id acct_no`）
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
- table id：`ft_acct_table`（schema id 全部转小写）

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="Ft_acct_table" package="com.spdb.ccbs.loan.bcc.tables.ft" longname="福费延账户表" classgen="auto" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <table id="ft_acct_table" name="ft_acct_table" longname="福费延账户表" extension="SysCommFieldTable.kapp_sys_genl_pub_fld">
        <fields>
            <field id="fRFTGDueBillCd" type="MBaseType.U_DAI_KUAN_JIE_JU_BIAN_MA" nullable="false" ref="MDict.F.fRFTGDueBillCd" primarykey="true" final="false" identity="false" allowSubType="true" dbname="frftg_due_bill_cd"/>
            <field id="fncgBsnID" type="MBaseType.U_RONG_ZI_YE_WU_BIAN_MA" nullable="false" ref="MDict.F.fncgBsnID" primarykey="false" final="false" identity="false" allowSubType="true" dbname="fncg_bsn_id"/>
            <field id="crcyCd" type="MBaseType.U_BI_ZHONG_DAI_MA" nullable="true" ref="MDict.C.crcyCd" primarykey="false" final="false" identity="false" allowSubType="true" dbname="crcy_cd"/>
        </fields>
    </table>
</schema>
```

> ⛔ 用户只指定了字段，未提及索引 → 不生成 `<odbindexes>` 和 `<indexes>`。

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
  ✅ 客户编号  →  id=custId  type=MBaseType.U_KE_HU_BIAN_HAO  ref=MDict.C.custId  dbname=cust_id
  ✅ 客户名称  →  id=custName  type=MBaseType.U_KE_HU_MING_CHENG  ref=MDict.C.custName  dbname=cust_name
  ❌ 未知字段  →  未贯标（MCP 返回 null），已跳过
```

**生成的 XML**（未贯标字段跳过）：
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="Cust_info_table" package="com.spdb.ccbs.comm.bcc.tables" longname="客户信息表" classgen="auto" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <table id="cust_info_table" name="cust_info_table" longname="客户信息表" extension="SysCommFieldTable.kapp_sys_genl_pub_fld">
        <fields>
            <field id="custId" type="MBaseType.U_KE_HU_BIAN_HAO" nullable="false" ref="MDict.C.custId" primarykey="true" final="false" identity="false" allowSubType="true" dbname="cust_id"/>
            <field id="custName" type="MBaseType.U_KE_HU_MING_CHENG" nullable="false" ref="MDict.C.custName" primarykey="false" final="false" identity="false" allowSubType="true" dbname="cust_name"/>
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
  ✅ 客户编号  →  id=custId  dbname=cust_id
  ❌ 未知字段  →  未贯标（MCP 返回 null），已跳过
```

**生成的 XML**（未贯标字段跳过，相关索引不创建）：
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="Test_table" package="com.spdb.ccbs.loan.bcc.tables" longname="测试表" classgen="auto" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <table id="test_table" name="test_table" longname="测试表" extension="SysCommFieldTable.kapp_sys_genl_pub_fld">
        <fields>
            <field id="custId" type="MBaseType.U_KE_HU_BIAN_HAO" nullable="false" ref="MDict.C.custId" primarykey="true" final="false" identity="false" allowSubType="true" dbname="cust_id"/>
        </fields>
    </table>
</schema>
```

> 因 `未知字段` 未贯标，索引 `selectByAll` 和 `PK_TEST` 均包含该字段，**整个索引不创建**。
> 虽然用户指定了 ODB 索引和物理索引，但所有索引都因包含未贯标字段而不创建，最终 XML 中不出现索引标签。

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
- 用户只指定了字段 → 仅生成 `<fields>`，不生成索引标签

---

## 示例 7：修改现有表定义（新增字段）

**用户输入**：
```
修改 Loan_acct_table，新增字段：
开户日期  非空
账户状态  default="N"
```

**处理**：
1. 定位文件 `Loan_acct_table.tables.xml`
2. 读取原文件，保留 `schema`/`table` 标签所有属性及现有内容
3. 调用 MCP 查询新增字段

**MCP 查询结果展示**：
```
📋 MCP 字段查询结果：
  ✅ 开户日期  →  id=opnAcctDt  type=MBaseType.U_RI_QI  ref=MDict.O.opnAcctDt  dbname=opn_acct_dt
  ✅ 账户状态  →  id=acctSts  type=MBaseType.U_ZHANG_HU_ZHUANG_TAI  ref=MDict.A.acctSts  dbname=acct_sts
```

**修改后的 XML**（仅在 `<fields>` 末尾追加新字段，其他部分保持不变）：
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="Loan_acct_table" package="com.spdb.ccbs.loan.bcc.tables" longname="贷款账户表" classgen="auto" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <table id="loan_acct_table" name="loan_acct_table" longname="贷款账户表" extension="SysCommFieldTable.kapp_sys_genl_pub_fld">
        <fields>
            <field id="custId" type="MBaseType.U_KE_HU_BIAN_HAO" nullable="false" ref="MDict.C.custId" primarykey="true" final="false" identity="false" allowSubType="true" dbname="cust_id"/>
            <field id="acctNo" type="MBaseType.U_ZHANG_HAO" nullable="false" ref="MDict.A.acctNo" primarykey="true" final="false" identity="false" allowSubType="true" dbname="acct_no"/>
            <field id="acctBal" type="MBaseType.U_JIN_E" nullable="true" ref="MDict.A.acctBal" primarykey="false" final="false" identity="false" allowSubType="true" dbname="acct_bal"/>
            <field id="crcyCd" type="MBaseType.U_BI_ZHONG_DAI_MA" nullable="true" ref="MDict.C.crcyCd" primarykey="false" final="false" identity="false" allowSubType="true" default="CNY" dbname="crcy_cd"/>
            <field id="opnAcctDt" type="MBaseType.U_RI_QI" nullable="false" ref="MDict.O.opnAcctDt" primarykey="false" final="false" identity="false" allowSubType="true" dbname="opn_acct_dt"/>
            <field id="acctSts" type="MBaseType.U_ZHANG_HU_ZHUANG_TAI" nullable="true" ref="MDict.A.acctSts" primarykey="false" final="false" identity="false" allowSubType="true" default="N" dbname="acct_sts"/>
        </fields>
    </table>
</schema>
```

**关键说明**：
- ⛔ 修改模式下，仅修改用户明确要求的部分，未提及的部分保持原样
- 新增字段追加到 `<fields>` 末尾，原有字段保持不变
- 原文件中如果有 `<odbindexes>` 和 `<indexes>`，且用户未要求修改，则原样保留

---

## 示例 8：修改现有表定义（新增 ODB 索引）

**用户输入**：
```
修改 Loan_acct_table，新增 ODB索引：
selectByAcctNo  unique  账号  operate=单记录查询 单记录更新
```

**处理**：
1. 定位文件，读取原内容
2. 调用 MCP 查询索引中涉及的字段
3. 仅在 `<odbindexes>` 中追加新索引（若原文件无 `<odbindexes>` 则新建该标签）
4. 原有字段、其他索引保持不变

---

## 对话指令速查

| 场景 | 指令起始语 |
|------|-----------|
| 创建新表（只有字段） | `帮我新建 {SchemaId} {中文名}，{领域}领域` + 字段列表 |
| 创建带索引的表 | 同上 + ODB索引 和/或 物理索引 |
| 创建带子目录的表 | `帮我新建 {SchemaId} {中文名}，{领域}领域，子目录 {子目录}` |
| 只有中文名 | `帮我新建 {中文名}，{领域}领域`（自动生成英文名） |
| 修改表字段 | `修改 {SchemaId}，新增字段 {字段描述}` |
| 修改表索引 | `修改 {SchemaId}，新增 ODB索引/物理索引 {索引描述}` |
| 非空字段 | 字段行末加 `非空` |
| 主键字段 | 字段行末加 `主键` |
| 默认值 | 字段行末加 `default="xxx"` |
