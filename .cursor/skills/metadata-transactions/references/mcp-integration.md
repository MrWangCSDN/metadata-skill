# MCP 服务集成详细说明

本文档详细说明如何使用 `dict-mcp-server` 进行字段元数据查询。

## MCP 服务概述

**MCP 服务名称**: `dict-mcp-server`
**方法名**: `getDictDefByLongNameList`
**用途**: 批量查询字段的元数据信息

## 接口规范

### 方法签名

```typescript
getDictDefByLongNameList(longNameList: string[]): Map<string, FieldDefinition | null>
```

### 输入参数

**参数名**: `longNameList`
**类型**: `string[]` (字符串数组)
**说明**: 字段的中文名称集合

**示例**:
```javascript
["客户ID", "查询日期", "收费项目编码", "收费金额", "结果列表"]
```

### 返回结果

**类型**: `Map<string, FieldDefinition | null>`
**说明**: Map 对象,key 为中文名称,value 为字段定义对象或 null

**字段定义对象 (FieldDefinition)**:
```typescript
interface FieldDefinition {
    id: string;          // 字段英文名
    type: string;        // 字段类型 (如 MBaseType.U_KE_HU_BIAN_HAO)
    longname: string;    // 字段中文名
    ref?: string;        // 字典引用 (可选,如 MDict.C.custId)
}
```

**返回示例**:
```javascript
{
  "客户ID": {
    "id": "custId",
    "type": "MBaseType.U_KE_HU_BIAN_HAO",
    "longname": "客户ID",
    "ref": "MDict.C.custId"
  },
  "查询日期": {
    "id": "queryDate",
    "type": "MBaseType.U_RI_QI",
    "longname": "查询日期",
    "ref": "MDict.Q.queryDate"
  },
  "收费项目编码": {
    "id": "fPrjCd",
    "type": "MBaseType.U_SHOU_FEI_XIANG_MU_BIAN_MA",
    "longname": "收费项目编码",
    "ref": "MDict.F.fPrjCd"
  },
  "未贯标字段": null  // null 表示该字段未贯标
}
```

## 调用流程

### 完整调用流程

```javascript
// 1. 收集所有字段的中文名称
const longNameList = [];
for (const field of inputFields) {
    longNameList.push(field.longname);
}
for (const field of outputFields) {
    longNameList.push(field.longname);
}

// 2. 调用 MCP 服务
const mcpResult = await mcpServer.call('dict-mcp-server', 'getDictDefByLongNameList', {
    longNameList: longNameList
});

// 3. 处理返回结果
const processedFields = [];
const unstandardizedFields = [];

for (const [longname, fieldDef] of Object.entries(mcpResult)) {
    if (fieldDef === null) {
        // 字段未贯标
        unstandardizedFields.push(longname);
    } else {
        // 字段已贯标
        processedFields.push(fieldDef);
    }
}

// 4. 检查未贯标字段
if (unstandardizedFields.length > 0) {
    console.error(`以下字段未贯标,请先完成贯标:\n${unstandardizedFields.join(', ')}`);
}
```

### Python 实现示例

```python
def query_fields_from_mcp(longname_list: list[str]) -> dict:
    """
    调用 MCP 服务查询字段元数据
    
    Args:
        longname_list: 字段中文名称列表
        
    Returns:
        {
            'processed': 已贯标的字段列表,
            'unstandardized': 未贯标的字段名列表
        }
    """
    # 调用 MCP 服务
    mcp_result = mcp_client.call(
        server='dict-mcp-server',
        method='getDictDefByLongNameList',
        params={'longNameList': longname_list}
    )
    
    processed_fields = []
    unstandardized_fields = []
    
    # 处理返回结果
    for longname in longname_list:
        field_def = mcp_result.get(longname)
        
        if field_def is None:
            # 未贯标
            unstandardized_fields.append(longname)
        else:
            # 已贯标
            processed_fields.append({
                'id': field_def['id'],
                'type': field_def['type'],
                'longname': field_def['longname'],
                'ref': field_def.get('ref', '')
            })
    
    return {
        'processed': processed_fields,
        'unstandardized': unstandardized_fields
    }


# 使用示例
longnames = ["客户ID", "查询日期", "未贯标字段"]
result = query_fields_from_mcp(longnames)

print(f"已处理字段: {len(result['processed'])} 个")
print(f"未贯标字段: {len(result['unstandardized'])} 个")

if result['unstandardized']:
    print(f"\n❌ 以下字段需要贯标处理:")
    for field in result['unstandardized']:
        print(f"  - {field}")
```

