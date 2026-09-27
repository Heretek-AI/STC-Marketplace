# Contributing (core team only)

Publishing to the marketplace requires core-team review. Community proposals
arrive as issues; only core-team PRs land.

## Pack format (mandatory)

Every `roles/<name>/` directory must contain:

1. `rolepack.yaml` — RolePack v2 (`name, version, tools ⊆ 15-tool catalog,
   skill_lockfile_hash, system_prompt, mcp_manifest, model_slot,
   harness_profile, spawns, output_schema`).
2. `rolepack.lock` — pinned hashes (`pack_hash` + per-asset sha256),
   verifiable with `verify_lock` (`--locked` semantics: any drift fails closed).
3. Emitted targets: `agents/<name>.md` (omp drop), `package.json` (base-pi
   shim), `.opencode/agents/<name>.md` (mirror) — each listing exactly the
   pack tools in front matter / `pi.tools`.
4. Provenance: every adapted prompt cites its source spec section; generated
   stubs are marked `unverified-template-origin`, never presented as reviewed.

## Rules

- Tools must already exist in the STC tool catalog (no catalog additions
  without the H-C fidelity result).
- Secrets are `{{STUDIO_SECRET:label}}` placeholders only. Raw `sk-` / `AKIA` /
  `xox` / `ghp_` material anywhere fails validation.
- Spawns never escalate: children inherit read-only scopes at most; anything
  else is a typed rejection, never a silent downgrade.
- `Isolated` default; `Supervised` only with narrow inheritable scopes.

## PR checklist (also in the PR template)

- [ ] `rolepack.yaml` parses with all v2 fields present
- [ ] tools ⊆ catalog; manifest check green (`check_manifest`)
- [ ] secret scan clean (placeholders only)
- [ ] `rolepack.lock` present, name/version match, hashes pinned
- [ ] emitted targets present with matching tool lists
- [ ] provenance headers / citations present
