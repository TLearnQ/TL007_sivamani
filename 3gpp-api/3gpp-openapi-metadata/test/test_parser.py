# # tests/test_parser.py
# from pathlib import Path
# from src.parse_openapi import parse_openapi_yaml

# def test_parse_minimal(tmp_path: Path):
#     yaml_text = """
# openapi: 3.0.3
# info:
#   title: Test API
#   version: v1
# paths:
#   /items:
#     get:
#       tags: [Inventory]
#       responses:
#         '200':
#           description: OK
# """
#     f = tmp_path / "api.yaml"
#     f.write_text(yaml_text, encoding="utf-8")
#     meta = parse_openapi_yaml(f)
#     assert meta["title"] == "Test API"
#     assert meta["coverage"]["total_endpoints"] == 1
#     assert meta["method_count"]["GET"] == 1
#     assert meta["basic_services"] == ["Inventory"]