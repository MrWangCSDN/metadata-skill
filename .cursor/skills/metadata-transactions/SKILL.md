---
name: metadata-transactions
description: 创建联机交易元数据定义，描述端到端的交易流程、报文格式、渠道适配及风控规则。当用户需要定义联机交易、交易报文、交易流程或渠道路由元数据时使用。
---

# 元数据联机交易定义

## 定位

联机交易（Online Transaction）是面向终端用户或外部系统的完整交易单元，描述从请求接入到结果返回的端到端处理流程，是系统对外的最小交易契约。

---

## 交易定义结构

### 基本信息

```yaml
type: online_transaction
code: TXN_ORDER_SUBMIT
name: 提交订单交易
module: 订单管理
version: "1.0.0"
channel:
  - APP
  - WEB
  - MINI_PROGRAM
description: 用户在各渠道发起下单操作的联机交易

timeout: 10000            # 交易超时时间（毫秒）
idempotent: true          # 是否支持幂等重试
```

### 报文定义

```yaml
request:
  format: JSON
  fields:
    - name: userId
      dataType: String
      required: true
      description: 用户ID
    - name: items
      dataType: List<OrderItemDTO>
      required: true
      description: 购买商品列表
    - name: addressId
      dataType: String
      required: true
      description: 收货地址ID
    - name: couponCode
      dataType: String
      required: false
      description: 优惠券码

response:
  format: JSON
  fields:
    - name: code
      dataType: String
      description: 结果码，"0000" 表示成功
    - name: message
      dataType: String
      description: 结果描述
    - name: data
      dataType: OrderSubmitResult
      description: 成功时的交易结果
```

### 交易流程

```yaml
flow:
  - seq: 1
    name: 渠道鉴权
    type: auth
    description: 校验 token/签名，确认渠道合法性

  - seq: 2
    name: 入参校验
    type: validate
    description: 必填项、格式、业务规则校验

  - seq: 3
    name: 风控检查
    type: risk_control
    riskPolicy: ORDER_SUBMIT_RISK
    description: 频率限制、黑名单、异常行为检测

  - seq: 4
    name: 业务处理
    type: service_call
    callType: pcs_interface
    ref: IOrderSubmitService
    method: submitOrder

  - seq: 5
    name: 结果封装
    type: response_build
    description: 统一封装响应报文，错误码映射

  - seq: 6
    name: 交易日志
    type: audit_log
    async: true
    description: 异步记录交易流水，供对账使用
```

### 字段说明

| 字段 | 说明 |
|------|------|
| `channel` | 适用渠道：APP / WEB / MINI_PROGRAM / API 等 |
| `idempotent` | 是否幂等，true 时需传 `requestId` 做去重 |
| `flow[].type` | 步骤类型：auth / validate / risk_control / service_call / response_build / audit_log |
| `flow[].async` | 是否异步执行（不阻塞主流程） |

---

## 风控策略定义

联机交易可引用风控策略，风控策略单独定义：

```yaml
type: risk_policy
code: ORDER_SUBMIT_RISK
name: 提交订单风控策略
rules:
  - name: 频率限制
    dimension: userId
    limit: 10
    window: 60s
    action: REJECT

  - name: 金额预警
    condition: "totalAmount > 50000"
    action: MANUAL_REVIEW
```

---

## 幂等处理规范

当 `idempotent: true` 时：

1. 请求必须携带 `requestId`（全局唯一，由调用方生成）
2. 系统在交易执行前检查 `requestId` 是否已处理：
   - 已处理且成功 → 直接返回原结果
   - 已处理且失败 → 返回原失败结果，不重试
   - 未处理 → 正常执行
3. `requestId` 有效期由常量 `TXN_IDEMPOTENT_TTL` 定义

---

## 交易码命名规范

- 格式：`TXN_` + 模块缩写 + `_` + 动词 + 名词
- 例如：`TXN_ORDER_SUBMIT`、`TXN_PAY_CONFIRM`、`TXN_REFUND_APPLY`

---

## 参考资料

- 组合服务定义（PCS）请参考 [metadata-services](../metadata-services/SKILL.md)
- 错误码定义请参考 [metadata-basic-types](../metadata-basic-types/SKILL.md)
