# Flowtran 完整示例集

本文档提供 flowtran 交易创建和修改的完整示例。

> 以下示例假设工作空间绝对路径为 `/Users/xxx/project`。

## 示例 1: 基本交易创建 (TY291)

**用户输入**:
```
帮我新建 TY291 收费明细文件批量查询 的联机交易

输入:
cst     国家    非必输
xb      性别    必输

输出:
cst     国家
xb      性别
```

**生成的 XML** (注意:属性单行,标签间无空行,层级缩进):
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<flowtran xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="TY291" longname="收费明细文件批量查询" kind="auto" package="com.spdb.ccbs.comm.pbf.trans" txnMode="A" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <description><![CDATA[收费明细文件批量查询]]></description>
    <interface package="com.spdb.ccbs.comm.pbf.trans.intf">
        <input packMode="true">
            <field id="cst" type="MBaseType.U_GUO_JIA" required="false" multi="false" array="false" longname="国家" ref="MDict.C.cst"/>
            <field id="xb" type="MBaseType.U_XING_BIE" required="true" multi="false" array="false" longname="性别" ref="MDict.X.xb"/>
        </input>
        <output asParm="true" packMode="true">
            <field id="cst" type="MBaseType.U_GUO_JIA" required="false" multi="false" array="false" longname="国家" ref="MDict.C.cst"/>
            <field id="xb" type="MBaseType.U_XING_BIE" required="false" multi="false" array="false" longname="性别" ref="MDict.X.xb"/>
        </output>
    </interface>
</flowtran>
```

**文件绝对路径**: `/Users/xxx/project/ccbs-comm-impl/comm-pbf/src/main/resources/trans/TY291.flowtrans.xml`

## 示例 2: 带数组字段的交易 (TY292)

**用户输入**:
```
帮我新建 TY292 客户信息查询 的联机交易

输入:
custId  客户ID  必输
chargCdArray 收费代码数组 start
    包含 fPrjCd   收费项目编码  非必输
    包含 chrgAmt  收费金额     必输
chargCdArray 收费代码数组 end

输出:
custName  客户名称
resultArray 结果数组 start
    包含 code  代码
    包含 msg   消息
resultArray 结果数组 end
```

**生成的 XML** (注意 fields 内 field 多缩进 4 个空格):
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<flowtran xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="TY292" longname="客户信息查询" kind="auto" package="com.spdb.ccbs.comm.pbf.trans" txnMode="A" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <description><![CDATA[客户信息查询]]></description>
    <interface package="com.spdb.ccbs.comm.pbf.trans.intf">
        <input packMode="true">
            <field id="custId" type="MBaseType.U_KE_HU_BIAN_HAO" required="true" multi="false" array="false" longname="客户ID" ref="MDict.C.custId"/>
            <fields id="chargCdArray" scope="" required="false" multi="true" array="false" longname="收费代码数组">
                <field id="fPrjCd" type="MBaseType.U_SHOU_FEI_XIANG_MU_BIAN_MA" required="false" multi="false" array="false" longname="收费项目编码" ref="MDict.F.fPrjCd"/>
                <field id="chrgAmt" type="MBaseType.U_JIN_E" required="true" multi="false" array="false" longname="收费金额" ref="MDict.C.chrgAmt"/>
            </fields>
        </input>
        <output asParm="true" packMode="true">
            <field id="custName" type="MBaseType.U_KE_HU_MING_CHENG" required="false" multi="false" array="false" longname="客户名称" ref="MDict.C.custName"/>
            <fields id="resultArray" scope="" required="false" multi="true" array="false" longname="结果数组">
                <field id="code" type="MBaseType.U_DAI_MA" required="false" multi="false" array="false" longname="代码" ref="MDict.C.code"/>
                <field id="msg" type="MBaseType.U_XIAO_XI" required="false" multi="false" array="false" longname="消息" ref="MDict.M.msg"/>
            </fields>
        </output>
    </interface>
</flowtran>
```