### TypeScript 实现示例

```typescript
interface FieldDefinition {
    id: string;
    type: string;
    longname: string;
    ref?: string;
}

interface QueryResult {
    processed: FieldDefinition[];
    unstandardized: string[];
}

async function queryFieldsFromMCP(longnameList: string[]): Promise<QueryResult> {
    // 调用 MCP 服务
    const mcpResult: Map<string, FieldDefinition | null> = await mcpClient.call(
        'dict-mcp-server',
        'getDictDefByLongNameList',
        { longNameList: longnameList }
    );
    
    const processedFields: FieldDefinition[] = [];
    const unstandardizedFields: string[] = [];
    
    // 处理返回结果
    for (const longname of longnameList) {
        const fieldDef = mcpResult[longname];
        
        if (fieldDef === null || fieldDef === undefined) {
            // 未贯标
            unstandardizedFields.push(longname);
        } else {
            // 已贯标
            processedFields.push({
                id: fieldDef.id,
                type: fieldDef.type,
                longname: fieldDef.longname,
                ref: fieldDef.ref
            });
        }
    }
    
    return {
        processed: processedFields,
        unstandardized: unstandardizedFields
    };
}

// 使用示例
const longnames = ["客户ID", "查询日期", "未贯标字段"];
const result = await queryFieldsFromMCP(longnames);

console.log(`已处理字段: ${result.processed.length} 个`);
console.log(`未贯标字段: ${result.unstandardized.length} 个`);

if (result.unstandardized.length > 0) {
    console.error('\n❌ 以下字段需要贯标处理:');
    result.unstandardized.forEach(field => {
        console.error(`  - ${field}`);
    });
}
```

## 调用示例详解

### 示例 1: 所有字段都已贯标

**输入**:
```javascript
const longnames = ["客户ID", "查询日期", "收费项目编码"];
```

**MCP 返回**:
```javascript
{
  "客户ID": {
    "id": "custId",
    "type": "MBaseType.U_KE_HU_BIAN_HAO",
    "longname": "客户ID",
    "ref": "MDict.C.custId"
  },
  "查询日期": {
    "id": "queryDate",
    "type": "MBaseType.U_RI_QI",
    "longname": "查询日期",
    "ref": "MDict.Q.queryDate"
  },
  "收费项目编码": {
    "id": "fPrjCd",
    "type": "MBaseType.U_SHOU_FEI_XIANG_MU_BIAN_MA",
    "longname": "收费项目编码",
    "ref": "MDict.F.fPrjCd"
  }
}
```

**处理结果**:
```
✅ 所有字段都已贯标 (3/3)

📥 字段信息:
  1. custId (客户ID) - MBaseType.U_KE_HU_BIAN_HAO
  2. queryDate (查询日期) - MBaseType.U_RI_QI
  3. fPrjCd (收费项目编码) - MBaseType.U_SHOU_FEI_XIANG_MU_BIAN_MA

✅ 可以继续生成 XML 文件
```

### 示例 2: 部分字段未贯标

**输入**:
```javascript
const longnames = ["客户ID", "未知字段", "测试字段", "查询日期"];
```

**MCP 返回**:
```javascript
{
  "客户ID": {
    "id": "custId",
    "type": "MBaseType.U_KE_HU_BIAN_HAO",
    "longname": "客户ID",
    "ref": "MDict.C.custId"
  },
  "未知字段": null,  // 未贯标
  "测试字段": null,  // 未贯标
  "查询日期": {
    "id": "queryDate",
    "type": "MBaseType.U_RI_QI",
    "longname": "查询日期",
    "ref": "MDict.Q.queryDate"
  }
}
```

**处理结果**:
```
⚠️  部分字段未贯标

❌ 以下字段需要贯标处理:
  1. 未知字段
  2. 测试字段

✅ 已贯标字段 (2/4):
  - 客户ID
  - 查询日期

💡 请先在 MCP 系统中完成字段贯标,然后重新创建交易
```

### 示例 3: 完整工作流

**自然语言输入**:
```
帮我新建 TY292 客户查询 的联机交易

输入:
客户ID      必输
查询日期     非必输
未知字段     必输

输出:
客户名称
结果列表
```

