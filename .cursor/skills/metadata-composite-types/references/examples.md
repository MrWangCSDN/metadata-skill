# 复合类型元数据完整示例

## 示例 1：基本复合类型创建（含输入输出 Pojo）

**用户输入**：
```
帮我新建 FtAcctgType 福费延还款复合类型，贷款领域，子包 ft/repay

包含以下复合对象：

FtAcctRepayChkInPojo 福费延还款校验输入
  fRFTGDueBillCd  福费延借据编码  非必输
  fncgBsnID       融资业务编码    非必输

FtAcctRepayChkOutPojo 福费延还款校验输出
  fRFTGDueBillCd  福费延借据编码
  fncgBsnID       融资业务编码
```

**生成的 XML**：
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="FtAcctgType" package="com.spdb.ccbs.loan.resources.type.ft.repay" longname="福费延还款复合类型" classgen="auto" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
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

**文件路径**：`loan-resources/src/main/resources/type/ft/repay/FtAcctgType.c_schema.xml`

---

## 示例 2：含复合类型引用字段（用户提供英文名）

**用户输入**：
```
帮我新建 SyndAgrmLoanType 银团贷款协议复合类型，贷款领域，子包 synd

SyndAgrmLoanQryOutPojo 银团贷款协议查询输出
  custId                       客户ID                  必输
  lstSyndAgrmLoanInfoPojo       银团贷款出资份额信息（复合对象）  多值
```

**处理流程**：
1. `custId` → 查 MCP
2. `lstSyndAgrmLoanInfoPojo 银团贷款出资份额信息（复合对象）多值`：
   - 用户**提供了英文名** `lstSyndAgrmLoanInfoPojo` → id 直接使用 `lstSyndAgrmLoanInfoPojo`
   - longname = `银团贷款出资份额信息`
   - 在 `loan-resources/src/main/resources/type/` 下搜索 `*.c_schema.xml`，找到 `longname="银团贷款出资份额信息"` 的 complexType
   - 假设找到文件 schema id=`SyndAgrmLoanType`，complexType id=`SyndAgrmLoanInfoPojo`
   - type = `SyndAgrmLoanType.SyndAgrmLoanInfoPojo`
   - multi = `true`（标注了多值）

**生成的 XML**：
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="SyndAgrmLoanType" package="com.spdb.ccbs.loan.resources.type.synd" longname="银团贷款协议复合类型" classgen="auto" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <complexType abstract="false" dict="false" id="SyndAgrmLoanQryOutPojo" introduct="false" localName="" longname="银团贷款协议查询输出" extension="" tags="">
        <element id="custId" longname="客户ID" type="MBaseType.U_KE_HU_BIAN_HAO" required="true" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.C.custId"/>
        <element id="lstSyndAgrmLoanInfoPojo" longname="银团贷款出资份额信息" type="SyndAgrmLoanType.SyndAgrmLoanInfoPojo" required="false" multi="true" range="false" array="false" final="false" override="false" allowSubType="true" key="false"/>
    </complexType>
</schema>
```

**关键点**：
- 用户提供了英文名 `lstSyndAgrmLoanInfoPojo`，直接作为 `id`，不自动追加 `List`
- `type` 的值来自搜索到的文件：`{schema标签id}.{complexType id}`
- 无 `ref` 属性
- `multi="true"` 表示这是一个 List（对象数组）

---

## 示例 2b：含复合类型引用字段（用户未提供英文名）

**用户输入**：
```
帮我新建 ObDealType 交易处理复合类型，结算领域

ObDealQryOutPojo 交易查询输出
  结算信息输出（复合对象）
  结算信息输出（复合对象）  多值
