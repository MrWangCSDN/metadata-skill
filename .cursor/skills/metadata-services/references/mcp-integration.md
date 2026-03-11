# PBS/PCS 服务 MCP 集成说明

**服务名**：`dict-mcp-server`
**方法**：`getDictDefByLongNameList`

- 输入：字段中文名称数组，如 `["币种代码", "利息金额"]`
- 输出：`Map<中文名, 字段定义对象 | null>`
- `null` 表示未贯标，**禁止写入 XML**
- **调用时机**：创建或修改时，一次性批量查询所有普通字段（不含复合引用字段）

## 复合类型引用脚本

对 `[中文名]` 语法的字段，调用 `find_composite_ref.py` 脚本搜索：

```bash
python "{工作区根目录}/.speedstudio/skills/metadata-composite-types/scripts/find_composite_ref.py" "{搜索目录}" 中文名
```

搜索目录与领域对应：

| 领域 | 搜索目录 |
|------|---------|
| 存款 | `{工作区根目录}/dept-resources/src/main/resources/type` |
| 贷款 | `{工作区根目录}/loan-resources/src/main/resources/type` |
| 结算 | `{工作区根目录}/sett-resources/src/main/resources/type` |
| 公共 | `{工作区根目录}/comm-resources/src/main/resources/type` |
