# PBS/PCS 服务 XML 模板详解

## 格式强制规则

| 规则 | 说明 | 强制等级 |
|------|------|----------|
| ⛔ 属性不换行 | 所有标签属性必须写在同一行 | 强制 |
| ⛔ 无空行 | 不同标签之间不能有空行 | 强制 |
| ⛔ 禁用 Tab | 只使用空格缩进 | 强制 |
| 询问配套实现 | 创建新服务时必须询问用户是否创建实现文件 | 强制 |
| 4 空格缩进 | 每层子标签缩进 4 空格 | 强制 |

---

## 缩进级别对照表

| 层级 | 标签 | 缩进空格 |
|------|------|----------|
| 0 | `serviceType` / `serviceImpl` | 0 |
| 1 | `service` | 4 |
| 2 | `description` / `interface` | 8 |
| 3 | `input` / `output` | 12 |
| 4 | `field`（直接子节点） | 16 |
| 5 | `field`（位于 `fields` 内） | 20 |

---

## 接口文件模板

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

---

## serviceType 属性表和顺序

| 顺序 | 属性 | 说明 | 固定值/来源 |
|------|------|------|-------------|
| 1 | `xmlns:xsi` | XML Schema 实例命名空间 | 固定 |
| 2 | `id` | 服务唯一标识 | 大驼峰业务名 + 服务类型后缀（如 `PbsSvtp`） |
| 3 | `kind` | 类型 | 固定 `auto` |
| 4 | `longname` | 中文名称 | 用户提供 |
| 5 | `package` | 接口包路径 | 根据领域、服务类型、子目录映射 |
| 6 | `xsi:noNamespaceSchemaLocation` | Schema 位置 | 固定 `ltts-model.xsd` |
| 7 | `outbound` | 出站标志 | 固定 `false` |

---

## 实现文件模板

实现文件仅包含一个 `<serviceImpl>` 根标签，**无** `<service>` 子标签，使用自闭合 `/>` 结尾。XML 声明第一行为 `<?xml  version=`（xml 与 version 之间双空格）。

```xml
<?xml  version="1.0" encoding="UTF-8" standalone="yes"?>
<serviceImpl xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="FtAcctgDealPbsImpl" longname="福费延账务处理类服务实现" serviceType="FtAcctgDealPbsSvtp" package="com.spdb.ccbs.loan.pbs.impl.serviceimpl.ft" xsi:noNamespaceSchemaLocation="ltts-model.xsd"/>
```

---

## serviceImpl 属性表和顺序

| 顺序 | 属性 | 说明 | 固定值/来源 |
|------|------|------|-------------|
| 1 | `xmlns:xsi` | XML Schema 实例命名空间 | 固定 |
| 2 | `id` | 实现唯一标识 | 服务 id 的 `Svtp` 替换为 `Impl` |
| 3 | `longname` | 实现中文名称 | 服务 longname + 「类服务实现」 |
| 4 | `serviceType` | 关联的接口 id | 接口文件的 `serviceType` 的 `id` |
| 5 | `package` | 实现包路径 | 根据领域、服务类型、子目录映射 |
| 6 | `xsi:noNamespaceSchemaLocation` | Schema 位置 | 固定 `ltts-model.xsd` |

---

## service 标签说明（仅接口文件）

| 属性 | 说明 |
|------|------|
| `id` | 服务标识，大驼峰 + 服务类型后缀（如 `FtAcctgDealPbsSvtp`） |
| `name` | 接口方法名，小驼峰（如 `ftAcctgDeal`） |
| `longname` | 服务中文名 |

---

## input / output 说明

| 标签 | 属性 | 说明 |
|------|------|------|
| `input` | `packMode` | 默认 `false`；用户指明生成输入接口类时为 `true` |
| `output` | `asParm` | 固定 `false` |
| `output` | `packMode` | 默认 `false`；用户指明生成输出接口类时为 `true` |

---

## 字段说明

参考 metadata-pbc 和 metadata-transactions skill：普通字段查 MCP、复合引用 `[xxx]` 调脚本、数组字段 `fields` start/end。
