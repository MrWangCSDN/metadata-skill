# 包路径和模块映射规则

本文档详细说明根据交易码前缀自动确定包路径、工程、模块和文件路径的规则。

> ⛔ **强制规则**：创建 XML 文件时，必须使用当前工作空间的绝对路径。创建前必须先获取并展示工作空间路径。

## 路径构成顺序

创建文件的完整绝对路径按以下顺序拼接：

```
{工作空间绝对路径}/{工程}/{模块}/src/main/resources/trans/{子目录}/{交易码}.flowtrans.xml
```

| 顺序 | 层级 | 说明 |
|------|------|------|
| 1 | 工作空间 | 当前打开项目的根目录绝对路径（如 `/Users/xxx/Desktop/myproject`） |
| 2 | 工程 | 按领域映射（如 `ccbs-comm-impl`） |
| 3 | 模块 | 按领域映射（如 `comm-pbf`） |
| 4 | 资源路径 | 固定 `src/main/resources/trans` |
| 5 | 子目录 | 用户指定时追加，未指定则无 |
| 6 | 文件名 | `{交易码}.flowtrans.xml` |

## 基本映射规则

### 核心映射表

| 交易码前缀 | 领域 | 工程 | 模块 | 包路径 |
|----------|------|------|------|--------|
| **TC** | 存款 | ccbs-dept-impl | dept-pbf | com.spdb.ccbs.dept.pbf.trans |
| **TD** | 贷款 | ccbs-loan-impl | loan-pbf | com.spdb.ccbs.loan.pbf.trans |
| **TG** | 结算 | ccbs-sett-impl | sett-pbf | com.spdb.ccbs.sett.pbf.trans |
| **TY** | 平台公共 | ccbs-comm-impl | comm-pbf | com.spdb.ccbs.comm.pbf.trans |

### 映射规则说明

**工程规则**:
- TC → `ccbs-dept-impl` (存款)
- TD → `ccbs-loan-impl` (贷款)
- TG → `ccbs-sett-impl` (结算)
- TY → `ccbs-comm-impl` (平台公共)

**模块名规则**:
- TC → `dept-pbf` (存款)
- TD → `loan-pbf` (贷款)
- TG → `sett-pbf` (结算)
- TY → `comm-pbf` (平台公共)

**包路径规则**:
- TC → `com.spdb.ccbs.dept.pbf.trans`
- TD → `com.spdb.ccbs.loan.pbf.trans`
- TG → `com.spdb.ccbs.sett.pbf.trans`
- TY → `com.spdb.ccbs.comm.pbf.trans`

**文件路径规则**:
- 完整绝对路径: `{工作空间}/{工程}/{模块}/src/main/resources/trans`
- Maven 项目标准结构

## 详细示例

> 以下示例假设工作空间绝对路径为 `/Users/xxx/project`。

### TC 开头 - 存款领域

**交易码**: TC100

**生成信息**:
```yaml
交易码: TC100
领域: 对公分布式核心存款领域
工程: ccbs-dept-impl
模块名: dept-pbf
包路径: com.spdb.ccbs.dept.pbf.trans
interface包: com.spdb.ccbs.dept.pbf.trans.intf
文件绝对路径: /Users/xxx/project/ccbs-dept-impl/dept-pbf/src/main/resources/trans/TC100.flowtrans.xml
```

### TD 开头 - 贷款领域

**交易码**: TD250

**生成信息**:
```yaml
交易码: TD250
领域: 对公分布式核心贷款领域
工程: ccbs-loan-impl
模块名: loan-pbf
包路径: com.spdb.ccbs.loan.pbf.trans
interface包: com.spdb.ccbs.loan.pbf.trans.intf
文件绝对路径: /Users/xxx/project/ccbs-loan-impl/loan-pbf/src/main/resources/trans/TD250.flowtrans.xml
```

### TG 开头 - 结算领域

**交易码**: TG350

**生成信息**:
```yaml
交易码: TG350
领域: 对公分布式核心结算领域
工程: ccbs-sett-impl
模块名: sett-pbf
包路径: com.spdb.ccbs.sett.pbf.trans
interface包: com.spdb.ccbs.sett.pbf.trans.intf
文件绝对路径: /Users/xxx/project/ccbs-sett-impl/sett-pbf/src/main/resources/trans/TG350.flowtrans.xml
```

### TY 开头 - 平台公共领域

**交易码**: TY291

