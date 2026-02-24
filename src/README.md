# src - Skill 案件来源目录

本目录用于存放 skill 的案件来源素材，包括真实业务案例、样本数据、参考文档等，
作为各元数据 skill 的输入来源和知识积累。

## 目录结构

```
src/
├── basic-types/          # 基础类型案件（枚举、字典、错误码、常量）
├── composite-types/      # 复合类型案件（表定义、自定义SQL）
├── components/           # 构件案件（PBCB/PBCP/PBCC/PBCT）
├── services/             # 服务案件（PCS组合服务/PBS基础服务）
└── transactions/         # 联机交易案件
```

## 使用说明

- 每个案件建议创建独立子目录，包含案件描述文件和相关素材
- 文件命名：`[业务域]-[案件简述]/`，例如 `order-submit/`
- 案件目录内可存放：原始需求文档、字段清单、参考样例等
