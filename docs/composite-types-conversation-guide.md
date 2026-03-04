# 复合类型元数据 —— 对话指令指南

本文档为开发人员提供与 AI 对话创建/修改复合类型元数据（`*.c_schema.xml`）的标准指令模板。

---

## 前置说明

### 领域与模块映射

| 领域 | resources 模块 | 默认文件路径 |
|------|--------------|-------------|
| 存款 | dept-resources | `dept-resources/src/main/resources/type/` |
| 贷款 | loan-resources | `loan-resources/src/main/resources/type/` |
| 结算 | sett-resources | `sett-resources/src/main/resources/type/` |
| 平台公共 | comm-resources | `comm-resources/src/main/resources/type/` |

### 字段必输说明

- **必输**：`required="true"`
- **非必输**（缺省）：`required="false"`

### 多值字段说明

- **多值**：`multi="true"`，表示该字段是 List 集合
- **单值**（缺省）：`multi="false"`

### 复合对象引用写法

| 写法 | 说明 |
|------|------|
| `[中文名]` | **推荐**：中括号语法，简洁直观 |
| `中文名（复合对象）` | 兼容旧写法，同样有效 |
| `英文id [中文名]` | 指定英文字段名时，放在中括号前 |
| `[中文名]  多值` | 多值复合对象引用 |
| `[中文名]  必输` | 必输复合对象引用 |

---

## 场景 1：创建新复合类型（默认路径）

### 指令模板

```
帮我新建 {SchemaId} {文件中文名}，{领域}领域

{ComplexTypeId} {复合对象中文名}
  {字段中文名}  {必输/非必输}
  {字段中文名}
  ...

{ComplexTypeId} {复合对象中文名}
  {字段中文名}
  ...
```

### 示例 1-A：基本创建（单个复合对象）

```
帮我新建 CustInfoType 客户信息复合类型，平台公共领域

CustBaseInfoPojo 客户基础信息
  客户ID    必输
  客户名称
  账号
```

### 示例 1-B：多个复合对象

```
帮我新建 FtAcctgType 福费延还款复合类型，贷款领域

FtAcctRepayChkInPojo 福费延还款校验输入
  福费延借据编码
  融资业务编码

FtAcctRepayChkOutPojo 福费延还款校验输出
  福费延借据编码
  融资业务编码
  处理结果
```

### 示例 1-C：含多值字段

```
帮我新建 LoanApplType 贷款申请复合类型，贷款领域

LoanApplPojo 贷款申请对象
  客户ID       必输
  申请金额     必输
  担保方式     多值
  币种代码
```

### AI 返回格式示例

```
📋 MCP 字段查询结果：
  ✅ 客户ID    →  type=MBaseType.U_KE_HU_BIAN_HAO  ref=MDict.C.custId
  ✅ 客户名称  →  type=MBaseType.U_KE_HU_MING_CHENG  ref=MDict.C.custName
  ❌ 账号      →  未贯标（MCP 返回 null），已跳过

✅ 成功创建复合类型文件

📁 文件位置: comm-resources/src/main/resources/type/CustInfoType.c_schema.xml
📦 package:  com.spdb.ccbs.comm.resources.type
🗂️  复合对象: CustBaseInfoPojo（客户基础信息）

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  以下字段未写入 XML，请确认后补充：

【未贯标字段】（MCP 返回 null，需完成贯标后重新执行）：
  1. 账号（CustBaseInfoPojo）

💡 完成上述问题后，可重新执行以补充这些字段。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 场景 2：创建带子包的复合类型

### 指令模板

```
帮我新建 {SchemaId} {文件中文名}，{领域}领域，子包 {子包路径}

{ComplexTypeId} {复合对象中文名}
  {字段中文名}
  ...
```

> 子包路径用 `/` 分隔，会自动转为 Java package 中的 `.`

### 示例 2-A：单级子包

```
帮我新建 FtAcctgType 福费延记账复合类型，贷款领域，子包 ft

FtAcctgInPojo 福费延记账输入
  融资业务编码  必输
  福费延借据编码
```

**生成结果**：
- 文件路径：`loan-resources/src/main/resources/type/ft/FtAcctgType.c_schema.xml`
- package：`com.spdb.ccbs.loan.resources.type.ft`

### 示例 2-B：多级子包

```
帮我新建 FtRepayType 福费延还款复合类型，贷款领域，子包 ft/repay

FtRepayChkInPojo 福费延还款校验输入
  福费延借据编码  必输
  融资业务编码

FtRepayChkOutPojo 福费延还款校验输出
  处理结果
  错误信息
