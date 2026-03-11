# PBC 构件 MCP 服务集成说明

## MCP 服务概述

**MCP 服务名称**：`dict-mcp-server`
**方法名**：`getDictDefByLongNameList`
**用途**：批量查询字段的元数据信息

## 接口规范

### 方法签名

```typescript
getDictDefByLongNameList(longNameList: string[]): Map<string, FieldDefinition | null>
```

### 输入参数

**参数名**：`longNameList`
**类型**：`string[]`（字符串数组）
**说明**：字段的中文名称集合

**示例**：
```javascript
["币种代码", "利息金额", "客户编号"]
```

### 返回结果

**类型**：`Map<string, FieldDefinition | null>`

**字段定义对象**：
```typescript
interface FieldDefinition {
    id: string;       // 字段英文名
    type: string;     // 字段类型（如 MBaseType.U_BI_ZHONG_DAI_MA）
    longname: string; // 字段中文名
    ref?: string;     // 字典引用（可选，如 MDict.C.crcyCd）
}
```

**返回示例**：
```javascript
{
  "币种代码": {
    "id": "crcyCd",
    "type": "MBaseType.U_BI_ZHONG_DAI_MA",
    "longname": "币种代码",
    "ref": "MDict.C.crcyCd"
  },
  "自定义字段": null  // null 表示未贯标
}
```

---

## 调用流程

### 构件字段查询流程

1. **收集字段** — 从所有 service 的 input/output 中提取普通字段的中文名（排除 `[xxx]` 复合引用和 fields 数组容器名）
2. **去重** — 对字段中文名去重（同一字段可能出现在多个 service 中）
3. **批量查询** — 调用 `getDictDefByLongNameList` 一次性查询
4. **分类处理** — 将返回结果分为已贯标和未贯标（null）
5. **强制过滤** — null 字段不写入 XML
6. **反馈** — 在工作台展示查询结果并汇总

### fields 数组中子字段

数组字段（`fields` 标签）内的子字段也需要查询 MCP：
- 子字段已贯标 → 正常写入 `<field>` 标签
- 子字段未贯标 → 跳过
- 数组内所有子字段均未贯标 → 整个 `<fields>` 标签不写入

---

## ⛔ 强制规则：null 字段禁止写入 XML

> MCP 返回 null 的字段，必须从生成列表中移除，不得生成任何 `<field>` 或 `<fields>` 标签。

### 处理策略

1. **强制过滤**：null 字段立即移除
2. **数组子字段**：部分 null → 仅写入贯标子字段；全部 null → `<fields>` 也不写入
3. **不中断流程**：过滤后继续用剩余已贯标字段生成 XML
4. **统一反馈**：生成完成后明确列出所有被排除字段

---

## 查询结果展示规范

### MCP 查询结果

```
📋 MCP 字段查询结果：
  ✅ 币种代码      →  type=MBaseType.U_BI_ZHONG_DAI_MA  ref=MDict.C.crcyCd
  ✅ 利息金额      →  type=MBaseType.U_JIN_E  ref=MDict.I.intrstAmt
  ❌ 自定义字段    →  未贯标（MCP 返回 null），已跳过
```

### 复合对象搜索结果

```
🔍 复合对象引用搜索结果：
  ✅ [保函费用试算输入]  →  GnFeeTrialType.GnFeeTrialApsInPojo
  ❌ [结算信息输出]       →  未找到匹配的 c_schema.xml，已跳过
```

### 最终汇总

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  以下字段未写入 XML，请确认后补充：

【未贯标字段】（MCP 返回 null，需完成贯标后重新执行）：
  1. 自定义字段

【复合对象引用未找到】（需确认文件是否已创建）：
  1. [结算信息输出]

💡 完成上述问题后，可重新执行以补充这些字段。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

> 若所有字段均已贯标且所有复合对象均找到，则只输出「✅ 所有字段均已写入 XML」。

---

## 字段映射：MCP 结果到 XML

### 普通字段映射

| MCP 返回字段 | XML 属性 | 说明 |
|-------------|---------|------|
| `id` | `id` | 直接使用 |
| `type` | `type` | 直接使用 |
| `longname` | `longname` | 直接使用 |
| `ref` | `ref` | 有值则添加，无值则省略 |
| — | `required` | 用户指定（必输/非必输），默认 `false` |
| — | `multi` | 用户指定（多值），默认 `false` |
| — | `array` | 固定 `false` |

### 复合类型引用字段

不查 `getDictDefByLongNameList`，通过三步查询获取 type 值：

**三步查询回退**：
1. **优先调用 `find_composite_ref.py` 脚本**（工作空间递归遍历所有 `*.c_schema.xml`）
2. **脚本未找到 → 调用 MCP `dict-mcp-server.queryComplexDetail`**
3. **MCP 也未找到 → 不写入 XML，提示用户**

> ⛔ **强制规则：查询参数必须是 `[]` 中括号内的完整原文，禁止截取、翻译或改写。**

| 属性 | 来源 |
|------|------|
| `id` | 用户指定或脚本/MCP 返回的 complexTypeId 首字母小写 + Pojo |
| `type` | 脚本/MCP 返回的 `{SchemaId}.{ComplexTypeId}` |
| `required` | 用户指定，默认 `false` |
| `multi` | 用户指定，默认 `false` |
| `longname` | 用户提供的中文名 |

> 复合引用字段**不生成** `array` 和 `ref` 属性。

---

## queryComplexDetail 方法

**MCP 服务名称**：`dict-mcp-server`
**方法名**：`queryComplexDetail`
**用途**：查询复合类型（complexType）的详细信息，作为 `find_composite_ref.py` 脚本的回退方案

### 方法签名

```typescript
queryComplexDetail(query: string): ComplexTypeDefinition | null
```

### 输入参数

**参数名**：`query`
**类型**：`string`
**说明**：复合类型的中文名称（longname）或英文标识（complexType id），必须是 `[]` 中括号内的完整原文

**示例**：
```javascript
"保函费用试算输入"    // 中文查询
"GnFeeTrialApsInPojo" // 英文查询
```

### 返回结果

**类型**：`ComplexTypeDefinition | null`

```typescript
interface ComplexTypeDefinition {
    schemaId: string;            // schema 标识（如 GnFeeTrialType）
    complexTypeId: string;       // complexType 标识（如 GnFeeTrialApsInPojo）
    complexTypeLongname: string; // complexType 中文名
    type: string;                // 完整类型引用（如 GnFeeTrialType.GnFeeTrialApsInPojo）
}
```

### 调用时机

- `find_composite_ref.py` 脚本搜索返回 `found: false` 时
- 返回结果需去重（按 schemaId + complexTypeId）
- 去重后多条 → 列出候选让用户选择
- 返回 null → 不写入 XML，汇总提示
