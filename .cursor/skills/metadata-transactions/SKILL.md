---
name: metadata-transactions
description: 处理基于 XML 的 flowtran 联机交易元数据模型的创建和修改。支持根据交易码（TC/TD/TG/TY 格式）、输入输出字段自动生成完整的 .flowtrans.xml 文件，包括数组字段处理（fields 标签）、dict-mcp-server 服务集成进行字段元数据查询、自动包路径生成和模块路径定位。触发场景：新建/创建/修改 flowtran 联机交易、TC/TD/TG/TY 开头的交易码、.flowtrans.xml 文件操作。
---

# Flowtran 联机交易元数据

处理基于 XML 格式的 flowtran 联机交易元数据，支持**创建**和**修改**两种模式。

## 核心工作流

### 模式 1：创建新交易

触发关键词：「新建」/「创建」+ 交易码

**处理步骤**：

1. **验证交易码** — 格式 `T+C/D/G/Y+4位数字`（详见 [references/transaction-id-rules.md](references/transaction-id-rules.md)）
2. **确定目标路径** — 根据交易码前缀自动映射模块和包路径（详见 [references/package-module-mapping.md](references/package-module-mapping.md)）
3. **检查文件存在性** — 在 `trans` 目录下查找 `.flowtrans.xml`，已存在则自动切换为修改模式
4. **处理子目录** — 检查是否指定子目录，追加到包路径和文件路径
5. **调用 MCP 查询字段** — 使用 `dict-mcp-server.getDictDefByLongNameList` 批量查询（详见 [references/mcp-integration.md](references/mcp-integration.md)）
6. **处理未贯标字段** — 收集返回 null 的字段，处理完成后统一提示
7. **生成 XML** — 按标准模板生成（属性单行，标签间无空行，4 空格缩进）
8. **保存并反馈** — 保存至 `{模块}-pbf/src/main/resources/trans/{交易码}.flowtrans.xml`

### 模式 2：修改现有交易

触发关键词：「修改」+ 交易码

**处理步骤**：

1. **定位文件** — 在 `trans` 目录（含子目录）下查找已有 `.flowtrans.xml`
2. **读取原文件** — 保留 `flowtran`/`description`/`interface` 标签的所有属性
3. **调用 MCP** — 查询新增字段的元数据
4. **仅覆盖 input/output** — 更新 `interface` 内的 input 和 output 标签内容
5. **保存** — 其他标签和属性保持不变

---

## 交易码规则

格式：`T + (C/D/G/Y) + 4位数字`（共 6 位，全大写）

| 前缀 | 领域 | 有效范围 | 示例 |
|------|------|---------|------|
| TC | 存款 | TC021–TC999 | TC100 |
| TD | 贷款 | TD001–TD499 | TD250 |
| TG | 结算 | TG001–TG499 | TG350 |
| TY | 平台公共 | TY001–TY999 | TY291 |

- 交易码全局唯一，文件名为 `{交易码}.flowtrans.xml`（注意扩展名是 `.flowtrans.xml`）
- 详细验证规则见 [references/transaction-id-rules.md](references/transaction-id-rules.md)

---

## 包路径与模块映射

| 前缀 | 包路径 | 模块名 | 文件路径 |
|------|--------|--------|---------|
| TC | com.spdb.ccbs.dept.pbf.trans | dept-pbf | dept-pbf/src/main/resources/trans |
| TD | com.spdb.ccbs.loan.pbf.trans | loan-pbf | loan-pbf/src/main/resources/trans |
| TG | com.spdb.ccbs.sett.pbf.trans | sett-pbf | sett-pbf/src/main/resources/trans |
| TY | com.spdb.ccbs.comm.pbf.trans | comm-pbf | comm-pbf/src/main/resources/trans |

- `interface package` = `flowtran package` + `.intf`
- 指定子目录时，包路径和文件路径均追加子目录
- 详见 [references/package-module-mapping.md](references/package-module-mapping.md)

---

## MCP 服务集成

**服务名**：`dict-mcp-server`  **方法**：`getDictDefByLongNameList`

- 输入：字段中文名称数组，如 `["国家", "性别"]`
- 输出：`Map<中文名, 字段定义对象 | null>`，`null` 表示未贯标
- **调用时机**：创建或修改时，一次性批量查询所有字段
- **未贯标处理**：继续处理其他已贯标字段，最后统一提示未贯标字段列表

详见 [references/mcp-integration.md](references/mcp-integration.md)

---

