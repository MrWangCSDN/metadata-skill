---
name: metadata-services
description: 创建和修改 PBS/PCS 服务元数据 XML 文件，包括接口定义（serviceType）与实现定义（serviceImpl）。支持两种服务类型：基础服务（pbs）、组合服务（pcs）。创建新服务时可选择是否配套创建实现文件，修改时仅更新接口/实现内容。一个服务文件下可包含多个 service 服务接口。集成 dict-mcp-server 查询字段元数据，支持复合类型引用和数组字段（fields 标签）。触发场景：新建/创建/修改服务、pbs/pcs 相关操作、基础服务/组合服务。
---

# 服务元数据（PBS/PCS）

处理基于 XML 格式的服务元数据文件，包含**接口定义**和**实现定义**两个文件。

| 项目 | 说明 |
|------|------|
| 类型 | 服务（PBS 基础服务、PCS 组合服务） |
| 分类 | 基础服务 pbs、组合服务 pcs |
| 接口文件 | `{name}.{服务类型}.xml`（如 `PriceCalc.pbs.xml`） |
| 实现文件 | `{name}.{服务类型}Impl.xml`（如 `PriceCalc.pbsImpl.xml`） |

> ⛔ **强制规则**：创建新服务时，**必须询问用户**是否配套创建实现文件；用户确认后才创建。修改模式不涉及实现文件的新建。

---

## 两种服务类型

| 服务类型 | 缩写 | id 后缀 | 实现 id 后缀 | 接口文件后缀 | 实现文件后缀 |
|---------|------|---------|-------------|-------------|-------------|
| 基础服务 | pbs | PbsSvtp | PbsImpl | `.pbs.xml` | `.pbsImpl.xml` |
| 组合服务 | pcs | PcsSvtp | PcsImpl | `.pcs.xml` | `.pcsImpl.xml` |

---

## 核心工作流

### 模式 1：创建新服务

触发关键词：「新建」/「创建」+ 基础服务 / 组合服务 / PBS / PCS

**处理步骤**：

1. **确定服务类型** — 从用户输入识别是 pbs / pcs
2. **确定 id 和 longname** — 用户指定英文名（大驼峰）+ 固定后缀（如 `PbsSvtp`）；未指定则中文翻译生成大驼峰
3. **确定领域和包路径** — 根据领域映射模块、路径、package（详见 [references/module-mapping.md](references/module-mapping.md)）
4. **检查文件存在性** — 在对应目录下查找是否已存在同名文件，已存在则提示用户是否需要修改
5. **处理子目录** — 如用户指定子目录，追加到路径和包名
6. **调用 MCP 查询字段** — 对 service 中 input/output 的普通字段，使用 `dict-mcp-server.getDictDefByLongNameList` 批量查询
7. **过滤未贯标字段** — MCP 返回 null 的字段**强制不写入 XML**，统一提示
8. **处理复合类型引用** — 对 `[中文名]` 语法的字段，调用 `find_composite_ref.py` 脚本搜索
9. **处理数组字段** — 识别 start/end 标记的 fields 标签
10. **生成接口 XML** — `serviceType` 标签 + `service` 标签（可包含多个 service）
11. **询问用户** — 明确询问「是否同时创建该服务的实现文件？」；用户确认后继续
12. **生成实现 XML**（用户确认时）— 按模板生成 `serviceImpl` 标签（含 id、longname、serviceType、package）
13. **保存文件** — 接口文件必存；实现文件仅在用户确认时保存

### 模式 2：修改现有服务

触发关键词：「修改」+ 服务名

1. 定位接口文件（及实现文件，若存在）
2. 新增/修改 service（仅作用于接口文件）
3. 若服务 longname 变更且实现文件存在，则同步更新实现的 longname；其他情况实现文件无需变更（`serviceType` 引用已覆盖全部 service）

---

## id 命名规则

> ⛔ **强制规则**：服务 id 由大驼峰业务名 + 服务类型后缀组成。

### 服务文件 id（serviceType 的 id）

