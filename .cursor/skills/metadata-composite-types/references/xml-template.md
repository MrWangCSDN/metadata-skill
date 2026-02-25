# 复合类型 XML 模板完整说明

本文档详细说明 `c_schema.xml` 文件的完整结构、各标签属性规则和格式规范。

## 完整 XML 结构

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="{SchemaId}" package="{包路径}" longname="{复合类型文件中文名}" classgen="auto" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <complexType abstract="false" dict="false" id="{对象英文名}" introduct="false" localName="" longname="{对象中文名}" extension="" tags="">
        <element id="{字段英文名}" longname="{字段中文名}" type="{字段类型}" required="{true|false}" multi="{true|false}" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="{字典引用}"/>
        <!-- 更多 element... -->
    </complexType>
    <!-- 更多 complexType... -->
</schema>
```

---

## schema 标签

### 属性详解

| 属性 | 说明 | 规则 |
|------|------|------|
| `xmlns:xsi` | XML Schema Instance 命名空间 | 固定 `http://www.w3.org/2001/XMLSchema-instance` |
| `id` | 文件唯一标识 | 大驼峰，与文件名前缀完全一致，全局唯一 |
| `package` | Java 包路径 | 根据领域自动映射，可含子包 |
| `longname` | 文件级中文名称 | 用户提供 |
| `classgen` | 代码生成模式 | 固定 `auto` |
| `xsi:noNamespaceSchemaLocation` | Schema 文件位置 | 固定 `ltts-model.xsd` |

### 格式示例

```xml
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="FtAcctgType" package="com.spdb.ccbs.loan.resources.type.ft.repay" longname="福费延还款复合类型" classgen="auto" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
```

---

## complexType 标签

### 属性详解

| 属性 | 说明 | 默认值 | 规则 |
|------|------|--------|------|
| `id` | 对象英文名，生成 Java 类名 | 用户提供 | 大驼峰，同文件内唯一 |
| `longname` | 对象中文名 | 用户提供 | — |
| `abstract` | 是否抽象类 | `false` | 通常保持默认 |
| `dict` | 是否字典类型 | `false` | 通常保持默认 |
| `introduct` | — | `false` | 固定 |
| `localName` | 本地名称 | `""` | 固定空字符串 |
| `extension` | 继承父类 | `""` | 需要继承时填父类名 |
| `tags` | 标签 | `""` | 固定空字符串 |

### 属性顺序（必须保持）

```
abstract → dict → id → introduct → localName → longname → extension → tags
```

### 格式示例

```xml
<complexType abstract="false" dict="false" id="FtAcctRepayChkInPojo" introduct="false" localName="" longname="福费延还款校验输入" extension="" tags="">
```

**命名规范**：
- 输入对象：`{业务前缀}InPojo` 或 `{业务前缀}QryInPojo`
- 输出对象：`{业务前缀}OutPojo` 或 `{业务前缀}QryOutPojo`

---

## element 标签（普通字段）

### 属性详解

| 属性 | 来源 | 说明 | 默认值 |
|------|------|------|--------|
| `id` | MCP 返回 | 字段英文名 | — |
| `longname` | MCP 返回 | 字段中文名 | — |
| `type` | MCP 返回 | 字段类型（MBaseType.U_XXX） | — |
| `required` | 用户输入 | 是否必填 | `false` |
| `multi` | 用户输入 | `true`=集合，`false`=单值 | `false` |
| `range` | — | 固定 | `false` |
| `array` | — | 固定 | `false` |
| `final` | — | 固定 | `false` |
| `override` | — | 固定 | `false` |
| `allowSubType` | — | 固定 | `true` |
| `key` | — | 固定 | `false` |
| `ref` | MCP 返回（可选） | 字典引用（MDict.X.fieldName） | — |

### 属性顺序（必须保持）

```
id → longname → type → required → multi → range → array → final → override → allowSubType → key → ref
```

### 格式示例

```xml
<element id="fRFTGDueBillCd" longname="福费延借据编码" type="MBaseType.U_DAI_KUAN_JIE_JU_BIAN_MA" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.F.fRFTGDueBillCd"/>
```

---

## element 标签（复合类型引用字段）

