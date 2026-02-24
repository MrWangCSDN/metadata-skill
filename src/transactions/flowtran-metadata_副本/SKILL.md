---
name: flowtran-metadata
description: 处理基于 XML 的 flowtran 联机交易元数据模型的创建和修改。支持根据交易ID(T+C/D/G/Y格式)、输入输出字段自动生成完整的 .flowtrans.xml 文件,包括数组字段处理(fields标签)、dict-mcp-server 服务集成进行字段元数据查询、自动包路径生成和模块路径定位。使用场景:创建新 flowtran 交易、修改现有交易、处理数组字段、子目录管理。触发关键词:新建/创建/修改+flowtran/联机交易、TC/TD/TG/TY 开头的交易码、.flowtrans.xml 文件。
---

# Flowtran 联机交易元数据模型开发

本技能用于处理基于 XML 格式的 flowtran 联机交易元数据模型开发,支持创建和修改功能。

## 核心工作流

### 模式 1: 创建新 Flowtran 交易

**识别关键词**: "新建"/"创建" + "flowtran"/"联机交易" + 交易码

**用户输入示例**:
```
帮我新建 TY291 收费明细文件批量查询 的联机交易

输入:
cst     国家    非必输
xb      性别    必输

输出:
cst     国家    
xb      性别
```

**处理步骤**:

1. **验证交易码**: 检查格式 T+C/D/G/Y+数字 (详见 [references/transaction-id-rules.md](references/transaction-id-rules.md))
2. **确定目标路径**: 根据交易码确定模块和目录 (详见 [references/package-module-mapping.md](references/package-module-mapping.md))
3. **检查文件存在性**: 在 trans 目录下查找 .flowtrans.xml 文件,存在则修改,不存在则创建
4. **处理子目录**: 检查自然语言中是否指定子目录
5. **调用 MCP 查询字段**: 使用 dict-mcp-server 的 getDictDefByLongNameList 方法批量查询
6. **处理未贯标字段**: 收集返回值为 null 的字段并提示用户
7. **生成 XML**: 使用标准模板生成完整 flowtran XML (属性单行,标签间无空行)
8. **保存文件**: 保存到 `{模块名}-pbf/src/main/resources/trans/{交易码}.flowtrans.xml`

### 模式 2: 修改现有 Flowtran 交易

**识别关键词**: "修改" + 交易码

**处理步骤**:

1. **定位文件**: 在 trans 目录下查找现有 .flowtrans.xml 文件
2. **读取原文件**: 保留 flowtran/description/interface 标签的所有属性
3. **调用 MCP**: 使用 getDictDefByLongNameList 查询新增字段的元数据
4. **覆盖 input/output**: 仅更新 interface 中的 input 和 output 标签内容
5. **保存文件**: 保持其他标签和属性不变

## 交易码规则

**格式**: T + (C/D/G/Y) + 4位数字

| 前缀 | 完整格式 | 编码范围 | 领域 | 示例 |
|------|---------|---------|------|------|
| TC | TC021-TC999 | C021-C999 | 存款领域 | TC021, TC100 |
| TD | TD001-TD499 | D001-D499 | 贷款领域 | TD001, TD250 |
| TG | TG001-TG499 | G001-G499 | 结算领域 | TG100, TG350 |
| TY | TY001-TY999 | Y001-Y999 | 平台公共领域 | TY001, TY291 |

**重要**: 
- 交易码全局唯一
- 文件名为 `{交易码}.flowtrans.xml`
- 注意扩展名是 .flowtrans.xml 不是 .flowtran.xml

详细规则见 [references/transaction-id-rules.md](references/transaction-id-rules.md)

## 包路径和模块映射

根据交易码前缀自动确定:

| 前缀 | 包路径 | 模块名 | 文件路径 |
|------|--------|--------|---------|
| TC | com.spdb.ccbs.dept.pbf.trans | dept-pbf | dept-pbf/src/main/resources/trans |
| TD | com.spdb.ccbs.loan.pbf.trans | loan-pbf | loan-pbf/src/main/resources/trans |
| TG | com.spdb.ccbs.sett.pbf.trans | sett-pbf | sett-pbf/src/main/resources/trans |
| TY | com.spdb.ccbs.comm.pbf.trans | comm-pbf | comm-pbf/src/main/resources/trans |

