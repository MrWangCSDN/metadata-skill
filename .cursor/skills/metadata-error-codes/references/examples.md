# 错误码完整示例

## 示例 1：创建错误码文件（含多模块、参数）

### 用户输入

```
帮我创建 AtLoanError 资产模块错误码，贷款领域

描述：资产模块错误码定义

Colt 抵押物模块错误码
  描述：抵押物模块错误码
  E0000 错误描述：[${chmiaosh}]
    参数：chmiaosh 错误描述 BaseType.U_LONG_DESC
  E00002 资产目前只支持负债结算！

Obsb 表外业务模块错误码
  描述：表外业务模块错误码
  E0000 错误描述：[${chmiaosh}]
    参数：chmiaosh 错误描述 BaseType.U_LONG_DESC
  E00002 资产目前只支持负债结算！
```

### 生成文件

**路径**：`loan-resources/src/main/resources/errors/AtLoanError.errors.xml`

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<errorConf xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="AtLoanError" longname="资产模块错误码" package="com.spdb.ccbs.loan.resources.errors" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <description><![CDATA[资产模块错误码定义]]></description>
    <errors id="Colt" longname="抵押物模块错误码">
        <description><![CDATA[抵押物模块错误码]]></description>
        <error id="E0000" message="错误描述：[${chmiaosh}]" type="error">
            <parameter id="chmiaosh" longname="错误描述" type="BaseType.U_LONG_DESC"/>
        </error>
        <error id="E00002" message="资产目前只支持负债结算！" type="error"/>
    </errors>
    <errors id="Obsb" longname="表外业务模块错误码">
        <description><![CDATA[表外业务模块错误码]]></description>
        <error id="E0000" message="错误描述：[${chmiaosh}]" type="error">
            <parameter id="chmiaosh" longname="错误描述" type="BaseType.U_LONG_DESC"/>
        </error>
        <error id="E00002" message="资产目前只支持负债结算！" type="error"/>
    </errors>
</errorConf>
```

---

## 示例 2：简单错误码（无描述、无参数）

### 用户输入

```
创建 SettBaseError 结算基础错误码，结算领域

Pay 支付模块错误码
  E0001 交易金额不能为零！
  E0002 账户状态异常，无法完成交易！
  E0003 币种不匹配！
```

### 生成文件

**路径**：`sett-resources/src/main/resources/errors/SettBaseError.errors.xml`

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<errorConf xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="SettBaseError" longname="结算基础错误码" package="com.spdb.ccbs.sett.resources.errors" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <errors id="Pay" longname="支付模块错误码">
        <error id="E0001" message="交易金额不能为零！" type="error"/>
        <error id="E0002" message="账户状态异常，无法完成交易！" type="error"/>
        <error id="E0003" message="币种不匹配！" type="error"/>
    </errors>
</errorConf>
```

---

## 示例 3：多参数错误码

### 用户输入

```
创建 DeptAcctError 存款账户错误码，存款领域

AcctMgmt 账户管理模块错误码
  E0001 错误描述：[${errDesc}]
    参数：errDesc 错误描述 BaseType.U_LONG_DESC
  E0002 账户${acctNo}的金额${amt}超过限额！
    参数：acctNo 账号 BaseType.U_ZHANG_HAO
    参数：amt 金额 BaseType.U_JIN_E
  E0003 客户${custId}不存在！
    参数：custId 客户编号 BaseType.U_KE_HU_BIAN_HAO
  E0004 账户已冻结，无法操作！
```

### 生成文件

**路径**：`dept-resources/src/main/resources/errors/DeptAcctError.errors.xml`

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<errorConf xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="DeptAcctError" longname="存款账户错误码" package="com.spdb.ccbs.dept.resources.errors" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <errors id="AcctMgmt" longname="账户管理模块错误码">
        <error id="E0001" message="错误描述：[${errDesc}]" type="error">
            <parameter id="errDesc" longname="错误描述" type="BaseType.U_LONG_DESC"/>
        </error>
        <error id="E0002" message="账户${acctNo}的金额${amt}超过限额！" type="error">
            <parameter id="acctNo" longname="账号" type="BaseType.U_ZHANG_HAO"/>
            <parameter id="amt" longname="金额" type="BaseType.U_JIN_E"/>
        </error>
        <error id="E0003" message="客户${custId}不存在！" type="error">
            <parameter id="custId" longname="客户编号" type="BaseType.U_KE_HU_BIAN_HAO"/>
        </error>
        <error id="E0004" message="账户已冻结，无法操作！" type="error"/>
    </errors>
