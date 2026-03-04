# 联机交易元数据 —— 对话指令指南

本文档为开发人员提供与 AI 对话创建/修改 flowtran 联机交易元数据的标准指令模板。

---

## 前置说明

### 交易码规范

| 前缀 | 领域 | 有效范围 | 示例 |
|------|------|---------|------|
| TC | 存款 | TC021–TC999 | TC100 |
| TD | 贷款 | TD001–TD499 | TD250 |
| TG | 结算 | TG001–TG499 | TG350 |
| TY | 平台公共 | TY001–TY999 | TY291 |

### 字段必输说明

- **必输**：`required="true"`
- **非必输**（缺省）：`required="false"`

### 数组字段写法

```
{数组名}Array {中文名}数组 start
    包含 {字段名}  {中文名}  {必输/非必输}
{数组名}Array {中文名}数组 end
```

### 属性接口写法

属性接口对应 XML 中的 `<property packMode="true">` 标签，位于输出之后。

支持两种字段类型：

| 类型 | 写法 | 说明 |
|------|------|------|
| 复合对象引用 | `[中文名]` | AI 自动搜索对应复合类型 |
| 普通字段 | 直接写中文名 | 同输入/输出字段，查 MCP |

修饰词：`多值`（multi=true）、`必输`（required=true），可组合使用。

```
属性接口：
[{引用复合对象中文名}]  {多值}  {必输}
{英文id} [{引用复合对象中文名}]
{普通字段中文名}  {必输/非必输}
```

---

## 场景 1：直接创建新交易

### 指令模板

```
帮我新建 {交易码} {交易中文名} 的联机交易

输入:
{字段名}  {字段中文名}  {必输/非必输}
...

输出:
{字段名}  {字段中文名}
...
```

### 示例 1-A：基本字段

```
帮我新建 TY291 收费明细文件批量查询 的联机交易

输入:
cst     国家    非必输
xb      性别    必输

输出:
cst     国家
xb      性别
```

### 示例 1-B：含数组字段

```
帮我新建 TY292 客户账户信息查询 的联机交易

输入:
custId    客户ID    必输
accountArray 账户数组 start
    包含 accountNo    账号        必输
    包含 accountType  账户类型     非必输
accountArray 账户数组 end

输出:
custName  客户名称
accountArray 账户数组 start
    包含 accountNo  账号
    包含 balance    余额
accountArray 账户数组 end
totalCount  总记录数
```

### 示例 1-C：只读查询交易（txnMode=R）

```
帮我新建 TC100 存款账户余额查询 的联机交易，交易模式为只读

输入:
accountNo  账号  必输

输出:
accountNo  账号
balance    余额
```

### AI 返回格式示例

```
✅ 成功创建 flowtran 交易

📁 文件位置: comm-pbf/src/main/resources/trans/TY291.flowtrans.xml
📋 交易编码: TY291
📝 交易名称: 收费明细文件批量查询
🏢 所属领域: 平台公共领域
📦 包路径:   com.spdb.ccbs.comm.pbf.trans

📥 输入字段(2个):
  ✅ cst (国家) - 非必输
  ✅ xb  (性别) - 必输

📤 输出字段(2个):
  ✅ cst (国家)
  ✅ xb  (性别)
```

---

## 场景 2：修改现有交易

### 指令模板

```
修改 {交易码}

输入:
{字段名}  {字段中文名}  {必输/非必输}
...

输出:
{字段名}  {字段中文名}
...
```

> ⚠️ **说明**：修改指令会完整替换原交易的 input 和 output 字段。
> 如需保留原有字段，请在指令中把原字段一并列出。

### 示例 2-A：替换字段

```
修改 TY291

输入:
cst       国家      非必输
xb        性别      必输
custId    客户ID    必输

输出:
cst       国家
xb        性别
custId    客户ID
result    处理结果
```

### 示例 2-B：在原有字段基础上新增

```
修改 TY291，在原有字段基础上，输入增加 queryDate 查询日期（非必输），输出增加 totalCount 总记录数
```