**子目录处理**: 如果用户指定子目录(如"在 chrg 子目录下"),包路径和文件路径都要追加子目录。

详见 [references/package-module-mapping.md](references/package-module-mapping.md)

## MCP 服务集成

**MCP 服务名**: `dict-mcp-server`
**调用方法**: `getDictDefByLongNameList`

**调用时机**: 创建或修改时,批量查询所有字段的元数据

**输入参数**: 字段中文名称集合 (字符串数组)
```javascript
["国家", "性别", "客户ID", "查询日期"]
```

**返回结果**: Map<中文名称, 字段定义对象>
```javascript
{
  "国家": {
    "id": "cst",
    "type": "MBaseType.U_GUO_JIA",
    "longname": "国家",
    "ref": "MDict.C.cst"
  },
  "性别": {
    "id": "xb",
    "type": "MBaseType.U_XING_BIE",
    "longname": "性别",
    "ref": "MDict.X.xb"
  },
  "未知字段": null  // null 表示未贯标
}
```

**未贯标处理**: 
- 如果返回值为 null,收集该字段
- 继续处理其他字段
- 最后统一提示用户哪些字段未贯标

详见 [references/mcp-integration.md](references/mcp-integration.md)

## 标准 XML 模板

### 基本结构 (注意:属性单行,标签间无空行,层级缩进)

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

**关键格式要求**:
- ✅ 所有标签的属性必须在一行内
- ✅ 标签之间不要有空行
- ✅ 同层级标签缩进相同
- ✅ 子层级基于父标签缩进 + 4个空格
- ✅ kind 固定为 "auto"
- ✅ txnMode 默认 A,只读查询用 R
- ✅ interface package = flowtran package + ".intf"
- ✅ input packMode 默认 true
- ✅ output asParm 和 packMode 都默认 true

完整模板说明见 [references/xml-template.md](references/xml-template.md)

## 数组字段处理

使用 `<fields>` 标签处理数组/列表类型。

**自然语言识别**:
```
chargCdArray 收费代码数组 start
    包含 fPrjCd   收费项目编码  非必输
    包含 chrgAmt  收费金额     必输
chargCdArray 收费代码数组 end
```

**生成 XML** (属性单行,层级缩进):
```xml
<fields id="chargCdArray" scope="" required="false" multi="true" array="false" longname="收费代码数组">
    <field id="fPrjCd" type="MBaseType.U_SHOU_FEI_XIANG_MU_BIAN_MA" required="false" multi="false" array="false" longname="收费项目编码" ref="MDict.F.fPrjCd"/>
    <field id="chrgAmt" type="MBaseType.U_JIN_E" required="true" multi="false" array="false" longname="收费金额" ref="MDict.C.chrgAmt"/>
</fields>
```

**规则**:
- `id` 必须以 "Array" 结尾
- `scope=""` 固定
- `multi="true"` 固定
- `array="false"` 固定
- `longname` 以"数组"结尾
- 使用 start/end 标记数组范围
- 属性全部在一行内

详见 [references/array-fields.md](references/array-fields.md)

## 字段属性规则

### field 标签

| 属性 | 说明 | 来源 | 固定值 |
|-----|------|------|--------|
| id | 字段英文名 | MCP 返回 | - |
| type | 字段类型 | MCP 返回 | - |
| required | 是否必输 | 用户输入 | true/false |
| multi | 是否多值 | - | false |
| array | 是否数组 | - | false |
| longname | 字段中文名 | MCP 返回 | - |
| ref | 字典引用 | MCP 返回(可选) | - |

**required 默认值**: 如果用户未指定,默认为 false (非必输)

### fields 标签(数组)

| 属性 | 值 | 说明 |
|-----|---|------|
| id | {名称}Array | 必须以 Array 结尾 |
| scope | "" | 固定为空字符串 |
| required | false | 固定为 false |
| multi | true | 固定为 true |
| array | false | 固定为 false |
| longname | {中文名}数组 | 必须以"数组"结尾 |

## 完整示例

### 示例 1: 基本交易创建

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

**生成的完整 XML** (属性单行,标签间无空行):
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

**文件路径**: `comm-pbf/src/main/resources/trans/TY291.flowtrans.xml`

