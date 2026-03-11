#!/usr/bin/env python
"""
find_services_ref.py — 在工作空间下递归扫描所有 *.pbs.xml / *.pcs.xml 服务接口文件，
根据 service 的 id（英文）或 longname（中文）匹配，返回服务引用信息。

用法：
  python find_services_ref.py <workspace> <query1> [<query2> ...]

参数：
  workspace    - 工作空间根目录（绝对路径）
  query        - 一个或多个查询关键词（英文匹配 service id，中文匹配 service longname）

输出（JSON 格式，数组）：
  [
    {
      "found": true,
      "query": "福费延账务处理",
      "serviceTypeId": "FtAcctgDealPbsSvtp",
      "serviceId": "FtAcctgDealPbs",
      "serviceName": "ftAcctgDeal",
      "serviceLongname": "福费延账务处理",
      "filePath": "ccbs-loan-impl/loan-pbs-api/src/main/resources/api/servicetype/ft/FtAcctgDeal.pbs.xml",
      "serviceKind": "pbs"
    }
  ]

示例：
  python find_services_ref.py /Users/xxx/project 福费延账务处理
  python find_services_ref.py /Users/xxx/project FtAcctgDealPbs OrderSubmitPcs
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


def _scan_service_files(workspace: Path) -> list:
    """
    在工作空间下递归扫描所有 *.pbs.xml 和 *.pcs.xml 文件，
    解析出所有 service 信息。
    """
    all_services = []
    scanned_files = 0

    for xml_file in workspace.rglob("*"):
        if "target" in xml_file.parts:
            continue

        if xml_file.name.endswith(".pbs.xml"):
            svc_kind = "pbs"
        elif xml_file.name.endswith(".pcs.xml"):
            svc_kind = "pcs"
        else:
            continue

        scanned_files += 1

        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            if root.tag != "serviceType":
                continue

            service_type_id = root.get("id", "")

            for svc in root.findall("service"):
                svc_id = svc.get("id", "")
                svc_name = svc.get("name", "")
                svc_longname = svc.get("longname", "")

                rel_path = str(xml_file.relative_to(workspace))

                all_services.append({
                    "serviceTypeId": service_type_id,
                    "serviceId": svc_id,
                    "serviceName": svc_name,
                    "serviceLongname": svc_longname,
                    "filePath": rel_path,
                    "serviceKind": svc_kind
                })

        except ET.ParseError:
            continue
        except Exception:
            continue

    return all_services, scanned_files


def _match_services(all_services: list, query: str) -> list:
    """
    根据查询关键词匹配 service。
    中文 → 匹配 service longname；英文 → 匹配 service id。
    """
    matches = []
    is_cn = _is_chinese(query)

    for svc in all_services:
        if is_cn:
            if svc["serviceLongname"] == query:
                matches.append(svc)
        else:
            if svc["serviceId"] == query:
                matches.append(svc)

    return matches


def find_services_ref(workspace: str, queries: list) -> list:
    """
    在工作空间下递归搜索所有 *.pbs.xml / *.pcs.xml 文件，
    按查询关键词匹配并返回结果列表。
    """
    workspace_path = Path(workspace).resolve()
    if not workspace_path.exists():
        return [{
            "found": False,
            "query": q,
            "message": f"工作空间目录不存在: {workspace_path}"
        } for q in queries]

    all_services, scanned_files = _scan_service_files(workspace_path)

    if not all_services:
        return [{
            "found": False,
            "query": q,
            "scannedFiles": scanned_files,
            "message": f"在 {workspace_path} 下未找到任何服务接口（共扫描 {scanned_files} 个 .pbs.xml/.pcs.xml 文件）"
        } for q in queries]

    results = []
    for query in queries:
        matches = _match_services(all_services, query)

        if len(matches) == 0:
            results.append({
                "found": False,
                "query": query,
                "scannedFiles": scanned_files,
                "scannedServices": len(all_services),
                "message": f"未找到匹配 '{query}' 的服务（共扫描 {scanned_files} 个文件，{len(all_services)} 个 service）"
            })
        elif len(matches) == 1:
            result = matches[0].copy()
            result["found"] = True
            result["query"] = query
            results.append(result)
        else:
            results.append({
                "found": True,
                "query": query,
                "multiple": True,
                "candidates": matches,
                "message": f"找到 {len(matches)} 个匹配 '{query}' 的服务"
            })

    return results


def main():
    parser = argparse.ArgumentParser(
        description="在工作空间下递归扫描所有 *.pbs.xml / *.pcs.xml 文件，按英文 id 或中文 longname 匹配服务"
    )
    parser.add_argument("workspace", help="工作空间根目录（绝对路径）")
    parser.add_argument("queries", nargs="+", help="查询关键词（英文匹配 service id，中文匹配 service longname）")

    args = parser.parse_args()

    results = find_services_ref(args.workspace, args.queries)
    print(json.dumps(results, ensure_ascii=False, indent=2))

    all_found = all(r.get("found", False) for r in results)
    sys.exit(0 if all_found else 1)


if __name__ == "__main__":
    main()
