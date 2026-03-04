---
name: metadata-components-services
description: 创建构件和服务元数据 XML 文件，包括 PBCB 基础构件、PBCP 产品构件、PBCC 公共构件、PBCT 技术构件、PBS 基础服务、PCS 组合服务的接口定义与实现定义。每个构件/服务文件配套创建实现文件。触发场景：新建/创建/修改构件、服务、pbcb/pbcp/pbcc/pbct/pbs/pcs 相关操作。
---

# 构件与服务元数据

处理基于 XML 格式的构件和服务元数据文件，每类均包含**接口定义**和**实现定义**两个文件，配套创建。

## 类型总览

| 类型 | 全称 | 接口文件 | 实现文件 | 定位 |
|------|------|---------|---------|------|
| PBCB | 基础构件 | `{name}.pbcb.xml` | `{name}.pbcbImpl.xml` | 承载具体业务逻辑 |
| PBCP | 产品构件 | `{name}.pbcp.xml` | `{name}.pbcpImpl.xml` | 跨业务复用的产品能力 |
| PBCC | 公共构件 | `{name}.pbcc.xml` | `{name}.pbccImpl.xml` | 通用工具与公共能力（仅 comm 领域） |
| PBCT | 技术构件 | `{name}.pbct.xml` | `{name}.pbctImpl.xml` | 基础技术能力封装 |
| PBS | 基础服务 | `{name}.pbs.xml` | `{name}.pbsImpl.xml` | 单一业务能力，供 PCS 调用 |
| PCS | 组合服务 | `{name}.pcs.xml` | `{name}.pcsImpl.xml` | 编排多个构件/服务，面向外部 |

> ⛔ **强制规则**：创建接口文件时，**必须同时创建对应的实现文件**。接口与实现在同一子目录下。

---

## 核心工作流

### 模式 1：创建新构件/服务

触发关键词：「新建」/「创建」+ 构件/服务类型名

**处理步骤**：

1. **识别类型** — 从用户描述中识别是哪种构件或服务
2. **确定 id 和 longname** — 用户指定英文名（大驼峰）+ 固定后缀 `Svtp`；未指定则中文翻译生成
3. **确定领域和包路径** — 根据领域和类型映射模块、路径、package（详见 [references/module-mapping.md](references/module-mapping.md)）
4. **生成接口 XML** — `serviceType` 标签 + `method` 标签
5. **生成实现 XML** — `serviceImpl` 标签 + `method` 标签（ref 引用接口）
6. **保存两个文件** — 接口文件和实现文件分别保存到对应模块

### 模式 2：修改现有构件/服务

触发关键词：「修改」+ 构件/服务名

1. 定位接口和实现文件
2. 新增/修改 method
3. 接口和实现**同步更新**

---

## id 命名规则

> ⛔ **强制规则**：id 由大驼峰业务名 + 类型后缀 + `Svtp` 组成。

| 类型 | id 后缀 | 示例 |
|------|--------|------|
| PBCB | `PbcbSvtp` | `LoanQueryPbcbSvtp` |
| PBCP | `PbcpSvtp` | `ProductCalcPbcpSvtp` |
| PBCC | `PbccSvtp` | `DateUtilPbccSvtp` |
| PBCT | `PbctSvtp` | `CacheManagePbctSvtp` |
| PBS | `PbsSvtp` | `PriceCalcPbsSvtp` |
| PCS | `PcsSvtp` | `OrderSubmitPcsSvtp` |

**规则**：用户指定英文名则用大驼峰 + 后缀；未指定则根据中文翻译生成大驼峰 + 后缀。

---

## 文件路径与模块映射

> ⛔ **公共构件（PBCC）领域固定为 comm**，不允许其他领域。

### 构件类（PBCB / PBCP / PBCC / PBCT）

| 类型 | 接口工程 | 接口模块 | 接口路径 | 实现工程 | 实现模块 | 实现路径 |
|------|---------|---------|---------|---------|---------|---------|
| PBCB | ccbs-{领域}-impl | {领域}-pbcb-api | `src/main/resources/serviceType/` | ccbs-{领域}-impl | {领域}-pbcb-impl | `src/main/resources/serviceimpl/` |
| PBCP | ccbs-{领域}-impl | {领域}-pbcp-api | `src/main/resources/serviceType/` | ccbs-{领域}-impl | {领域}-pbcp-impl | `src/main/resources/serviceimpl/` |
| PBCC | ccbs-comm-api | comm-pbcc-api | `src/main/resources/serviceType/` | ccbs-comm-impl | comm-pbcc-impl | `src/main/resources/serviceimpl/` |
| PBCT | ccbs-{领域}-impl | {领域}-pbct-api | `src/main/resources/serviceType/` | ccbs-{领域}-impl | {领域}-pbct-impl | `src/main/resources/serviceimpl/` |

