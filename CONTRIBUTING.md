# Contributing

- Make small, reviewable changes.
- Keep API, agent runtime, policy, and execution boundaries explicit.
- Add tests for behavior changes and regression fixes.
- Record material architectural changes as ADRs.
- Never commit credentials, tokens, private keys, .env files, or customer data.
- Never weaken permission or sandbox controls to make a test pass.

Every PR should explain the change, related issue, validation commands/results, and security/privacy impact. Changes to authentication, authorization, file access, process/network execution, secrets, or isolation require explicit security review.

Use concise imperative commits, e.g. `feat(workspace): add repository import`.