**生成信息**:
```yaml
交易码: TY291
领域: 对公分布式核心平台公共领域
工程: ccbs-comm-impl
模块名: comm-pbf
包路径: com.spdb.ccbs.comm.pbf.trans
interface包: com.spdb.ccbs.comm.pbf.trans.intf
文件绝对路径: /Users/xxx/project/ccbs-comm-impl/comm-pbf/src/main/resources/trans/TY291.flowtrans.xml
```

## 子目录处理

### 子目录识别

**关键词识别**: "在 {子目录名} 子目录下"

**示例**:
```
帮我在 chrg 子目录下新建 TY291 的联机交易
帮我在 sttt 子目录下新建 TC100 的联机交易
```

### 子目录路径调整

**基本规则**:
- 文件路径: 追加子目录
- 包路径: 追加子目录(用点分隔)
- interface 包: 在 flowtran 包路径基础上追加 .intf

**示例 1: TY291 在 chrg 子目录**（工作空间 = `/Users/xxx/project`）

```yaml
自然语言: 帮我在 chrg 子目录下新建 TY291 的联机交易

交易码: TY291
工程: ccbs-comm-impl
模块: comm-pbf
基础包路径: com.spdb.ccbs.comm.pbf.trans
子目录: chrg
实际包路径: com.spdb.ccbs.comm.pbf.trans.chrg
interface包: com.spdb.ccbs.comm.pbf.trans.chrg.intf

文件绝对路径: /Users/xxx/project/ccbs-comm-impl/comm-pbf/src/main/resources/trans/chrg/TY291.flowtrans.xml
```

**生成的 XML**:
```xml
<flowtran id="TY291" 
          package="com.spdb.ccbs.comm.pbf.trans.chrg"
          ...>
    <interface package="com.spdb.ccbs.comm.pbf.trans.chrg.intf">
```

**示例 2: TC100 在 sttt 子目录**（工作空间 = `/Users/xxx/project`）

```yaml
自然语言: 帮我在 sttt 子目录下新建 TC100 的联机交易

交易码: TC100
工程: ccbs-dept-impl
模块: dept-pbf
基础包路径: com.spdb.ccbs.dept.pbf.trans
子目录: sttt
实际包路径: com.spdb.ccbs.dept.pbf.trans.sttt
interface包: com.spdb.ccbs.dept.pbf.trans.sttt.intf

文件绝对路径: /Users/xxx/project/ccbs-dept-impl/dept-pbf/src/main/resources/trans/sttt/TC100.flowtrans.xml
```

**示例 3: 多级子目录**（工作空间 = `/Users/xxx/project`）

```yaml
自然语言: 帮我在 chrg/plszn 子目录下新建 TY291 的联机交易

交易码: TY291
工程: ccbs-comm-impl
模块: comm-pbf
子目录: chrg/plszn
实际包路径: com.spdb.ccbs.comm.pbf.trans.chrg.plszn
interface包: com.spdb.ccbs.comm.pbf.trans.chrg.plszn.intf

文件绝对路径: /Users/xxx/project/ccbs-comm-impl/comm-pbf/src/main/resources/trans/chrg/plszn/TY291.flowtrans.xml
```

### 子目录创建

**规则**: 如果子目录不存在,自动创建

```python
import os

def ensure_directory_exists(file_path: str):
    """确保目录存在,不存在则创建"""
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"✅ 创建子目录: {directory}")
```

## Interface 包路径规则

### 基本规则

**interface 包路径 = flowtran 包路径 + ".intf"**

**示例**:
- flowtran package: `com.spdb.ccbs.comm.pbf.trans`
- interface package: `com.spdb.ccbs.comm.pbf.trans.intf`

**带子目录示例**:
- flowtran package: `com.spdb.ccbs.comm.pbf.trans.chrg.plszn`
- interface package: `com.spdb.ccbs.comm.pbf.trans.chrg.plszn.intf`

### XML 表示

```xml
<flowtran id="TY291" 
          package="com.spdb.ccbs.comm.pbf.trans.chrg.plszn"
          ...>
    <interface package="com.spdb.ccbs.comm.pbf.trans.chrg.plszn.intf">
        <input>...</input>
        <output>...</output>
    </interface>
</flowtran>
```

## 实现示例

### Python 实现