| 服务类型 | id 格式 | 示例 |
|---------|---------|------|
| 基础服务 | 大驼峰 + `PbsSvtp` | `PriceCalcPbsSvtp` |
| 组合服务 | 大驼峰 + `PcsSvtp` | `OrderSubmitPcsSvtp` |

### 实现文件 id（serviceImpl 的 id）

服务的 id 后缀 `Svtp` 替换为 `Impl`：

| 服务类型 | 实现 id 格式 | 示例 |
|---------|-------------|------|
| 基础服务 | 大驼峰 + `PbsImpl` | `PriceCalcPbsImpl` |
| 组合服务 | 大驼峰 + `PcsImpl` | `OrderSubmitPcsImpl` |

**规则**：用户指定英文名则用大驼峰 + 后缀；未指定则根据中文翻译生成大驼峰 + 后缀。

---

## service 标签 id 命名

> ⛔ **强制规则**：每个 `<service>` 标签的 id 独立于服务文件 id。

| 属性 | 说明 | 来源 |
|------|------|------|
| `id` | 服务接口标识 | 用户指定或中文翻译大驼峰 + 服务类型（如 `PriceCalcPbsSvtp`） |
| `name` | 接口方法名 | 用户指定或中文翻译小驼峰（如 `calcLoanPrice`） |
| `longname` | 服务中文名 | 用户提供 |

---

## 文件路径与模块映射

| 项目 | 接口 | 实现 |
|------|------|------|
| 工程 | ccbs-{领域}-api | ccbs-{领域}-impl |
| 模块 | {领域}-{服务类型}-api | {领域}-{服务类型}-impl |
| 路径 | `src/main/resources/serviceType/{子目录}` | `src/main/resources/serviceimpl/{子目录}` |
| 文件 | `{name}.{服务类型}.xml` | `{name}.{服务类型}Impl.xml` |
| package | `com.spdb.ccbs.{领域}.{服务类型}.api.serviceType.{子目录}` | `com.spdb.ccbs.{领域}.{服务类型}.impl.serviceimpl.{子目录}` |

**示例**（贷款领域 pbs，子目录 ft）：

| | 接口 | 实现 |
|--|------|------|
| 模块 | loan-pbs-api | loan-pbs-impl |
| 文件 | `src/main/resources/serviceType/ft/PriceCalc.pbs.xml` | `src/main/resources/serviceimpl/ft/PriceCalc.pbsImpl.xml` |
| package | `com.spdb.ccbs.loan.pbs.api.serviceType.ft` | `com.spdb.ccbs.loan.pbs.impl.serviceimpl.ft` |

### 子目录规则

- 用户指定子目录 → `serviceType/{子目录}/` 和 `serviceimpl/{子目录}/`
- 未指定 → 直接在 `serviceType/` 和 `serviceimpl/` 根目录
- **接口和实现的子目录保持一致**
- 子目录路径中 `/` 转换为 package 中的 `.`

详见 [references/module-mapping.md](references/module-mapping.md)

---

## 领域映射

| 领域 | 缩写 | 接口 package 基础 | 实现 package 基础 |
|------|------|-------------------|-------------------|
| 存款 | dept | `com.spdb.ccbs.dept.pbs.api.serviceType` | `com.spdb.ccbs.dept.pbs.impl.serviceimpl` |
| 贷款 | loan | `com.spdb.ccbs.loan.pbs.api.serviceType` | `com.spdb.ccbs.loan.pbs.impl.serviceimpl` |
| 结算 | sett | `com.spdb.ccbs.sett.pbs.api.serviceType` | `com.spdb.ccbs.sett.pbs.impl.serviceimpl` |
| 公共 | comm | `com.spdb.ccbs.comm.pbs.api.serviceType` | `com.spdb.ccbs.comm.pbs.impl.serviceimpl` |

> 上表以 pbs 为例，pcs 替换 `pbs` 为 `pcs`。

---

## serviceType 标签（接口定义）