```

**处理流程**：
1. `结算信息输出（复合对象）`：
   - 用户**未提供英文名**
   - 在 `sett-resources/src/main/resources/type/` 下搜索，找到 `ObDealTpMgmtType.c_schema.xml`，其中 `complexType longname="结算信息输出"` 对应 id=`ObCstSetl`
   - type = `ObDealTpMgmtType.ObCstSetl`
   - id = complexType id 首字母改小写 = `obCstSetl`（单值）
   - id = `obCstSetlList`（多值时追加 List）
   - longname = `结算信息输出`

**生成的 XML**：
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="ObDealType" package="com.spdb.ccbs.sett.resources.type" longname="交易处理复合类型" classgen="auto" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <complexType abstract="false" dict="false" id="ObDealQryOutPojo" introduct="false" localName="" longname="交易查询输出" extension="" tags="">
        <element id="obCstSetl" longname="结算信息输出" type="ObDealTpMgmtType.ObCstSetl" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false"/>
        <element id="obCstSetlList" longname="结算信息输出" type="ObDealTpMgmtType.ObCstSetl" required="false" multi="true" range="false" array="false" final="false" override="false" allowSubType="true" key="false"/>
    </complexType>
</schema>
```

**关键点**：
- 未提供英文名 → 参考找到的 complexType id（`ObCstSetl`），首字母小写作为 id（单值：`obCstSetl`，多值：`obCstSetlList`）
- `type` = `ObDealTpMgmtType.ObCstSetl`（从文件 schema id + complexType id 组合）

---

## 示例 3：含未贯标字段

**用户输入**：
```
帮我新建 CustInfoType 客户信息复合类型，平台公共领域

CustBaseInfoPojo 客户基础信息
  custId    客户ID    必输
  custName  客户名称  非必输
  unknownField  未知字段  非必输
```

**MCP 查询结果**：
```
custId    → ✅ 已贯标
custName  → ✅ 已贯标
unknownField → ❌ 返回 null（未贯标）
```

**生成的 XML**（未贯标字段强制排除）：
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="CustInfoType" package="com.spdb.ccbs.comm.resources.type.cust" longname="客户信息复合类型" classgen="auto" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <complexType abstract="false" dict="false" id="CustBaseInfoPojo" introduct="false" localName="" longname="客户基础信息" extension="" tags="">
        <element id="custId" longname="客户ID" type="MBaseType.U_KE_HU_BIAN_HAO" required="true" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.C.custId"/>
        <element id="custName" longname="客户名称" type="MBaseType.U_KE_HU_MING_CHENG" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.C.custName"/>
    </complexType>
</schema>
```

**AI 反馈**：
```
⚠️  以下字段未贯标，已从 XML 中强制排除（共 1 个）:
  1. unknownField（未知字段）← MCP 返回 null，未写入 XML

✅ 已成功写入字段（共 2 个）:
  - custId (客户ID)
  - custName (客户名称)

📁 文件位置: comm-resources/src/main/resources/type/cust/CustInfoType.c_schema.xml
```

---

## 示例 4：修改现有复合类型

**用户输入**：
```
修改 FtAcctgType 中的 FtAcctRepayChkInPojo，新增字段 applyDate 申请日期（非必输）
```

**处理流程**：
1. 定位 `FtAcctgType.c_schema.xml`
2. 读取原文件，保留 `schema` 标签所有属性
3. 调用 MCP 查询 `申请日期`
4. 仅更新 `FtAcctRepayChkInPojo` 的 `element` 列表，追加新字段
5. `FtAcctRepayChkOutPojo` 保持不变

**修改后**：
```xml
<complexType abstract="false" dict="false" id="FtAcctRepayChkInPojo" introduct="false" localName="" longname="福费延还款校验输入" extension="" tags="">
    <element id="fRFTGDueBillCd" longname="福费延借据编码" type="MBaseType.U_DAI_KUAN_JIE_JU_BIAN_MA" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.F.fRFTGDueBillCd"/>
    <element id="fncgBsnID" longname="融资业务编码" type="MBaseType.U_RONG_ZI_YE_WU_BIAN_MA" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.F.fncgBsnID"/>
    <element id="applyDate" longname="申请日期" type="MBaseType.U_RI_QI" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.A.applyDate"/>
