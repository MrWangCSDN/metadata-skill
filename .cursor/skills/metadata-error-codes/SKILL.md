---
name: metadata-error-codes
description: 创建和修改基于 XML 的错误码元数据文件（*.errors.xml）。支持错误码模块（errors）、错误码条目（error）、参数占位符（parameter）的定义。按领域自动映射 package 路径，支持子目录。触发场景：新建/创建/修改错误码、errors.xml 文件操作、错误码定义。
---

# 错误码元数据（errors.xml）

处理基于 XML 格式的错误码元数据文件，文件命名规则：`{Id}.errors.xml`。

| 项目 | 说明 |
|------|------|
| 文件类型 | 错误码定义（Error Configuration） |
| 根标签 | `<errorConf>` |
| 文件后缀 | `.errors.xml` |
| 支持领域 | 存款（dept）、贷款（loan）、结算（sett）、公共（comm） |

---

## 核心工作流

### 模式 1：创建新错误码文件

触发关键词：「新建」/「创建」+ 错误码 / 错误码定义 / errors

**处理步骤**：

1. **确定 errorConf id** — 大驼峰命名，用户指定；未指定则根据中文翻译生成大驼峰
2. **确定 longname** — 用户提供中文名称
3. **确定领域和包路径** — 根据领域映射 resources 模块和 package（详见 [references/package-module-mapping.md](references/package-module-mapping.md)）
4. **处理子目录** — 如用户指定子目录，追加到路径和包名
5. **处理 description** — 用户有描述则添加 `<description><![CDATA[描述内容]]></description>`；无描述则不生成该标签
6. **整理 errors 模块列表** — 每个错误码模块一个 `<errors>` 标签
7. **整理 error 条目** — 每个错误码一个 `<error>` 标签，识别 message 中的 `${xxx}` 占位符
8. **处理 parameter** — 对 message 中的每个 `${xxx}` 占位符，生成对应 `<parameter>` 子标签
9. **生成 XML** — 按标准模板生成（属性单行，同级无空行，子标签缩进 4 空格）
10. **保存文件** — 保存至目标路径

### 模式 2：修改现有错误码文件

触发关键词：「修改」+ 错误码名称 / Id

1. **定位文件** — 查找对应 `{Id}.errors.xml`
2. **读取原文件** — 保留 `errorConf` 标签所有属性
3. **更新内容** — 新增/修改 `errors` 模块或 `error` 条目
4. **保存** — 保持 XML 格式一致

---

## 文件路径规则

> ⛔ **强制决策逻辑**：生成文件前必须先执行以下判断。

### 判断流程

```
用户是否指定子目录？
│
├─ 否 → 【默认路径】放在 errors/ 根目录下
│        package = 领域基础包（不追加子路径）
│
└─ 是 → 【子目录路径】放在 errors/{子目录}/ 下
         package = 领域基础包 + .{子目录用.分隔}
```

### 领域到模块映射

| 领域 | resources 模块 | 默认文件路径 | 默认 package |
|------|--------------|-------------|-------------|
| 存款 | dept-resources | `src/main/resources/errors/` | `com.spdb.ccbs.dept.resources.errors` |
| 贷款 | loan-resources | `src/main/resources/errors/` | `com.spdb.ccbs.loan.resources.errors` |
| 结算 | sett-resources | `src/main/resources/errors/` | `com.spdb.ccbs.sett.resources.errors` |
| 平台公共 | comm-resources | `src/main/resources/errors/` | `com.spdb.ccbs.comm.resources.errors` |

### 指定子目录

```
文件路径：src/main/resources/errors/{子目录}/{Id}.errors.xml
package： {领域基础包}.{子目录（/改为.）}
```

**示例**（贷款领域，子目录 `at`）：
```
文件路径：src/main/resources/errors/at/AtLoanError.errors.xml
package： com.spdb.ccbs.loan.resources.errors.at
```

详见 [references/package-module-mapping.md](references/package-module-mapping.md)

---