**处理步骤**:

```javascript
// 1. 收集字段中文名
const inputLongnames = ["客户ID", "查询日期", "未知字段"];
const outputLongnames = ["客户名称", "结果列表"];
const allLongnames = [...inputLongnames, ...outputLongnames];

// 2. 批量调用 MCP
const mcpResult = await mcpServer.call('dict-mcp-server', 'getDictDefByLongNameList', {
    longNameList: allLongnames
});

// 3. 处理返回结果
const processed = [];
const unstandardized = [];

for (const longname of allLongnames) {
    const fieldDef = mcpResult[longname];
    if (fieldDef === null) {
        unstandardized.push(longname);
    } else {
        processed.push(fieldDef);
    }
}

// 4. 判断是否可以继续
if (unstandardized.length > 0) {
    console.error(`❌ 以下字段未贯标:`);
    unstandardized.forEach(field => console.error(`  - ${field}`));
    console.error(`\n💡 请先完成字段贯标,然后重新创建交易`);
    return;  // 终止创建流程
}

// 5. 继续生成 XML
const xml = generateFlowtranXML({
    transId: 'TY292',
    transName: '客户查询',
    inputFields: processed.filter(f => inputLongnames.includes(f.longname)),
    outputFields: processed.filter(f => outputLongnames.includes(f.longname))
});
```

## 字段映射逻辑

### 从 MCP 结果到 XML 字段

**MCP 返回**:
```javascript
{
    "id": "custId",
    "type": "MBaseType.U_KE_HU_BIAN_HAO",
    "longname": "客户ID",
    "ref": "MDict.C.custId"
}
```

**生成的 XML** (input 字段):
```xml
<field id="custId" 
       type="MBaseType.U_KE_HU_BIAN_HAO" 
       required="true" 
       multi="false" 
       array="false" 
       longname="客户ID" 
       ref="MDict.C.custId"/>
```

**映射规则**:
1. `id` → XML field 的 id 属性 (来自 MCP)
2. `type` → XML field 的 type 属性 (来自 MCP)
3. `longname` → XML field 的 longname 属性 (来自 MCP)
4. `ref` → XML field 的 ref 属性 (来自 MCP,可选)
5. `required` → 根据用户输入 (必输/非必输)
6. `multi` → 固定为 "false"
7. `array` → 固定为 "false"

### 处理 ref 属性

**规则**: 
- 如果 MCP 返回的 ref 字段存在且非空,添加到 XML
- 如果 ref 为空或不存在,XML 中省略 ref 属性

```python
def build_field_xml(field_def, required):
    """构建字段 XML"""
    xml = f'<field id="{field_def["id"]}" '
    xml += f'type="{field_def["type"]}" '
    xml += f'required="{str(required).lower()}" '
    xml += 'multi="false" '
    xml += 'array="false" '
    xml += f'longname="{field_def["longname"]}"'
    
    # 只有当 ref 存在且非空时才添加
    if field_def.get("ref"):
        xml += f' ref="{field_def["ref"]}"'
    
    xml += '/>'
    return xml
```

## 未贯标字段处理

### 判断逻辑

**未贯标判断**: `mcpResult[longname] === null` 或 key 不存在

### ⛔ 强制规则：null 字段禁止写入 XML

> **MCP 返回 null 的字段，必须从生成列表中移除，不得生成任何 `<field>` 或 `<fields>` 标签。**
> 这是不可绕过的强制规则，无论用户是否明确要求，均须执行。

### 处理策略

1. **强制过滤**: MCP 返回 null 的字段**立即从字段列表中删除**，不写入 XML
2. **数组子字段处理**:
   - 若数组（fields）内**部分子字段**为 null → 仅写入已贯标的子字段，null 子字段跳过
   - 若数组内**全部子字段**均为 null → 整个 `<fields>` 标签也不写入
3. **不中断流程**: 过滤后继续用剩余已贯标字段生成 XML
4. **统一反馈**: 生成完成后，明确列出所有被排除的字段名

### 反馈提示格式

```
⚠️  以下字段未贯标，已从 XML 中排除（共 N 个）:
  1. 未知字段  ← MCP 返回 null，未写入 XML
  2. 测试字段  ← MCP 返回 null，未写入 XML

✅ 已成功写入字段（共 M 个）:
  - cst (国家)
  - xb  (性别)

📊 统计:
   - 用户输入字段总数: 5
   - 已贯标并写入 XML: 3
   - 未贯标已排除:     2

💡 如需完整交易，请在 dict-mcp-server 系统中完成上述字段的贯标后重新执行指令
```

