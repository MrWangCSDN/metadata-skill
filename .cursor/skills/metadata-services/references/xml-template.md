# PBS/PCS 服务 XML 模板详解

## 格式强制规则

| 规则 | 说明 | 强制等级 |
|------|------|----------|
| ⛔ 属性不换行 | 所有标签属性必须写在同一行 | 强制 |
| ⛔ 无空行 | 不同标签之间不能有空行 | 强制 |
| ⛔ 禁用 Tab | 只使用空格缩进 | 强制 |
| 询问配套实现 | 创建新服务时必须询问用户是否创建实现文件 | 强制 |
| 4 空格缩进 | 每层子标签缩进 4 空格 | 强制 |

---

## 缩进级别对照表

| 层级 | 标签 | 缩进空格 |
|------|------|----------|
| 0 | `serviceType` / `serviceImpl` | 0 |
| 1 | `service` | 4 |
| 2 | `description` / `interface` | 8 |
| 3 | `input` / `output` | 12 |
| 4 | `field`（直接子节点） | 16 |
| 5 | `field`（位于 `fields` 内） | 20 |

---

## 接口文件模板

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

---

## serviceType 属性表和顺序

| 顺序 | 属性 | 说明 | 固定值/来源 |
|------|------|------|-------------|
| 1 | `xmlns:xsi` | XML Schema 实例命名空间 | 固定 `http://www.w3.org/2001/XMLSchema-instance` |
| 2 | `id` | 服务唯一标识 | 大驼峰业务名 + 服务类型后缀（如 `PbsSvtp`） |
| 3 | `kind` | 类型 | 固定 `auto` |
| 4 | `longname` | 中文名称 | 用户提供（服务文件的名称） |
| 5 | `package` | 接口包路径 | 根据领域、服务类型、子目录映射 |
| 6 | `xsi:noNamespaceSchemaLocation` | Schema 位置 | 固定 `ltts-model.xsd` |
| 7 | `outbound` | 出站标志 | 固定 `false` |

**属性顺序**：`xmlns:xsi` → `id` → `kind` → `longname` → `package` → `xsi:noNamespaceSchemaLocation` → `outbound`

---

## 实现文件模板

实现文件仅包含一个 `<serviceImpl>` 根标签，**无** `<service>` 子标签，使用自闭合 `/>` 结尾。XML 声明第一行为 `<?xml  version=`（xml 与 version 之间双空格）。通过 `serviceType` 属性引用接口。

```xml
<?xml  version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceImpl xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="FtAcctgDealPbsImpl" longname="福费延账务处理类服务实现" serviceType="FtAcctgDealPbsSvtp" package="com.spdb.ccbs.loan.pbs.impl.serviceimpl.ft" xsi:noNamespaceSchemaLocation="ltts-model.xsd"/>
```

---

## serviceImpl 属性表和顺序

| 顺序 | 属性 | 说明 | 固定值/来源 |
|------|------|------|-------------|
| 1 | `xmlns:xsi` | XML Schema 实例命名空间 | 固定 `http://www.w3.org/2001/XMLSchema-instance` |
| 2 | `id` | 实现唯一标识 | 服务 id 的 `Svtp` 替换为 `Impl` |
| 3 | `longname` | 实现中文名称 | 服务 longname + 「类服务实现」 |
| 4 | `serviceType` | 关联的接口 id | 接口文件的 `serviceType` 的 `id` |
| 5 | `package` | 实现包路径 | 根据领域、服务类型、子目录映射 |
| 6 | `xsi:noNamespaceSchemaLocation` | Schema 位置 | 固定 `ltts-model.xsd` |

**属性顺序**：`xmlns:xsi` → `id` → `longname` → `serviceType` → `package` → `xsi:noNamespaceSchemaLocation`

---

## service 标签说明（仅接口文件）

| 属性 | 说明 |
|------|------|
| `id` | 服务标识，大驼峰 + 服务类型缩写（如 `FtAcctgDealPbs`），注意与 serviceType id 不同 |
| `name` | 接口方法名，小驼峰（如 `ftAcctgDeal`） |
| `longname` | 服务中文名 |

---

## description 标签

- 用户提供了描述 → `<description><![CDATA[描述内容]]></description>`
- 用户未提供描述 → **不生成** `<description>` 标签
- 可出现在 `<serviceType>` 直接子级或 `<service>` 内部

---

## interface 标签

- 位于 `<service>` 标签内部
- **无任何属性**
- 包含 `<input>` 和 `<output>` 子标签

---

## input / output 说明

| 标签 | 属性 | 说明 |
|------|------|------|
| `input` | `packMode` | 默认 `false`；用户指明生成输入接口类时为 `true` |
| `output` | `asParm` | 固定 `false` |
| `output` | `packMode` | 默认 `false`；用户指明生成输出接口类时为 `true` |

---

## field 说明

### 普通字段（MCP 查询）

| 属性 | 说明 | 来源 |
|------|------|------|
| `id` | 字段英文名，小驼峰 | MCP 返回 |
| `type` | 基础类型 | MCP 返回 |
| `required` | 是否必输 | 用户指定，默认 `false` |
| `multi` | 是否多值 | 用户指定，默认 `false` |
| `array` | 是否数组 | 固定 `false` |
| `longname` | 字段中文名 | MCP 返回 |
| `ref` | 字典引用 | MCP 返回（可选） |

**field 属性顺序**：`id` → `type` → `required` → `multi` → `array` → `longname` → `ref`

### 复合类型引用字段

| 属性 | 说明 | 来源 |
|------|------|------|
| `id` | 用户指定或脚本返回 complexTypeId 首字母小写 + Pojo | 用户/脚本 |
| `type` | `{SchemaId}.{ComplexTypeId}` | 脚本返回 |
| `required` | 是否必输 | 用户指定，默认 `false` |
| `multi` | 是否多值 | 用户指定，默认 `false` |
| `longname` | 中文名 | 用户提供 |

> 复合引用字段**无** `array` 和 `ref` 属性。

**field 属性顺序**：`id` → `type` → `required` → `multi` → `longname`

---

## fields 标签（数组字段）

| 属性 | 值 | 说明 |
|------|---|------|
| `id` | `{名称}Array` | 必须以 Array 结尾 |
| `scope` | `""` | 固定空字符串 |
| `required` | `false` | 固定 |
| `multi` | `true` | 固定 |
| `array` | `false` | 固定 |
| `longname` | `{中文名}数组` | 必须以「数组」结尾 |

fields 内的 field 标签缩进比 fields 多 4 空格。

---

## 多 service 场景

一个服务文件可包含多个 `<service>` 标签，每个 service 独立定义自己的 interface、input、output。

实现文件始终为一个 `<serviceImpl>` 根标签，通过 `serviceType` 引用整个 `serviceType` 接口，无 `<service>` 子标签。

---

## 文件后缀对照表

| 服务类型 | 接口后缀 | 实现后缀 |
|---------|----------|----------|
| pbs | `.pbs.xml` | `.pbsImpl.xml` |
| pcs | `.pcs.xml` | `.pcsImpl.xml` |