## 示例 3: 子目录创建 (TY291 in chrg)

**用户输入**:
```
帮我在 chrg 子目录下新建 TY291 收费明细查询 的联机交易

输入:
fPrjCd  收费项目编码  必输

输出:
fPrjCd  收费项目编码
chrgAmt 收费金额
```

**生成的 XML**:
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<flowtran xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="TY291" longname="收费明细查询" kind="auto" package="com.spdb.ccbs.comm.pbf.trans.chrg" txnMode="A" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <description><![CDATA[收费明细查询]]></description>
    <interface package="com.spdb.ccbs.comm.pbf.trans.chrg.intf">
        <input packMode="true">
            <field id="fPrjCd" type="MBaseType.U_SHOU_FEI_XIANG_MU_BIAN_MA" required="true" multi="false" array="false" longname="收费项目编码" ref="MDict.F.fPrjCd"/>
        </input>
        <output asParm="true" packMode="true">
            <field id="fPrjCd" type="MBaseType.U_SHOU_FEI_XIANG_MU_BIAN_MA" required="false" multi="false" array="false" longname="收费项目编码" ref="MDict.F.fPrjCd"/>
            <field id="chrgAmt" type="MBaseType.U_JIN_E" required="false" multi="false" array="false" longname="收费金额" ref="MDict.C.chrgAmt"/>
        </output>
    </interface>
</flowtran>
```

**文件绝对路径**: `/Users/xxx/project/ccbs-comm-impl/comm-pbf/src/main/resources/trans/chrg/TY291.flowtrans.xml`

**关键差异**:
- package: `com.spdb.ccbs.comm.pbf.trans.chrg` (追加了 .chrg)
- interface package: `com.spdb.ccbs.comm.pbf.trans.chrg.intf`

## 示例 4: 不同领域交易

### 存款领域 (TC100)

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<flowtran xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="TC100" longname="存款账户查询" kind="auto" package="com.spdb.ccbs.dept.pbf.trans" txnMode="A" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <description><![CDATA[存款账户查询]]></description>
    <interface package="com.spdb.ccbs.dept.pbf.trans.intf">
        <input packMode="true">
            <field id="accountNo" type="MBaseType.U_ZHANG_HAO" required="true" multi="false" array="false" longname="账号" ref="MDict.A.accountNo"/>
        </input>
        <output asParm="true" packMode="true">
            <field id="accountNo" type="MBaseType.U_ZHANG_HAO" required="false" multi="false" array="false" longname="账号" ref="MDict.A.accountNo"/>
            <field id="balance" type="MBaseType.U_JIN_E" required="false" multi="false" array="false" longname="余额" ref="MDict.B.balance"/>
        </output>
    </interface>
</flowtran>
```

**文件绝对路径**: `/Users/xxx/project/ccbs-dept-impl/dept-pbf/src/main/resources/trans/TC100.flowtrans.xml`

### 贷款领域 (TD250)

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<flowtran xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="TD250" longname="贷款申请" kind="auto" package="com.spdb.ccbs.loan.pbf.trans" txnMode="A" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <description><![CDATA[贷款申请]]></description>
    <interface package="com.spdb.ccbs.loan.pbf.trans.intf">
        <input packMode="true">
            <field id="custId" type="MBaseType.U_KE_HU_BIAN_HAO" required="true" multi="false" array="false" longname="客户ID" ref="MDict.C.custId"/>
            <field id="loanAmount" type="MBaseType.U_JIN_E" required="true" multi="false" array="false" longname="贷款金额" ref="MDict.L.loanAmount"/>
        </input>
        <output asParm="true" packMode="true">
            <field id="applicationId" type="MBaseType.U_BIAN_HAO" required="false" multi="false" array="false" longname="申请编号" ref="MDict.A.applicationId"/>
            <field id="approvalStatus" type="MBaseType.U_ZHUANG_TAI" required="false" multi="false" array="false" longname="审批状态" ref="MDict.A.approvalStatus"/>
        </output>
    </interface>