当字段类型引用另一个复合对象时，规则不同：

| 差异点 | 规则 |
|--------|------|
| `type` | 使用 `{SchemaId}.{ComplexTypeId}` 格式 |
| `ref` | **不写此属性** |
| MCP 查询 | **不需要**，此类字段不查字典 MCP |
| `multi="false"` | 单个对象 |
| `multi="true"` | 对象数组（List） |

### 格式示例

```xml
<!-- 单个对象 -->
<element id="repayInfoPojo" longname="还款信息" type="FtAcctgType.FtAcctRepayChkInPojo" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false"/>

<!-- 对象数组（List） -->
<element id="lstSyndAgrmLoanQryOutPojo" longname="银团贷款出资份额信息" type="SyndAgrmLoanType.SysdAgrmLoanInfoPojo" required="false" multi="true" range="false" array="false" final="false" override="false" allowSubType="true" key="false"/>
```

---

## XML 格式规范

### 缩进规则

子标签相对父标签首行缩进 **4 个空格**，每深一层追加 4 个空格：

| 层级 | 标签 | 空格数 | 说明 |
|------|------|--------|------|
| 0 | `<schema>` | 0 | 根标签 |
| 1 | `<complexType>` | 4 | schema 的子标签，缩进 4 |
| 2 | `<element>` | 8 | complexType 的子标签，缩进 8 |

### 同级标签间距规则

> ⛔ **同级标签之间不换行（无空行）**，紧密排列。

**正确** ✅：
```xml
<schema ...>
    <complexType ...>
        <element .../>
        <element .../>
    </complexType>
    <complexType ...>
        <element .../>
    </complexType>
</schema>
```

**错误** ❌（同级标签间有空行）：
```xml
<schema ...>
    <complexType ...>
        <element .../>

        <element .../>    <!-- ❌ 同级 element 之间不允许空行 -->
    </complexType>

    <complexType ...>     <!-- ❌ 同级 complexType 之间不允许空行 -->
        <element .../>
    </complexType>
</schema>
```

### 属性格式规则

> ⛔ **所有标签（`schema`、`complexType`、`element`）的属性必须写在同一行，不得换行。**

- 使用 4 个空格缩进，**禁用 Tab**
- `<element>` 使用自闭合 `/>` 结尾

### 完整格式示例

**正确** ✅：
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

**错误** ❌（多种错误汇总）：
```xml
<!-- ❌ schema 属性换行（同样禁止） -->
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        id="FtAcctgType"
        package="com.spdb.ccbs.loan.resources.type.ft.repay"
        classgen="auto"/>

<!-- ❌ element 属性换行 -->
<element id="fRFTGDueBillCd"
         longname="福费延借据编码"
         type="MBaseType.U_DAI_KUAN_JIE_JU_BIAN_MA"/>

<!-- ❌ 同级 element 之间有空行 -->
<complexType ...>
    <element .../>

    <element .../>
</complexType>

<!-- ❌ 同级 complexType 之间有空行 -->
<schema ...>
    <complexType .../>

    <complexType .../>
</schema>

<!-- ❌ 使用 Tab 缩进 -->
<schema ...>
	<complexType ...>    ← Tab 字符，禁止
		<element .../>
	</complexType>
</schema>
```

### 格式规范速查清单

生成 XML 前必须确认：

- [ ] `<complexType>` 缩进 4 个空格（相对 `<schema>`）
- [ ] `<element>` 缩进 8 个空格（相对 `<schema>`，即 `<complexType>` 再加 4）
- [ ] **同级 `<element>` 之间无空行**
- [ ] **同级 `<complexType>` 之间无空行**
- [ ] `<complexType>` 所有属性在同一行
- [ ] `<element>` 所有属性在同一行
- [ ] 使用空格缩进，无 Tab 字符
- [ ] `<element>` 以 `/>` 自闭合结尾

---

## 属性顺序速查

### complexType 属性顺序
```
abstract  dict  id  introduct  localName  longname  extension  tags
```

### element 属性顺序
```
id  longname  type  required  multi  range  array  final  override  allowSubType  key  [ref]
```
（复合类型引用字段无 `ref`）
