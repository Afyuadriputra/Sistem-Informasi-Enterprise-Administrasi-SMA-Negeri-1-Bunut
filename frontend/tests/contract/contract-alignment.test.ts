import { describe, it, expect } from "vitest";
import * as fs from "fs";
import * as path from "path";
import type { paths, operations } from "@/types/api.generated";

describe("OpenAPI v1.1.0 Contract Alignment Verification", () => {
  const contractPath = path.resolve(__dirname, "../../../contracts/openapi.v1.yaml");
  const contractContent = fs.readFileSync(contractPath, "utf-8");

  // Parse all operations from openapi.v1.yaml
  const lines = contractContent.split("\n");
  const contractOperations: Array<{
    path: string;
    method: string;
    operationId: string;
  }> = [];

  let currentPath = "";
  let currentMethod = "";

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i].replace(/\r$/, "");

    // Detect path line (e.g. "  /auth/login:")
    const pathMatch = line.match(/^  (\/[a-zA-Z0-9_\-\/{}\.]+):$/);
    if (pathMatch) {
      currentPath = pathMatch[1];
      continue;
    }

    // Detect HTTP method (e.g. "    get:", "    post:", "    patch:")
    const methodMatch = line.match(/^    (get|post|put|patch|delete|options|head):$/);
    if (methodMatch) {
      currentMethod = methodMatch[1];
      continue;
    }

    // Detect operationId
    const opMatch = line.match(/^\s+operationId:\s*([a-zA-Z0-9_]+)/);
    if (opMatch) {
      contractOperations.push({
        path: currentPath,
        method: currentMethod,
        operationId: opMatch[1],
      });
    }
  }

  it("verifies the exact contract operation count is 49", () => {
    expect(contractOperations.length).toBe(49);
    const uniqueOpIds = new Set(contractOperations.map((o) => o.operationId));
    expect(uniqueOpIds.size).toBe(49);
  });

  it("verifies all operation IDs follow consistent camelCase naming convention", () => {
    const camelCaseRegex = /^[a-z][a-zA-Z0-9]*$/;
    contractOperations.forEach((op) => {
      expect(
        camelCaseRegex.test(op.operationId),
        `Operation ID '${op.operationId}' must be camelCase`,
      ).toBe(true);
    });
  });

  it("verifies the 3 previously missing operations exist in contract and are typed", () => {
    const getUserDetail = contractOperations.find(
      (o) => o.operationId === "getUserDetail",
    );
    expect(getUserDetail).toBeDefined();
    expect(getUserDetail?.path).toBe("/accounts/users/{id}");
    expect(getUserDetail?.method).toBe("get");

    const updateEnrollment = contractOperations.find(
      (o) => o.operationId === "updateEnrollment",
    );
    expect(updateEnrollment).toBeDefined();
    expect(updateEnrollment?.path).toBe("/master/enrollments/{id}");
    expect(updateEnrollment?.method).toBe("patch");

    const updateClassAssignment = contractOperations.find(
      (o) => o.operationId === "updateClassAssignment",
    );
    expect(updateClassAssignment).toBeDefined();
    expect(updateClassAssignment?.path).toBe("/master/assignments/{id}");
    expect(updateClassAssignment?.method).toBe("patch");
  });

  it("verifies student status enum contains exactly 4 valid states", () => {
    // Audit StudentStatusEnum in openapi
    const expectedEnum = ["AKTIF", "MUTASI_KELUAR", "LULUS", "NONAKTIF"];
    expectedEnum.forEach((status) => {
      expect(contractContent).toContain(`- ${status}`);
    });

    // Verify invalid legacy statuses are NOT in the contract enum
    expect(contractContent).not.toMatch(/StudentStatusEnum:[\s\S]*?- MUTASI\b(?!_KELUAR)/);
    expect(contractContent).not.toMatch(/StudentStatusEnum:[\s\S]*?- KELUAR\b/);
    expect(contractContent).not.toMatch(/StudentStatusEnum:[\s\S]*?- DO\b/);
  });

  it("verifies updateStudent uses PATCH method, not PUT", () => {
    const updateStudent = contractOperations.find(
      (o) => o.operationId === "updateStudent",
    );
    expect(updateStudent).toBeDefined();
    expect(updateStudent?.path).toBe("/master/students/{id}");
    expect(updateStudent?.method).toBe("patch");
  });

  it("verifies service types management operations are defined with correct methods", () => {
    const listServiceTypes = contractOperations.find(
      (o) => o.operationId === "listServiceTypes",
    );
    expect(listServiceTypes).toBeDefined();
    expect(listServiceTypes?.path).toBe("/administration/service-types");
    expect(listServiceTypes?.method).toBe("get");

    const createServiceType = contractOperations.find(
      (o) => o.operationId === "createServiceType",
    );
    expect(createServiceType).toBeDefined();
    expect(createServiceType?.path).toBe("/administration/service-types");
    expect(createServiceType?.method).toBe("post");

    const updateServiceType = contractOperations.find(
      (o) => o.operationId === "updateServiceType",
    );
    expect(updateServiceType).toBeDefined();
    expect(updateServiceType?.path).toBe("/administration/service-types/{id}");
    expect(updateServiceType?.method).toBe("patch");
  });

  it("verifies compile-time type safety of paths and operations generated interfaces", () => {
    // Type assertion checks: if types in api.generated.ts break, this test file fails at build
    type PathList = keyof paths;
    const testPath1: PathList = "/accounts/users/{id}";
    const testPath2: PathList = "/master/enrollments/{id}";
    const testPath3: PathList = "/master/assignments/{id}";
    const testPath4: PathList = "/administration/service-types/{id}";
    expect(testPath1).toBe("/accounts/users/{id}");
    expect(testPath2).toBe("/master/enrollments/{id}");
    expect(testPath3).toBe("/master/assignments/{id}");
    expect(testPath4).toBe("/administration/service-types/{id}");

    type OperationKeys = keyof operations;
    const op1: OperationKeys = "getUserDetail";
    const op2: OperationKeys = "updateEnrollment";
    const op3: OperationKeys = "updateClassAssignment";
    const op4: OperationKeys = "updateStudent";
    const op5: OperationKeys = "updateServiceType";
    expect(op1).toBe("getUserDetail");
    expect(op2).toBe("updateEnrollment");
    expect(op3).toBe("updateClassAssignment");
    expect(op4).toBe("updateStudent");
    expect(op5).toBe("updateServiceType");
  });
});
