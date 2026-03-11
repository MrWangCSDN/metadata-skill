# 表定义 XML 模板详解

## 按需生成原则（⛔ 强制）

> **只生成用户明确指定的部分，不擅自补充未提及的内容。**

| 用户输入 | 生成部分 | 未提及时 |
|---------|---------|---------|
| 字段列表（「字段：」） | `<fields>` | 不生成 `<fields>` 标签 |
| ODB 索引（「ODB索引：」） | `<odbindexes>` | 不生成 `<odbindexes>` 标签 |
| 物理索引（「物理索引：」/「DB索引：」） | `<indexes>` | 不生成 `<indexes>` 标签 |

## 最完整 XML 模板（用户同时指定了字段 + ODB 索引 + 物理索引）

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="Loan_acct_table" package="com.spdb.ccbs.loan.bcc.tables" longname="贷款账户表" classgen="normal" generate="auto" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <table id="loan_acct_table" name="loan_acct_table" longname="贷款账户表" extension="SysCommFieldTable.kapp_sys_genl_pub_fld">
        <fields>
            <field id="custId" type="MBaseType.U_KE_HU_BIAN_HAO" nullable="false" longname="客户编号" ref="MDict.C.custId" primarykey="true" final="false" identity="false" allowSubType="true" dbname="cust_id"/>
            <field id="acctNo" type="MBaseType.U_ZHANG_HAO" nullable="false" longname="账号" ref="MDict.A.acctNo" primarykey="true" final="false" identity="false" allowSubType="true" dbname="acct_no"/>
            <field id="acctBal" type="MBaseType.U_JIN_E" nullable="true" longname="账户余额" ref="MDict.A.acctBal" primarykey="false" final="false" identity="false" allowSubType="true" dbname="acct_bal"/>
            <field id="crcyCd" type="MBaseType.U_BI_ZHONG_DAI_MA" nullable="true" longname="币种代码" ref="MDict.C.crcyCd" primarykey="false" final="false" identity="false" allowSubType="true" default="CNY" dbname="crcy_cd"/>
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

## 仅字段的 XML 模板（用户只指定了字段，未提及索引）

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="Loan_acct_table" package="com.spdb.ccbs.loan.bcc.tables" longname="贷款账户表" classgen="normal" generate="auto" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <table id="loan_acct_table" name="loan_acct_table" longname="贷款账户表" extension="SysCommFieldTable.kapp_sys_genl_pub_fld">
        <fields>
            <field id="custId" type="MBaseType.U_KE_HU_BIAN_HAO" nullable="false" longname="客户编号" ref="MDict.C.custId" primarykey="true" final="false" identity="false" allowSubType="true" dbname="cust_id"/>
            <field id="acctBal" type="MBaseType.U_JIN_E" nullable="true" longname="账户余额" ref="MDict.A.acctBal" primarykey="false" final="false" identity="false" allowSubType="true" dbname="acct_bal"/>
        </fields>
    </table>
</schema>
```

> ⛔ 用户未提及 ODB 索引和物理索引，**不生成** `<odbindexes>` 和 `<indexes>` 标签。

## 格式强制规则

- ⛔ **按需生成**：只生成用户明确指定的部分，不擅自补充
- ⛔ **单文件单表**：1 个 XML 文件中只能有 1 个 `<table>` 标签，不允许多张表
- ⛔ **属性不换行**：所有标签的属性必须写在同一行，绝对不允许换行
- ⛔ **无空行**：不同标签之间不能有空行，紧密排列
- ⛔ **禁用 Tab**：只使用空格缩进
- 子标签相对父标签首行缩进 **4 个空格**

## 缩进级别对照表

| 标签 | 层级 | 空格数 | 示例 |
|------|------|--------|------|
| schema | 0 | 0 | `<schema ...>` |
| table | 1 | 4 | `    <table ...>` |
| fields / odbindexes / indexes | 2 | 8 | `        <fields>` |
| field / index | 3 | 12 | `            <field .../>` |

## schema 标签

```xml
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="Loan_acct_table" package="com.spdb.ccbs.loan.bcc.tables" longname="贷款账户表" classgen="normal" generate="auto" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
```

| 属性 | 固定/动态 | 说明 |
|------|----------|------|
| `xmlns:xsi` | 固定 | `http://www.w3.org/2001/XMLSchema-instance` |
| `id` | 动态 | 蛇形命名首字母大写，如 `Loan_acct_table` |
| `package` | 动态 | 根据领域映射 |
| `longname` | 动态 | 表中文名 |
| `classgen` | 固定 | `normal` |
| `generate` | 固定 | `auto` |
| `xsi:noNamespaceSchemaLocation` | 固定 | `ltts-model.xsd` |

属性顺序：`xmlns:xsi → id → package → longname → classgen → generate → xsi:noNamespaceSchemaLocation`

## table 标签

```xml
<table id="loan_acct_table" name="loan_acct_table" longname="贷款账户表" extension="SysCommFieldTable.kapp_sys_genl_pub_fld">
```

