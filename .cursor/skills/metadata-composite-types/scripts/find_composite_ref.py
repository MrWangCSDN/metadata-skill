#!/usr/bin/env python
"""
find_composite_ref.py — 在指定目录下搜索 *.c_schema.xml 文件，
根据 complexType 的 longname（或 id）匹配，返回引用所需的信息。

用法：
  python find_composite_ref.py <search_dir> <longname> [--id <complexTypeId>] [--workspace <项目根目录>]

参数：
  search_dir   - 搜索根目录（建议使用绝对路径，如 /path/to/project/loan-resources/src/main/resources/type）
  longname     - 要匹配的 complexType 中文名（longname 属性值）
  --id         - 可选，直接按 complexType id 匹配
  --workspace  - 可选，项目根目录绝对路径；传入后若 search_dir 为相对路径则自动解析

输出（JSON 格式）：
  找到时：
    {
      "found": true,
      "schemaId": "GuaranteeType",
      "complexTypeId": "GrntRcvCxlClmPojo",
      "filePath": "loan-resources/src/main/resources/type/GuaranteeType.c_schema.xml",
      "type": "GuaranteeType.GrntRcvCxlClmPojo"
    }
  未找到时：
    {
      "found": false,
      "searchDir": "<search_dir>",
      "longname": "<longname>",
      "message": "在 <search_dir> 下未找到 longname='<longname>' 的 complexType"
    }

示例（推荐使用绝对路径）：
  python find_composite_ref.py /path/to/metadata-skill/loan-resources/src/main/resources/type 保函收到撤销索偿
  python find_composite_ref.py loan-resources/src/main/resources/type 保函收到撤销索偿 --workspace /path/to/metadata-skill
"""

import sys
import os
import json
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path


def _resolve_search_dir(search_dir: str, workspace: str = None) -> Path:
    """
    解析搜索目录为绝对路径。
    - 若 search_dir 已是绝对路径且存在，直接使用
    - 若 search_dir 不存在且 workspace 已指定，尝试 workspace/search_dir
    - 若 search_dir 不存在且未指定 workspace，尝试从脚本位置推断项目根目录
    """
    path = Path(search_dir)
    if path.is_absolute() and path.exists():
        return path.resolve()
    if path.is_absolute():
        return path.resolve()  # 即使不存在也返回，由调用方处理

    # 相对路径：需要 workspace 或自动推断
    workspace_path = None
    if workspace:
        workspace_path = Path(workspace).resolve()
    else:
        # 从脚本位置推断：scripts -> metadata-composite-types -> skills -> .cursor -> 项目根
        script_dir = Path(__file__).resolve().parent
        skill_dir = script_dir.parent
        if skill_dir.name == "metadata-composite-types":
            skills_dir = skill_dir.parent
            if skills_dir.name == "skills":
                cursor_dir = skills_dir.parent
                if cursor_dir.name == ".cursor":
                    workspace_path = cursor_dir.parent

    if workspace_path and workspace_path.exists():
        return (workspace_path / search_dir).resolve()

    # 无 workspace 或无法推断：相对路径按 cwd 解析
    return Path(search_dir).resolve()


def find_composite_ref(search_dir: str, longname: str, complex_type_id: str = None, workspace: str = None) -> dict:
    """
    在 search_dir 目录（含子目录）下搜索所有 *.c_schema.xml，
    找到 complexType 的 longname 或 id 匹配的条目，返回引用信息。
    """
    search_path = _resolve_search_dir(search_dir, workspace)
    if not search_path.exists():
        return {
            "found": False,
            "searchDir": str(search_path),
            "longname": longname,
            "message": f"搜索目录不存在: {search_path}"
        }

    xml_files = list(search_path.rglob("*.c_schema.xml"))
    if not xml_files:
        return {
            "found": False,
            "searchDir": str(search_path),
            "longname": longname,
            "message": f"在 {search_path} 下未找到任何 *.c_schema.xml 文件"
        }

    candidates = []

    for xml_file in xml_files:
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            # 获取 schema 标签的 id
            schema_id = root.get("id", "")
            if not schema_id:
                continue

            # 遍历所有 complexType
            for ct in root.findall("complexType"):
                ct_id = ct.get("id", "")
                ct_longname = ct.get("longname", "")

                matched = False
                if longname and ct_longname == longname:
                    matched = True
                if complex_type_id and ct_id == complex_type_id:
                    matched = True

                if matched:
                    candidates.append({
                        "found": True,
                        "schemaId": schema_id,
                        "complexTypeId": ct_id,
                        "complexTypeLongname": ct_longname,
                        "filePath": str(xml_file),
                        "type": f"{schema_id}.{ct_id}"
                    })

        except ET.ParseError as e:
            # XML 解析失败，跳过该文件
            continue
        except Exception:
            continue

    if len(candidates) == 1:
        return candidates[0]

    if len(candidates) > 1:
        # 多个匹配，返回所有候选供用户确认
        return {
            "found": True,
            "multiple": True,
            "candidates": candidates,
            "message": f"找到 {len(candidates)} 个匹配，请确认使用哪一个"
        }

    return {
        "found": False,
        "searchDir": str(search_path),
        "longname": longname,
        "scannedFiles": len(xml_files),
        "message": f"在 {search_path} 下未找到 longname='{longname}' 的 complexType（共扫描 {len(xml_files)} 个文件）"
    }


def main():
    parser = argparse.ArgumentParser(
        description="搜索 c_schema.xml 中的 complexType，返回引用信息"
    )
    parser.add_argument("search_dir", help="搜索根目录路径（建议使用绝对路径）")
    parser.add_argument("longname", nargs="?", default="", help="complexType 中文名（longname）")
    parser.add_argument("--id", dest="complex_type_id", default=None, help="complexType 英文 id")
    parser.add_argument("--workspace", dest="workspace", default=None,
                        help="项目根目录绝对路径；传入后若 search_dir 为相对路径则自动解析")

    args = parser.parse_args()

    if not args.longname and not args.complex_type_id:
        print(json.dumps({
            "found": False,
            "message": "必须提供 longname 或 --id 参数"
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    result = find_composite_ref(args.search_dir, args.longname, args.complex_type_id, args.workspace)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    sys.exit(0 if result.get("found") else 1)


if __name__ == "__main__":
    main()
