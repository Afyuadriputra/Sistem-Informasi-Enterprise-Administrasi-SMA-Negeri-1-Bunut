import hashlib
from pathlib import Path

import pytest
import yaml

from config.api import api


def test_openapi_contract_checksum():
    """Verify contracts/openapi.v1.yaml SHA-256 integrity."""
    contract_path = Path(__file__).resolve().parent.parent.parent / "contracts" / "openapi.v1.yaml"
    assert contract_path.exists(), f"Contract file not found at {contract_path}"

    sha256 = hashlib.sha256(contract_path.read_bytes()).hexdigest().upper()
    assert sha256 == "F1618EB80154D970F639A5617AD645D3A37D139A9CC6B90AFA8E4E054A10B72B"


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


def test_infrastructure_healthcheck_operation():
    """Verify healthcheck endpoint as an infrastructure operation outside domain operations."""
    ninja_schema = api.get_openapi_schema()
    health_op = None
    for path, path_item in ninja_schema["paths"].items():
        if path in ["/health", "/api/health"]:
            health_op = path_item.get("get")
            break

    assert health_op is not None, "Infrastructure health check endpoint must be registered in Ninja"
    assert "System" in health_op.get("tags", [])


def test_contract_semantic_error_envelope_spec():
    """Verify that OpenAPI ErrorEnvelope specification and Pydantic ErrorEnvelope schema match."""
    from apps.core.schemas import ErrorEnvelope

    contract_path = Path(__file__).resolve().parent.parent.parent / "contracts" / "openapi.v1.yaml"
    with open(contract_path, encoding="utf-8") as f:
        spec = yaml.safe_load(f)

    yaml_err = spec["components"]["schemas"]["ErrorEnvelope"]
    yaml_props = yaml_err["properties"]

    assert "code" in yaml_props
    assert "message" in yaml_props
    assert "details" in yaml_props
    assert "request_id" in yaml_props

    pydantic_fields = ErrorEnvelope.model_fields
    assert "code" in pydantic_fields
    assert "message" in pydantic_fields
    assert "details" in pydantic_fields
    assert "request_id" in pydantic_fields


def test_contract_multipart_and_binary_media_types():
    """Verify semantic content types for multipart upload and binary exports."""
    contract_path = Path(__file__).resolve().parent.parent.parent / "contracts" / "openapi.v1.yaml"
    with open(contract_path, encoding="utf-8") as f:
        spec = yaml.safe_load(f)

    paths = spec["paths"]

    # 1. Upload must be multipart/form-data
    upload_body = paths["/administration/requests/{id}/documents"]["post"]["requestBody"]
    assert "multipart/form-data" in upload_body["content"]

    # 2. Excel export must be application/vnd.openxmlformats-officedocument.spreadsheetml.sheet
    excel_res = paths["/reports/attendance.xlsx"]["get"]["responses"]["200"]
    assert "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" in excel_res["content"]

    # 3. PDF export must be application/pdf
    pdf_res = paths["/reports/administration.pdf"]["get"]["responses"]["200"]
    assert "application/pdf" in pdf_res["content"]


@pytest.mark.django_db
def test_runtime_error_envelope_conformance(client):
    """Verify that runtime errors strictly return the ErrorEnvelope structure."""
    # 1. 401 Unauthorized
    res401 = client.get("/api/auth/me")
    assert res401.status_code == 401
    body401 = res401.json()
    assert "code" in body401
    assert "message" in body401
    assert "request_id" in body401

    # 2. 404 Not Found
    res404 = client.get("/api/non-existent-endpoint")
    assert res404.status_code == 404

    # 3. 422 Unprocessable Entity (Invalid validation payload)
    res422 = client.post(
        "/api/auth/login",
        data={"invalid_field": "test"},
        content_type="application/json",
    )
    assert res422.status_code == 422
    body422 = res422.json()
    assert body422["code"] == "VALIDATION_ERROR"
    assert "message" in body422
    assert "details" in body422
    assert "request_id" in body422