```python
def get_package_info(workspace: str, trans_id: str, subdirectory: str = "") -> dict:
    """
    根据交易码获取包路径信息（基于工作空间绝对路径）
    
    Args:
        workspace: 工作空间绝对路径 (如 /Users/xxx/project)
        trans_id: 交易码 (如 TY291)
        subdirectory: 子目录 (可选,如 chrg 或 chrg/plszn)
        
    Returns:
        包含工程、模块、包路径、文件绝对路径等信息的字典
    """
    trans_id = trans_id.upper()
    prefix = trans_id[1]  # C/D/G/Y
    
    mapping = {
        'C': {
            'package': 'com.spdb.ccbs.dept.pbf.trans',
            'project': 'ccbs-dept-impl',
            'module': 'dept-pbf',
            'domain': '对公分布式核心存款领域'
        },
        'D': {
            'package': 'com.spdb.ccbs.loan.pbf.trans',
            'project': 'ccbs-loan-impl',
            'module': 'loan-pbf',
            'domain': '对公分布式核心贷款领域'
        },
        'G': {
            'package': 'com.spdb.ccbs.sett.pbf.trans',
            'project': 'ccbs-sett-impl',
            'module': 'sett-pbf',
            'domain': '对公分布式核心结算领域'
        },
        'Y': {
            'package': 'com.spdb.ccbs.comm.pbf.trans',
            'project': 'ccbs-comm-impl',
            'module': 'comm-pbf',
            'domain': '对公分布式核心平台公共领域'
        }
    }
    
    base_info = mapping.get(prefix)
    if not base_info:
        raise ValueError(f"无效的交易码前缀: {prefix}")
    
    package_path = base_info['package']
    resource_path = f"{base_info['project']}/{base_info['module']}/src/main/resources/trans"
    
    if subdirectory:
        sub_package = subdirectory.replace('/', '.')
        package_path = f"{package_path}.{sub_package}"
        resource_path = f"{resource_path}/{subdirectory}"
    
    abs_file_path = f"{workspace}/{resource_path}/{trans_id}.flowtrans.xml"
    abs_dir_path = f"{workspace}/{resource_path}"
    
    return {
        'trans_id': trans_id,
        'domain': base_info['domain'],
        'project': base_info['project'],
        'module': base_info['module'],
        'package': package_path,
        'interface_package': f"{package_path}.intf",
        'file_path': abs_file_path,
        'directory': abs_dir_path,
        'filename': f"{trans_id}.flowtrans.xml"
    }


# 使用示例
info = get_package_info('/Users/xxx/project', 'TY291', 'chrg/plszn')
print(info)
# {
#     'trans_id': 'TY291',
#     'domain': '对公分布式核心平台公共领域',
#     'project': 'ccbs-comm-impl',
#     'module': 'comm-pbf',
#     'package': 'com.spdb.ccbs.comm.pbf.trans.chrg.plszn',
#     'interface_package': 'com.spdb.ccbs.comm.pbf.trans.chrg.plszn.intf',
#     'file_path': '/Users/xxx/project/ccbs-comm-impl/comm-pbf/src/main/resources/trans/chrg/plszn/TY291.flowtrans.xml',
#     'directory': '/Users/xxx/project/ccbs-comm-impl/comm-pbf/src/main/resources/trans/chrg/plszn',
#     'filename': 'TY291.flowtrans.xml'
# }
```

### JavaScript/TypeScript 实现

```typescript
interface PackageInfo {
    transId: string;
    domain: string;
    project: string;
    module: string;
    package: string;
    interfacePackage: string;
    filePath: string;
    directory: string;
    filename: string;
}

function getPackageInfo(workspace: string, transId: string, subdirectory: string = ""): PackageInfo {
    transId = transId.toUpperCase();
    const prefix = transId[1];  // C/D/G/Y
    
    const mapping: {[key: string]: {package: string, project: string, module: string, domain: string}} = {
        'C': {
            package: 'com.spdb.ccbs.dept.pbf.trans',
            project: 'ccbs-dept-impl',
            module: 'dept-pbf',
            domain: '对公分布式核心存款领域'
        },
        'D': {
            package: 'com.spdb.ccbs.loan.pbf.trans',
            project: 'ccbs-loan-impl',
            module: 'loan-pbf',
            domain: '对公分布式核心贷款领域'
        },
        'G': {
            package: 'com.spdb.ccbs.sett.pbf.trans',
            project: 'ccbs-sett-impl',
            module: 'sett-pbf',
            domain: '对公分布式核心结算领域'
        },
        'Y': {
            package: 'com.spdb.ccbs.comm.pbf.trans',
            project: 'ccbs-comm-impl',
            module: 'comm-pbf',
            domain: '对公分布式核心平台公共领域'
        }
    };
    
    const baseInfo = mapping[prefix];
    if (!baseInfo) {
        throw new Error(`无效的交易码前缀: ${prefix}`);
    }
    
    let packagePath = baseInfo.package;
    let resourcePath = `${baseInfo.project}/${baseInfo.module}/src/main/resources/trans`;
    
    if (subdirectory) {
        const subPackage = subdirectory.replace(/\//g, '.');
        packagePath = `${packagePath}.${subPackage}`;
        resourcePath = `${resourcePath}/${subdirectory}`;
    }
    
    return {
        transId: transId,
        domain: baseInfo.domain,
        project: baseInfo.project,
        module: baseInfo.module,
        package: packagePath,
        interfacePackage: `${packagePath}.intf`,
        filePath: `${workspace}/${resourcePath}/${transId}.flowtrans.xml`,
        directory: `${workspace}/${resourcePath}`,
        filename: `${transId}.flowtrans.xml`
    };
}
```