## errorConf 标签（根标签）

| 属性 | 说明 | 来源 |
|------|------|------|
| `xmlns:xsi` | — | 固定 `http://www.w3.org/2001/XMLSchema-instance` |
| `id` | 错误码文件唯一标识 | 大驼峰命名，用户指定 / 中文翻译生成 |
| `longname` | 错误码文件中文名 | 用户提供 |
| `package` | Java 包路径 | 根据领域自动映射 |
| `xsi:noNamespaceSchemaLocation` | — | 固定 `ltts-model.xsd` |

属性顺序：`xmlns:xsi → id → longname → package → xsi:noNamespaceSchemaLocation`

### description 标签（errorConf 级别）

- 用户提供了描述 → 在 `<errorConf>` 标签下添加 `<description><![CDATA[描述内容]]></description>`
- 用户未提供描述 → **不生成** `<description>` 标签

---

## errors 标签（错误码模块）

一个 `errorConf` 下可包含**多个** `errors` 模块，每个模块代表一个错误码分类。

| 属性 | 说明 | 来源 |
|------|------|------|
| `id` | 错误码模块标识 | 用户指定 |
| `longname` | 模块中文名 | 用户指定 |

### description 标签（errors 级别）

- 用户提供了模块描述 → 在 `<errors>` 标签下添加 `<description><![CDATA[描述内容]]></description>`
- 用户未提供描述 → **不生成** `<description>` 标签

---

## error 标签（错误码条目）

每个 `errors` 模块下包含**多个** `error` 条目。

| 属性 | 说明 | 来源 |
|------|------|------|
| `id` | 错误码 id | 用户指定（如 `E0000`、`E00002`） |
| `message` | 错误信息 | 用户指定，可包含 `${xxx}` 占位符 |
| `type` | — | 固定 `error` |

属性顺序：`id → message → type`

### 有无参数的判断

```
error 的 message 中是否包含 ${xxx} 占位符？
│
├─ 否 → error 标签自闭合 <error ... />
│
└─ 是 → error 标签包含 parameter 子标签
         对 message 中的每个 ${xxx}，生成一个 <parameter> 标签
```

---

## parameter 标签（错误码参数）

当 `error` 的 `message` 中包含 `${xxx}` 占位符时，在 `<error>` 标签内为每个占位符生成 `<parameter>` 子标签。

| 属性 | 说明 | 来源 |
|------|------|------|
| `id` | 参数标识 | 与 `${xxx}` 中的 `xxx` 一致 |
| `longname` | 参数中文名 | 用户指定 |
| `type` | 参数类型 | 用户指定（如 `BaseType.U_LONG_DESC`） |

属性顺序：`id → longname → type`

> ⛔ **强制规则：parameter 的 `id` 必须与 message 中 `${xxx}` 的 `xxx` 完全一致。**

**示例**：`message="错误描述：[${chmiaosh}]"` → `<parameter id="chmiaosh" ...>`

---

## 自然语言解析

### errors 模块格式

```
{模块id} {模块中文名}
  描述：{模块描述}                    ← 可选，有则生成 description 标签
  {错误码id} {错误信息}
  {错误码id} {错误信息}               ← 无 ${} 则 error 自闭合
  {错误码id} {错误信息含${xxx}}
    参数：{参数id} {参数中文名} {参数类型}
  ...
```

### 解析规则

```
输入写法                                        → 解析结果
──────────────────────────────────────────────────────────────────
E0000 错误描述：[${chmiaosh}]                  → error 含参数，需 parameter 子标签
  参数：chmiaosh 错误描述 BaseType.U_LONG_DESC → parameter id=chmiaosh
E00002 资产目前只支持负债结算！                 → error 无参数，自闭合
E00003 金额${amt}超过限额${maxAmt}             → error 含 2 个参数
  参数：amt 金额 BaseType.U_JIN_E              → parameter id=amt
  参数：maxAmt 最大金额 BaseType.U_JIN_E       → parameter id=maxAmt
```