### AI 返回格式示例

```
✅ 成功修改 flowtran 交易

📁 文件位置: comm-pbf/src/main/resources/trans/TY291.flowtrans.xml
📋 交易编码: TY291

保留原有属性:
  ✅ flowtran 标签属性保持不变
  ✅ description 内容保持不变
  ✅ interface package 保持不变

更新内容:
  📥 输入字段更新为 3 个
  📤 输出字段更新为 4 个
```

---

## 场景 3：在子目录下创建交易

### 指令模板

```
帮我在 {子目录名} 子目录下新建 {交易码} {交易中文名} 的联机交易

输入:
{字段名}  {字段中文名}  {必输/非必输}
...

输出:
{字段名}  {字段中文名}
...
```

### 示例 3-A：单级子目录

```
帮我在 chrg 子目录下新建 TY291 收费明细查询 的联机交易

输入:
fPrjCd  收费项目编码  必输

输出:
fPrjCd  收费项目编码
chrgAmt 收费金额
```

**生成结果**：
- 文件路径：`comm-pbf/src/main/resources/trans/chrg/TY291.flowtrans.xml`
- 包路径：`com.spdb.ccbs.comm.pbf.trans.chrg`

### 示例 3-B：多级子目录

```
帮我在 chrg/plszn 子目录下新建 TY292 平摊结算查询 的联机交易

输入:
settDate  结算日期  必输

输出:
settDate  结算日期
settAmt   结算金额
```

**生成结果**：
- 文件路径：`comm-pbf/src/main/resources/trans/chrg/plszn/TY292.flowtrans.xml`
- 包路径：`com.spdb.ccbs.comm.pbf.trans.chrg.plszn`

### AI 返回格式示例

```
✅ 成功创建 flowtran 交易

📁 文件位置: comm-pbf/src/main/resources/trans/chrg/TY291.flowtrans.xml
📋 交易编码: TY291
📦 包路径:   com.spdb.ccbs.comm.pbf.trans.chrg
🗂️  子目录:   chrg
```

---

## 场景 4：含属性接口的交易

### 指令模板

```
帮我新建 {交易码} {交易中文名} 的联机交易

输入:
{字段名}  {字段中文名}  {必输/非必输}
...

输出:
{字段名}  {字段中文名}
...

属性接口：
[{引用复合对象中文名}]  {多值}  {必输}
{普通字段中文名}
```

### 示例 4-A：含复合对象引用的属性接口

```
帮我新建 TD300 贷款账号综合查询 的联机交易

输入:
custId    客户ID    必输
queryDate 查询日期

输出:
custName   客户名称
totalCount 总记录数

属性接口：
[贷款查询存款账号输入列表]  多值  必输
[贷款查询公共账号输出列表]
查询笔数
可用余额
```

### 示例 4-B：指定英文 id 的复合对象引用

```
帮我新建 TD301 贷款信息查询 的联机交易

输入:
custId  客户ID  必输

输出:
custName  客户名称

属性接口：
lstDkCxIn [贷款查询输入列表]  多值
avlBal    可用余额
```

> `lstDkCxIn` 是用户指定的英文 id，直接作为 `field` 的 `id` 属性使用。

### AI 返回格式示例