**AI 反馈**:
```
✅ 成功创建 flowtran 交易

📁 文件位置: comm-pbf/src/main/resources/trans/TY291.flowtrans.xml
📋 交易编码: TY291
📝 交易名称: 收费明细文件批量查询
🏢 所属领域: 平台公共领域
📦 包路径: com.spdb.ccbs.comm.pbf.trans

📥 输入字段(2个):
  ✅ cst (国家) - 非必输
  ✅ xb (性别) - 必输

📤 输出字段(2个):
  ✅ cst (国家)
  ✅ xb (性别)
```

### 示例 2: 带数组字段的交易

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

**生成的 XML** (属性单行,标签间无空行):
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

更多示例见 [references/examples.md](references/examples.md)

## 错误处理

### 交易码格式错误

```
❌ 交易码验证失败: 交易码必须以 T+C/D/G/Y 开头

当前: Y291
正确: TY291

💡 正确格式:
   - TC021-TC999: 存款领域
   - TD001-TD499: 贷款领域
   - TG001-TG499: 结算领域
   - TY001-TY999: 平台公共领域
```

### 字段未贯标

```
❌ 以下字段未贯标,需要在 MCP 系统中完成贯标处理:
  1. 未知字段 (unknownField) - MCP 返回 null
  2. 测试字段 (testField) - MCP 返回 null

✅ 已成功处理的字段: 3个
❌ 需要贯标的字段: 2个

💡 请在 dict-mcp-server 系统中完成字段贯标后重试
```

### 数组格式错误

```
❌ 数组字段格式错误

字段: chargCd (收费代码)
问题: 数组字段 id 必须以 "Array" 结尾

正确示例:
chargCdArray 收费代码数组 start
    包含 fPrjCd  收费项目编码
chargCdArray 收费代码数组 end
```

更多错误场景见 [references/error-handling.md](references/error-handling.md)

## 快速参考

### 创建流程清单

- [ ] 验证交易码格式 (T+C/D/G/Y+4位数字)
- [ ] 确定模块和包路径 (根据前缀)
- [ ] 检查 .flowtrans.xml 文件是否存在
- [ ] 处理子目录(如有)
- [ ] 调用 dict-mcp-server.getDictDefByLongNameList 查询
- [ ] 处理返回值为 null 的未贯标字段
- [ ] 处理数组字段 (start/end 标记)
- [ ] 生成 XML (属性单行,标签间无空行)
- [ ] 保存到 {模块}-pbf/src/main/resources/trans/
- [ ] 验证并反馈结果

### 修改流程清单

- [ ] 定位现有 .flowtrans.xml 文件
- [ ] 读取原文件完整内容
- [ ] 保留 flowtran/description/interface 标签属性
- [ ] 调用 MCP 查询新字段
- [ ] 仅覆盖 input 和 output 标签内容
- [ ] 保持 XML 格式一致 (属性单行,标签间无空行)
- [ ] 保存修改后的文件

### XML 格式重要提醒

1. **文件扩展名**: `.flowtrans.xml` (不是 .flowtran.xml)
2. **属性格式**: 所有属性必须在一行内,不能换行
3. **标签间距**: 不同标签之间不要有空行
4. **缩进规则**: 同层级标签缩进相同,子层级基于父标签 +4 个空格
5. **kind 属性**: 固定为 "auto"
6. **交易码格式**: T+C/D/G/Y+4位数字
7. **包路径**: 根据交易码前缀自动确定
8. **interface 包**: flowtran package + ".intf"
9. **数组字段**: id 以 Array 结尾,multi="true"
10. **MCP 服务**: dict-mcp-server.getDictDefByLongNameList
11. **修改保留**: 修改时只更新 input/output,保留其他内容

## 参考资源

- **交易码规则**: [references/transaction-id-rules.md](references/transaction-id-rules.md)
- **包路径和模块映射**: [references/package-module-mapping.md](references/package-module-mapping.md)
- **XML 模板详解**: [references/xml-template.md](references/xml-template.md)
- **数组字段处理**: [references/array-fields.md](references/array-fields.md)
- **MCP 服务集成**: [references/mcp-integration.md](references/mcp-integration.md)
- **错误处理指南**: [references/error-handling.md](references/error-handling.md)
- **完整示例集**: [references/examples.md](references/examples.md)
