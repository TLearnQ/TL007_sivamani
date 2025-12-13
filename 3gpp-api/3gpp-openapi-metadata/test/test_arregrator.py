# # tests/test_aggregator.py
# from src.aggregator import aggregate

# def test_aggregate_basic():
#     m1 = {
#         "method_count":{"GET":2,"POST":1},
#         "coverage":{"total_endpoints":3,"endpoints_with_response":3,"endpoints_without_response":0},
#         "auth_methods":["OAuth2"],
#         "basic_services":["Session","Policy"]
#     }
#     m2 = {
#         "method_count":{"GET":1,"DELETE":1},
#         "coverage":{"total_endpoints":2,"endpoints_with_response":1,"endpoints_without_response":1},
#         "auth_methods":["ApiKey"],
#         "basic_services":["Policy","Events"]
#     }
#     summary = aggregate([m1,m2])
#     assert summary["http_method_count"]["GET"] == 3
#     assert summary["endpoints_without_response"] == 1
#     assert "OAuth2" in summary["auth_methods"]
#     assert "Policy" in summary["basic_services"]