```

**生成结果**：
- 文件路径：`loan-resources/src/main/resources/type/ft/repay/FtRepayType.c_schema.xml`
- package：`com.spdb.ccbs.loan.resources.type.ft.repay`

### AI 返回格式示例

```
✅ 成功创建复合类型文件

📁 文件位置: loan-resources/src/main/resources/type/ft/repay/FtRepayType.c_schema.xml
📦 package:  com.spdb.ccbs.loan.resources.type.ft.repay
🗂️  子包:     ft/repay
🧩 复合对象: FtRepayChkInPojo、FtRepayChkOutPojo
```

---

## 场景 3：含复合对象引用（[xxx] 语法）

### 指令模板

```
帮我新建 {SchemaId} {文件中文名}，{领域}领域

{ComplexTypeId} {复合对象中文名}
  {普通字段中文名}
  [{引用复合对象中文名}]
  {英文id} [{引用复合对象中文名}]  多值
```

> `[中文名]` 表示引用另一个复合类型对象；中括号前可加英文 id，不加则自动生成。

### 示例 3-A：单值引用（不加英文名）

```
帮我新建 GnSubType 保函处理复合类型，贷款领域

GnSubInPojo 保函处理输入
  币种代码
  摘要编码
  [保函收到撤销索偿]
```

**AI 处理说明**：
- `[保函收到撤销索偿]` → 在 `loan-resources/src/main/resources/type/` 下搜索匹配 complexType
- 找到 `GuaranteeType.GrntRcvCxlClmPojo`
- 自动生成 id：`grntRcvCxlClmPojo`（complexType id 首字母改小写）

### 示例 3-B：多值引用（不加英文名）

```
GnSubInPojo 保函处理输入
  币种代码
  [保函收到撤销索偿]  多值
```

- 多值时 id 自动追加 `List`：`grntRcvCxlClmPojoList`
- `multi="true"`

### 示例 3-C：指定英文 id 的引用

```
GnSubInPojo 保函处理输入
  币种代码
  lstGrntRcvCxl [保函收到撤销索偿]  多值
```

- 用户提供了英文名 `lstGrntRcvCxl` → 直接使用，不自动追加 `List`

### AI 返回格式示例

```
📋 MCP 字段查询结果：
  ✅ 币种代码  →  type=MBaseType.U_BI_ZHONG_DAI_MA  ref=MDict.C.crcyCd
  ✅ 摘要编码  →  type=MBaseType.U_ZHI_YAO_BIAN_MA  ref=MDict.A.abstractCd

🔍 复合对象引用搜索结果：
  ✅ [保函收到撤销索偿]  →  GuaranteeType.GrntRcvCxlClmPojo

✅ 成功创建复合类型文件

📁 文件位置: loan-resources/src/main/resources/type/GnSubType.c_schema.xml
📦 package:  com.spdb.ccbs.loan.resources.type

✅ 所有字段均已写入 XML
```

### 示例 3-D：引用未找到时的提示

```
帮我新建 TestType 测试复合类型，贷款领域

TestPojo 测试对象
  币种代码
  [不存在的对象]
```

**AI 返回**：

```
🔍 复合对象引用搜索结果：
  ❌ [不存在的对象]  →  未找到匹配的 c_schema.xml，已跳过

📋 MCP 字段查询结果：
  ✅ 币种代码  →  type=MBaseType.U_BI_ZHONG_DAI_MA  ref=MDict.C.crcyCd

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  以下字段未写入 XML，请确认后补充：

【复合对象引用未找到】（需确认文件是否已创建）：
  1. [不存在的对象]

💡 完成上述问题后，可重新执行以补充这些字段。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 场景 4：修改现有复合类型

### 指令模板（新增字段）

```
修改 {SchemaId} 中的 {ComplexTypeId}，新增字段 {字段描述}
```

### 指令模板（删除字段）

```
修改 {SchemaId} 中的 {ComplexTypeId}，删除字段 {字段中文名}
```

### 示例 4-A：新增普通字段

```
修改 FtAcctgType 中的 FtAcctRepayChkInPojo，新增字段 申请日期（非必输）、处理结果
```

### 示例 4-B：新增复合对象引用字段

```
修改 GnSubType 中的 GnSubInPojo，新增字段 [保函撤销信息]  多值
```

### 示例 4-C：删除字段

```
修改 FtAcctgType 中的 FtAcctRepayChkInPojo，删除字段 融资业务编码
```

> ⚠️ **说明**：修改指令只更新指定 complexType，文件内其他 complexType 保持不变。

### AI 返回格式示例

