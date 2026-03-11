---
name: metadata-services
description: 创建和修改 PBS/PCS 服务元数据 XML 文件，包括接口定义（serviceType）与实现定义（serviceImpl）。支持两种服务类型：基础服务（pbs）、组合服务（pcs）。每个服务文件可包含多个 service 接口。创建新服务时必须先询问用户是否配套创建实现文件，确认后才创建。集成 dict-mcp-server 查询字段元数据，支持复合类型引用（[xxx] 语法）和数组字段（fields 标签）。触发场景：新建/创建/修改服务、pbs/pcs 相关操作、基础服务/组合服务。
---

# 服务元数据（PBS/PCS）

处理基于 XML 格式的服务元数据文件，包含**接口定义**和**实现定义**两个文件。

| 项目 | 说明 |
|------|------|
| 类型 | 服务（PBS 基础服务、PCS 组合服务） |
| 分类 | 基础服务 pbs、组合服务 pcs |
| 接口文件 | `{name}.{服务类型}.xml`（如 `FtAcctgDeal.pbs.xml`） |
| 实现文件 | `{name}.{服务类型}Impl.xml`（如 `FtAcctgDeal.pbsImpl.xml`） |

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
3. **确定领域和包路径** — 接口模块 = `{领域}-{服务类型}-api`，实现模块 = `{领域}-{服务类型}-impl`，详见 [references/module-mapping.md](references/module-mapping.md)
4. **检查文件存在性** — 在对应目录下查找是否已存在同名文件，已存在则提示用户是否需要修改
5. **处理子目录** — 如用户指定子目录，追加到路径和包名
6. **调用 MCP 查询字段** — 对 service 中 input/output 的普通字段，使用 `dict-mcp-server.getDictDefByLongNameList` 批量查询
7. **过滤未贯标字段** — MCP 返回 null 的字段**强制不写入 XML**，统一提示
8. **处理复合类型引用** — 对 `[中文名]` 语法的字段，调用 `find_composite_ref.py` 脚本搜索
9. **处理数组字段** — 识别 start/end 标记的 fields 标签
10. **生成接口 XML** — `serviceType` 标签 + `service` 标签（可包含多个 service）
11. **询问用户** — 明确询问「是否同时创建该服务的实现文件？」；用户确认后继续
12. **生成实现 XML**（用户确认时）— 按模板生成 `serviceImpl` 自闭合标签（含 id、longname、serviceType、package）
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
| 基础服务 | 大驼峰 + `PbsSvtp` | `FtAcctgDealPbsSvtp`、`IoCpCustAccountQryPbsSvtp` |
| 组合服务 | 大驼峰 + `PcsSvtp` | `OrderSubmitPcsSvtp` |

### 实现文件 id（serviceImpl 的 id）

服务的 id 后缀 `Svtp` 替换为 `Impl`：

| 服务类型 | 实现 id 格式 | 示例 |
|---------|-------------|------|
| 基础服务 | 大驼峰 + `PbsImpl` | `FtAcctgDealPbsImpl` |
| 组合服务 | 大驼峰 + `PcsImpl` | `OrderSubmitPcsImpl` |

**规则**：用户指定英文名则用大驼峰 + 后缀；未指定则根据中文翻译生成大驼峰 + 后缀。

---

## service 标签 id 命名

> ⛔ **强制规则**：每个 `<service>` 标签的 id 独立于服务文件 id。

| 属性 | 说明 | 来源 |
|------|------|------|
| `id` | 服务接口标识 | 用户指定或中文翻译大驼峰 + 服务类型缩写（如 `GnfeeTrialChecksPbs`） |
| `name` | 接口方法名 | 用户指定或中文翻译小驼峰（如 `gnfeeTrialChecks`） |
| `longname` | 服务中文名 | 用户提供 |

---

## 文件路径与模块映射

> ⛔ **强制规则**：服务接口必须生成在 `{领域}-{服务类型}-api` 模块，服务实现必须生成在 `{领域}-{服务类型}-impl` 模块。

### 模块命名规则（必须严格遵守）

| 文件类型 | 模块名格式 | 说明 |
|---------|-----------|------|
| **服务（接口）** | `{领域}-{服务类型}-api` | 领域与服务类型均为小写，用 `-` 连接 |
| **服务实现** | `{领域}-{服务类型}-impl` | 同上 |

**领域**（4 个）：`dept`（存款）、`loan`（贷款）、`sett`（结算）、`comm`（公共）
**服务类型**（2 个）：`pbs`（基础服务）、`pcs`（组合服务）

### 完整模块对照表

