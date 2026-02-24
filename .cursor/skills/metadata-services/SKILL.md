---
name: metadata-services
description: 创建服务类元数据定义，包括PCS组合服务（接口定义与实现定义）和PBS基础服务（接口定义与实现定义）。当用户需要定义组合服务或基础服务的接口与实现元数据时使用。
---

# 元数据服务定义

## 服务类型总览

| 类型 | 全称 | 定位 |
|------|------|------|
| PCS | Platform Composite Service | 组合服务，编排多个构件或基础服务，面向前端/外部系统 |
| PBS | Platform Basic Service | 基础服务，封装单一业务能力，供组合服务调用 |

每种服务均分为**接口定义**和**实现定义**两部分。

---

## PCS 组合服务

### PCS 接口定义

**用途**：定义组合服务对外暴露的 API 契约，通常对应一个业务用例或页面操作。

**示例结构**：

```yaml
type: pcs_interface
code: IOrderSubmitService
name: 提交订单组合服务接口
module: 订单管理
version: "1.0.0"
description: 处理用户提交订单的完整流程，包含库存检查、价格计算、订单创建

protocol: HTTP          # HTTP / DUBBO / gRPC
httpMethod: POST
path: /order/submit

methods:
  - code: submitOrder
    name: 提交订单
    input:
      - name: request
        dataType: OrderSubmitRequest
        required: true
    output:
      dataType: OrderSubmitResponse
    errors:
      - ORD1001
      - INV2001
    timeout: 5000       # 毫秒
```

### PCS 实现定义

**用途**：描述组合服务的编排逻辑，定义调用哪些构件或基础服务及其顺序。

**示例结构**：

```yaml
type: pcs_impl
code: OrderSubmitServiceImpl
name: 提交订单组合服务实现
module: 订单管理
version: "1.0.0"
interfaceRef: IOrderSubmitService

steps:
  - seq: 1
    name: 校验库存
    callType: component_interface
    ref: IInventoryCheckService
    method: checkStock
    onError: ABORT          # ABORT / SKIP / COMPENSATE

  - seq: 2
    name: 计算订单价格
    callType: pbs_interface
    ref: IPriceCalculateService
    method: calculate
    onError: ABORT

  - seq: 3
    name: 创建订单
    callType: component_interface
    ref: IOrderCreateService
    method: createOrder
    onError: COMPENSATE
    compensate:
      ref: IOrderCreateService
      method: rollbackOrder

  - seq: 4
    name: 扣减库存
    callType: component_interface
    ref: IInventoryDeductService
    method: deductStock
    onError: COMPENSATE
```

### PCS 实现步骤字段说明

| 字段 | 说明 |
|------|------|
| `seq` | 执行顺序 |
| `callType` | 调用类型：`component_interface` / `pbs_interface` |
| `ref` | 被调用的接口 code |
| `onError` | 异常处理策略：ABORT（中止）/ SKIP（跳过）/ COMPENSATE（补偿） |
| `compensate` | `onError=COMPENSATE` 时的补偿调用 |

---

## PBS 基础服务

### PBS 接口定义

**用途**：定义单一业务能力的服务契约，粒度比 PCS 细，通常被 PCS 编排调用。

**示例结构**：

```yaml
type: pbs_interface
code: IPriceCalculateService
name: 价格计算基础服务接口
module: 促销定价
version: "1.0.0"
description: 根据商品信息及促销规则计算实付价格

methods:
  - code: calculate
    name: 计算价格
    input:
      - name: items
        dataType: List<OrderItemDTO>
        required: true
      - name: couponCode
        dataType: String
        required: false
        description: 优惠券码，不传则不使用优惠
    output:
      dataType: PriceResult
    errors:
      - PRC3001
```

### PBS 实现定义

**用途**：描述基础服务的具体实现逻辑，依赖构件完成业务处理。

**示例结构**：

```yaml
type: pbs_impl
code: PriceCalculateServiceImpl
name: 价格计算基础服务实现
module: 促销定价
version: "1.0.0"
interfaceRef: IPriceCalculateService

dependencies:
  - type: component_interface
    ref: IPromotionQueryService
  - type: component_interface
    ref: ICouponValidateService

methods:
  - code: calculate
    implementation: |
      1. 查询商品原价列表
      2. 调用 IPromotionQueryService 获取适用促销规则
      3. 若传入 couponCode，调用 ICouponValidateService 校验并计算优惠
      4. 按规则优先级叠加折扣，计算最终价格
      5. 返回 PriceResult（含明细）
```

---

## PCS 与 PBS 的区别

| 维度 | PCS 组合服务 | PBS 基础服务 |
|------|-------------|-------------|
| 调用者 | 前端 / 外部系统 | PCS 服务 |
| 粒度 | 业务用例级 | 单一能力级 |
| 是否编排 | 是，多步骤编排 | 否，单一逻辑 |
| 事务边界 | 可含分布式事务 | 通常本地事务 |

---

## 参考资料

- 构件定义（PBCB/PBCP/PBCC/PBCT）请参考 [metadata-components](../metadata-components/SKILL.md)
- 联机交易定义请参考 [metadata-transactions](../metadata-transactions/SKILL.md)
