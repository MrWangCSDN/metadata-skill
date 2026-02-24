---
name: metadata-components
description: 创建构件类元数据定义，包括PBCB业务构件、PBCP产品构件、PBCC公共构件、PBCT技术构件的接口定义与实现定义。当用户需要定义构件接口或构件实现元数据时使用。
---

# 元数据构件定义

## 构件类型总览

| 类型 | 全称 | 定位 |
|------|------|------|
| PBCB | Platform Business Component Business | 业务构件，承载具体业务逻辑 |
| PBCP | Platform Business Component Product | 产品构件，跨业务复用的产品能力 |
| PBCC | Platform Business Component Common | 公共构件，通用工具与公共能力 |
| PBCT | Platform Business Component Technical | 技术构件，基础技术能力封装 |

每种构件均分为**接口定义**和**实现定义**两部分。

---

## 接口定义（Interface Definition）

接口定义描述构件对外暴露的契约，不涉及实现细节。

**示例结构**：

```yaml
type: component_interface
componentType: PBCB          # PBCB / PBCP / PBCC / PBCT
code: IOrderQueryService
name: 订单查询构件接口
module: 订单管理
version: "1.0.0"
description: 提供订单查询相关能力

methods:
  - code: queryOrderById
    name: 根据ID查询订单
    description: 通过订单ID查询订单详情
    input:
      - name: orderId
        dataType: String
        required: true
        description: 订单ID
    output:
      dataType: OrderDetailDTO
      description: 订单详情对象
    errors:
      - ORD1001   # 关联错误码 code

  - code: queryOrderList
    name: 分页查询订单列表
    input:
      - name: query
        dataType: OrderQueryDTO
        required: true
    output:
      dataType: PageResult<OrderDTO>
```

### 接口方法字段说明

| 字段 | 说明 |
|------|------|
| `code` | 方法编码，驼峰命名 |
| `input` | 入参列表 |
| `output.dataType` | 返回值类型，支持泛型写法 |
| `errors` | 可能抛出的错误码列表（引用错误码定义 code） |

---

## 实现定义（Implementation Definition）

实现定义描述构件的具体实现方式，与接口定义关联。

**示例结构**：

```yaml
type: component_impl
componentType: PBCB
code: OrderQueryServiceImpl
name: 订单查询构件实现
module: 订单管理
version: "1.0.0"
interfaceRef: IOrderQueryService    # 关联接口定义 code
description: 订单查询构件的默认实现

dependencies:
  - type: table
    ref: T_ORDER
  - type: table
    ref: T_ORDER_ITEM
  - type: component_interface
    ref: IUserInfoService            # 依赖其他构件接口

methods:
  - code: queryOrderById
    implementation: |
      1. 参数校验：orderId 不为空
      2. 查询 T_ORDER 表获取订单主信息
      3. 查询 T_ORDER_ITEM 表获取订单明细
      4. 调用 IUserInfoService.getUserById 补充用户信息
      5. 组装 OrderDetailDTO 返回
```

### 实现定义字段说明

| 字段 | 说明 |
|------|------|
| `interfaceRef` | 对应接口定义的 code |
| `dependencies` | 依赖的其他元数据（表、构件接口等） |
| `methods` | 各方法的实现逻辑描述 |

---

## 各构件类型差异说明

### PBCB 业务构件
- 关注具体业务场景
- 允许直接依赖业务表（T_ 前缀）
- 方法命名贴近业务语义

### PBCP 产品构件
- 面向产品功能抽象，跨业务域复用
- 不应依赖特定业务表，通过 PBCB 构件获取数据

### PBCC 公共构件
- 通用工具类能力，如日期处理、加解密、文件操作
- 无业务含义，纯技术或工具逻辑

### PBCT 技术构件
- 基础技术能力，如缓存、消息、分布式锁
- 封装中间件操作，屏蔽技术细节

---

## 命名规范

- 接口定义：`I` + 大驼峰，例如 `IOrderQueryService`
- 实现定义：接口名去掉 `I` + `Impl`，例如 `OrderQueryServiceImpl`
- 方法编码：小驼峰，例如 `queryOrderById`

---

## 参考资料

- 服务定义（PCS/PBS）请参考 [metadata-services](../metadata-services/SKILL.md)
- 错误码定义请参考 [metadata-basic-types](../metadata-basic-types/SKILL.md)
