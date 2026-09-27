## Marketplace pack checklist (core-team publishing)

- [ ] `rolepack.yaml` parses with all RolePack v2 fields
- [ ] tools ⊆ 15-tool catalog; `check_manifest` green
- [ ] Secret scan clean (placeholders only, no raw material)
- [ ] `rolepack.lock` present; name/version match; hashes pinned
- [ ] Emitted targets (`agents/`, `package.json`, `.opencode/`) present with matching tool lists
- [ ] Provenance headers / spec citations present
- [ ] Versioning: new pack (v1) or bumped with migration note