## 批量查询优化

### 一次性批量查询

**优势**:
- 减少网络往返次数
- 提高查询效率
- 简化错误处理

**实现**:
```javascript
// ✅ 推荐: 批量查询
const allLongnames = [...inputLongnames, ...outputLongnames];
const mcpResult = await getDictDefByLongNameList(allLongnames);

// ❌ 不推荐: 逐个查询
for (const longname of allLongnames) {
    const result = await getDictDef(longname);  // 多次网络调用
}
```

### 去重处理

在调用 MCP 前,对字段中文名去重:

```javascript
function deduplicateLongnames(longnames) {
    return [...new Set(longnames)];
}

const allLongnames = [
    ...inputLongnames,
    ...outputLongnames
];

// 去重
const uniqueLongnames = deduplicateLongnames(allLongnames);

// 调用 MCP
const mcpResult = await getDictDefByLongNameList(uniqueLongnames);
```

## 错误处理

### MCP 服务不可用

```javascript
try {
    const mcpResult = await mcpServer.call('dict-mcp-server', 'getDictDefByLongNameList', {
        longNameList: longnames
    });
} catch (error) {
    console.error('❌ MCP 服务调用失败');
    console.error(`错误信息: ${error.message}`);
    console.error('\n💡 建议:');
    console.error('1. 检查 MCP 服务是否正常运行');
    console.error('2. 确认网络连接正常');
    console.error('3. 稍后重试或联系系统管理员');
    throw error;
}
```

### MCP 返回格式错误

```javascript
// 验证返回结果格式
if (!mcpResult || typeof mcpResult !== 'object') {
    throw new Error('MCP 返回数据格式异常');
}

// 验证每个字段定义
for (const [longname, fieldDef] of Object.entries(mcpResult)) {
    if (fieldDef !== null) {
        if (!fieldDef.id || !fieldDef.type || !fieldDef.longname) {
            console.warn(`⚠️  字段 "${longname}" 的元数据不完整`);
        }
    }
}
```

### 超时处理

```javascript
async function queryWithTimeout(longnames, timeout = 5000) {
    const timeoutPromise = new Promise((_, reject) => {
        setTimeout(() => reject(new Error('MCP 查询超时')), timeout);
    });
    
    const queryPromise = mcpServer.call('dict-mcp-server', 'getDictDefByLongNameList', {
        longNameList: longnames
    });
    
    try {
        return await Promise.race([queryPromise, timeoutPromise]);
    } catch (error) {
        console.error('❌ MCP 服务响应超时');
        console.error('💡 建议: 稍后重试或检查网络连接');
        throw error;
    }
}
```

## 完整工作流示例

```javascript
async function createFlowtranTransaction(transData) {
    // 1. 收集所有字段的中文名称
    const inputLongnames = transData.inputFields.map(f => f.longname);
    const outputLongnames = transData.outputFields.map(f => f.longname);
    const allLongnames = [...inputLongnames, ...outputLongnames];
    
    // 去重
    const uniqueLongnames = [...new Set(allLongnames)];
    
    console.log(`📋 准备查询 ${uniqueLongnames.length} 个字段的元数据...`);
    
    // 2. 批量调用 MCP
    let mcpResult;
    try {
        mcpResult = await mcpServer.call('dict-mcp-server', 'getDictDefByLongNameList', {
            longNameList: uniqueLongnames
        });
    } catch (error) {
        console.error('❌ MCP 服务调用失败:', error.message);
        return { success: false, error: 'MCP_SERVICE_ERROR' };
    }
    
    // 3. 处理返回结果
    const fieldMap = new Map();
    const unstandardized = [];
    
    for (const longname of uniqueLongnames) {
        const fieldDef = mcpResult[longname];
        
        if (fieldDef === null || fieldDef === undefined) {
            unstandardized.push(longname);
        } else {
            fieldMap.set(longname, fieldDef);
        }
    }
    
    // 4. 检查未贯标字段
    if (unstandardized.length > 0) {
        console.error(`\n❌ 以下字段需要贯标处理:`);
        unstandardized.forEach((field, index) => {
            console.error(`  ${index + 1}. ${field}`);
        });
        
        console.error(`\n📊 统计:`);
        console.error(`   - 总字段数: ${uniqueLongnames.length}`);
        console.error(`   - 已贯标: ${fieldMap.size}`);
        console.error(`   - 未贯标: ${unstandardized.length}`);
        
        return { 
            success: false, 
            error: 'UNSTANDARDIZED_FIELDS',
            unstandardizedFields: unstandardized 
        };
    }
    
    // 5. 组装字段数据
    const inputFields = transData.inputFields.map(f => ({
        ...fieldMap.get(f.longname),
        required: f.required
    }));
    
    const outputFields = transData.outputFields.map(f => ({
        ...fieldMap.get(f.longname),
        required: false  // output 字段固定为 false
    }));
    
    // 6. 生成 XML
    const xml = generateFlowtranXML({
        transId: transData.transId,
        transName: transData.transName,
        inputFields: inputFields,
        outputFields: outputFields
    });
    
    // 7. 保存文件
    const filePath = getFilePath(transData.transId, transData.subdirectory);
    saveFile(filePath, xml);
    
    console.log(`\n✅ 成功创建 flowtran 交易`);
    console.log(`📁 文件位置: ${filePath}`);
    
    return { 
        success: true, 
        filePath: filePath,
        processedFields: fieldMap.size 
    };
}
```

