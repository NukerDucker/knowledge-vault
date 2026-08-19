# nacl-nextpath-x

## Vault Notes
- `.github/hooks/rtk-rewrite.json`: PreToolUse runs `rtk hook copilot` from repo root.
- `.github/hooks/memory.json`: sessionStart loads vault state into `.ai/context.md`; sessionEnd saves `.ai/session-summary.md`, `.ai/state-update.md`, and `.ai/new-decisions.md` back to KnowledgeVault.
- `scripts/vault-init.sh`: one-time setup for `~/KnowledgeVault/02-programming/<project>` with `state.md`, `decisions.md`, and `sessions/`.
- `scripts/session-start.sh`: reads vault into `.ai/context.md`.
- `scripts/session-end.sh`: writes session notes/state/decisions into vault and cleans `.ai/context.md`.

## Session End
- Root `.github` hooks read and saved.
- Home KnowledgeVault note created at `~/KnowledgeVault/02-programming/nacl-nextpath-x.md`.
- API/backend fixes landed earlier: onboarding now uses `onboarded_at`, dev seeds mark users onboarded, and `year` can derive from `student_id`.
- Backend build checked clean with `go build ./...`.
