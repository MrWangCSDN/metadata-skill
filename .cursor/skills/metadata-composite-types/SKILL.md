---
name: metadata-composite-types
description: 处理基于 XML 的复合类型元数据文件（*.c_schema.xml）的创建、修改和删除。支持根据领域自动生成 schema 结构、complexType 定义、element 字段，集成 dict-mcp-server 查询字段元数据，处理复合类型间引用。触发场景：创建/修改/删除复合类型、复合对象、c_schema.xml 文件。
---

# 复合类型元数据（c_schema.xml）

处理基于 XML 格式的复合类型元数据文件，文件命名规则：`{SchemaId}.c_schema.xml`。

## 核心工作流

### 模式 1：创建新复合类型文件

触发关键词：「新建」/「创建」+ 复合类型/复合对象

**处理步骤**：

1. **确定 SchemaId** — 全局唯一，同时作为文件名前缀（如 `FtAcctgType`）
2. **确定领域和包路径** — 根据领域映射模块和包路径（详见 [references/package-module-mapping.md](references/package-module-mapping.md)）
3. **定义 complexType 列表** — 每个复合对象一个 `complexType`
4. **调用 MCP 查询字段** — 使用 `dict-mcp-server.getDictDefByLongNameList` 批量查询所有 element 的字段元数据
5. **过滤未贯标字段** — MCP 返回 null 的字段**强制不写入 XML**，统一提示（⚠️ 强制规则）
6. **处理复合类型引用字段** — 此类字段不查 MCP，`type` 使用 `{SchemaId}.{ComplexTypeId}` 格式，无 `ref` 属性
7. **生成 XML** — 按标准模板生成（属性单行，4 空格缩进）
8. **保存文件** — 保存至 `{模块}/src/main/resources/type/{SchemaId}.c_schema.xml`

### 模式 2：修改现有复合类型文件

触发关键词：「修改」+ complexType 名称 / SchemaId

**处理步骤**：

1. **定位文件** — 查找对应 `{SchemaId}.c_schema.xml`
2. **读取原文件** — 保留 `schema` 标签所有属性
3. **调用 MCP** — 查询新增字段的元数据
4. **更新指定 complexType** — 仅修改目标 `complexType` 内的 `element` 列表，不影响其他 complexType
5. **保存** — 保持 XML 格式一致

### 模式 3：删除

触发关键词：「删除」+ complexType 名称 / SchemaId

- 删除整个 `complexType` 节点，或删除指定 `element`
- 若整个文件无 `complexType`，询问是否删除文件

---

## schema 标签属性

| 属性 | 说明 | 固定/来源 |
|------|------|---------|
| `xmlns:xsi` | — | 固定 `http://www.w3.org/2001/XMLSchema-instance` |
| `id` | 文件唯一标识，同文件名前缀 | 用户提供，全局唯一 |
| `package` | Java 包路径 | 根据领域自动映射 |
| `longname` | 复合类型文件中文名 | 用户提供 |
| `classgen` | — | 固定 `auto` |
| `xsi:noNamespaceSchemaLocation` | — | 固定 `ltts-model.xsd` |

---

## complexType 标签属性

| 属性 | 说明 | 默认值 |
|------|------|--------|
| `id` | 对象英文名（生成 Java 类名），文件内唯一 | 用户提供 |
| `longname` | 对象中文名 | 用户提供 |
| `abstract` | — | `false` |
| `dict` | — | `false` |
| `introduct` | — | `false` |
| `localName` | — | `""` |
| `extension` | — | `""` |
| `tags` | — | `""` |

---

## element 字段属性

| 属性 | 来源 | 默认值 |
|------|------|--------|
| `id` | MCP 返回 | — |
| `longname` | MCP 返回 | — |
| `type` | MCP 返回 / 复合类型引用 | — |
| `required` | 用户输入，未指定默认 | `false` |
| `multi` | 用户输入（集合为 true） | `false` |
| `ref` | MCP 返回（复合类型引用字段无 ref） | — |
| `range` | — | `false` |
| `array` | — | `false` |
| `final` | — | `false` |
| `override` | — | `false` |
| `allowSubType` | — | `true` |
| `key` | — | `false` |

> 历史文件中可能出现 `elemment`（拼写差异），新增内容统一使用 `element`。

---

## MCP 服务集成

**服务名**：`dict-mcp-server`  **方法**：`getDictDefByLongNameList`

> ⛔ **强制规则：MCP 返回 null 的字段禁止写入 XML。**
>
> - null 字段不生成任何 `<element>` 标签
> - 生成完成后在反馈中列出所有被排除的字段，提示用户完成贯标后重新执行

---

## 复合类型引用规则

当一个 element 的类型是另一个复合类型时：

- `type` 格式：`{SchemaId}.{ComplexTypeId}`
- 不填写 `ref` 属性
- 无需查询字典 MCP
- `multi="false"` → 单个对象；`multi="true"` → 对象数组（List）

```xml
<element required="false" multi="false" range="false" array="false" final="false"
         override="false" allowSubType="true" key="false"
         type="SyndAgrmLoanType.SysdAgrmLoanInfoPojo"
         longname="银团贷款出资份额信息"
         id="lstSyndAgrmLoanQryOutPojo"/>
```

---

## 标准 XML 模板

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
        id="FtAcctgType"
        package="com.spdb.ccbs.loan.resources.type.ft.repay"
        longname="福费延还款复合类型"
        classgen="auto"
        xsi:noNamespaceSchemaLocation="ltts-model.xsd">
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

**格式要点**：
- `schema` 标签属性可多行；`complexType` 和 `element` 属性必须单行
- 每个 `element` 属性顺序：`id → longname → type → required → multi → range → array → final → override → allowSubType → key → ref`
- 4 空格缩进，禁用 Tab

完整模板说明见 [references/xml-template.md](references/xml-template.md)

---

## 执行清单

### 创建流程

- [ ] 确认 SchemaId（全局唯一，与文件名前缀一致）
- [ ] 确定领域，映射包路径和模块
- [ ] 整理 complexType 列表（每个对象的 id、longname、字段列表）
- [ ] 区分普通字段（查 MCP）和复合类型引用字段（不查 MCP）
- [ ] 调用 `dict-mcp-server.getDictDefByLongNameList` 批量查询普通字段
- [ ] **强制过滤**：MCP 返回 null 的字段不写入 XML
- [ ] 生成 XML（属性单行，4空格缩进）
- [ ] 保存至 `{模块}/src/main/resources/type/`
- [ ] 输出反馈（写入字段数、排除字段列表）

### 修改流程

- [ ] 定位 `{SchemaId}.c_schema.xml` 文件
- [ ] 读取原文件，保留 `schema` 标签属性
- [ ] 调用 MCP 查询新增字段
- [ ] 仅更新目标 `complexType` 内容，不影响其他 complexType

---

## 参考资源

- [references/package-module-mapping.md](references/package-module-mapping.md) — 领域到包路径/模块映射
- [references/xml-template.md](references/xml-template.md) — XML 完整模板说明
- [references/examples.md](references/examples.md) — 完整创建/修改/引用示例