| 属性 | 取值规则 |
|------|---------|
| `id` | schema id 全部转小写（`Loan_acct_table` → `loan_acct_table`） |
| `name` | 与 table id 相同 |
| `longname` | 与 schema longname 相同 |
| `extension` | 固定 `SysCommFieldTable.kapp_sys_genl_pub_fld` |

属性顺序：`id → name → longname → extension`

## field 标签（仅用户指定字段时生成）

### 普通字段（无 default）

```xml
<field id="acctBal" type="MBaseType.U_JIN_E" nullable="true" longname="账户余额" ref="MDict.A.acctBal" primarykey="false" final="false" identity="false" allowSubType="true" dbname="acct_bal"/>
```

### 主键字段

```xml
<field id="custId" type="MBaseType.U_KE_HU_BIAN_HAO" nullable="false" longname="客户编号" ref="MDict.C.custId" primarykey="true" final="false" identity="false" allowSubType="true" dbname="cust_id"/>
```

> 主键字段 `primarykey="true"` + `nullable="false"`（强制）

### 带默认值字段

```xml
<field id="crcyCd" type="MBaseType.U_BI_ZHONG_DAI_MA" nullable="true" longname="币种代码" ref="MDict.C.crcyCd" primarykey="false" final="false" identity="false" allowSubType="true" default="CNY" dbname="crcy_cd"/>
```

> `default` 属性仅在用户指定时出现，位于 `allowSubType` 之后、`dbname` 之前。

### field 属性顺序

```
id → type → nullable → longname → ref → primarykey → final → identity → allowSubType → [default] → dbname
```

| 属性 | 来源 | 固定值 |
|------|------|--------|
| `id` | MCP 返回 | — |
| `type` | MCP 返回 | — |
| `nullable` | 用户输入（默认 true） | — |
| `longname` | MCP 返回（字段中文名） | — |
| `ref` | MCP 返回 | — |
| `primarykey` | 用户输入（默认 false） | — |
| `final` | — | `false` |
| `identity` | — | `false` |
| `allowSubType` | — | `true` |
| `default` | 用户指定时才有 | — |
| `dbname` | MCP 返回 | — |

## ODB 索引标签（仅用户指定 ODB 索引时生成）

```xml
<odbindexes>
    <index id="selectByCustIdAndAcctNo" type="unique" fields="custId acctNo" operate="selectOne deleteOne updateOne selectOneWithLock"/>
    <index id="selectByCustId" type="index" fields="custId" operate="selectAll selectPage"/>
</odbindexes>
```

| 属性 | 说明 |
|------|------|
| `id` | 用户指定的索引 id |
| `type` | `unique` 或 `index` |
| `fields` | MCP 返回的 **id** 值（驼峰），多个空格分隔 |
| `operate` | 操作方法列表，多个空格分隔 |

index 属性顺序：`id → type → fields → operate`

### unique 类型可用操作

| 中文 | operate 值 |
|------|-----------|
| 单记录查询 | `selectOne` |
| 删除一条记录 | `deleteOne` |
| 单记录更新 | `updateOne` |
| 单记录查询（带锁） | `selectOneWithLock` |

### index 类型可用操作

| 中文 | operate 值 |
|------|-----------|
| 查询第一条 | `selectFirst` |
| 多记录查询 | `selectAll` |
| 翻页查询 | `selectPage` |
| 多记录更新 | `update` |
| 删除多条记录 | `delete` |
| 游标处理 | `selectCursor` |
| 带总记录数的翻页查询 | `selectPageWithCount` |
| 批量更新 | `updateBatch` |

## 物理索引标签（仅用户指定物理索引/DB索引时生成）

```xml
<indexes>
    <index id="PK_LOAN_ACCT" type="primarykey" fields="cust_id acct_no"/>
    <index id="IDX_LOAN_ACCT_01" type="index" fields="cust_id"/>
</indexes>
```

| 属性 | 说明 |
|------|------|
| `id` | 用户指定的索引 id |
| `type` | `primarykey`、`unique` 或 `index` |
| `fields` | MCP 返回的 **dbname** 值（小写），多个空格分隔 |

> 物理索引**无 operate 属性**。

index 属性顺序：`id → type → fields`

## 关键区别：ODB 索引 vs 物理索引

| 对比项 | ODB 索引 | 物理索引 |
|--------|---------|---------|
| 触发条件 | 用户输入含「ODB索引：」 | 用户输入含「物理索引：」或「DB索引：」 |
| 外层标签 | `<odbindexes>` | `<indexes>` |
| fields 取值 | MCP 返回的 **id**（驼峰） | MCP 返回的 **dbname**（小写） |
| type 可选值 | `unique`、`index` | `primarykey`、`unique`、`index` |
| operate 属性 | ✅ 有 | ❌ 无 |
| 用户未指定时 | ⛔ 不生成 | ⛔ 不生成 |
