# src/parser.py
import json
import yaml
from pathlib import Path
from typing import Dict, Any, List
from logger import get_logger
# 
log = get_logger(__name__)

ALLOWED_METHODS = {'GET','POST','PUT','DELETE','PATCH','HEAD','OPTIONS','TRACE'}

def parse_openapi_yaml(path: Path) -> Dict[str, Any]:
    with path.open('r', encoding='utf-8') as f:
        spec = yaml.safe_load(f)

    info = spec.get('info', {})
    title = info.get('title') or path.stem
    version = info.get('version', 'unknown')

    components = spec.get('components', {}) or {}
    sec_schemes = components.get('securitySchemes', {}) or {}
    top_security = spec.get('security', []) or []

    auth_methods = sorted(sec_schemes.keys()) if isinstance(sec_schemes, dict) else []
    has_global_security = bool(top_security)

    paths = spec.get('paths', {}) or {}
    endpoints: List[Dict[str, Any]] = []
    method_count: Dict[str, int] = {}

    for endpoint, ops in paths.items():
        if not isinstance(ops, dict):
            continue
        for method, op in ops.items():
            m = method.upper()
            if m not in ALLOWED_METHODS or not isinstance(op, dict):
                continue
            method_count[m] = method_count.get(m, 0) + 1

            tags = op.get('tags', []) or []
            summary = op.get('summary')
            description = op.get('description')

            req_body = op.get('requestBody')
            has_request = req_body is not None

            responses = op.get('responses', {}) or {}
            response_codes = sorted(responses.keys())
            has_response = bool(responses)

            endpoints.append({
                "path": endpoint,
                "method": m,
                "tags": tags,
                "summary": summary,
                "description": description,
                "response_codes": response_codes,
                "has_request": has_request,
                "has_response": has_response,
            })

    endpoints_with_response = sum(1 for e in endpoints if e["has_response"])
    endpoints_without_response = len(endpoints) - endpoints_with_response

    metadata = {
        "file": str(path),
        "title": title,
        "version": version,
        "auth_methods": auth_methods,
        "has_global_security": has_global_security,
        "method_count": method_count,
        "endpoints": endpoints,
        "coverage": {
            "total_endpoints": len(endpoints),
            "endpoints_with_response": endpoints_with_response,
            "endpoints_without_response": endpoints_without_response,
        },
        "basic_services": sorted({t for e in endpoints for t in e["tags"]})
    }

    log.info("parsed_openapi", extra={
        "event": "parsed_openapi",
        "file": str(path),
        "title": title,
        "endpoint_count": len(endpoints),
        "auth_methods": auth_methods
    })
    return metadata

def parse_many(input_dir: Path, limit: int = 5) -> List[Dict[str, Any]]:
    files = sorted(input_dir.glob("*.yaml"))[:limit]
    results = []
    for p in files:
        try:
            results.append(parse_openapi_yaml(p))
        except Exception as exc:
            log.error("parse_error", extra={
                "event": "parse_error",
                "file": str(p),
                "exception": exc.__class__.__name__,
                "message": str(exc),
            })
    return results

def write_outputs(metadata_list: List[Dict[str, Any]], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "metadata.json").write_text(json.dumps(metadata_list, indent=2), encoding="utf-8")

    total_methods: Dict[str, int] = {}
    total_endpoints = 0
    with_resp = 0
    without_resp = 0
    auth = set()
    services = set()

    for m in metadata_list:
        for k, v in m["method_count"].items():
            total_methods[k] = total_methods.get(k, 0) + v
        total_endpoints += m["coverage"]["total_endpoints"]
        with_resp += m["coverage"]["endpoints_with_response"]
        without_resp += m["coverage"]["endpoints_without_response"]
        for a in m["auth_methods"]:
            auth.add(a)
        for s in m["basic_services"]:
            services.add(s)

    summary = {
        "http_method_count": total_methods,
        "total_endpoints": total_endpoints,
        "endpoints_with_response": with_resp,
        "endpoints_without_response": without_resp,
        "auth_methods": sorted(auth),
        "basic_services": sorted(services),
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    log.info("write_outputs", extra={"event": "write_outputs", "summary": summary})

if __name__ == "__main__":
    base = Path(__file__).resolve().parents[1]
    input_dir = base / "data" / "openapi"
    out_dir = base / "outputs"
    metas = parse_many(input_dir, limit=5)
    write_outputs(metas, out_dir)