## 标准 XML 模板

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<flowtran xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="TY291" longname="收费明细文件批量查询" kind="auto" package="com.spdb.ccbs.comm.pbf.trans" txnMode="A" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <description><![CDATA[收费明细文件批量查询]]></description>
    <interface package="com.spdb.ccbs.comm.pbf.trans.intf">
        <input packMode="true">
            <field id="cst" type="MBaseType.U_GUO_JIA" required="false" multi="false" array="false" longname="国家" ref="MDict.C.cst"/>
        </input>
        <output asParm="true" packMode="true">
            <field id="cst" type="MBaseType.U_GUO_JIA" required="false" multi="false" array="false" longname="国家" ref="MDict.C.cst"/>
        </output>
    </interface>
</flowtran>
```

**格式要点**：

| 规则 | 说明 |
|------|------|
| 属性单行 | 所有标签属性必须在一行内，不能换行 |
| 无空行 | 同级标签之间不要有空行 |
| 4空格缩进 | 每层级增加 4 个空格，禁用 Tab |
| kind | 固定为 `"auto"` |
| txnMode | 默认 `A`，只读查询用 `R` |
| output | `asParm="true"` 和 `packMode="true"` 均固定 |

缩进层级：`flowtran(0)` → `description/interface(4)` → `input/output(8)` → `field(12)` → `fields内field(16)`

完整模板说明见 [references/xml-template.md](references/xml-template.md)

---

## 数组字段处理

使用 `<fields>` 标签表示数组/列表类型。

**自然语言格式**：
```
chargCdArray 收费代码数组 start
    包含 fPrjCd   收费项目编码  非必输
    包含 chrgAmt  收费金额     必输
chargCdArray 收费代码数组 end
```

**生成 XML**：
```xml
<fields id="chargCdArray" scope="" required="false" multi="true" array="false" longname="收费代码数组">
    <field id="fPrjCd" type="MBaseType.U_SHOU_FEI_XIANG_MU_BIAN_MA" required="false" multi="false" array="false" longname="收费项目编码" ref="MDict.F.fPrjCd"/>
    <field id="chrgAmt" type="MBaseType.U_JIN_E" required="true" multi="false" array="false" longname="收费金额" ref="MDict.C.chrgAmt"/>
</fields>
```

**关键规则**：`id` 必须以 `Array` 结尾，`scope=""` 固定，`multi="true"` 固定，`longname` 以「数组」结尾。

详见 [references/array-fields.md](references/array-fields.md)

---

## 字段属性说明

| 属性 | 来源 | 固定值 |
|------|------|--------|
| `id` | MCP 返回 | — |
| `type` | MCP 返回 | — |
| `required` | 用户输入（必输/非必输），默认 false | — |
| `multi` | — | `false` |
| `array` | — | `false` |
| `longname` | MCP 返回 | — |
| `ref` | MCP 返回（可选） | — |

---

## 执行清单

### 创建流程

- [ ] 验证交易码格式（T+C/D/G/Y+4位数字，范围合法）
- [ ] 确定模块和包路径（根据前缀映射）
- [ ] 检查 `.flowtrans.xml` 是否已存在（存在则切换修改模式）
- [ ] 处理子目录（如有，追加到路径和包名）
- [ ] 调用 `dict-mcp-server.getDictDefByLongNameList` 批量查询
- [ ] 处理数组字段（识别 start/end 标记，生成 fields 标签）
- [ ] 收集未贯标字段，统一提示
- [ ] 生成 XML（属性单行，无空行，4空格缩进）
- [ ] 保存至 `{模块}-pbf/src/main/resources/trans/`
- [ ] 输出反馈摘要

### 修改流程

- [ ] 定位现有 `.flowtrans.xml`（含子目录搜索）
- [ ] 读取并保留 `flowtran`/`description`/`interface` 标签属性
- [ ] 调用 MCP 查询新字段
- [ ] 仅覆盖 `input` 和 `output` 标签内容
- [ ] 保持 XML 格式一致（属性单行，无空行）

---

## 参考资源

- [references/transaction-id-rules.md](references/transaction-id-rules.md) — 交易码验证规则与实现
- [references/package-module-mapping.md](references/package-module-mapping.md) — 包路径和模块映射
- [references/xml-template.md](references/xml-template.md) — XML 模板完整说明
- [references/array-fields.md](references/array-fields.md) — 数组字段处理详解
- [references/mcp-integration.md](references/mcp-integration.md) — MCP 服务集成说明
- [references/error-handling.md](references/error-handling.md) — 错误处理指南
- [references/examples.md](references/examples.md) — 完整示例集
