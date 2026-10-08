# Mobile Virtual Testing

Reusable mobile-device testing infrastructure for ChatGPT-directed software development.

## Mission

Provide a provider-neutral execution layer that can build, launch, interact with, visually inspect, and validate mobile applications using Android emulators and iOS simulators.

The governing principle is:

> Use deterministic software for execution. Use AI for judgment. Involve humans only when genuinely necessary.

## Architecture

```text
ChatGPT
   |
Orchestrator
   |
Mobile Testing Request
   |
Worker / Provider Adapter
   |
Android Emulator | iOS Simulator
   |
Evidence Bundle
   |
Deterministic Validation
   |
Bridge Continuation
```

GitHub is an integration and coordination surface, not a required execution provider.

## Repository boundaries

This repository owns reusable mobile-testing infrastructure. Application-specific code remains in application repositories. Deadshift will be the first acceptance workload, but this repository must remain reusable for future applications.

## Initial milestones

1. Define stable request and evidence contracts.
2. Implement a provider-neutral worker interface.
3. Add deterministic local/fake-provider qualification.
4. Add Android emulator execution.
5. Add iOS simulator execution.
6. Integrate standardized evidence with the Personal GitHub <-> ChatGPT bridge.
7. Run Deadshift as the first end-to-end acceptance test.
