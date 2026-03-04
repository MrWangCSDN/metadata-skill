---
name: metadata-tables
description: 创建和修改基于 XML 的表定义元数据文件（*.tables.xml）。支持根据领域自动生成 schema/table/fields 结构、ODB 索引和物理索引，集成 dict-mcp-server 查询字段元数据。触发场景：新建/创建/修改表定义、tables.xml 文件操作。
---

# 表定义元数据（tables.xml）

处理基于 XML 格式的表定义元数据文件，文件命名规则：`{SchemaId}.tables.xml`。

## 核心工作流

### 模式 1：创建新表定义

触发关键词：「新建」/「创建」+ 表定义 / 表

**处理步骤**：

1. **确定 SchemaId** — 用户指定英文名（蛇形命名法，首字母大写，如 `Acct_info_table`）；未指定则根据中文翻译生成同样格式
2. **确定领域和包路径** — 根据领域映射 bcc 模块和包路径（详见 [references/package-module-mapping.md](references/package-module-mapping.md)）
3. **确定文件路径** — `{领域}-bcc/src/main/resources/tables/{子目录}/`
4. **调用 MCP 查询字段** — 使用 `dict-mcp-server.getDictDefByLongNameList` 批量查询所有字段
5. **过滤未贯标字段** — MCP 返回 null 的字段**强制不写入 XML**，统一提示（⚠️ 强制规则）
6. **处理索引** — ODB 索引和物理索引，索引中的字段需查 MCP 获取 id/dbname
7. **生成 XML** — 按标准模板生成（属性单行，同级无空行，子标签缩进 4 空格）
8. **保存文件** — 保存至确定的目标路径，输出文件路径和 package 信息

### 模式 2：修改现有表定义

触发关键词：「修改」+ 表名 / SchemaId

**处理步骤**：

1. **定位文件** — 查找对应 `{SchemaId}.tables.xml`
2. **读取原文件** — 保留 `schema`/`table` 标签所有属性
3. **调用 MCP** — 查询新增字段
4. **更新内容** — 新增字段追加到 `fields`，或更新索引
5. **保存** — 保持 XML 格式一致

---

## 文件路径规则

> ⛔ **强制决策逻辑**：生成文件前必须先执行以下判断。

### 判断流程

```
用户是否指定子目录？
│
├─ 否 → 【默认路径】放在 tables/ 根目录下
│        package = 领域基础包（不追加子路径）
│
└─ 是 → 【子目录路径】放在 tables/{子目录}/ 下
         package = 领域基础包 + .{子目录用.分隔}
```

### 领域到模块映射

| 领域 | 模块 | 默认文件路径 | 默认 package |
|------|------|-------------|-------------|
| 存款 | dept-bcc | `dept-bcc/src/main/resources/tables/` | `com.spdb.ccbs.dept.bcc.tables` |
| 贷款 | loan-bcc | `loan-bcc/src/main/resources/tables/` | `com.spdb.ccbs.loan.bcc.tables` |
| 结算 | sett-bcc | `sett-bcc/src/main/resources/tables/` | `com.spdb.ccbs.sett.bcc.tables` |
| 平台公共 | comm-bcc | `comm-bcc/src/main/resources/tables/` | `com.spdb.ccbs.comm.bcc.tables` |

### 指定子目录

```
文件路径：{领域}-bcc/src/main/resources/tables/{子目录}/{SchemaId}.tables.xml
package： {领域基础包}.{子目录（/改为.）}
```

**示例**（贷款领域，子目录 `ft`）：
```
文件路径：loan-bcc/src/main/resources/tables/ft/Loan_acct_table.tables.xml
package： com.spdb.ccbs.loan.bcc.tables.ft
```

详见 [references/package-module-mapping.md](references/package-module-mapping.md)

---

## schema 标签属性

| 属性 | 说明 | 来源 |
|------|------|------|
| `xmlns:xsi` | — | 固定 `http://www.w3.org/2001/XMLSchema-instance` |
| `id` | 表定义唯一标识，蛇形命名（首字母大写，如 `Loan_acct_table`） | 用户指定 / 中文翻译生成 |
| `package` | Java 包路径 | 根据领域自动映射 |
| `longname` | 表中文名称 | 用户提供 |
| `classgen` | — | 固定 `auto` |
| `xsi:noNamespaceSchemaLocation` | — | 固定 `ltts-model.xsd` |