</complexType>
```

---

## 示例 5：多领域示例对比

| 场景 | SchemaId | 领域 | package | 文件路径 |
|------|---------|------|---------|---------|
| 存款账户类型 | DeptAcctType | 存款 | com.spdb.ccbs.dept.resources.type | dept-resources/src/main/resources/type/DeptAcctType.c_schema.xml |
| 贷款申请类型 | LoanApplType | 贷款 | com.spdb.ccbs.loan.resources.type | loan-resources/src/main/resources/type/LoanApplType.c_schema.xml |
| 结算流水类型 | SettFlowType | 结算 | com.spdb.ccbs.sett.resources.type | sett-resources/src/main/resources/type/SettFlowType.c_schema.xml |
| 公共客户类型 | CommCustType | 平台公共 | com.spdb.ccbs.comm.resources.type | comm-resources/src/main/resources/type/CommCustType.c_schema.xml |

---

## 对话指令速查

| 场景 | 指令示例 |
|------|---------|
| 创建新文件 | `帮我新建 {SchemaId} {文件中文名}，{领域}领域` |
| 指定子包 | `帮我新建 {SchemaId} {中文名}，{领域}领域，子包 {子包路径}` |
| 修改某 complexType | `修改 {SchemaId} 中的 {ComplexTypeId}，{新增/删除/修改}字段 {字段描述}` |
| 删除某 complexType | `删除 {SchemaId} 中的 {ComplexTypeId}` |
| 删除整个文件 | `删除复合类型文件 {SchemaId}` |

---

## 示例 6：含复合对象引用和多值字段

**用户输入**：
```
帮我新建 FtExtAcctgType 福费延外部记账复合类型，贷款领域

FtExtAcctgPojo 福费延外部记账对象
  币种代码
  摘要编码
  保函收到撤销索偿（复合对象）
  S码
```

**处理流程**：

1. `币种代码`、`摘要编码`、`S码` → 查 MCP 获取字段元数据
2. `保函收到撤销索偿（复合对象）` → **调用脚本**（必须传脚本文件完整路径，以 `find_composite_ref.py` 结尾）：
   ```bash
   python "{工作区根目录}/.speedstudio/skills/metadata-composite-types/scripts/find_composite_ref.py" "{工作区根目录}/loan-resources/src/main/resources/type" 保函收到撤销索偿
   ```
   脚本返回：
   ```json
   {
     "found": true,
     "schemaId": "GuaranteeType",
     "complexTypeId": "GrntRcvCxlClmPojo",
     "type": "GuaranteeType.GrntRcvCxlClmPojo"
   }
   ```
   - type = 脚本返回的 `type` 字段 = `GuaranteeType.GrntRcvCxlClmPojo`
   - 用户未提供英文名 → id = 脚本返回 `complexTypeId` 首字母小写 = `grntRcvCxlClmPojo`
   - longname = `保函收到撤销索偿`
   - **脚本返回 `found: false`** → 不写入，反馈提示

**生成的 XML（找到引用的情况）**：
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="FtExtAcctgType" package="com.spdb.ccbs.loan.resources.type" longname="福费延外部记账复合类型" classgen="auto" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <complexType abstract="false" dict="false" id="FtExtAcctgPojo" introduct="false" localName="" longname="福费延外部记账对象" extension="" tags="">
        <element id="crcyCd" longname="币种代码" type="MBaseType.U_BI_ZHONG_DAI_MA" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.C.crcyCd"/>
        <element id="abstractCd" longname="摘要编码" type="MBaseType.U_ZHI_YAO_BIAN_MA" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.A.abstractCd"/>
        <element id="grntRcvCxlClmPojo" longname="保函收到撤销索偿" type="GuaranteeType.GrntRcvCxlClmPojo" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false"/>
        <element id="sCd" longname="S码" type="MBaseType.U_S_MA" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.S.sCd"/>
    </complexType>
</schema>
```

---

## 示例 7：含多值字段（multi=true）

**用户输入**：
```
帮我新建 FtExtAcctgType 福费延外部记账复合类型，贷款领域

FtExtAcctgPojo 福费延外部记账对象
  币种代码   多值
  摘要编码
  保函收到撤销索偿（复合对象）  多值
  S码
```