</flowtran>
```

**文件绝对路径**: `/Users/xxx/project/ccbs-loan-impl/loan-pbf/src/main/resources/trans/TD250.flowtrans.xml`

## 示例 5: 修改现有交易

**原 TY291 文件内容**:
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<flowtran id="TY291" longname="收费明细文件批量查询" kind="auto" package="com.spdb.ccbs.comm.pbf.trans" txnMode="A" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
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

**用户输入**:
```
修改 TY291

输入:
cst     国家    非必输
xb      性别    必输
newField  新字段  非必输

输出:
cst     国家
xb      性别
newField  新字段
result    结果
```

**修改后的文件** (保留 flowtran/description/interface 属性,仅更新 input/output):
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<flowtran id="TY291" longname="收费明细文件批量查询" kind="auto" package="com.spdb.ccbs.comm.pbf.trans" txnMode="A" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <description><![CDATA[收费明细文件批量查询]]></description>
    <interface package="com.spdb.ccbs.comm.pbf.trans.intf">
        <input packMode="true">
            <field id="cst" type="MBaseType.U_GUO_JIA" required="false" multi="false" array="false" longname="国家" ref="MDict.C.cst"/>
            <field id="xb" type="MBaseType.U_XING_BIE" required="true" multi="false" array="false" longname="性别" ref="MDict.X.xb"/>
            <field id="newField" type="MBaseType.U_NEW_FIELD" required="false" multi="false" array="false" longname="新字段" ref="MDict.N.newField"/>
        </input>
        <output asParm="true" packMode="true">
            <field id="cst" type="MBaseType.U_GUO_JIA" required="false" multi="false" array="false" longname="国家" ref="MDict.C.cst"/>
            <field id="xb" type="MBaseType.U_XING_BIE" required="false" multi="false" array="false" longname="性别" ref="MDict.X.xb"/>
            <field id="newField" type="MBaseType.U_NEW_FIELD" required="false" multi="false" array="false" longname="新字段" ref="MDict.N.newField"/>
            <field id="result" type="MBaseType.U_JIE_GUO" required="false" multi="false" array="false" longname="结果" ref="MDict.R.result"/>
        </output>
    </interface>
</flowtran>
```

**关键**:
- ✅ 保留 flowtran 标签的所有属性
- ✅ 保留 description 标签内容
- ✅ 保留 interface package 属性
- ✅ 只更新 input 和 output 的内容
- ✅ 保持正确的缩进层级

## 示例 6: 复杂数组嵌套

**用户输入**:
```
帮我新建 TY295 客户账户综合查询 的联机交易

输入:
custId  客户ID  必输
accountArray 账户数组 start
    包含 accountNo    账号        必输
    包含 accountType  账户类型     非必输
accountArray 账户数组 end
transArray 交易数组 start
    包含 transId      交易ID      必输
    包含 transAmt     交易金额     必输
transArray 交易数组 end
queryDate  查询日期  非必输

输出:
custName  客户名称
accountArray 账户数组 start
    包含 accountNo    账号
    包含 balance      余额
accountArray 账户数组 end
totalCount  总记录数
```