> **关键判断**：message 中有 `${xxx}` → error 包含 parameter 子标签，`xxx` 即为 parameter 的 id；无 `${xxx}` → error 自闭合。

---

## 标准 XML 模板

### 完整示例（含多模块、描述、参数）

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<errorConf xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="AtLoanError" longname="资产模块错误码" package="com.spdb.ccbs.loan.resources.errors" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <description><![CDATA[资产模块错误码定义]]></description>
    <errors id="Colt" longname="抵押物模块错误码">
        <description><![CDATA[抵押物模块错误码]]></description>
        <error id="E0000" message="错误描述：[${chmiaosh}]" type="error">
            <parameter id="chmiaosh" longname="错误描述" type="BaseType.U_LONG_DESC"/>
        </error>
        <error id="E00002" message="资产目前只支持负债结算！" type="error"/>
    </errors>
    <errors id="Obsb" longname="表外业务模块错误码">
        <description><![CDATA[表外业务模块错误码]]></description>
        <error id="E0000" message="错误描述：[${chmiaosh}]" type="error">
            <parameter id="chmiaosh" longname="错误描述" type="BaseType.U_LONG_DESC"/>
        </error>
        <error id="E00002" message="资产目前只支持负债结算！" type="error"/>
    </errors>
</errorConf>
```

### 无描述、无参数的简化示例

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<errorConf xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="SettBaseError" longname="结算基础错误码" package="com.spdb.ccbs.sett.resources.errors" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <errors id="Pay" longname="支付模块错误码">
        <error id="E0001" message="交易金额不能为零！" type="error"/>
        <error id="E0002" message="账户状态异常，无法完成交易！" type="error"/>
    </errors>
</errorConf>
```

**格式强制规则**：

| 规则 | 说明 | 强制等级 |
|------|------|---------|
| ⛔ 属性不换行 | 所有标签属性必须写在同一行 | 强制 |
| ⛔ 同级无空行 | 不同标签之间不能有空行 | 强制 |
| ⛔ 禁用 Tab | 只使用空格缩进 | 强制 |
| 子标签缩进 | 每层 4 空格 | 必须 |
| 自闭合 | 无参数的 `error` 和 `parameter` 使用 `/>` 自闭合 | 必须 |

缩进层级：`errorConf(0)` → `description/errors(4)` → `description/error(8)` → `parameter(12)`

完整模板见 [references/xml-template.md](references/xml-template.md)

---

## 执行清单

### 创建流程

- [ ] 确定 errorConf id（大驼峰命名，用户指定 / 中文翻译生成）
- [ ] 确定 longname（用户提供中文名）
- [ ] 确定领域，映射 resources 模块和包路径
- [ ] ⛔ **路径判断**：用户是否指定子目录？
  - 否 → `src/main/resources/errors/{Id}.errors.xml`
  - 是 → 追加子目录，package 同步追加
- [ ] 处理 errorConf 级别 description（有则添加，无则不生成）
- [ ] 整理 errors 模块列表（id、longname、description）
- [ ] 整理每个模块下的 error 条目（id、message、参数列表）
- [ ] 对每个 error 的 message，识别 `${xxx}` 占位符
  - 有占位符 → 为每个 `${xxx}` 生成 `<parameter>` 子标签（id 与 xxx 一致）
  - 无占位符 → error 自闭合
- [ ] 生成 XML（属性单行，无空行，4 空格缩进）
- [ ] 保存至目标路径

### 修改流程

- [ ] 定位 `{Id}.errors.xml` 文件
- [ ] 读取原文件，保留 `errorConf` 标签所有属性
- [ ] 新增/修改 errors 模块或 error 条目
- [ ] 保持 XML 格式一致

---

## 参考资源

- [references/xml-template.md](references/xml-template.md) — XML 完整模板说明
- [references/examples.md](references/examples.md) — 完整创建/修改示例
- [references/package-module-mapping.md](references/package-module-mapping.md) — 领域到包路径/模块映射
