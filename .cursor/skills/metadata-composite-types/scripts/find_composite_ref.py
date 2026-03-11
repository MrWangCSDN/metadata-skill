#!/usr/bin/env python
"""
find_composite_ref.py — 在工作空间下递归扫描所有 *.c_schema.xml 文件，
根据 complexType 的 longname（中文）或 id（英文）匹配，返回引用所需的信息。

自动判断查询词语言：包含中文字符则按 longname 匹配，纯英文则按 complexType id 匹配。
结果会按 schemaId + complexTypeId 去重，去重后若仍有多条记录则全部返回供用户选择。

用法：
  python find_composite_ref.py <workspace> <query>

参数：
  workspace    - 工作空间根目录（绝对路径）
  query        - 查询关键词（中文匹配 complexType longname，英文匹配 complexType id）

输出（JSON 格式）：
  找到唯一匹配时：
    {
      "found": true,
      "query": "保函收到撤销索偿",
      "schemaId": "GuaranteeType",
      "complexTypeId": "GrntRcvCxlClmPojo",
      "complexTypeLongname": "保函收到撤销索偿",
      "filePath": "ccbs-loan-impl/loan-resources/src/main/resources/type/GuaranteeType.c_schema.xml",
      "type": "GuaranteeType.GrntRcvCxlClmPojo"
    }
  去重后多个匹配时：
    {
      "found": true,
      "query": "...",
      "multiple": true,
      "candidates": [...],
      "message": "找到 N 个匹配（已去重），请确认使用哪一个"
    }
  未找到时：
    {
      "found": false,
      "query": "...",
      "scannedFiles": 10,
      "message": "在 ... 下未找到匹配 '...' 的 complexType（共扫描 10 个文件）"
    }

示例：
  python find_composite_ref.py /Users/xxx/project 保函收到撤销索偿
  python find_composite_ref.py /Users/xxx/project GrntRcvCxlClmPojo
"""

import sys
import json
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path


def _is_chinese(text: str) -> bool:
    """判断字符串是否包含中文字符。"""
    for ch in text:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def _deduplicate(candidates: list) -> list:
    """按 schemaId + complexTypeId 去重。"""
    seen = set()
    result = []
    for c in candidates:
        key = (c["schemaId"], c["complexTypeId"])
        if key not in seen:
            seen.add(key)
            result.append(c)
    return result


def find_composite_ref(workspace: str, query: str) -> dict:
    """
    在工作空间下递归扫描所有 *.c_schema.xml，
    按中文 longname 或英文 id 匹配 complexType，返回引用信息。
    """
    workspace_path = Path(workspace).resolve()
    if not workspace_path.exists():
        return {
            "found": False,
            "query": query,
            "message": f"工作空间目录不存在: {workspace_path}"
        }

    xml_files = list(workspace_path.rglob("*.c_schema.xml"))
    if not xml_files:
        return {
            "found": False,
            "query": query,
            "scannedFiles": 0,
            "message": f"在 {workspace_path} 下未找到任何 *.c_schema.xml 文件"
        }

    is_cn = _is_chinese(query)
    candidates = []

    for xml_file in xml_files:
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            schema_id = root.get("id", "")
            if not schema_id:
                continue

            for ct in root.findall("complexType"):
                ct_id = ct.get("id", "")
                ct_longname = ct.get("longname", "")

                matched = False
                if is_cn and ct_longname == query:
                    matched = True
                elif not is_cn and ct_id == query:
                    matched = True

                if matched:
                    rel_path = str(xml_file.relative_to(workspace_path))
                    candidates.append({
                        "found": True,
                        "query": query,
                        "schemaId": schema_id,
                        "complexTypeId": ct_id,
                        "complexTypeLongname": ct_longname,
                        "filePath": rel_path,
                        "type": f"{schema_id}.{ct_id}"
                    })

        except ET.ParseError:
            continue
        except Exception:
            continue

    candidates = _deduplicate(candidates)

    if len(candidates) == 1:
        return candidates[0]

    if len(candidates) > 1:
        return {
            "found": True,
            "query": query,
            "multiple": True,
            "candidates": candidates,
            "message": f"找到 {len(candidates)} 个匹配（已去重），请确认使用哪一个"
        }

    return {
        "found": False,
        "query": query,
        "scannedFiles": len(xml_files),
        "message": f"在 {workspace_path} 下未找到匹配 '{query}' 的 complexType（共扫描 {len(xml_files)} 个文件）"
    }


def main():
    parser = argparse.ArgumentParser(
        description="在工作空间下递归扫描所有 *.c_schema.xml，按中文 longname 或英文 id 匹配 complexType"
    )
    parser.add_argument("workspace", help="工作空间根目录（绝对路径）")
    parser.add_argument("query", help="查询关键词（中文匹配 longname，英文匹配 complexType id）")

    args = parser.parse_args()

    result = find_composite_ref(args.workspace, args.query)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    sys.exit(0 if result.get("found") else 1)


if __name__ == "__main__":
    main()