</errorConf>
```

---

## 示例 4：含子目录

### 用户输入

```
创建 CommAuthError 公共认证错误码，公共领域，子目录 auth

Auth 认证模块错误码
  描述：用户认证相关错误码
  E0001 用户名或密码错误！
  E0002 登录超时，请重新登录！
  E0003 无权限访问资源${resId}！
    参数：resId 资源标识 BaseType.U_RESOURCE_ID
```

### 生成文件

**路径**：`comm-resources/src/main/resources/errors/auth/CommAuthError.errors.xml`

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<errorConf xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="CommAuthError" longname="公共认证错误码" package="com.spdb.ccbs.comm.resources.errors.auth" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <errors id="Auth" longname="认证模块错误码">
        <description><![CDATA[用户认证相关错误码]]></description>
        <error id="E0001" message="用户名或密码错误！" type="error"/>
        <error id="E0002" message="登录超时，请重新登录！" type="error"/>
        <error id="E0003" message="无权限访问资源${resId}！" type="error">
            <parameter id="resId" longname="资源标识" type="BaseType.U_RESOURCE_ID"/>
        </error>
    </errors>
</errorConf>
```

---

## 示例 5：用户仅提供中文名

### 用户输入

```
帮我创建 贷款还款错误码，贷款领域

Repay 还款模块错误码
  E0001 还款金额不能为零！
  E0002 借据${dueBillCd}已结清！
    参数：dueBillCd 借据编码 BaseType.U_DAI_KUAN_JIE_JU_BIAN_MA
```

### 处理逻辑

- 用户未指定英文名，翻译生成大驼峰：`LoanRepayError`
- errorConf id：`LoanRepayError`
- longname：`贷款还款错误码`

### 生成文件

**路径**：`loan-resources/src/main/resources/errors/LoanRepayError.errors.xml`

```xml
<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<errorConf xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="LoanRepayError" longname="贷款还款错误码" package="com.spdb.ccbs.loan.resources.errors" xsi:noNamespaceSchemaLocation="ltts-model.xsd">
    <errors id="Repay" longname="还款模块错误码">
        <error id="E0001" message="还款金额不能为零！" type="error"/>
        <error id="E0002" message="借据${dueBillCd}已结清！" type="error">
            <parameter id="dueBillCd" longname="借据编码" type="BaseType.U_DAI_KUAN_JIE_JU_BIAN_MA"/>
        </error>
    </errors>
</errorConf>
```

---

## 示例 6：修改现有错误码

### 用户输入

```
修改 AtLoanError 错误码

在 Colt 模块下新增：
  E00003 抵押物估值${colVal}低于最低要求${minVal}！
    参数：colVal 抵押物估值 BaseType.U_JIN_E
    参数：minVal 最低估值 BaseType.U_JIN_E
```

### 处理逻辑

1. 定位 `AtLoanError.errors.xml`
2. 读取原文件内容
3. 在 `<errors id="Colt">` 模块内追加新的 `<error>` 条目
4. 保持其他内容不变

---

## 对话指令速查表

| 场景 | 示例指令 |
|------|----------|
| 创建错误码 | 「创建 XXX 错误码」「新建 errors」 |
| 指定领域 | 「贷款领域」「存款领域」「结算领域」「公共领域」 |
| 指定子目录 | 「子目录 auth」「放在 at 下」 |
| 只有中文名 | 仅提供中文名 → 自动翻译为大驼峰 |
| 修改错误码 | 「修改 AtLoanError 错误码」「在 XXX 里加错误码」 |
| 含参数 | message 写 `${xxx}`，下方用 `参数：xxx 中文名 类型` |
| 模块描述 | 模块下方写 `描述：xxx` |
| 文件描述 | 模块列表前写 `描述：xxx` |
