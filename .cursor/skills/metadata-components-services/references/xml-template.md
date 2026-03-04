# 构件与服务 XML 模板详解

## 格式强制规则

- ⛔ **属性不换行**：所有标签属性必须写在同一行
- ⛔ **无空行**：不同标签之间不能有空行
- ⛔ **禁用 Tab**：只使用空格缩进
- ⛔ **配套创建**：接口文件和实现文件必须同时创建
- 子标签相对父标签首行缩进 **4 个空格**

## 缩进级别对照表

| 标签 | 层级 | 空格数 |
|------|------|--------|
| serviceType / serviceImpl | 0 | 0 |
| method | 1 | 4 |
| input / output | 2 | 8 |
| field / fields | 3 | 12 |
| fields 内 field | 4 | 16 |

---

## 接口文件模板（serviceType）

### 完整模板（以 PBCB 为例）

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

### serviceType 属性

| 属性 | 固定/动态 | 说明 |
|------|----------|------|
| `xmlns:xsi` | 固定 | `http://www.w3.org/2001/XMLSchema-instance` |
| `id` | 动态 | 大驼峰 + 类型后缀 + `Svtp` |
| `kind` | 固定 | `auto` |
| `longname` | 动态 | 中文名称 |
| `package` | 动态 | 接口 package |
| `xsi:noNamespaceSchemaLocation` | 固定 | `ltts-model.xsd` |

属性顺序：`xmlns:xsi → id → kind → longname → package → xsi:noNamespaceSchemaLocation`

### id 后缀映射

| 类型 | id 后缀 | 示例 |
|------|--------|------|
| PBCB | `PbcbSvtp` | `LoanQueryPbcbSvtp` |
| PBCP | `PbcpSvtp` | `ProductCalcPbcpSvtp` |
| PBCC | `PbccSvtp` | `DateUtilPbccSvtp` |
| PBCT | `PbctSvtp` | `CacheManagePbctSvtp` |
| PBS | `PbsSvtp` | `PriceCalcPbsSvtp` |
| PCS | `PcsSvtp` | `OrderSubmitPcsSvtp` |

---

## 实现文件模板（serviceImpl）

### 完整模板（以 PBCB 为例）

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceImpl xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="LoanQueryPbcbSvtpImpl" kind="auto" longname="贷款查询基础构件实现" package="com.spdb.ccbs.loan.pbcb.impl.serviceimpl" ref="LoanQueryPbcbSvtp" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <method id="queryLoanInfo" longname="查询贷款信息" ref="LoanQueryPbcbSvtp.queryLoanInfo">
    </method>
    <method id="queryLoanList" longname="查询贷款列表" ref="LoanQueryPbcbSvtp.queryLoanList">
    </method>
</serviceImpl>
```

### serviceImpl 属性

| 属性 | 固定/动态 | 说明 |
|------|----------|------|
| `xmlns:xsi` | 固定 | `http://www.w3.org/2001/XMLSchema-instance` |
| `id` | 动态 | 接口 id + `Impl`（如 `LoanQueryPbcbSvtpImpl`） |
| `kind` | 固定 | `auto` |
| `longname` | 动态 | 中文名称 + `实现` |
| `package` | 动态 | 实现 package |
| `ref` | 动态 | 对应接口的 id |
| `xsi:noNamespaceSchemaLocation` | 固定 | `ltts-model.xsd` |

属性顺序：`xmlns:xsi → id → kind → longname → package → ref → xsi:noNamespaceSchemaLocation`

### 实现 method 的 ref

实现文件中 method 的 `ref` = `{接口id}.{方法id}`

```xml
<method id="queryLoanInfo" longname="查询贷款信息" ref="LoanQueryPbcbSvtp.queryLoanInfo">
```

---

## method 标签

### 接口文件中的 method

```xml
<method id="queryLoanInfo" longname="查询贷款信息">
    <input packMode="true">
        <field .../>
    </input>
    <output asParm="true" packMode="true">
        <field .../>
    </output>
</method>
```

| 属性 | 说明 |
|------|------|
| `id` | 方法英文名，小驼峰 |
| `longname` | 方法中文名 |

### 实现文件中的 method

```xml
<method id="queryLoanInfo" longname="查询贷款信息" ref="LoanQueryPbcbSvtp.queryLoanInfo">
</method>
```

| 属性 | 说明 |
|------|------|
| `id` | 与接口方法 id 一致 |
| `longname` | 与接口方法 longname 一致 |
| `ref` | `{接口serviceType的id}.{方法id}` |

---

## input / output 标签

与 flowtran 联机交易的 input/output 完全相同。

**input**：`packMode="true"` 固定
**output**：`asParm="true"` + `packMode="true"` 固定

### field 属性顺序

```
id → type → required → multi → array → longname → ref
```

所有字段通过 MCP 查询获取，MCP 返回 null 的字段不写入。

---

## 各类型文件后缀对照

| 类型 | 接口文件后缀 | 实现文件后缀 |
|------|------------|------------|
| PBCB | `.pbcb.xml` | `.pbcbImpl.xml` |
| PBCP | `.pbcp.xml` | `.pbcpImpl.xml` |
| PBCC | `.pbcc.xml` | `.pbccImpl.xml` |
| PBCT | `.pbct.xml` | `.pbctImpl.xml` |
| PBS | `.pbs.xml` | `.pbsImpl.xml` |
| PCS | `.pcs.xml` | `.pcsImpl.xml` |