**生成的 XML** (完整层级缩进):
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<flowtran xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="TY295" longname="客户账户综合查询" kind="auto" package="com.spdb.ccbs.comm.pbf.trans" txnMode="A" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <description><![CDATA[客户账户综合查询]]></description>
    <interface package="com.spdb.ccbs.comm.pbf.trans.intf">
        <input packMode="true">
            <field id="custId" type="MBaseType.U_KE_HU_BIAN_HAO" required="true" multi="false" array="false" longname="客户ID" ref="MDict.C.custId"/>
            <fields id="accountArray" scope="" required="false" multi="true" array="false" longname="账户数组">
                <field id="accountNo" type="MBaseType.U_ZHANG_HAO" required="true" multi="false" array="false" longname="账号" ref="MDict.A.accountNo"/>
                <field id="accountType" type="MBaseType.U_ZHANG_HU_LEI_XING" required="false" multi="false" array="false" longname="账户类型" ref="MDict.A.accountType"/>
            </fields>
            <fields id="transArray" scope="" required="false" multi="true" array="false" longname="交易数组">
                <field id="transId" type="MBaseType.U_JIAO_YI_BIAN_HAO" required="true" multi="false" array="false" longname="交易ID" ref="MDict.T.transId"/>
                <field id="transAmt" type="MBaseType.U_JIN_E" required="true" multi="false" array="false" longname="交易金额" ref="MDict.T.transAmt"/>
            </fields>
            <field id="queryDate" type="MBaseType.U_RI_QI" required="false" multi="false" array="false" longname="查询日期" ref="MDict.Q.queryDate"/>
        </input>
        <output asParm="true" packMode="true">
            <field id="custName" type="MBaseType.U_KE_HU_MING_CHENG" required="false" multi="false" array="false" longname="客户名称" ref="MDict.C.custName"/>
            <fields id="accountArray" scope="" required="false" multi="true" array="false" longname="账户数组">
                <field id="accountNo" type="MBaseType.U_ZHANG_HAO" required="false" multi="false" array="false" longname="账号" ref="MDict.A.accountNo"/>
                <field id="balance" type="MBaseType.U_YU_E" required="false" multi="false" array="false" longname="余额" ref="MDict.B.balance"/>
            </fields>
            <field id="totalCount" type="MBaseType.U_JI_SHU" required="false" multi="false" array="false" longname="总记录数" ref="MDict.T.totalCount"/>
        </output>
    </interface>
</flowtran>
```

## 缩进层级对照表

| 标签路径 | 层级 | 空格数 | 示例 |
|---------|------|--------|------|
| flowtran | 0 | 0 | `<flowtran>` |
| flowtran/description | 1 | 4 | `    <description>` |
| flowtran/interface | 1 | 4 | `    <interface>` |
| flowtran/interface/input | 2 | 8 | `        <input>` |
| flowtran/interface/input/field | 3 | 12 | `            <field>` |
| flowtran/interface/input/fields | 3 | 12 | `            <fields>` |
| flowtran/interface/input/fields/field | 4 | 16 | `                <field>` |

## 示例 7: 含属性接口（property）的交易

**用户输入**：
```
帮我新建 TD300 贷款账号综合查询 的联机交易

输入:
custId   客户ID   必输
queryDate 查询日期

输出:
custName  客户名称
totalCount 总记录数

属性接口：
[贷款查询存款账号输入列表]  多值  必输
[贷款查询公共账号输出列表]
查询笔数
可用余额
```

**字段分类处理**：

1. **input**（`custId`、`queryDate`）→ 查 MCP
2. **output**（`custName`、`totalCount`）→ 查 MCP
3. **property 中 `[贷款查询存款账号输入列表]`** → 调用脚本：
   ```bash
   python "{工作区根目录}/.speedstudio/skills/metadata-composite-types/scripts/find_composite_ref.py" "{工作区根目录}/loan-resources/src/main/resources/type" 贷款查询存款账号输入列表
   ```
   - 找到：`type=LoanQueryType.DkCxCkZhSrIn`，多值 → `multi="true"`，必输 → `required="true"`
   - id：无英文名 + 多值 → 取 complexTypeId 首字母小写 + `List` = `dkCxCkZhSrInList`
4. **property 中 `[贷款查询公共账号输出列表]`** → 调用脚本搜索，单值
5. **property 中 `查询笔数`、`可用余额`** → 查 MCP（普通字段）

**工作台展示**：
```
📋 MCP 字段查询结果：
  ✅ 客户ID     →  type=MBaseType.U_KE_HU_BIAN_HAO  ref=MDict.C.custId
  ✅ 查询日期   →  type=MBaseType.U_RI_QI  ref=MDict.Q.queryDate
  ✅ 客户名称   →  type=MBaseType.U_KE_HU_MING_CHENG  ref=MDict.C.custName
  ✅ 总记录数   →  type=MBaseType.U_JI_SHU  ref=MDict.T.totalCount
  ✅ 查询笔数   →  type=MBaseType.U_JI_SHU  ref=MDict.Q.queryCount
  ❌ 可用余额   →  未贯标（MCP 返回 null），已跳过

