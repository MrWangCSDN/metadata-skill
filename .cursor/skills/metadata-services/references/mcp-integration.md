# PBS/PCS 服务 MCP 服务集成说明

## MCP 服务概述

**MCP 服务名称**：`dict-mcp-server`
**方法名**：`getDictDefByLongNameList`
**用途**：批量查询字段的元数据信息

## 接口规范

- **输入**：字段中文名称数组，如 `["币种代码", "利息金额"]`
- **输出**：`Map<中文名, 字段定义对象 | null>`，`null` 表示未贯标
- **调用时机**：创建或修改时，一次性批量查询所有普通字段

> ⛔ **强制规则：MCP 返回 null 的字段，禁止写入 XML。**

字段处理逻辑（普通字段、复合引用、数组字段）与 metadata-pbc、metadata-transactions 一致，详见其 MCP 集成文档。
