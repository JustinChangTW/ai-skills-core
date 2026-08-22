#!/usr/bin/env python3
"""Fast probe for MCP Streamable HTTP endpoints.

Usage:
  python scripts/probe_streamable_http.py "http://127.0.0.1:9091/mcp"
  python scripts/probe_streamable_http.py "http://127.0.0.1:9091" --pretty
  python scripts/probe_streamable_http.py "http://127.0.0.1:9091/mcp" --bearer-token xxx
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


DEFAULT_VERSIONS = ["2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05"]


def _header_lookup(headers: dict[str, str], name: str) -> str | None:
    target = name.lower()
    for key, value in headers.items():
        if key.lower() == target:
            return value
    return None


def _read_http_error(exc: urllib.error.HTTPError) -> tuple[int, dict[str, str], str]:
    return exc.code, dict(exc.headers.items()), exc.read().decode("utf-8", errors="replace")


def _request_json(
    method: str,
    url: str,
    *,
    headers: dict[str, str] | None = None,
    payload: dict[str, Any] | None = None,
    timeout: float = 10.0,
) -> tuple[int, dict[str, str], str]:
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers or {}, method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, dict(response.headers.items()), response.read().decode(
                "utf-8", errors="replace"
            )
    except urllib.error.HTTPError as exc:
        return _read_http_error(exc)


def _candidate_endpoints(raw_url: str) -> list[str]:
    parsed = urllib.parse.urlparse(raw_url)
    if not parsed.scheme or not parsed.netloc:
        raise ValueError(f"Invalid URL: {raw_url}")
    exact = raw_url.rstrip("/")
    candidates = [exact]
    path = parsed.path.rstrip("/")
    if path == "":
        candidates.append(exact + "/mcp")
    elif path != "/mcp" and not path.endswith("/mcp"):
        candidates.append(exact + "/mcp")
    deduped: list[str] = []
    for item in candidates:
        if item not in deduped:
            deduped.append(item)
    return deduped


def _classify_error(status: int, body_text: str) -> str:
    try:
        body = json.loads(body_text) if body_text else {}
    except json.JSONDecodeError:
        body = {}
    error_name = body.get("error")
    if status == 401:
        return "auth_required"
    if error_name == "protocol_version_mismatch":
        return "protocol_version_mismatch"
    if error_name == "session_not_found":
        return "session_not_found"
    if status in (404, 405):
        return "wrong_endpoint_or_non_streamable"
    if status == 406:
        return "not_acceptable"
    if status >= 500:
        return "server_error"
    return "request_failed"


def _try_initialize(
    endpoint: str,
    *,
    versions: list[str],
    bearer_token: str | None,
    timeout: float,
) -> dict[str, Any]:
    attempts: list[dict[str, Any]] = []
    for version in versions:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "MCP-Protocol-Version": version,
        }
        if bearer_token:
            headers["Authorization"] = f"Bearer {bearer_token}"
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {"protocolVersion": version},
        }
        status, response_headers, body_text = _request_json(
            "POST", endpoint, headers=headers, payload=payload, timeout=timeout
        )
        attempt: dict[str, Any] = {
            "endpoint": endpoint,
            "version": version,
            "status": status,
            "response_headers": response_headers,
        }
        try:
            attempt["body"] = json.loads(body_text) if body_text else None
        except json.JSONDecodeError:
            attempt["body_text"] = body_text
        attempts.append(attempt)
        if status == 200:
            return {
                "ok": True,
                "attempts": attempts,
                "initialize": attempt,
                "session_id": _header_lookup(response_headers, "Mcp-Session-Id"),
                "protocol_version": _header_lookup(response_headers, "MCP-Protocol-Version")
                or (attempt.get("body") or {}).get("result", {}).get("protocolVersion"),
            }
        if _classify_error(status, body_text) != "protocol_version_mismatch":
            break
    return {"ok": False, "attempts": attempts}


def _call_tools_list(
    endpoint: str,
    *,
    session_id: str,
    protocol_version: str,
    bearer_token: str | None,
    timeout: float,
) -> dict[str, Any]:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Mcp-Session-Id": session_id,
        "MCP-Protocol-Version": protocol_version,
    }
    if bearer_token:
        headers["Authorization"] = f"Bearer {bearer_token}"
    payload = {"jsonrpc": "2.0", "id": 2, "method": "tools/list"}
    status, response_headers, body_text = _request_json(
        "POST", endpoint, headers=headers, payload=payload, timeout=timeout
    )
    try:
        body = json.loads(body_text) if body_text else None
    except json.JSONDecodeError:
        body = None
    return {
        "status": status,
        "response_headers": response_headers,
        "body": body,
        "body_text": None if body is not None else body_text,
    }


def _probe_root_descriptor(raw_url: str, timeout: float) -> dict[str, Any] | None:
    parsed = urllib.parse.urlparse(raw_url)
    root_url = urllib.parse.urlunparse((parsed.scheme, parsed.netloc, "/", "", "", ""))
    status, headers, body_text = _request_json("GET", root_url, timeout=timeout)
    try:
        body = json.loads(body_text) if body_text else None
    except json.JSONDecodeError:
        body = None
    if status == 200 and isinstance(body, dict):
        return {"url": root_url, "status": status, "headers": headers, "body": body}
    return None


def probe(raw_url: str, *, bearer_token: str | None, timeout: float, versions: list[str]) -> dict[str, Any]:
    results: dict[str, Any] = {
        "ok": False,
        "input_url": raw_url,
        "candidate_endpoints": _candidate_endpoints(raw_url),
    }
    for endpoint in results["candidate_endpoints"]:
        initialize_result = _try_initialize(
            endpoint, versions=versions, bearer_token=bearer_token, timeout=timeout
        )
        if not initialize_result["ok"]:
            results.setdefault("failed_initialize_attempts", []).extend(initialize_result["attempts"])
            continue

        initialize = initialize_result["initialize"]
        init_body = initialize.get("body") or {}
        tool_result = _call_tools_list(
            endpoint,
            session_id=initialize_result["session_id"],
            protocol_version=initialize_result["protocol_version"],
            bearer_token=bearer_token,
            timeout=timeout,
        )
        tool_body = tool_result.get("body") or {}
        tools = tool_body.get("result", {}).get("tools", [])
        results.update(
            {
                "ok": tool_result["status"] == 200,
                "resolved_endpoint": endpoint,
                "session_id": initialize_result["session_id"],
                "protocol_version": initialize_result["protocol_version"],
                "server_info": init_body.get("result", {}).get("serverInfo"),
                "capabilities": init_body.get("result", {}).get("capabilities"),
                "dependencies_tools": init_body.get("result", {}).get("dependencies", {}).get("tools"),
                "initialize": initialize,
                "tools_list": tool_result,
                "tools_count": len(tools),
                "tool_names": [tool.get("name") for tool in tools],
                "tools": tools,
            }
        )
        return results

    root_descriptor = _probe_root_descriptor(raw_url, timeout)
    if root_descriptor is not None:
        results["root_descriptor"] = root_descriptor
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="Probe an MCP Streamable HTTP endpoint")
    parser.add_argument("url", help="Target URL, ideally the exact /mcp endpoint")
    parser.add_argument("--bearer-token", help="Optional bearer token for Authorization header")
    parser.add_argument("--timeout", type=float, default=10.0, help="Request timeout in seconds")
    parser.add_argument(
        "--versions",
        default=",".join(DEFAULT_VERSIONS),
        help="Comma-separated protocol versions to try in order",
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON output")
    args = parser.parse_args()

    versions = [item.strip() for item in args.versions.split(",") if item.strip()]
    try:
        result = probe(
            args.url,
            bearer_token=args.bearer_token,
            timeout=args.timeout,
            versions=versions,
        )
    except Exception as exc:
        result = {"ok": False, "input_url": args.url, "fatal_error": repr(exc)}

    dump = json.dumps(result, ensure_ascii=False, indent=2 if args.pretty else None)
    sys.stdout.write(dump + "\n")
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
