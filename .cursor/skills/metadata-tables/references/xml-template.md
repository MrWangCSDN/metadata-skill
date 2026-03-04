# 表定义 XML 模板详解

## 完整 XML 模板

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

## 格式强制规则

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
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="Loan_acct_table" package="com.spdb.ccbs.loan.bcc.tables" longname="贷款账户表" classgen="auto" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
```

| 属性 | 固定/动态 | 说明 |
|------|----------|------|
| `xmlns:xsi` | 固定 | `http://www.w3.org/2001/XMLSchema-instance` |
| `id` | 动态 | 蛇形命名首字母大写，如 `Loan_acct_table` |
| `package` | 动态 | 根据领域映射 |
| `longname` | 动态 | 表中文名 |
| `classgen` | 固定 | `auto` |
| `xsi:noNamespaceSchemaLocation` | 固定 | `ltts-model.xsd` |

属性顺序：`xmlns:xsi → id → package → longname → classgen → xsi:noNamespaceSchemaLocation`

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

## field 标签

### 普通字段（无 default）

```xml
<field id="acctBal" type="MBaseType.U_JIN_E" nullable="true" ref="MDict.A.acctBal" primarykey="false" final="false" identity="false" allowSubType="true" dbname="ACCT_BAL"/>
```

### 主键字段

```xml
<field id="custId" type="MBaseType.U_KE_HU_BIAN_HAO" nullable="false" ref="MDict.C.custId" primarykey="true" final="false" identity="false" allowSubType="true" dbname="CUST_ID"/>
```

> 主键字段 `primarykey="true"` + `nullable="false"`（强制）

### 带默认值字段

```xml
<field id="crcyCd" type="MBaseType.U_BI_ZHONG_DAI_MA" nullable="true" ref="MDict.C.crcyCd" primarykey="false" final="false" identity="false" allowSubType="true" default="CNY" dbname="CRCY_CD"/>
```

> `default` 属性仅在用户指定时出现，位于 `allowSubType` 之后、`dbname` 之前。

### field 属性顺序

```
id → type → nullable → ref → primarykey → final → identity → allowSubType → [default] → dbname
```

| 属性 | 来源 | 固定值 |
|------|------|--------|
| `id` | MCP 返回 | — |
| `type` | MCP 返回 | — |
| `nullable` | 用户输入（默认 true） | — |
| `ref` | MCP 返回 | — |
| `primarykey` | 用户输入（默认 false） | — |
| `final` | — | `false` |
| `identity` | — | `false` |
| `allowSubType` | — | `true` |
| `default` | 用户指定时才有 | — |
| `dbname` | MCP 返回 | — |

## ODB 索引标签（odbindexes）

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
| `fields` | MCP 返回的 **id** 值，多个空格分隔 |
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

## 物理索引标签（indexes）

```xml
<indexes>
    <index id="PK_LOAN_ACCT" type="primarykey" fields="CUST_ID ACCT_NO"/>
    <index id="IDX_LOAN_ACCT_01" type="index" fields="CUST_ID"/>
</indexes>
```

| 属性 | 说明 |
|------|------|
| `id` | 用户指定的索引 id |
| `type` | `primarykey`、`unique` 或 `index` |
| `fields` | MCP 返回的 **dbname** 值，多个空格分隔 |

> 物理索引**无 operate 属性**。

index 属性顺序：`id → type → fields`

## 关键区别：ODB 索引 vs 物理索引

| 对比项 | ODB 索引 | 物理索引 |
|--------|---------|---------|
| 外层标签 | `<odbindexes>` | `<indexes>` |
| fields 取值 | MCP 返回的 **id** | MCP 返回的 **dbname** |
| type 可选值 | `unique`、`index` | `primarykey`、`unique`、`index` |
| operate 属性 | ✅ 有 | ❌ 无 |