| 属性 | 说明 | 来源 |
|------|------|------|
| `xmlns:xsi` | — | 固定 `http://www.w3.org/2001/XMLSchema-instance` |
| `id` | 服务唯一标识 | 大驼峰 + 服务类型后缀（如 `PbsSvtp`） |
| `kind` | — | 固定 `auto` |
| `longname` | 中文名称 | 用户提供 |
| `package` | 接口包路径 | 根据领域映射 |
| `xsi:noNamespaceSchemaLocation` | — | 固定 `ltts-model.xsd` |
| `outbound` | — | 固定 `false` |

属性顺序：`xmlns:xsi → id → kind → longname → package → xsi:noNamespaceSchemaLocation → outbound`

---

## serviceImpl 标签（实现定义）

> 实现文件仅包含一个 `<serviceImpl>` 根标签，**无** `<service>` 子标签，使用自闭合 `/>` 结尾。XML 声明为 `<?xml  version=`（双空格）。通过 `serviceType` 属性引用接口。

| 属性 | 说明 | 来源 |
|------|------|------|
| `xmlns:xsi` | — | 固定 `http://www.w3.org/2001/XMLSchema-instance` |
| `id` | 实现唯一标识 | 服务 id 后缀 `Svtp` 替换为 `Impl` |
| `longname` | 实现中文名称 | 服务 longname + 「类服务实现」（如「福费延账务处理类服务实现」） |
| `serviceType` | 关联的接口 id | 接口文件的 `serviceType` 的 `id`（如 `FtAcctgDealPbsSvtp`） |
| `package` | 实现包路径 | 根据领域映射 |
| `xsi:noNamespaceSchemaLocation` | — | 固定 `ltts-model.xsd` |

属性顺序：`xmlns:xsi → id → longname → serviceType → package → xsi:noNamespaceSchemaLocation`

---

## service 标签

### 接口文件中的 service

| 属性 | 说明 |
|------|------|
| `id` | 服务标识，用户指定或翻译大驼峰 + 服务类型后缀（如 `PriceCalcPbsSvtp`） |
| `name` | 接口方法名，小驼峰（如 `calcLoanPrice`） |
| `longname` | 服务中文名 |

> 实现文件中**无** `<service>` 子标签，仅根标签 `serviceImpl` 通过 `serviceType` 引用接口。

### description 标签

- 用户提供了描述 → 在 `<service>` 标签下添加 `<description><![CDATA[描述内容]]></description>`
- 用户未提供描述 → **不生成** `<description>` 标签

同样的规则适用于 `<serviceType>` 标签级别的 `<description>`。

### interface 标签

`<interface>` 标签位于 `<service>` 标签下，无任何属性。

---

## input / output 标签

### input 标签

| 属性 | 说明 |
|------|------|
| `packMode` | 默认 `false`；用户指明「生成对应的输入接口类」时为 `true` |

### output 标签

| 属性 | 说明 |
|------|------|
| `packMode` | 默认 `false`；用户指明「生成对应的输出接口类」时为 `true` |
| `asParm` | 固定 `false` |

---

## 字段处理

与 [metadata-pbc](.cursor/skills/metadata-pbc/SKILL.md) 及 [metadata-transactions](.cursor/skills/metadata-transactions/SKILL.md) 一致：

- **普通字段**：调用 `dict-mcp-server.getDictDefByLongNameList` 查询
- **复合类型引用**：`[中文名]` 语法，调用 `find_composite_ref.py` 脚本搜索
- **数组字段**：`fields` 标签，`xxxArray xxx数组 start ... end` 格式