| 领域 | 服务类型 | 接口模块 | 实现模块 |
|------|---------|---------|---------|
| dept | pbs | dept-pbs-api | dept-pbs-impl |
| dept | pcs | dept-pcs-api | dept-pcs-impl |
| loan | pbs | loan-pbs-api | loan-pbs-impl |
| loan | pcs | loan-pcs-api | loan-pcs-impl |
| sett | pbs | sett-pbs-api | sett-pbs-impl |
| sett | pcs | sett-pcs-api | sett-pcs-impl |
| comm | pbs | comm-pbs-api | comm-pbs-impl |
| comm | pcs | comm-pcs-api | comm-pcs-impl |

### 路径与 package

| 项目 | 接口 | 实现 |
|------|------|------|
| 工程 | ccbs-{领域}-api | ccbs-{领域}-impl |
| 模块 | **{领域}-{服务类型}-api** | **{领域}-{服务类型}-impl** |
| 路径 | `src/main/resources/serviceType/{子目录}` | `src/main/resources/serviceimpl/{子目录}` |
| 文件 | `{name}.{服务类型}.xml` | `{name}.{服务类型}Impl.xml` |
| package | `com.spdb.ccbs.{领域}.{服务类型}.api.servicetype.{子目录}` | `com.spdb.ccbs.{领域}.{服务类型}.impl.serviceimpl.{子目录}` |

**示例 1**（贷款领域 pbs，子目录 ft）：

| | 接口 | 实现 |
|--|------|------|
| 模块 | **loan-pbs-api** | **loan-pbs-impl** |
| 完整路径 | `loan-pbs-api/src/main/resources/serviceType/ft/FtAcctgDeal.pbs.xml` | `loan-pbs-impl/src/main/resources/serviceimpl/ft/FtAcctgDeal.pbsImpl.xml` |
| package | `com.spdb.ccbs.loan.pbs.api.servicetype.ft` | `com.spdb.ccbs.loan.pbs.impl.serviceimpl.ft` |

**示例 2**（结算领域 pcs，无子目录）：

| | 接口 | 实现 |
|--|------|------|
| 模块 | **sett-pcs-api** | **sett-pcs-impl** |
| 完整路径 | `sett-pcs-api/src/main/resources/serviceType/OrderSubmit.pcs.xml` | `sett-pcs-impl/src/main/resources/serviceimpl/OrderSubmit.pcsImpl.xml` |
| package | `com.spdb.ccbs.sett.pcs.api.servicetype` | `com.spdb.ccbs.sett.pcs.impl.serviceimpl` |

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
| 存款 | dept | `com.spdb.ccbs.dept.pbs.api.servicetype` | `com.spdb.ccbs.dept.pbs.impl.serviceimpl` |
| 贷款 | loan | `com.spdb.ccbs.loan.pbs.api.servicetype` | `com.spdb.ccbs.loan.pbs.impl.serviceimpl` |
| 结算 | sett | `com.spdb.ccbs.sett.pbs.api.servicetype` | `com.spdb.ccbs.sett.pbs.impl.serviceimpl` |
| 公共 | comm | `com.spdb.ccbs.comm.pbs.api.servicetype` | `com.spdb.ccbs.comm.pbs.impl.serviceimpl` |

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

> 实现文件仅包含一个 `<serviceImpl>` 根标签，**无** `<service>` 子标签，使用自闭合 `/>` 结尾。XML 声明为 `<?xml  version=`（xml 与 version 之间双空格）。通过 `serviceType` 属性引用接口。

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
| `id` | 服务标识，用户指定或翻译大驼峰 + 服务类型缩写（如 `FtAcctgDealPbs`） |
| `name` | 接口方法名，小驼峰（如 `ftAcctgDeal`） |
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

### 普通字段

调用 `dict-mcp-server.getDictDefByLongNameList` 查询字段元数据。

**field 属性顺序**：`id → type → required → multi → array → longname → ref`

| 属性 | 来源 | 默认值 |
|------|------|--------|
| `id` | MCP 返回 | — |
| `type` | MCP 返回 | — |
| `required` | 用户输入（必输/非必输） | `false` |
| `multi` | 用户输入（多值） | `false` |
| `array` | — | `false` |
| `longname` | MCP 返回 | — |
| `ref` | MCP 返回（可选） | — |

### 复合类型引用字段（[xxx] 语法）

> ⛔ **强制规则：`[xxx]` 引用必须调用 `find_composite_ref.py` 脚本搜索，不得自行猜测 type。**

**完整语法对照表**：