---

## table 标签属性

| 属性 | 说明 | 取值规则 |
|------|------|---------|
| `id` | 表 id | 与 schema 的 `id` 相同，**全部转小写**（如 `Loan_acct_table` → `loan_acct_table`） |
| `name` | 表名 | 与 table 的 `id` 相同 |
| `longname` | 表中文名 | 与 schema 的 `longname` 相同 |
| `extension` | 扩展基表 | 固定 `SysCommFieldTable.kapp_sys_genl_pub_fld` |

---

## field 字段属性

| 属性 | 来源 | 默认值 |
|------|------|--------|
| `id` | MCP 返回 | — |
| `type` | MCP 返回 | — |
| `nullable` | 用户输入：默认允许为空 `true`；标注「非空」则 `false` | `true` |
| `ref` | MCP 返回 | — |
| `primarykey` | 用户标注「主键」则 `true`，否则 `false` | `false` |
| `final` | — | 固定 `false` |
| `identity` | — | 固定 `false` |
| `allowSubType` | — | 固定 `true` |
| `default` | 用户指定 `default="xxx"` 时写入，否则**不出现**该属性 | 不出现 |
| `dbname` | MCP 返回 | — |

> **主键规则**：`primarykey="true"` 时，`nullable` 强制为 `false`。

**field 属性顺序**：`id → type → nullable → ref → primarykey → final → identity → allowSubType → [default] → dbname`

### 自然语言解析对照表

```
输入写法                              → 解析结果
──────────────────────────────────────────────────────────────────
客户编号                              → 普通字段，nullable=true，primarykey=false
客户编号  非空                        → nullable=false
客户编号  主键                        → primarykey=true，nullable=false（强制）
客户编号  非空  主键                  → primarykey=true，nullable=false
客户编号  default="0"                → 追加 default="0" 属性
客户编号  非空  default="N"          → nullable=false，追加 default="N"
```

> **关键判断**：有「主键」→ primarykey=true + nullable=false；有「非空」→ nullable=false；有 `default="xxx"` → 追加 default 属性。

---

## MCP 服务集成

**服务名**：`dict-mcp-server`  **方法**：`getDictDefByLongNameList`

> ⛔ **强制规则：MCP 返回 null 的字段禁止写入 XML。**
>
> - null 字段不生成 `<field>` 标签
> - 索引中引用了未贯标字段时，该索引**整个不创建**
> - 生成完成后统一提示被排除的字段

### 查询结果展示规范

```
📋 MCP 字段查询结果：
  ✅ 客户编号  →  id=custId  type=MBaseType.U_KE_HU_BIAN_HAO  ref=MDict.C.custId  dbname=CUST_ID
  ✅ 账户余额  →  id=acctBal  type=MBaseType.U_JIN_E  ref=MDict.A.acctBal  dbname=ACCT_BAL
  ❌ 未知字段  →  未贯标（MCP 返回 null），已跳过
```

### 最终汇总提示

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  以下字段未写入 XML，请确认后补充：

【未贯标字段】（MCP 返回 null，需完成贯标后重新执行）：
  1. 未知字段

【因字段未贯标导致索引未创建】：
  1. idx_xxx（包含未贯标字段：未知字段）

💡 完成上述问题后，可重新执行以补充。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## ODB 索引（odbindexes）

### 自然语言格式

```
ODB索引：
{索引id}  unique  {字段中文名1} {字段中文名2}  operate={操作列表}
{索引id}  index   {字段中文名1}  operate={操作列表}
```

### index 标签属性

| 属性 | 说明 |
|------|------|
| `id` | 用户指定，不指定则不创建 |
| `type` | `unique` 或 `index` |
| `fields` | 字段的 **id**（MCP 返回），多个空格分隔 |
| `operate` | 操作方法列表，多个空格分隔 |

### type 与 operate 对应关系

| type | 可选操作 | operate 值 |
|------|---------|-----------|
| `unique` | 单记录查询 | `selectOne` |
| | 删除一条记录 | `deleteOne` |
| | 单记录更新 | `updateOne` |
| | 单记录查询（带锁） | `selectOneWithLock` |
| `index` | 查询第一条 | `selectFirst` |
| | 多记录查询 | `selectAll` |
| | 翻页查询 | `selectPage` |
| | 多记录更新 | `update` |
| | 删除多条记录 | `delete` |
| | 游标处理 | `selectCursor` |
| | 带总记录数的翻页查询 | `selectPageWithCount` |
| | 批量更新 | `updateBatch` |

