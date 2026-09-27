# Versioning + deprecation policy

- Packs are versioned `name vN` (`version` field in `rolepack.yaml`).
- Breaking changes (tool removal, slot rename, harness change) bump the major
  version and ship a `MIGRATING.md` note in the pack directory.
- Deprecated packs stay published for one minor release with
  `deprecated: true` + `superseded-by:` in `rolepack.yaml`, then are removed.
- Locks are immutable per release: re-pinning requires a version bump.
- Consumers pin with `--locked` verification; drift fails closed.