### 服务类（PBS / PCS）

| 类型 | 接口工程 | 接口模块 | 接口路径 | 实现工程 | 实现模块 | 实现路径 |
|------|---------|---------|---------|---------|---------|---------|
| PBS | ccbs-{领域}-api | {领域}-pbs-api | `src/main/resources/serviceType/` | ccbs-{领域}-impl | {领域}-pbs-impl | `src/main/resources/serviceimpl/` |
| PCS | ccbs-{领域}-api | {领域}-pcs-api | `src/main/resources/serviceType/` | ccbs-{领域}-impl | {领域}-pcs-impl | `src/main/resources/serviceimpl/` |

### 子目录规则

- 用户指定子目录 → `serviceType/{子目录}/` 和 `serviceimpl/{子目录}/`
- 未指定 → 直接在 `serviceType/` 和 `serviceimpl/` 根目录

### package 规则

**接口 package**：`com.spdb.ccbs.{领域}.{类型}.api.servicetype.{子目录}`

| 类型 | 接口 package 示例 |
|------|------------------|
| PBCB | `com.spdb.ccbs.loan.pbcb.api.servicetype` |
| PBCP | `com.spdb.ccbs.loan.pbcp.api.servicetype` |
| PBCC | `com.spdb.ccbs.comm.pbcc.api.servicetype` |
| PBCT | `com.spdb.ccbs.loan.pbct.api.servicetype` |
| PBS | `com.spdb.ccbs.loan.pbs.api.servicetype` |
| PCS | `com.spdb.ccbs.loan.pcs.api.servicetype` |

**实现 package**：`com.spdb.ccbs.{领域}.{类型}.impl.serviceimpl.{子目录}`

详见 [references/module-mapping.md](references/module-mapping.md)

---

## serviceType 标签（接口定义）

| 属性 | 说明 | 来源 |
|------|------|------|
| `xmlns:xsi` | — | 固定 `http://www.w3.org/2001/XMLSchema-instance` |
| `id` | 构件/服务唯一标识 | 大驼峰 + 类型后缀 + `Svtp` |
| `kind` | — | 固定 `auto` |
| `longname` | 中文名称 | 用户提供 |
| `package` | 接口包路径 | 根据领域和类型映射 |
| `xsi:noNamespaceSchemaLocation` | — | 固定 `ltts-model.xsd` |

属性顺序：`xmlns:xsi → id → kind → longname → package → xsi:noNamespaceSchemaLocation`

---

## serviceImpl 标签（实现定义）

| 属性 | 说明 | 来源 |
|------|------|------|
| `xmlns:xsi` | — | 固定 `http://www.w3.org/2001/XMLSchema-instance` |
| `id` | 实现唯一标识 | 接口 id 去掉 `Svtp` 后缀，改为 `SvtpImpl` |
| `kind` | — | 固定 `auto` |
| `longname` | 中文名称 + `实现` | 用户提供 |
| `package` | 实现包路径 | 根据领域和类型映射 |
| `ref` | 关联的接口 id | 接口文件的 `serviceType` id |
| `xsi:noNamespaceSchemaLocation` | — | 固定 `ltts-model.xsd` |

---

## method 标签

接口和实现文件中均有 `method` 标签，表示一个方法。

**接口文件中的 method**：

| 属性 | 说明 |
|------|------|
| `id` | 方法英文名，小驼峰 |
| `longname` | 方法中文名 |

**实现文件中的 method**：

| 属性 | 说明 |
|------|------|
| `id` | 方法英文名，与接口一致 |
| `longname` | 方法中文名 |
| `ref` | 引用接口方法：`{接口id}.{方法id}` |

### method 下的 input / output