🔍 复合对象引用搜索结果（property）：
  ✅ [贷款查询存款账号输入列表]  →  LoanQueryType.DkCxCkZhSrIn
  ✅ [贷款查询公共账号输出列表]  →  LoanQueryType.DkCxGgZhSc
```

**生成的 XML**：
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<flowtran xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="TD300" longname="贷款账号综合查询" kind="auto" package="com.spdb.ccbs.loan.pbf.trans" txnMode="A" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <description><![CDATA[贷款账号综合查询]]></description>
    <interface package="com.spdb.ccbs.loan.pbf.trans.intf">
        <input packMode="true">
            <field id="custId" type="MBaseType.U_KE_HU_BIAN_HAO" required="true" multi="false" array="false" longname="客户ID" ref="MDict.C.custId"/>
            <field id="queryDate" type="MBaseType.U_RI_QI" required="false" multi="false" array="false" longname="查询日期" ref="MDict.Q.queryDate"/>
        </input>
        <output asParm="true" packMode="true">
            <field id="custName" type="MBaseType.U_KE_HU_MING_CHENG" required="false" multi="false" array="false" longname="客户名称" ref="MDict.C.custName"/>
            <field id="totalCount" type="MBaseType.U_JI_SHU" required="false" multi="false" array="false" longname="总记录数" ref="MDict.T.totalCount"/>
        </output>
        <property packMode="true">
            <field id="dkCxCkZhSrInList" type="LoanQueryType.DkCxCkZhSrIn" required="true" multi="true" longname="贷款查询存款账号输入列表"/>
            <field id="dkCxGgZhSc" type="LoanQueryType.DkCxGgZhSc" required="false" multi="false" longname="贷款查询公共账号输出列表"/>
            <field id="queryCount" type="MBaseType.U_JI_SHU" required="false" multi="false" array="false" longname="查询笔数" ref="MDict.Q.queryCount"/>
        </property>
    </interface>
</flowtran>
```

**最终汇总提示**：
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  以下字段未写入 XML，请确认后补充：

【未贯标字段】（MCP 返回 null，需完成贯标后重新执行）：
  1. 可用余额（property）

💡 完成上述问题后，可重新执行以补充这些字段。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**关键说明**：
- `[贷款查询存款账号输入列表]  多值  必输` → 复合引用 field，无 `array`，无 `ref`，`required="true"`, `multi="true"`
- `[贷款查询公共账号输出列表]` → 单值复合引用，`multi="false"`，id 取 complexTypeId 首字母小写
- `查询笔数`、`可用余额` → 普通字段，查 MCP；`可用余额` 未贯标则跳过
- property 在 output 之后

---

## 示例 8: property 中复合引用未找到

**场景**：property 中的 `[贷款查询存款账号输入列表]` 在 `loan-resources` 目录下未找到对应 `*.c_schema.xml`

**脚本返回**：
```json
{
  "found": false,
  "message": "在 loan-resources/src/main/resources/type 下未找到 longname='贷款查询存款账号输入列表' 的 complexType（共扫描 8 个文件）"
}
```

**工作台立即输出**：
```
🔍 复合对象引用搜索结果（property）：
  ❌ [贷款查询存款账号输入列表]  →  未找到匹配的 c_schema.xml，已跳过
  ✅ [贷款查询公共账号输出列表]  →  LoanQueryType.DkCxGgZhSc
```