详见 [references/mcp-integration.md](references/mcp-integration.md)、[metadata-pbc 字段处理](.cursor/skills/metadata-pbc/SKILL.md#字段处理)

> ⛔ **强制规则：MCP 返回 null 的字段，禁止写入 XML。**
> ⛔ **强制规则：`[xxx]` 引用必须调用脚本搜索，不得自行猜测 type。**

---

## 标准 XML 模板

### 接口文件

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceType xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="FtAcctgDealPbsSvtp" kind="auto" longname="福费延账务处理" package="com.spdb.ccbs.loan.pbs.api.serviceType.ft" xsi:noNamespaceSchemaLocation="ltts-model.xsd" outbound="false">
    <service id="FtAcctgDealPbsSvtp" name="ftAcctgDeal" longname="福费延账务处理">
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

### 实现文件

```xml
<?xml  version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceImpl xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="FtAcctgDealPbsImpl" longname="福费延账务处理类服务实现" serviceType="FtAcctgDealPbsSvtp" package="com.spdb.ccbs.loan.pbs.impl.serviceimpl.ft" xsi:noNamespaceSchemaLocation="ltts-model.xsd"/>
```

**格式强制规则**：

| 规则 | 说明 | 强制等级 |
|------|------|---------|
| ⛔ 属性不换行 | 所有标签属性必须写在同一行 | 强制 |
| ⛔ 同级无空行 | 不同标签之间不能有空行 | 强制 |
| ⛔ 禁用 Tab | 只使用空格缩进 | 强制 |
| 询问配套实现 | 创建新服务时必须询问用户是否创建实现文件，确认后才创建 | 强制 |
| 子标签缩进 | 每层 4 空格 | 必须 |

缩进层级：`serviceType(0)` → `service(4)` → `description/interface(8)` → `input/output(12)` → `field(16)` → `fields 内 field(20)`；实现文件 `serviceImpl` 无子标签。

完整模板见 [references/xml-template.md](references/xml-template.md)

---

## MCP 服务集成

**服务名**：`dict-mcp-server`  **方法**：`getDictDefByLongNameList`

- 输入：字段中文名称数组
- 输出：`Map<中文名, 字段定义对象 | null>`，`null` 表示未贯标
- **调用时机**：创建或修改时，一次性批量查询所有普通字段

> ⛔ **强制规则：MCP 返回 null 的字段，禁止写入 XML。** 生成完成后在反馈中列出所有被排除字段。

---

## 执行清单

### 创建流程

- [ ] 确定服务类型（pbs/pcs）
- [ ] 确定 id（大驼峰业务名 + 服务类型后缀如 `PbsSvtp`）
- [ ] 确定领域，映射接口模块/路径和实现模块/路径
- [ ] 检查文件是否已存在，已存在则提示是否切换修改模式
- [ ] 处理子目录（如有）
- [ ] 整理 service 列表（每个服务的 id、name、longname、input/output 字段）
- [ ] 区分三类字段：普通字段（查 MCP）、复合类型引用字段（`[xxx]` 搜索脚本）、数组字段（start/end）
- [ ] 调用 MCP 批量查询 input/output 中的普通字段
- [ ] ⛔ **强制过滤**：MCP 返回 null 的字段不写入 XML
- [ ] ⛔ **复合类型引用**：对每个 `[中文名]`，调用 `find_composite_ref.py` 脚本；找到 → 生成无 array/ref 的 field；未找到 → 不写入 XML，提示用户
- [ ] 处理数组字段（识别 start/end 标记）
- [ ] 生成接口 XML（serviceType + 多个 service + interface + input/output）
- [ ] ⛔ **询问用户**：「是否同时创建该服务的实现文件？」；用户确认后才继续
- [ ] 用户确认时：生成实现 XML（serviceImpl 自闭合标签，含 id、longname、serviceType、package）
- [ ] 保存接口文件；用户确认时保存实现文件
- [ ] ⛔ **展示查询结果** + **汇总提示**

### 修改流程

- [ ] 定位接口文件（及实现文件，若存在）
- [ ] 读取原文件，保留 `serviceType` 标签属性
- [ ] 调用 MCP 查询新增字段；`[xxx]` 调用脚本搜索
- [ ] 新增/修改 service 内容（仅接口文件）
- [ ] 若服务 longname 变更且实现存在，更新实现文件的 longname
- [ ] 保持 XML 格式一致

---

## 参考资源

- [references/module-mapping.md](references/module-mapping.md) — 服务的模块路径映射
- [references/xml-template.md](references/xml-template.md) — XML 完整模板说明
- [references/mcp-integration.md](references/mcp-integration.md) — MCP 服务集成说明
- [references/examples.md](references/examples.md) — 完整创建/修改示例