```
输入写法                                      → 解析结果
──────────────────────────────────────────────────────────────────
[保函费用试算输入]                            → 复合引用，单值，id 自动生成，无 array/ref
[保函费用试算输入]  多值                      → 复合引用，multi=true，id 末尾加 List
[保函费用试算输入]  必输                      → 复合引用，required=true
[保函费用试算输入]  多值  必输                → 复合引用，multi=true，required=true，id 末尾加 List
gnFeeTrialApsInPojo [保函费用试算输入]        → 复合引用，id = gnFeeTrialApsInPojo（用户指定）
gnFeeTrialApsInPojo [保函费用试算输入]  多值  → 复合引用，id = gnFeeTrialApsInPojo，multi=true
普通字段名                                    → 普通字段，查 MCP，生成含 array/ref 的 field
```

> **关键判断**：一行中有 `[...]` → 复合引用（调脚本，无 array/ref）；否则 → 普通字段（查 MCP，有 array/ref）。

**脚本调用**（使用工作区绝对路径，python 命令）：

```bash
python "{工作区根目录}/.speedstudio/skills/metadata-composite-types/scripts/find_composite_ref.py" "{工作区根目录}/{领域}-resources/src/main/resources/type" 保函费用试算输入
```

**`<search_dir>` 与领域对应**：

| 领域 | 搜索目录绝对路径 |
|------|----------------|
| 存款 | `{工作区根目录}/dept-resources/src/main/resources/type` |
| 贷款 | `{工作区根目录}/loan-resources/src/main/resources/type` |
| 结算 | `{工作区根目录}/sett-resources/src/main/resources/type` |
| 平台公共 | `{工作区根目录}/comm-resources/src/main/resources/type` |

**找到时**，生成（无 `array`、无 `ref` 属性）：
```xml
<field id="gnFeeTrialApsInPojo" type="GnFeeTrialType.GnFeeTrialApsInPojo" required="false" multi="false" longname="保函费用试算输入"/>
```

**未找到时（⛔ 强制规则）**：
1. **XML 中不写入该 field**
2. **在工作台输出** `❌ [保函费用试算输入] → 未找到匹配的 c_schema.xml，已跳过`
3. **生成 XML 后在汇总框中统一提示**

**多个匹配时**：列出所有候选，询问用户选择哪一个。

**id 生成规则**：

| 用户输入 | id 取值 |
|---------|---------|
| 中括号前有英文名 | 直接使用英文名 |
| 无英文名 | 脚本返回 complexTypeId 首字母改小写 + `Pojo` |
| 无英文名 + 多值 | 首字母小写 + `List` 后缀 |

### 数组字段（fields 标签）

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

---

## 标准 XML 模板

### 接口文件

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

### 实现文件

```xml
<?xml  version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceImpl xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="FtAcctgDealPbsImpl" longname="福费延账务处理类服务实现" serviceType="FtAcctgDealPbsSvtp" package="com.spdb.ccbs.loan.pbs.impl.serviceimpl.ft" xsi:noNamespaceSchemaLocation="ltts-model.xsd"/>
```

### 多 service 接口文件示例

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceType xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="IoCpCustAccountQryPbsSvtp" kind="auto" longname="客户账户查询基础服务" package="com.spdb.ccbs.dept.pbs.api.servicetype" xsi:noNamespaceSchemaLocation="ltts-model.xsd" outbound="false">
    <service id="QueryCustAcctPbs" name="queryCustAcct" longname="查询客户账户">
        <interface>
            <input packMode="false">
                <field id="custId" type="MBaseType.U_KE_HU_BIAN_HAO" required="true" multi="false" array="false" longname="客户编号" ref="MDict.C.custId"/>
            </input>
            <output asParm="false" packMode="false">
                <field id="acctNo" type="MBaseType.U_ZHANG_HAO" required="false" multi="false" array="false" longname="账号" ref="MDict.A.acctNo"/>
            </output>
        </interface>
    </service>
    <service id="QueryCustBalancePbs" name="queryCustBalance" longname="查询客户余额">
        <interface>
            <input packMode="false">
                <field id="acctNo" type="MBaseType.U_ZHANG_HAO" required="true" multi="false" array="false" longname="账号" ref="MDict.A.acctNo"/>
            </input>
            <output asParm="false" packMode="false">
                <field id="avlBal" type="MBaseType.U_JIN_E" required="false" multi="false" array="false" longname="可用余额" ref="MDict.A.avlBal"/>
            </output>
        </interface>
    </service>
