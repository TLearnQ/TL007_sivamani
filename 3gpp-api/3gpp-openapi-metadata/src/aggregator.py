# src/aggregator.py
from typing import List, Dict, Any
import json
from pathlib import Path
from logging_conf import get_logger

log = get_logger(__name__)

def aggregate(metadata_list: List[Dict[str, Any]]) -> Dict[str, Any]:
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
        auth.update(m["auth_methods"])
        services.update(m["basic_services"])

    return {
        "http_method_count": total_methods,
        "total_endpoints": total_endpoints,
        "endpoints_with_response": with_resp,
        "endpoints_without_response": without_resp,
        "auth_methods": sorted(auth),
        "basic_services": sorted(services),
    }

def write_summary(summary: Dict[str, Any], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    log.info("write_outputs", extra={"event":"write_outputs","summary":summary})