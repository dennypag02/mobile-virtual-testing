# Architecture

## Design goal

Mobile Virtual Testing is a reusable execution module for autonomous software development. It is deliberately independent of both the application under test and the infrastructure provider.

## Control flow

1. An orchestrator produces a versioned test request.
2. A worker selects a provider adapter based on declared capabilities and policy.
3. The provider provisions or attaches to a virtual device.
4. The worker installs and launches the application.
5. Deterministic interaction steps are executed.
6. Evidence is captured during execution.
7. Deterministic validation produces a machine-readable result.
8. The evidence bundle is returned to the caller.
9. AI may inspect ambiguous visual or behavioral evidence only after deterministic execution is complete.

## Stable boundaries

### Request contract

A request describes:
- application artifact or build reference;
- platform and virtual-device requirements;
- deterministic interaction steps;
- required evidence;
- deterministic assertions;
- execution limits.

It does not contain provider-specific commands.

### Provider interface

A provider adapter owns:
- virtual-device provisioning;
- application installation;
- launch/stop lifecycle;
- deterministic input;
- screenshots and recordings;
- device logs;
- cleanup.

Provider adapters must not decide whether application behavior is correct.

### Evidence contract

Every run emits a standardized bundle containing:
- immutable request identity;
- provider and device metadata;
- execution timeline;
- step results;
- screenshots and optional video;
- application/device logs;
- deterministic assertion results;
- terminal run status.

## Initial providers

### fake

A deterministic in-process provider used to qualify contracts, orchestration, evidence generation, failure handling, and CI without a real mobile runtime.

### android

An Android Emulator / ADB adapter. The first production target should be compatible with common Linux or macOS execution environments.

### ios

An Apple Simulator / simctl adapter. This adapter requires macOS with Xcode and compatible simulator runtimes. The orchestration contract must not depend on whether the macOS host is GitHub-hosted, third-party, or user-owned.

## GitHub boundary

GitHub may:
- store source and contracts;
- invoke CI;
- transport artifacts and events;
- coordinate bridge continuation.

GitHub is not part of the provider contract and is not required by the worker API. A future scheduler or worker fleet must be able to submit the same request and consume the same evidence without GitHub Actions.

## AI boundary

AI is reserved for judgment, including:
- visual interpretation when deterministic assertions are insufficient;
- diagnosis after deterministic failure evidence exists;
- choosing the next development action.

AI must not replace deterministic lifecycle operations, input replay, evidence collection, cleanup, or schema validation.

## Acceptance strategy

1. Qualify the fake provider end to end.
2. Qualify Android with a purpose-built fixture app.
3. Qualify iOS with a purpose-built fixture app.
4. Prove provider interchangeability using identical logical test specifications.
5. Integrate bridge event publication.
6. Run Deadshift as the first independent application acceptance workload.
