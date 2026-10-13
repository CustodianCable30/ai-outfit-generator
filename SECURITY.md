# Security Policy

## Supported versions

| Version | Supported |
| ------- | --------- |
| 0.4.x   | yes       |
| 0.3.x   | security only |
| < 0.3   | no        |

## Reporting a vulnerability

Email `security@ai-outfit-generator.dev` with a description, reproduction
steps, and the affected version. Do not open a public issue for security bugs.
We aim to respond within 72 hours.

## Scope

In scope:
- Arbitrary file write via the wardrobe import path
- Prompt injection in the styling engine that escapes into the render pipeline
- Local privilege escalation via the updater service
- Deserialization bugs in `services/wardrobe_store.py`

Out of scope:
- Attacks requiring physical access to the machine
- Model output quality complaints
- Third-party ONNX runtime CVEs (report upstream)

## Hardening notes

- All user-supplied paths are validated with `utils.paths.safe_join`.
- The updater verifies a detached signature before applying a patch.
- Wardrobe DB is opened with `check_same_thread=False` and a lock; do not
  remove the lock without a concurrency review.