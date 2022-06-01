import os
import sys
import json
import pytest
from deepdiff import DeepDiff


TESTCASES_LIST = ["complete-mssql", "complete-postgres", "complete-oracle"]

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

@pytest.mark.parametrize("case", TESTCASES_LIST)
def test_snapshots(case):
    """Compare terraform plan with the golden snapshot tf plan
    """
    tf_plan_data = parse_tf_plan(f"testcases/{case}/plan_formated.json")
    snapshot_plan = parse_tf_plan(f"snapshots/{case}/plan.json")

    diff = DeepDiff(tf_plan_data, snapshot_plan, ignore_order=True)
    assert not diff, f"difference in response: {diff}"