**multi 处理规则**：
- `币种代码 多值` → `multi="true"`（普通字段的 List）
- `摘要编码` → `multi="false"`（单值，默认）
- `保函收到撤销索偿（复合对象） 多值` → `multi="true"`（复合对象的 List）
- `S码` → `multi="false"`

**生成的 XML**：
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="FtExtAcctgType" package="com.spdb.ccbs.loan.resources.type" longname="福费延外部记账复合类型" classgen="auto" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <complexType abstract="false" dict="false" id="FtExtAcctgPojo" introduct="false" localName="" longname="福费延外部记账对象" extension="" tags="">
        <element id="crcyCd" longname="币种代码" type="MBaseType.U_BI_ZHONG_DAI_MA" required="false" multi="true" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.C.crcyCd"/>
        <element id="abstractCd" longname="摘要编码" type="MBaseType.U_ZHI_YAO_BIAN_MA" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.A.abstractCd"/>
        <element id="grntRcvCxlClmPojoList" longname="保函收到撤销索偿" type="GuaranteeType.GrntRcvCxlClmPojo" required="false" multi="true" range="false" array="false" final="false" override="false" allowSubType="true" key="false"/>
        <element id="sCd" longname="S码" type="MBaseType.U_S_MA" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.S.sCd"/>
    </complexType>
</schema>
```

**关键差异**：`multi="true"` 时，复合对象引用的 `id` 建议以 `List` 结尾（如 `grntRcvCxlClmPojoList`）以表明是集合类型。

---

## 示例 8：复合对象引用未找到

**场景**：`保函收到撤销索偿（复合对象）` 在当前模块 `type/` 目录下未找到对应 `*.c_schema.xml`

**脚本调用**（必须传脚本文件完整路径；Windows 下若 `python` 不可用则改用 `py`）：
```bash
python "{工作区根目录}/.speedstudio/skills/metadata-composite-types/scripts/find_composite_ref.py" "{工作区根目录}/loan-resources/src/main/resources/type" 保函收到撤销索偿
```
**脚本返回**：
```json
{
  "found": false,
  "message": "在 loan-resources/src/main/resources/type 下未找到 longname='保函收到撤销索偿' 的 complexType（共扫描 5 个文件）"
}
```
→ `found: false`，该字段**强制不写入 XML**。

**生成的 XML**（跳过未找到的引用）：
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="FtExtAcctgType" package="com.spdb.ccbs.loan.resources.type" longname="福费延外部记账复合类型" classgen="auto" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <complexType abstract="false" dict="false" id="FtExtAcctgPojo" introduct="false" localName="" longname="福费延外部记账对象" extension="" tags="">
        <element id="crcyCd" longname="币种代码" type="MBaseType.U_BI_ZHONG_DAI_MA" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.C.crcyCd"/>
        <element id="abstractCd" longname="摘要编码" type="MBaseType.U_ZHI_YAO_BIAN_MA" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.A.abstractCd"/>
        <element id="sCd" longname="S码" type="MBaseType.U_S_MA" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.S.sCd"/>
    </complexType>
</schema>
```

**AI 反馈**：
```
🔍 复合对象引用搜索结果：
  ❌ [保函收到撤销索偿]  →  未找到匹配的 c_schema.xml，已跳过

📋 MCP 字段查询结果：
  ✅ 币种代码   →  type=MBaseType.U_BI_ZHONG_DAI_MA  ref=MDict.C.crcyCd
  ✅ 摘要编码   →  type=MBaseType.U_ZHI_YAO_BIAN_MA  ref=MDict.A.abstractCd
  ✅ S码        →  type=MBaseType.U_S_MA  ref=MDict.S.sCd

📁 文件位置: loan-resources/src/main/resources/type/FtExtAcctgType.c_schema.xml

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  以下字段未写入 XML，请确认后补充：

【复合对象引用未找到】（需确认文件是否已创建）：
  1. [保函收到撤销索偿]

💡 完成上述问题后，可重新执行以补充这些字段。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 示例 9：[中括号语法] 演示 — AbsTestType 测试复合类型

**用户输入**：
```
帮我创建 AbsTestType 测试复合类型，贷款领域

