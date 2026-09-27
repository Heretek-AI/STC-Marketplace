# STC-Marketplace

Community RolePack registry for the Software Team Collective.
Core-team published, PR-reviewed. The main repo
([Heretek-AI/STC](https://github.com/Heretek-AI/STC)) keeps the sources of
truth (`studio-core/src/roles`); this repo mirrors releases.

## Layout

- `roles/<name>/` — one directory per pack: `rolepack.yaml` (RolePack v2),
  `rolepack.lock` (pinned content hashes), plus emitted targets
  (`agents/<name>.md`, `package.json` base-pi shim, `.opencode/agents/` mirror).
- `profiles/` — curated pack sets (e.g. pi-library) referencing `roles/` entries.
- `skills/` — skill asset sources referenced by lockfiles.

## Publishing

Core team only, via PRs (see `CONTRIBUTING.md` + the PR template checklist).
Mirrors are cut with:

```bash
studio-cli export-packs --dir /path/to/STC-Marketplace/
```

Versioning + deprecation: see `VERSIONING.md`.
