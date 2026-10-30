# Security Policy

Report exploitable vulnerabilities privately using GitHub private vulnerability reporting when enabled. Do not publish secrets, customer code, or proof-of-concept credentials.

Security invariants:
- No implicit host-wide access.
- Authorization is enforced server-side.
- Workspace boundaries are enforced by filesystem/OS controls, not prompts alone.
- Platform secrets are never exposed to untrusted code.
- Destructive or privileged actions require explicit authorization.
- Security events are logged without secret values.

Until a release policy exists, fixes target the active development branch.
