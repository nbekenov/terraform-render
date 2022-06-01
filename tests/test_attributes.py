import os
import sys
import json
import pytest

TESTCASES_LIST = ["complete-mssql", "complete-postgres", pytest.param("complete-oracle", marks=pytest.mark.xfail) ]

def parse_tf_plan(file_name):
    """Parse terraform plan file in json format
    """
    project_dir = os.path.dirname(os.path.realpath(__file__))
    tf_plan_data = {}
    try:
        with open(f"{project_dir}/../{file_name}") as tf_plan_file:
            tf_plan_data = json.load(tf_plan_file)
    except FileNotFoundError as fnf_err:
        sys.exit(f"{fnf_err}: terraform plan file not found")

    return tf_plan_data

# @pytest.mark.parametrize("case", TESTCASES_LIST)
# def test_multi_az_is_enabled(case):
#     tf_plan_data = parse_tf_plan(f"testcases/{case}/plan_formated.json")["planned_values"]["root_module"]

#     for child_module in tf_plan_data["child_modules"]:
#         if child_module["address"] == "module.db":
#             for module in child_module["child_modules"]:
#                 if  module["address"] == "module.db.module.db_instance":
#                     for resource in module["resources"]:
#                         if resource["type"] == "aws_db_instance":
#                             multi_az = resource["values"]["multi_az"]
#                             assert multi_az


@pytest.mark.parametrize("case", TESTCASES_LIST)
def test_multi_az_is_enabled(case):
    """Test that multi az is disabled by default
    """
    tf_plan_data = parse_tf_plan(f"testcases/{case}/plan_formated.json")
    for resource in tf_plan_data["resource_changes"]:
        if resource["type"] == "aws_db_instance":
            multi_az = resource["change"]["after"]["multi_az"]
            assert not multi_az