**生成的 XML**（未找到的引用不写入）：
```xml
<property packMode="true">
    <field id="dkCxGgZhSc" type="LoanQueryType.DkCxGgZhSc" required="false" multi="false" longname="贷款查询公共账号输出列表"/>
    <field id="queryCount" type="MBaseType.U_JI_SHU" required="false" multi="false" array="false" longname="查询笔数" ref="MDict.Q.queryCount"/>
</property>
```

**最终汇总提示**：
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  以下字段未写入 XML，请确认后补充：

【property 复合对象引用未找到】（需确认 c_schema.xml 是否已创建）：
  1. [贷款查询存款账号输入列表]

💡 确认文件已创建后，可重新执行以补充这些字段。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 示例 9: 含流程编排（flow）的交易

**用户输入**：
```
帮我新建 TC200 存款账户综合处理 的联机交易

输入:
accountNo  账号  必输
crcyCd     币种代码

输出:
accountNo  账号
balance    余额

流程编排：
服务：内部户账户信息查询
服务：获取放款和贷款还款账号对应的模块信息
方法：beforeQryAcctInfo 外调存款公共通用记账前处理
服务：负债账户支取
方法：第一次记账后处理
```

**处理步骤**：

1. **input/output**（`账号`、`币种代码`、`余额`）→ 查 MCP
2. **流程编排服务搜索**：
   - `内部户账户信息查询` → 调用 `find_services_ref.py` 脚本：
     ```bash
     python "{工作区根目录}/.speedstudio/skills/metadata-services/scripts/find_services_ref.py" "{工作区根目录}" 内部户账户信息查询
     ```
     找到：`serviceTypeId=IoCpInnerAcctInfoQryPbsSvtp`，`serviceId=IoCpInnerAcctInfoQryPbsSvtp`
   - `获取放款和贷款还款账号对应的模块信息` → 调用脚本搜索
     找到：`serviceTypeId=LoanRepayModInfoQryPbsSvtp`，`serviceId=LoanRepayModInfoQryPbsSvtp`
   - `负债账户支取` → 调用脚本搜索
     未找到 → 调用 MCP `queryServiceDetail` → 找到：`serviceTypeId=DebtAcctWithdrawPbsSvtp`，`serviceId=DebtAcctWithdrawPbsSvtp`
3. **流程编排方法节点**：
   - `beforeQryAcctInfo 外调存款公共通用记账前处理` → method="beforeQryAcctInfo"，longname="外调存款公共通用记账前处理"，desc="外调存款公共通用记账前处理"
   - `第一次记账后处理` → 无英文名，翻译 → method="firstPostAcctProcess"，longname="第一次记账后处理"，desc="第一次记账后处理"

**工作台展示**：
```
📋 MCP 字段查询结果：
  ✅ 账号       →  type=MBaseType.U_ZHANG_HAO  ref=MDict.A.accountNo
  ✅ 币种代码   →  type=MBaseType.U_BI_ZHONG_DAI_MA  ref=MDict.C.crcyCd
  ✅ 余额       →  type=MBaseType.U_JIN_E  ref=MDict.B.balance

🔍 流程编排服务搜索结果：
  ✅ 内部户账户信息查询  →  serviceTypeId=IoCpInnerAcctInfoQryPbsSvtp, serviceId=IoCpInnerAcctInfoQryPbsSvtp → serviceName=IoCpInnerAcctInfoQryPbsSvtp.IoCpInnerAcctInfoQryPbsSvtp（脚本找到）
  ✅ 获取放款和贷款还款账号对应的模块信息  →  serviceTypeId=LoanRepayModInfoQryPbsSvtp, serviceId=LoanRepayModInfoQryPbsSvtp → serviceName=LoanRepayModInfoQryPbsSvtp.LoanRepayModInfoQryPbsSvtp（脚本找到）
  ✅ 负债账户支取  →  serviceTypeId=DebtAcctWithdrawPbsSvtp, serviceId=DebtAcctWithdrawPbsSvtp → serviceName=DebtAcctWithdrawPbsSvtp.DebtAcctWithdrawPbsSvtp（MCP 找到）
```