### 自然语言操作映射

```
输入写法                      → operate 值
──────────────────────────────────────────
单记录查询                    → selectOne
删除一条记录                  → deleteOne
单记录更新                    → updateOne
单记录查询（带锁）            → selectOneWithLock
查询第一条                    → selectFirst
多记录查询                    → selectAll
翻页查询                      → selectPage
多记录更新                    → update
删除多条记录                  → delete
游标处理                      → selectCursor
带总记录数的翻页查询          → selectPageWithCount
批量更新                      → updateBatch
```

> ODB 索引的 `fields` 使用 MCP 返回的 **id** 值。

---

## 物理索引（indexes）

### 自然语言格式

```
物理索引：
{索引id}  primarykey  {字段中文名1} {字段中文名2}
{索引id}  unique      {字段中文名1}
{索引id}  index       {字段中文名1} {字段中文名2}
```

### index 标签属性

| 属性 | 说明 |
|------|------|
| `id` | 用户指定，不指定则不创建 |
| `type` | `primarykey`、`unique` 或 `index` |
| `fields` | 字段的 **dbname**（MCP 返回），多个空格分隔 |

> 物理索引无 `operate` 属性；`fields` 使用 MCP 返回的 **dbname** 值（非 id）。

---

## 标准 XML 模板

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

**格式强制规则**：

| 规则 | 说明 | 强制等级 |
|------|------|---------|
| ⛔ 单文件单表 | **1 个 XML 文件中只能创建 1 张表**，不允许多个 `<table>` 标签 | 强制 |
| ⛔ 属性不换行 | 所有标签（schema、table、field、index 等）的属性**必须写在同一行**，绝对不允许换行 | 强制 |
| ⛔ 同级无空行 | 不同标签之间**不能有空行**，紧密排列 | 强制 |
| ⛔ 禁用 Tab | 只使用空格缩进 | 强制 |
| 子标签缩进 | 子标签相对父标签首行缩进 **4 个空格** | 必须 |
| 自闭合 | `field` 和 `index` 使用 `/>` 自闭合 | 必须 |

缩进层级：`schema(0)` → `table(4)` → `fields/odbindexes/indexes(8)` → `field/index(12)`

完整模板说明见 [references/xml-template.md](references/xml-template.md)

---

## 执行清单

### 创建流程

- [ ] 确认 SchemaId（蛇形命名法，首字母大写，如 `Loan_acct_table` / 根据中文翻译生成同样格式）
- [ ] 确定领域，映射 bcc 模块和包路径
- [ ] ⛔ **路径判断**：用户是否指定子目录？
  - 否 → `{领域}-bcc/src/main/resources/tables/{SchemaId}.tables.xml`
  - 是 → 追加子目录，package 同步追加
- [ ] 确定 table 标签的 id（schema id 全部转小写，如 `Loan_acct_table` → `loan_acct_table`）
- [ ] 整理字段列表，识别：主键、非空、default 值
- [ ] 调用 `dict-mcp-server.getDictDefByLongNameList` 批量查询
- [ ] ⛔ **强制过滤**：MCP 返回 null 的字段不写入 XML
- [ ] 处理 ODB 索引（fields 用 id 值，索引含未贯标字段则整个不创建）
- [ ] 处理物理索引（fields 用 dbname 值，索引含未贯标字段则整个不创建）
- [ ] ⛔ **展示查询结果**：工作台输出每个字段 ✅/❌
- [ ] 生成 XML（属性单行，无空行，4空格缩进）
- [ ] 保存至目标路径
- [ ] ⛔ **汇总提示**：列出未贯标字段和因此未创建的索引

### 修改流程

- [ ] 定位 `{SchemaId}.tables.xml` 文件
- [ ] 读取原文件，保留 `schema`/`table` 标签属性
- [ ] 调用 MCP 查询新增字段
- [ ] 追加字段到 `fields`，或更新索引
- [ ] 保持 XML 格式一致

---

## 参考资源

- [references/package-module-mapping.md](references/package-module-mapping.md) — 领域到包路径/模块映射
- [references/xml-template.md](references/xml-template.md) — XML 完整模板说明
- [references/examples.md](references/examples.md) — 完整创建/修改示例