```
✅ 成功修改复合类型

📁 文件位置: loan-resources/src/main/resources/type/ft/repay/FtAcctgType.c_schema.xml
🔧 修改对象: FtAcctRepayChkInPojo（福费延还款校验输入）
📌 其他复合对象（FtAcctRepayChkOutPojo）保持不变

📋 MCP 字段查询结果：
  ✅ 申请日期  →  type=MBaseType.U_RI_QI  ref=MDict.A.applyDate
  ✅ 处理结果  →  type=MBaseType.U_JIEGUO  ref=MDict.C.chkRslt

新增字段（共 2 个）:
  ✅ applyDate（申请日期）- 非必输
  ✅ chkRslt（处理结果）- 非必输
```

---

## 场景 5：综合场景（多复合对象 + 引用 + 多值）

```
帮我新建 AbsTestType 测试复合类型，贷款领域

复合对象：FtInternalAcctgPojo 福费延内部记账对象
  交易对方行号
  交易对方行名

复合对象：FtExternalAcctgPojo 福费延外部记账对象
  币种代码
  钞汇代码
  [保函收到撤销索偿]
  摘要编码
```

**AI 工作台展示**：
```
📋 MCP 字段查询结果：
  ✅ 交易对方行号  →  type=MBaseType.U_XX  ref=MDict.J.jyDfhh
  ✅ 交易对方行名  →  type=MBaseType.U_XX  ref=MDict.J.jyDfhm
  ✅ 币种代码      →  type=MBaseType.U_BI_ZHONG_DAI_MA  ref=MDict.C.crcyCd
  ❌ 钞汇代码      →  未贯标（MCP 返回 null），已跳过
  ✅ 摘要编码      →  type=MBaseType.U_ZHI_YAO_BIAN_MA  ref=MDict.A.abstractCd

🔍 复合对象引用搜索结果：
  ✅ [保函收到撤销索偿]  →  GuaranteeType.GrntRcvCxlClmPojo

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  以下字段未写入 XML，请确认后补充：

【未贯标字段】（MCP 返回 null，需完成贯标后重新执行）：
  1. 钞汇代码（FtExternalAcctgPojo）

💡 完成上述问题后，可重新执行以补充这些字段。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 常见错误与修正

### ❌ SchemaId 重复

```
❌ SchemaId 'FtAcctgType' 已存在
   文件位置: loan-resources/src/main/resources/type/ft/repay/FtAcctgType.c_schema.xml
```

**解决**：换一个全局唯一的 SchemaId，或改为修改现有文件。

---

### ❌ 字段未贯标

```
❌ 以下字段未贯标，已从 XML 中强制排除：
  1. 钞汇代码（FtExternalAcctgPojo）

💡 请在 dict-mcp-server 系统完成字段贯标后重新执行
```

**解决**：在 `dict-mcp-server` 字段管理系统中完成贯标，再重新执行指令。

---

### ❌ 复合对象引用未找到

```
❌ [保函收到撤销索偿] 在当前模块 type/ 目录下未找到对应文件
```

**解决**：
1. 确认引用的复合类型文件（`*.c_schema.xml`）已创建
2. 确认中文名与目标 complexType 的 `longname` 完全一致
3. 重新执行指令

---

### ❌ 复合对象引用有多个匹配

```
⚠️ [结算信息输出] 找到 2 个匹配，请确认使用哪一个：
  1. ObDealTpMgmtType.ObCstSetl（结算信息输出）
  2. SettFlowType.SettInfoOut（结算信息输出）
```

**解决**：回复序号（如「1」）指定使用哪一个。

---

### ❌ 领域填写错误

| 错误输入 | 原因 | 正确写法 |
|---------|------|---------|
| `贷款domain` | 不识别英文 | `贷款领域` |
| `loan` | 不识别英文缩写 | `贷款领域` |
| `公共领域` | 非标准领域名 | `平台公共领域` |

---

## 快速指令速查

| 场景 | 指令起始语 |
|------|-----------|
| 创建新复合类型（默认路径） | `帮我新建 {SchemaId} {中文名}，{领域}领域` |
| 创建带子包的复合类型 | `帮我新建 {SchemaId} {中文名}，{领域}领域，子包 {子包路径}` |
| 修改某 complexType | `修改 {SchemaId} 中的 {ComplexTypeId}，新增/删除字段 {字段描述}` |
| 删除某 complexType | `删除 {SchemaId} 中的 {ComplexTypeId}` |
| 引用其他复合类型（单值） | 字段行写 `[中文名]` |
| 引用其他复合类型（多值） | 字段行写 `[中文名]  多值` |
| 引用时指定英文 id | 字段行写 `英文id [中文名]` |
| 必输字段 | 字段行末加 `  必输` |
| 多值字段 | 字段行末加 `  多值` |