```
✅ 成功创建 flowtran 交易

📁 文件位置: loan-pbf/src/main/resources/trans/TD300.flowtrans.xml
📋 交易编码: TD300

📋 MCP 字段查询结果：
  ✅ 客户ID     →  type=MBaseType.U_KE_HU_BIAN_HAO
  ✅ 查询日期   →  type=MBaseType.U_RI_QI
  ✅ 客户名称   →  type=MBaseType.U_KE_HU_MING_CHENG
  ✅ 总记录数   →  type=MBaseType.U_JI_SHU
  ✅ 查询笔数   →  type=MBaseType.U_JI_SHU
  ❌ 可用余额   →  未贯标，已跳过

🔍 复合对象引用搜索结果（property）：
  ✅ [贷款查询存款账号输入列表]  →  LoanQueryType.DkCxCkZhSrIn
  ✅ [贷款查询公共账号输出列表]  →  LoanQueryType.DkCxGgZhSc

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  以下字段未写入 XML，请确认后补充：

【未贯标字段】（需完成贯标后重新执行）：
  1. 可用余额（property）

💡 完成上述问题后，可重新执行以补充这些字段。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### 属性接口字段未找到时

当 `[xxx]` 对应的复合类型在当前领域目录下不存在时：

```
🔍 复合对象引用搜索结果（property）：
  ❌ [贷款查询存款账号输入列表]  →  未找到匹配的 c_schema.xml，已跳过
  ✅ [贷款查询公共账号输出列表]  →  LoanQueryType.DkCxGgZhSc
```

未找到的引用**不写入 XML**，并在汇总提示中说明：

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  以下字段未写入 XML，请确认后补充：

【property 复合对象引用未找到】（需确认 c_schema.xml 是否已创建）：
  1. [贷款查询存款账号输入列表]

💡 确认文件已创建后，可重新执行以补充这些字段。
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 场景 6：综合场景（含数组 + 子目录）

```
帮我在 sttt 子目录下新建 TC150 结算账户综合查询 的联机交易

输入:
custId  客户ID  必输
transArray 交易数组 start
    包含 transId   交易ID    必输
    包含 transAmt  交易金额   必输
transArray 交易数组 end
queryDate  查询日期  非必输

输出:
custName   客户名称
transArray 交易数组 start
    包含 transId   交易ID
    包含 transAmt  交易金额
    包含 transDate 交易日期
transArray 交易数组 end
totalCount 总记录数
```

---

## 常见错误与修正

### ❌ 交易码格式错误

| 错误输入 | 原因 | 正确写法 |
|---------|------|---------|
| `Y291` | 缺少 T 前缀 | `TY291` |
| `ty291` | 必须大写 | `TY291` |
| `TC001` | TC 最小值为 TC021 | `TC021` |
| `TD500` | TD 最大值为 TD499 | `TD499` |
| `TX100` | X 不是有效前缀 | `TC100` 或 `TY100` |

### ❌ 字段未贯标

AI 会提示：
```
❌ 以下字段未贯标，需要在 dict-mcp-server 系统中完成贯标：
  1. 未知字段名
  2. 另一个字段名

💡 请先完成字段贯标后重新提交指令
```

**解决**：在 `dict-mcp-server` 字段管理系统中完成字段贯标（登记字段英文名、类型、中文名等元数据）后，重新执行指令。

### ❌ 数组字段格式错误

| 错误 | 正确 |
|------|------|
| `chargCd 收费代码数组 start` | `chargCdArray 收费代码数组 start`（id 必须以 Array 结尾） |
| 只有 start 没有 end | start 和 end 必须成对出现 |
| start 和 end 名称不一致 | 保持名称完全一致 |

### ❌ 属性接口复合对象未找到

AI 会提示：
```
❌ [贷款查询存款账号输入列表] → 未找到匹配的 c_schema.xml，已跳过
```

**解决**：确认对应的 `*.c_schema.xml` 复合类型文件已创建，且 `complexType` 的 `longname` 与中括号内的中文名**完全一致**，然后重新执行指令。

---

## 快速指令速查

| 场景 | 指令起始语 |
|------|-----------|
| 创建新交易 | `帮我新建 {交易码} {名称} 的联机交易` |
| 在子目录创建 | `帮我在 {子目录} 子目录下新建 {交易码} {名称} 的联机交易` |
| 修改现有交易 | `修改 {交易码}` |
| 只读交易 | 在指令末尾加：`，交易模式为只读` |
| 含属性接口 | 在输出之后加：`属性接口：` 并按行列出字段 |
| 属性接口复合引用 | 字段行写 `[中文名]`，可加 `多值`/`必输` |
| 属性接口指定英文 id | 字段行写 `英文id [中文名]` |
