#!/usr/bin/env python3
"""Search the public arXiv Atom API and print Markdown or JSON results."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ATOM = "http://www.w3.org/2005/Atom"
OPEN_SEARCH = "http://a9.com/-/spec/opensearch/1.1/"
NS = {"a": ATOM}


def node_text(entry: ET.Element, name: str) -> str:
    node = entry.find(f"a:{name}", NS)
    return "" if node is None or node.text is None else " ".join(node.text.split())


def build_url(args: argparse.Namespace) -> str:
    params: dict[str, str] = {"max_results": str(args.max)}
    if args.id:
        params["id_list"] = args.id
    else:
        terms = []
        if args.query:
            terms.append(f"all:{args.query}")
        if args.author:
            terms.append(f"au:{args.author}")
        if args.category:
            terms.append(f"cat:{args.category}")
        if not terms:
            raise ValueError("Provide a query, --author, --category, or --id.")
        params["search_query"] = " AND ".join(terms)
    params["sortBy"] = {
        "relevance": "relevance",
        "date": "submittedDate",
        "updated": "lastUpdatedDate",
    }[args.sort]
    params["sortOrder"] = "descending"
    return "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)


def fetch(url: str) -> tuple[int, list[dict[str, object]]]:
    request = urllib.request.Request(url, headers={"User-Agent": "Codex-arXiv-research/1.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        root = ET.fromstring(response.read())
    total_node = root.find(f"{{{OPEN_SEARCH}}}totalResults")
    total = int(total_node.text) if total_node is not None and total_node.text else 0
    results = []
    for entry in root.findall("a:entry", NS):
        full_id = node_text(entry, "id").rsplit("/abs/", 1)[-1]
        base_id = re.sub(r"v\d+$", "", full_id)
        results.append(
            {
                "id": full_id,
                "title": node_text(entry, "title"),
                "authors": [node_text(author, "name") for author in entry.findall("a:author", NS)],
                "published": node_text(entry, "published")[:10],
                "updated": node_text(entry, "updated")[:10],
                "categories": [node.get("term", "") for node in entry.findall("a:category", NS)],
                "abstract": node_text(entry, "summary"),
                "abstract_url": f"https://arxiv.org/abs/{base_id}",
                "pdf_url": f"https://arxiv.org/pdf/{base_id}",
            }
        )
    return total, results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="?", help="Topic keywords")
    parser.add_argument("--author")
    parser.add_argument("--category")
    parser.add_argument("--id", help="One or more comma-separated arXiv IDs")
    parser.add_argument("--max", type=int, default=5, choices=range(1, 101), metavar="1-100")
    parser.add_argument("--sort", choices=("relevance", "date", "updated"), default="relevance")
    parser.add_argument("--format", choices=("markdown", "json"), default="markdown")
    args = parser.parse_args()
    try:
        total, results = fetch(build_url(args))
    except (ValueError, OSError, ET.ParseError) as exc:
        print(f"arXiv query failed: {exc}", file=sys.stderr)
        return 1
    if args.format == "json":
        print(json.dumps({"total": total, "results": results}, ensure_ascii=False, indent=2))
        return 0
    print(f"Found {total} results; showing {len(results)}.\n")
    for index, item in enumerate(results, 1):
        print(f"{index}. {item['title']}")
        print(f"   ID: {item['id']} | Published: {item['published']} | Updated: {item['updated']}")
        print(f"   Authors: {', '.join(item['authors'])}")
        print(f"   Categories: {', '.join(item['categories'])}")
        abstract = str(item["abstract"])
        print(f"   Abstract: {abstract[:500]}{'...' if len(abstract) > 500 else ''}")
        print(f"   Links: {item['abstract_url']} | {item['pdf_url']}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