复合对象：福费延内部记账对象
  交易对方行号
  交易对方行名

复合对象：福费延外部记账对象
  币种代码
  钞汇代码
  [保函收到撤销索偿]
  摘要编码
```

**字段分析**：
- `福费延内部记账对象`：字段 `交易对方行号`、`交易对方行名` → 查 MCP
- `福费延外部记账对象`：`币种代码`、`摘要编码` → 查 MCP；`钞汇代码` → 查 MCP；`[保函收到撤销索偿]` → 调用脚本搜索

**脚本调用**（使用工作区绝对路径）：
```bash
python "{工作区根目录}/.speedstudio/skills/metadata-composite-types/scripts/find_composite_ref.py" "{工作区根目录}/loan-resources/src/main/resources/type" 保函收到撤销索偿
```

**工作台展示**：
```
📋 MCP 字段查询结果：
  ✅ 交易对方行号  →  type=MBaseType.U_JIAO_YI_DUI_FANG_HANG_HAO  ref=MDict.J.jyDfhh
  ✅ 交易对方行名  →  type=MBaseType.U_JIAO_YI_DUI_FANG_HANG_MING  ref=MDict.J.jyDfhm
  ✅ 币种代码      →  type=MBaseType.U_BI_ZHONG_DAI_MA  ref=MDict.C.crcyCd
  ❌ 钞汇代码      →  未贯标（MCP 返回 null），已跳过
  ✅ 摘要编码      →  type=MBaseType.U_ZHI_YAO_BIAN_MA  ref=MDict.A.abstractCd

🔍 复合对象引用搜索结果：
  ✅ [保函收到撤销索偿]  →  GuaranteeType.GrntRcvCxlClmPojo
```

**生成的 XML**（`钞汇代码` 未贯标跳过，`[保函收到撤销索偿]` 找到并写入）：
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<schema xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="AbsTestType" package="com.spdb.ccbs.loan.resources.type" longname="测试复合类型" classgen="auto" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <complexType abstract="false" dict="false" id="FtInternalAcctgPojo" introduct="false" localName="" longname="福费延内部记账对象" extension="" tags="">
        <element id="jyDfhh" longname="交易对方行号" type="MBaseType.U_JIAO_YI_DUI_FANG_HANG_HAO" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.J.jyDfhh"/>
        <element id="jyDfhm" longname="交易对方行名" type="MBaseType.U_JIAO_YI_DUI_FANG_HANG_MING" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.J.jyDfhm"/>
    </complexType>
    <complexType abstract="false" dict="false" id="FtExternalAcctgPojo" introduct="false" localName="" longname="福费延外部记账对象" extension="" tags="">
        <element id="crcyCd" longname="币种代码" type="MBaseType.U_BI_ZHONG_DAI_MA" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.C.crcyCd"/>
        <element id="grntRcvCxlClmPojo" longname="保函收到撤销索偿" type="GuaranteeType.GrntRcvCxlClmPojo" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false"/>
        <element id="abstractCd" longname="摘要编码" type="MBaseType.U_ZHI_YAO_BIAN_MA" required="false" multi="false" range="false" array="false" final="false" override="false" allowSubType="true" key="false" ref="MDict.A.abstractCd"/>
    </complexType>
</schema>
```

**最终汇总提示**：
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  以下字段未写入 XML，请确认后补充：

【未贯标字段】（MCP 返回 null，需完成贯标后重新执行）：
  1. 钞汇代码（福费延外部记账对象）

💡 完成上述问题后，可重新执行以补充这些字段。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**关键说明**：
- `[保函收到撤销索偿]` 用中括号语法标识复合对象引用，无需写 `（复合对象）`
- 找到后自动写入 element，`type` 来自脚本返回，无 `ref` 属性
- `钞汇代码` 未贯标，已跳过，在汇总框中提示
- 工作台展示 MCP 查询和脚本搜索的完整过程
