---
name: metadata-composite-types
description: 创建元数据复合类型定义，包括表定义（Table）和自定义SQL定义。当用户需要定义数据库表结构、建表元数据或自定义SQL查询元数据时使用。
---

# 元数据复合类型定义

## 包含模型

- **表定义（Table Definition）**
- **自定义SQL（Custom SQL）**

---

## 表定义（Table Definition）

**用途**：描述数据库表的结构元数据，包含字段、索引、主键、外键等信息。

**示例结构**：

```yaml
type: table
code: T_ORDER
name: 订单表
module: 订单管理
datasource: order_db
physicalName: t_order
comment: 存储订单主信息
columns:
  - code: ORDER_ID
    name: 订单ID
    physicalName: order_id
    dataType: VARCHAR
    length: 32
    nullable: false
    primaryKey: true
    comment: 订单唯一标识
  - code: USER_ID
    name: 用户ID
    physicalName: user_id
    dataType: VARCHAR
    length: 32
    nullable: false
    comment: 下单用户ID
  - code: STATUS
    name: 订单状态
    physicalName: status
    dataType: TINYINT
    nullable: false
    defaultValue: "0"
    enumRef: ORDER_STATUS
    comment: 关联枚举 ORDER_STATUS
  - code: CREATE_TIME
    name: 创建时间
    physicalName: create_time
    dataType: DATETIME
    nullable: false
indexes:
  - code: IDX_USER_ID
    columns: [user_id]
    unique: false
  - code: IDX_STATUS
    columns: [status, create_time]
    unique: false
```

### 字段（Column）说明

| 字段 | 说明 | 是否必填 |
|------|------|--------|
| `code` | 字段逻辑编码，大写下划线 | 是 |
| `physicalName` | 数据库实际列名，小写下划线 | 是 |
| `dataType` | 数据类型（VARCHAR/INT/DATETIME等） | 是 |
| `length` | 字段长度（字符串类型必填） | 按类型 |
| `nullable` | 是否可为空 | 是 |
| `primaryKey` | 是否主键 | 否 |
| `enumRef` | 关联枚举 code（枚举类型字段填写） | 否 |
| `defaultValue` | 默认值 | 否 |

### 命名规范

- 表物理名：`t_` 前缀 + 小写下划线，例如 `t_order_item`
- 字段物理名：小写下划线，例如 `order_id`
- 逻辑编码：大写下划线，例如 `ORDER_ID`

---

## 自定义SQL（Custom SQL）

**用途**：封装复杂查询逻辑，定义可复用的 SQL 片段或视图级查询，供上层服务引用。

**示例结构**：

```yaml
type: custom_sql
code: Q_ORDER_DETAIL
name: 订单详情查询
module: 订单管理
datasource: order_db
resultType: OrderDetailDTO
description: 根据订单ID查询订单及明细信息，包含联表

parameters:
  - name: orderId
    dataType: VARCHAR
    required: true
    description: 订单ID

sql: |
  SELECT
    o.order_id,
    o.status,
    o.create_time,
    i.item_id,
    i.sku_id,
    i.quantity
  FROM t_order o
  LEFT JOIN t_order_item i ON o.order_id = i.order_id
  WHERE o.order_id = :orderId
```

### 自定义SQL字段说明

| 字段 | 说明 |
|------|------|
| `resultType` | 返回结果映射的复合类型（DTO）名称 |
| `parameters` | SQL 入参列表，使用 `:paramName` 占位 |
| `datasource` | 目标数据源标识 |

### 注意事项

- SQL 中禁止硬编码业务参数，所有变量通过 `parameters` 传入
- 复杂 SQL 建议附加 `description` 说明联表逻辑
- 自定义SQL不包含DDL语句，仅限查询（SELECT）

---

## 参考资料

- 基础类型（枚举、字典、错误码、常量）请参考 [metadata-basic-types](../metadata-basic-types/SKILL.md)
- 构件接口/实现定义请参考 [metadata-components](../metadata-components/SKILL.md)