**生成的 XML**：
```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<flowtran xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="TC200" longname="存款账户综合处理" kind="auto" package="com.spdb.ccbs.dept.pbf.trans" txnMode="A" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <description><![CDATA[存款账户综合处理]]></description>
    <interface package="com.spdb.ccbs.dept.pbf.trans.intf">
        <input packMode="true">
            <field id="accountNo" type="MBaseType.U_ZHANG_HAO" required="true" multi="false" array="false" longname="账号" ref="MDict.A.accountNo"/>
            <field id="crcyCd" type="MBaseType.U_BI_ZHONG_DAI_MA" required="false" multi="false" array="false" longname="币种代码" ref="MDict.C.crcyCd"/>
        </input>
        <output asParm="true" packMode="true">
            <field id="accountNo" type="MBaseType.U_ZHANG_HAO" required="false" multi="false" array="false" longname="账号" ref="MDict.A.accountNo"/>
            <field id="balance" type="MBaseType.U_JIN_E" required="false" multi="false" array="false" longname="余额" ref="MDict.B.balance"/>
        </output>
    </interface>
    <flow>
        <service mappingToProperty="true" serviceName="IoCpInnerAcctInfoQryPbsSvtp.IoCpInnerAcctInfoQryPbsSvtp" id="IoCpInnerAcctInfoQryPbsSvtp" longname="内部户账户信息查询"/>
        <service mappingToProperty="true" serviceName="LoanRepayModInfoQryPbsSvtp.LoanRepayModInfoQryPbsSvtp" id="LoanRepayModInfoQryPbsSvtp" longname="获取放款和贷款还款账号对应的模块信息"/>
        <method method="beforeQryAcctInfo" id="beforeQryAcctInfo" longname="外调存款公共通用记账前处理" desc="外调存款公共通用记账前处理"/>
        <service mappingToProperty="true" serviceName="DebtAcctWithdrawPbsSvtp.DebtAcctWithdrawPbsSvtp" id="DebtAcctWithdrawPbsSvtp" longname="负债账户支取"/>
        <method method="firstPostAcctProcess" id="firstPostAcctProcess" longname="第一次记账后处理" desc="第一次记账后处理"/>
    </flow>
</flowtran>
```

**文件绝对路径**: `/Users/xxx/project/ccbs-dept-impl/dept-pbf/src/main/resources/trans/TC200.flowtrans.xml`

**关键说明**：
- flow 标签位于 interface 之后
- service 和 method 按用户指定的顺序排列
- service 标签的 `serviceName` 和 `id` 来自服务文件搜索结果
- method 标签的 `method` 和 `id` 值一致
- 未指定英文名的方法节点，中文翻译为英文小驼峰
- 未指定 `desc` 的方法节点，`desc` 与 `longname` 相同

---

## 示例 10: 流程编排中服务未找到

**场景**：流程编排中的「负债账户支取」在脚本和 MCP 中均未找到

**脚本返回**：
```json
[
  {
    "found": false,
    "query": "负债账户支取",
    "scannedServices": 156,
    "message": "未找到匹配 '负债账户支取' 的服务（共扫描 156 个 service）"
  }
]
```

**MCP queryServiceDetail 返回**：无匹配结果

**工作台输出**：
```
🔍 流程编排服务搜索结果：
  ✅ 内部户账户信息查询  →  serviceTypeId=IoCpInnerAcctInfoQryPbsSvtp, serviceId=IoCpInnerAcctInfoQryPbsSvtp → serviceName=IoCpInnerAcctInfoQryPbsSvtp.IoCpInnerAcctInfoQryPbsSvtp（脚本找到）
  ❌ 负债账户支取  →  服务不存在（脚本未找到，MCP 也未找到），已跳过
```

