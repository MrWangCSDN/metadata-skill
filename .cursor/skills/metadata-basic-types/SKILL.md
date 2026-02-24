---
name: metadata-basic-types
description: 创建元数据基础类型定义，包括自定义类型、枚举类型、字典定义、错误码定义、常量定义。当用户需要新增或修改枚举、字典、错误码、常量等基础元数据模型时使用。
---

# 元数据基础类型定义

## 包含模型

- **自定义类型**：枚举类型、字典定义
- **错误码定义**
- **常量定义**

## 通用字段规范

每个基础类型元数据必须包含：

| 字段 | 说明 | 是否必填 |
|------|------|--------|
| `code` | 唯一编码，大写下划线命名 | 是 |
| `name` | 中文名称 | 是 |
| `description` | 描述说明 | 否 |
| `module` | 所属模块/领域 | 是 |

---

## 枚举类型（Enum）

**用途**：定义有限取值集合，用于状态、类型等字段约束。

**示例结构**：

```yaml
type: enum
code: ORDER_STATUS
name: 订单状态
module: 订单管理
items:
  - value: "0"
    label: 待支付
  - value: "1"
    label: 已支付
  - value: "2"
    label: 已取消
```

**注意事项**：
- `value` 建议使用数字字符串或大写英文，避免中文
- 枚举项需穷举所有合法取值
- 枚举 code 在全局唯一

---

## 字典定义（Dictionary）

**用途**：可动态扩展的键值对集合，适合配置项、分类标签等。

**示例结构**：

```yaml
type: dictionary
code: REGION_CODE
name: 行政区划代码
module: 公共基础
dataType: string
items:
  - key: "110000"
    label: 北京市
  - key: "310000"
    label: 上海市
```

**与枚举的区别**：字典项可运行时动态维护，枚举在编译期固定。

---

## 错误码定义（ErrorCode）

**用途**：统一定义系统所有错误码，便于前后端对接和排查问题。

**编码规则**：`[系统前缀][模块编号][序号]`，例如 `SYS0001`、`ORD1001`

**示例结构**：

```yaml
type: error_code
code: ORD1001
name: 订单不存在
httpStatus: 404
message: "订单[{orderId}]不存在，请确认后重试"
module: 订单管理
level: WARN
```

**字段说明**：

| 字段 | 说明 |
|------|------|
| `httpStatus` | 对应 HTTP 状态码 |
| `message` | 错误提示模板，支持占位符 `{param}` |
| `level` | 日志级别：INFO / WARN / ERROR |

---

## 常量定义（Constant）

**用途**：系统中不变的固定值，如超时时长、分页大小、第三方配置键等。

**示例结构**：

```yaml
type: constant
code: MAX_PAGE_SIZE
name: 最大分页数
value: "200"
dataType: integer
module: 公共基础
description: 列表查询每页最多返回条数上限
```

**注意事项**：
- 常量值统一用字符串存储，通过 `dataType` 标明实际类型
- 避免将业务逻辑硬编码为常量，应使用枚举或字典

---

## 参考资料

- 复合类型（表定义、自定义SQL）请参考 [metadata-composite-types](../metadata-composite-types/SKILL.md)
- 构件接口/实现定义请参考 [metadata-components](../metadata-components/SKILL.md)