## 调试技巧

### 启用详细日志

```javascript
const DEBUG = true;

async function queryFieldsDebug(longnames) {
    if (DEBUG) {
        console.log('[MCP] 查询字段:', longnames);
    }
    
    const result = await getDictDefByLongNameList(longnames);
    
    if (DEBUG) {
        console.log('[MCP] 返回结果:');
        for (const [longname, fieldDef] of Object.entries(result)) {
            if (fieldDef === null) {
                console.log(`  - ${longname}: ❌ 未贯标`);
            } else {
                console.log(`  - ${longname}: ✅ ${fieldDef.id} (${fieldDef.type})`);
            }
        }
    }
    
    return result;
}
```

### Mock MCP 服务(测试用)

```javascript
class MockMCPService {
    constructor() {
        this.mockData = {
            "客户ID": {
                "id": "custId",
                "type": "MBaseType.U_KE_HU_BIAN_HAO",
                "longname": "客户ID",
                "ref": "MDict.C.custId"
            },
            "查询日期": {
                "id": "queryDate",
                "type": "MBaseType.U_RI_QI",
                "longname": "查询日期",
                "ref": "MDict.Q.queryDate"
            }
        };
    }
    
    async getDictDefByLongNameList(longNameList) {
        const result = {};
        
        for (const longname of longNameList) {
            result[longname] = this.mockData[longname] || null;
        }
        
        return result;
    }
}
```

## 最佳实践

1. **批量查询**: 一次性查询所有字段,避免多次调用
2. **去重处理**: 查询前对字段名去重,提高效率
3. **⛔ 强制过滤**: MCP 返回 null 的字段**必须从 XML 中排除**，不得写入任何标签
4. **验证结果**: 检查 MCP 返回的数据格式和完整性
5. **友好提示**: 生成后明确告知哪些字段被排除、哪些字段已写入
6. **继续生成**: 过滤 null 字段后，用剩余已贯标字段继续生成 XML，不中断整体流程

## 常见问题

### Q: MCP 返回 null 和不返回该 key 有区别吗?
**A**: 都表示未贯标，按相同方式处理——强制不写入 XML。

### Q: 如果所有字段都未贯标怎么办?
**A**: 所有字段均被过滤，生成空的 input/output 标签（不含任何 field），并提示用户完成贯标后重新执行。

### Q: MCP 查询失败如何处理?
**A**: 捕获异常,提示用户检查 MCP 服务状态,不继续创建。

### Q: 部分字段未贯标时，已贯标字段还会写入 XML 吗?
**A**: 会。已贯标字段正常写入 XML，null 字段被强制排除，并在反馈中明确列出。

### Q: 数组（fields）里有部分子字段未贯标怎么办?
**A**: 已贯标的子字段正常写入 `<fields>` 标签内；未贯标的子字段跳过。若所有子字段均未贯标，则整个 `<fields>` 标签不写入。

### Q: 如何知道字段的 type 格式?
**A**: type 由 MCP 返回,格式通常是 `MBaseType.U_XXX`,直接使用即可。
