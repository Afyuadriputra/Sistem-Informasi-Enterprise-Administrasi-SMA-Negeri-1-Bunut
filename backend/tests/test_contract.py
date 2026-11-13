import hashlib
from pathlib import Path

import yaml

from config.api import api


def test_openapi_contract_checksum():
    """Verify contracts/openapi.v1.yaml SHA-256 integrity."""
    contract_path = Path(__file__).resolve().parent.parent.parent / "contracts" / "openapi.v1.yaml"
    assert contract_path.exists(), f"Contract file not found at {contract_path}"

    sha256 = hashlib.sha256(contract_path.read_bytes()).hexdigest().upper()
    assert sha256 == "D3871BA834C17FC6DC49BB92F63391EB3EC63571E784A6623CE8E2A65CB52B9E"


def test_database_dbml_checksum():
    """Verify contracts/database.dbml SHA-256 integrity."""
    dbml_path = Path(__file__).resolve().parent.parent.parent / "contracts" / "database.dbml"
    assert dbml_path.exists(), f"DBML file not found at {dbml_path}"

    sha256 = hashlib.sha256(dbml_path.read_bytes()).hexdigest().upper()
    assert sha256 == "DA7B35DBBFC0DF1080DD40A93E4DB01D97CEB568EDF31EE3A97E1CAF723603B8"


def test_all_openapi_operations_implemented_in_ninja():
    """Verify that all 49 operations in contracts/openapi.v1.yaml are present in Django Ninja."""
    contract_path = Path(__file__).resolve().parent.parent.parent / "contracts" / "openapi.v1.yaml"
    with open(contract_path, encoding="utf-8") as f:
        yaml_schema = yaml.safe_load(f)

    ninja_schema = api.get_openapi_schema()

    ninja_ops = {}
    for path, path_item in ninja_schema["paths"].items():
        norm_path = path[4:] if path.startswith("/api") else path
        for method, op_data in path_item.items():
            if method.lower() in ["get", "post", "put", "patch", "delete"]:
                ninja_ops[(method.upper(), norm_path)] = op_data.get("operationId")

    yaml_ops = {}
    for path, path_item in yaml_schema["paths"].items():
        norm_path = path[4:] if path.startswith("/api") else path
        for method, op_data in path_item.items():
            if method.lower() in ["get", "post", "put", "patch", "delete"]:
                yaml_ops[(method.upper(), norm_path)] = op_data.get("operationId")

    assert len(yaml_ops) == 49, f"Expected 49 operations in OpenAPI contract, got {len(yaml_ops)}"

    missing_in_ninja = []
    mismatched_op_ids = []
    for (method, path), expected_op_id in yaml_ops.items():
        if (method, path) not in ninja_ops:
            missing_in_ninja.append(f"{method} {path}")
        elif ninja_ops[(method, path)] != expected_op_id:
            mismatched_op_ids.append(f"{method} {path}: expected {expected_op_id}, got {ninja_ops[(method, path)]}")

    assert not missing_in_ninja, f"Operations in OpenAPI missing from Ninja: {missing_in_ninja}"
    assert not mismatched_op_ids, f"Operation IDs mismatched between OpenAPI and Ninja: {mismatched_op_ids}"


def test_master_data_19_operations_complete():
    """Verify all 19 Master Data operations exist including PATCH lifecycle operations."""
    contract_path = Path(__file__).resolve().parent.parent.parent / "contracts" / "openapi.v1.yaml"
    with open(contract_path, encoding="utf-8") as f:
        yaml_schema = yaml.safe_load(f)

    master_ops = []
    for path, path_item in yaml_schema["paths"].items():
        if path.startswith("/master/"):
            for method in path_item:
                if method.lower() in ["get", "post", "put", "patch", "delete"]:
                    master_ops.append((method.upper(), path))

    assert len(master_ops) == 19, f"Expected 19 Master Data operations, found {len(master_ops)}"

    # Check specifically for DEC-TECH-16 PATCH operations
    expected_patches = [
        ("PATCH", "/master/academic-years/{id}"),
        ("PATCH", "/master/classes/{id}"),
        ("PATCH", "/master/employees/{id}"),
        ("PATCH", "/master/students/{id}"),
        ("PATCH", "/master/enrollments/{id}"),
        ("PATCH", "/master/assignments/{id}"),
    ]
    for method, path in expected_patches:
        assert (method, path) in master_ops, f"Missing master data PATCH operation: {method} {path}"