## 完整路径示例

> 以下示例假设工作空间绝对路径为 `/Users/xxx/project`。

### 无子目录示例

| 交易码 | 工程 | 模块 | 文件绝对路径 | flowtran package |
|-------|------|------|-------------|------------------|
| TC100 | ccbs-dept-impl | dept-pbf | /Users/xxx/project/ccbs-dept-impl/dept-pbf/src/main/resources/trans/TC100.flowtrans.xml | com.spdb.ccbs.dept.pbf.trans |
| TD250 | ccbs-loan-impl | loan-pbf | /Users/xxx/project/ccbs-loan-impl/loan-pbf/src/main/resources/trans/TD250.flowtrans.xml | com.spdb.ccbs.loan.pbf.trans |
| TG350 | ccbs-sett-impl | sett-pbf | /Users/xxx/project/ccbs-sett-impl/sett-pbf/src/main/resources/trans/TG350.flowtrans.xml | com.spdb.ccbs.sett.pbf.trans |
| TY291 | ccbs-comm-impl | comm-pbf | /Users/xxx/project/ccbs-comm-impl/comm-pbf/src/main/resources/trans/TY291.flowtrans.xml | com.spdb.ccbs.comm.pbf.trans |

### 带子目录示例

| 交易码 | 子目录 | 文件绝对路径 | flowtran package |
|-------|-------|-------------|------------------|
| TY291 | chrg | /Users/xxx/project/ccbs-comm-impl/comm-pbf/src/main/resources/trans/chrg/TY291.flowtrans.xml | com.spdb.ccbs.comm.pbf.trans.chrg |
| TY291 | chrg/plszn | /Users/xxx/project/ccbs-comm-impl/comm-pbf/src/main/resources/trans/chrg/plszn/TY291.flowtrans.xml | com.spdb.ccbs.comm.pbf.trans.chrg.plszn |
| TC100 | sttt | /Users/xxx/project/ccbs-dept-impl/dept-pbf/src/main/resources/trans/sttt/TC100.flowtrans.xml | com.spdb.ccbs.dept.pbf.trans.sttt |

## 常见问题

### Q: 如何确定完整的文件路径?
**A**: 按顺序拼接：`{工作空间}/{工程}/{模块}/src/main/resources/trans/{子目录}/{文件名}`。工程和模块根据交易码前缀自动映射。

### Q: 如何判断使用哪个工程和模块?
**A**: 根据交易码的第二个字符(C/D/G/Y)自动确定:
- TC → ccbs-dept-impl / dept-pbf
- TD → ccbs-loan-impl / loan-pbf
- TG → ccbs-sett-impl / sett-pbf
- TY → ccbs-comm-impl / comm-pbf

### Q: 子目录路径格式?
**A**: 
- 文件路径: 使用 `/` 分隔 (如 `chrg/plszn`)
- 包路径: 使用 `.` 分隔 (如 `chrg.plszn`)

### Q: interface 包路径如何生成?
**A**: 在 flowtran 包路径后面加 `.intf`

### Q: 多级子目录如何处理?
**A**: 支持多级子目录,如 `chrg/plszn/sub`,自动转换为包路径格式

### Q: 子目录不存在怎么办?
**A**: 自动创建目录,包括所有父目录

### Q: 必须使用绝对路径吗?
**A**: 是的。创建 XML 文件时必须使用工作空间的绝对路径，不能使用相对路径。创建前必须先获取并展示当前工作空间路径。