与 flowtran 交易的 input/output 结构相同：
- 调用 `dict-mcp-server.getDictDefByLongNameList` 查询字段元数据
- MCP 返回 null 的字段不写入 XML
- field 属性：`id → type → required → multi → array → longname → ref`

---

## 自然语言解析对照表

```
输入写法                                            → 解析结果
──────────────────────────────────────────────────────────────────────────
帮我创建 LoanQuery 贷款查询 基础构件，贷款领域     → PBCB，id=LoanQueryPbcbSvtp
帮我创建 贷款查询 基础构件，贷款领域                → PBCB，id 自动翻译
帮我创建 产品计算 产品构件，贷款领域                → PBCP
帮我创建 日期工具 公共构件                          → PBCC，领域固定 comm
帮我创建 缓存管理 技术构件，贷款领域                → PBCT
帮我创建 价格计算 基础服务，贷款领域                → PBS
帮我创建 订单提交 组合服务，贷款领域                → PCS
帮我创建 xxx 基础构件，贷款领域，子目录 ft          → 追加子目录
```

---

## 标准 XML 模板

### 接口文件（以 PBCB 为例）

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceType xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="LoanQueryPbcbSvtp" kind="auto" longname="贷款查询基础构件" package="com.spdb.ccbs.loan.pbcb.api.servicetype" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <method id="queryLoanInfo" longname="查询贷款信息">
        <input packMode="true">
            <field id="custId" type="MBaseType.U_KE_HU_BIAN_HAO" required="true" multi="false" array="false" longname="客户ID" ref="MDict.C.custId"/>
        </input>
        <output asParm="true" packMode="true">
            <field id="loanAmount" type="MBaseType.U_JIN_E" required="false" multi="false" array="false" longname="贷款金额" ref="MDict.L.loanAmount"/>
        </output>
    </method>
</serviceType>
```

### 实现文件（以 PBCB 为例）

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceImpl xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="LoanQueryPbcbSvtpImpl" kind="auto" longname="贷款查询基础构件实现" package="com.spdb.ccbs.loan.pbcb.impl.serviceimpl" ref="LoanQueryPbcbSvtp" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <method id="queryLoanInfo" longname="查询贷款信息" ref="LoanQueryPbcbSvtp.queryLoanInfo">
    </method>
</serviceImpl>
```

**格式强制规则**：

| 规则 | 说明 | 强制等级 |
|------|------|---------|
| ⛔ 属性不换行 | 所有标签属性必须写在同一行 | 强制 |
| ⛔ 同级无空行 | 不同标签之间不能有空行 | 强制 |
| ⛔ 禁用 Tab | 只使用空格缩进 | 强制 |
| ⛔ 配套创建 | 创建接口文件时必须同时创建实现文件 | 强制 |
| 子标签缩进 | 每层 4 空格 | 必须 |

缩进层级：`serviceType/serviceImpl(0)` → `method(4)` → `input/output(8)` → `field(12)`

完整模板见 [references/xml-template.md](references/xml-template.md)

---

## MCP 服务集成

**服务名**：`dict-mcp-server`  **方法**：`getDictDefByLongNameList`

> ⛔ **MCP 返回 null 的字段禁止写入 XML。** 生成后在工作台汇总提示。

---

## 执行清单

### 创建流程

- [ ] 识别构件/服务类型（PBCB/PBCP/PBCC/PBCT/PBS/PCS）
- [ ] 确定 id（大驼峰业务名 + 类型后缀 + `Svtp`）
- [ ] 确定领域（PBCC 固定 comm）
- [ ] 映射接口模块/路径和实现模块/路径
- [ ] 处理子目录（如有）
- [ ] 整理 method 列表（每个方法的 id、longname、input/output 字段）
- [ ] 调用 MCP 批量查询 input/output 字段
- [ ] ⛔ **强制过滤**：MCP 返回 null 的字段不写入 XML
- [ ] 生成接口 XML（serviceType + method）
- [ ] ⛔ **同时生成实现 XML**（serviceImpl + method，ref 引用接口）
- [ ] 保存两个文件到对应模块
- [ ] 工作台展示查询结果 + 汇总提示

---

## 参考资源

- [references/module-mapping.md](references/module-mapping.md) — 6 类构件/服务的模块路径映射
- [references/xml-template.md](references/xml-template.md) — XML 完整模板说明
- [references/examples.md](references/examples.md) — 完整创建/修改示例