**生成的 XML**（未找到的服务不写入 flow）：
```xml
<flow>
    <service mappingToProperty="true" serviceName="IoCpInnerAcctInfoQryPbsSvtp.IoCpInnerAcctInfoQryPbsSvtp" id="IoCpInnerAcctInfoQryPbsSvtp" longname="内部户账户信息查询"/>
    <method method="beforeQryAcctInfo" id="beforeQryAcctInfo" longname="外调存款公共通用记账前处理" desc="外调存款公共通用记账前处理"/>
</flow>
```

**最终汇总提示**：
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  以下内容未写入 XML，请确认后补充：

【流程编排服务未找到】（需确认服务是否已创建）：
  1. 负债账户支取

💡 确认服务已创建后，可重新执行以补充这些节点。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 示例 11: 含方法描述的流程编排

**用户输入**：
```
帮我新建 TC250 存款支取交易 的联机交易

输入:
accountNo  账号  必输

输出:
accountNo  账号

流程编排：
服务：内部户账户信息查询
方法：beforeQryAcctInfo 外调存款公共通用记账前处理
服务：负债账户支取   描述：用于存入支取
方法：doProcess 记账处理   描述：执行核心记账逻辑
方法：第一次记账后处理
```

**方法节点解析**：
- `beforeQryAcctInfo 外调存款公共通用记账前处理` → method="beforeQryAcctInfo"，desc="外调存款公共通用记账前处理"（无描述，desc=longname）
- `doProcess 记账处理   描述：执行核心记账逻辑` → method="doProcess"，longname="记账处理"，desc="执行核心记账逻辑"（有描述）
- `第一次记账后处理` → method=翻译英文，desc="第一次记账后处理"（无英文名，无描述）

**生成的 flow**：
```xml
<flow>
    <service mappingToProperty="true" serviceName="IoCpInnerAcctInfoQryPbsSvtp.IoCpInnerAcctInfoQryPbsSvtp" id="IoCpInnerAcctInfoQryPbsSvtp" longname="内部户账户信息查询"/>
    <method method="beforeQryAcctInfo" id="beforeQryAcctInfo" longname="外调存款公共通用记账前处理" desc="外调存款公共通用记账前处理"/>
    <service mappingToProperty="true" serviceName="DebtAcctWithdrawPbsSvtp.DebtAcctWithdrawPbsSvtp" id="DebtAcctWithdrawPbsSvtp" longname="负债账户支取"/>
    <method method="doProcess" id="doProcess" longname="记账处理" desc="执行核心记账逻辑"/>
    <method method="firstPostAcctProcess" id="firstPostAcctProcess" longname="第一次记账后处理" desc="第一次记账后处理"/>
</flow>
```

---

## 快速参考

### XML 格式清单

- [ ] 所有属性在一行内
- [ ] 标签之间无空行
- [ ] flowtran 子标签缩进 4 个空格
- [ ] interface 子标签缩进 8 个空格
- [ ] input/output/property 子标签缩进 12 个空格
- [ ] fields 内 field 缩进 16 个空格
- [ ] 使用空格不是 Tab
- [ ] 同层级标签对齐
- [ ] property 中复合引用 field：无 array，无 ref；普通字段：有 array，有 ref

### 创建命令模板

```
帮我新建 {交易码} {交易名称} 的联机交易

输入:
{字段} {中文名} {必输/非必输}

输出:
{字段} {中文名}

属性接口：
[{引用复合对象中文名}]  {多值}  {必输}
{普通字段中文名}

流程编排：
服务：{服务中文名}
服务：{服务中文名}   描述：{描述}
方法：{英文方法名} {方法中文名}
方法：{英文方法名} {方法中文名}   描述：{方法描述}
方法：{方法中文名}
```