</serviceType>
```

### 多 service 服务的实现文件

多 service 服务的实现文件格式与单 service 相同，一个 `serviceImpl` 对应整个 `serviceType`：

```xml
<?xml  version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceImpl xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="IoCpCustAccountQryPbsImpl" longname="客户账户查询基础服务类服务实现" serviceType="IoCpCustAccountQryPbsSvtp" package="com.spdb.ccbs.dept.pbs.impl.serviceimpl" xsi:noNamespaceSchemaLocation="ltts-model.xsd"/>
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

- 输入：字段中文名称数组，如 `["币种代码", "利息金额"]`
- 输出：`Map<中文名, 字段定义对象 | null>`，`null` 表示未贯标
- **调用时机**：创建或修改时，一次性批量查询所有普通字段

> ⛔ **强制规则：MCP 返回 null 的字段，禁止写入 XML。**
>
> - null 字段不生成任何 `<field>` 或 `<fields>` 标签
> - 数组（fields）内部分子字段 null → 仅写入贯标子字段；全部 null → 整个 `<fields>` 标签不写入
> - 生成完成后在反馈中列出所有被排除字段

### 查询结果展示规范

每次调用 MCP 和脚本后，**必须在工作台输出查询过程和结果**：

**MCP 查询结果**：
```
📋 MCP 字段查询结果：
  ✅ 币种代码      →  type=MBaseType.U_BI_ZHONG_DAI_MA  ref=MDict.C.crcyCd
  ❌ 自定义字段    →  未贯标（MCP 返回 null），已跳过
```

**复合对象脚本搜索结果**：
```
🔍 复合对象引用搜索结果：
  ✅ [保函费用试算输入]  →  GnFeeTrialType.GnFeeTrialApsInPojo
  ❌ [结算信息输出]       →  未找到匹配的 c_schema.xml，已跳过
```

**最终汇总提示**（生成 XML 后必须输出）：
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

> 若没有未贯标字段且所有复合对象均找到，则只输出「✅ 所有字段均已写入 XML」。

详见 [references/mcp-integration.md](references/mcp-integration.md)

---

## 执行清单

### 创建流程

- [ ] 确定服务类型（pbs/pcs）
- [ ] 确定 id（大驼峰业务名 + 服务类型后缀如 `PbsSvtp`）
- [ ] 确定领域（dept/loan/sett/comm），接口模块 = `{领域}-{服务类型}-api`，实现模块 = `{领域}-{服务类型}-impl`
- [ ] 检查文件是否已存在，已存在则提示是否切换修改模式
- [ ] 处理子目录（如有）
- [ ] 整理 service 列表（每个服务的 id、name、longname、input/output 字段）
- [ ] 区分三类字段：普通字段（查 MCP）、复合类型引用字段（`[xxx]` 搜索脚本）、数组字段（start/end）
- [ ] 调用 MCP 批量查询 input/output 中的普通字段
- [ ] ⛔ **强制过滤**：MCP 返回 null 的字段不写入 XML
- [ ] ⛔ **复合类型引用**：对每个 `[中文名]`，调用 `python "{工作区根目录}/.speedstudio/skills/metadata-composite-types/scripts/find_composite_ref.py" "{搜索目录绝对路径}" 中文名`；找到 → 生成无 array/ref 的 field；未找到 → 不写入 XML，提示用户；多匹配 → 询问用户
- [ ] 处理数组字段（识别 start/end 标记，子字段全 null 则整个 fields 不写入）
- [ ] 生成接口 XML（serviceType + 多个 service + interface + input/output）
- [ ] ⛔ **询问用户**：「是否同时创建该服务的实现文件？」；用户确认后才继续
- [ ] 用户确认时：生成实现 XML（serviceImpl 自闭合标签，含 id、longname、serviceType、package）
- [ ] 保存接口文件；用户确认时保存实现文件
- [ ] ⛔ **展示查询结果**：MCP 查询结果 + 脚本搜索结果
- [ ] ⛔ **汇总提示**：列出所有未写入字段

### 修改流程

- [ ] 定位接口文件（及实现文件，若存在）
- [ ] 读取原文件，保留 `serviceType` 标签属性
- [ ] 调用 MCP 查询新增字段；`[xxx]` 调用脚本搜索
- [ ] 新增/修改 service 内容（仅接口文件）
- [ ] 若服务 longname 变更且实现存在，更新实现文件的 longname
- [ ] 保持 XML 格式一致

---

## 参考资源

- [references/module-mapping.md](references/module-mapping.md) — PBS/PCS 服务的模块路径映射
- [references/xml-template.md](references/xml-template.md) — XML 完整模板说明
- [references/mcp-integration.md](references/mcp-integration.md) — MCP 服务集成说明
- [references/examples.md](references/examples.md) — 完整创建/修改示例
