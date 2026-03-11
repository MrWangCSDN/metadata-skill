# 错误码 XML 模板说明

## XML 声明

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
```

固定不变，文件第一行。

---

## errorConf 标签（根标签）

```xml
<errorConf xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="{Id}" longname="{中文名}" package="{包路径}" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    ...
</errorConf>
```

### 属性说明

| 属性 | 顺序 | 取值 |
|------|------|------|
| `xmlns:xsi` | 1 | 固定 `http://www.w3.org/2001/XMLSchema-instance` |
| `id` | 2 | 大驼峰命名（如 `AtLoanError`） |
| `longname` | 3 | 用户提供的中文名 |
| `package` | 4 | `com.spdb.ccbs.{领域}.resources.errors.{子目录}` |
| `xsi:noNamespaceSchemaLocation` | 5 | 固定 `ltts-model.xsd` |

---

## description 标签

```xml
<description><![CDATA[描述内容]]></description>
```

- 位于 `errorConf` 或 `errors` 标签下
- 用户提供描述 → 生成；未提供 → **不生成**
- 使用 CDATA 包裹描述内容

---

## errors 标签（错误码模块）

```xml
<errors id="{模块id}" longname="{模块中文名}">
    <description><![CDATA[模块描述]]></description>
    <error .../>
    <error ...>
        <parameter .../>
    </error>
</errors>
```

### 属性说明

| 属性 | 顺序 | 取值 |
|------|------|------|
| `id` | 1 | 用户指定 |
| `longname` | 2 | 用户指定的中文名 |

---

## error 标签（错误码条目）

### 无参数（自闭合）

```xml
<error id="E00002" message="资产目前只支持负债结算！" type="error"/>
```

### 有参数（含 parameter 子标签）

```xml
<error id="E0000" message="错误描述：[${chmiaosh}]" type="error">
    <parameter id="chmiaosh" longname="错误描述" type="BaseType.U_LONG_DESC"/>
</error>
```

### 多个参数

```xml
<error id="E0003" message="账户${acctNo}的金额${amt}超过限额！" type="error">
    <parameter id="acctNo" longname="账号" type="BaseType.U_ZHANG_HAO"/>
    <parameter id="amt" longname="金额" type="BaseType.U_JIN_E"/>
</error>
```

### 属性说明

| 属性 | 顺序 | 取值 |
|------|------|------|
| `id` | 1 | 用户指定（如 `E0000`） |
| `message` | 2 | 用户指定，可含 `${xxx}` 占位符 |
| `type` | 3 | 固定 `error` |

---

## parameter 标签（错误码参数）

```xml
<parameter id="{参数id}" longname="{参数中文名}" type="{参数类型}"/>
```

### 属性说明

| 属性 | 顺序 | 取值 |
|------|------|------|
| `id` | 1 | 与 message 中 `${xxx}` 的 `xxx` 完全一致 |
| `longname` | 2 | 用户指定的参数中文名 |
| `type` | 3 | 用户指定的参数类型（如 `BaseType.U_LONG_DESC`） |

> ⛔ parameter 的 id 必须与 message 中 `${xxx}` 的 xxx 完全一致。

---

## 缩进规则

| 层级 | 标签 | 缩进 |
|------|------|------|
| 0 | `errorConf` | 0 空格 |
| 1 | `description`（errorConf 级） | 4 空格 |
| 1 | `errors` | 4 空格 |
| 2 | `description`（errors 级） | 8 空格 |
| 2 | `error` | 8 空格 |
| 3 | `parameter` | 12 空格 |

---

## 完整模板

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<errorConf xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="{Id}" longname="{中文名}" package="{包路径}" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <description><![CDATA[{文件描述}]]></description>
    <errors id="{模块id}" longname="{模块中文名}">
        <description><![CDATA[{模块描述}]]></description>
        <error id="{错误码id}" message="{错误信息含${参数}}" type="error">
            <parameter id="{参数id}" longname="{参数中文名}" type="{参数类型}"/>
        </error>
        <error id="{错误码id}" message="{无参数错误信息}" type="error"/>
    </errors>
</errorConf>
```
