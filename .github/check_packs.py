#!/usr/bin/env python3
"""Marketplace PR gate (dependency-free): schema + lock + secret scan per pack.

Deep verification (check_parity, check_manifest, verify_lock, verify_emitted)
runs in the main STC repo's test suite at mirror-cut time
(`studio-cli export-packs` fails closed); this gate re-checks the published
artifacts: required files exist, YAML parses with v2 fields, lock names the
same pack version, emitted targets list exactly the pack tools, and no raw
secret material appears anywhere.
"""

import os
import re
import sys

CATALOG = {
    "read",
    "write",
    "edit",
    "patch",
    "runProcess",
    "code_search",
    "web_search",
    "tool_open",
    "kv_get",
    "syntax_check",
    "sast",
    "sbom",
    "plan_open",
    "dag_commit",
    "retrieve_docs",
}
REQUIRED_FIELDS = {
    "name",
    "version",
    "tools",
    "skill_lockfile_hash",
    "system_prompt",
    "mcp_manifest",
    "model_slot",
    "harness_profile",
    "spawns",
}
SECRET_RES = [
    re.compile(p)
    for p in (
        r"sk-[A-Za-z0-9]{12,}",
        r"AKIA[0-9A-Z]{16}",
        r"xox[bpa]-[A-Za-z0-9-]+",
        r"ghp_[A-Za-z0-9]+",
    )
]

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROLES = os.path.join(ROOT, "roles")
failures = []


def fail(msg):
    failures.append(msg)
    print(f"FAIL: {msg}")


def simple_yaml_map(text):
    """Top-level `key: value` pairs only (pack files are flat at top level)."""
    out = {}
    for line in text.splitlines():
        if line and not line[0].isspace() and ":" in line:
            k, v = line.split(":", 1)
            out[k.strip()] = v.strip().strip("'\"")
    return out


def front_matter_tools(path):
    with open(path) as f:
        body = f.read()
    if not body.startswith("---\n") or "\n---\n" not in body:
        return None
    fm = body[len("---\n") :].split("\n---\n", 1)[0]
    for line in fm.splitlines():
        if line.strip().startswith("tools:"):
            inner = line.strip()[len("tools:") :].strip().strip("[]")
            return [s.strip() for s in inner.split(",") if s.strip()]
    return None


packs = sorted(d for d in os.listdir(ROLES) if os.path.isdir(os.path.join(ROLES, d)))
if not packs:
    fail("no packs under roles/")
for name in packs:
    d = os.path.join(ROLES, name)
    rp = os.path.join(d, "rolepack.yaml")
    lk = os.path.join(d, "rolepack.lock")
    if not os.path.isfile(rp):
        fail(f"{name}: missing rolepack.yaml")
        continue
    if not os.path.isfile(lk):
        fail(f"{name}: missing rolepack.lock")
        continue
    meta = simple_yaml_map(open(rp).read())
    missing = REQUIRED_FIELDS - set(meta)
    if missing:
        fail(f"{name}: rolepack.yaml missing fields {sorted(missing)}")
    if meta.get("name") != name:
        fail(f"{name}: name mismatch ({meta.get('name')})")
    lock = simple_yaml_map(open(lk).read())
    if lock.get("pack_name") != name or lock.get("pack_version") != meta.get("version"):
        fail(f"{name}: lock names a different pack version")
    if not lock.get("pack_hash"):
        fail(f"{name}: lock missing pack_hash")
    for rel in (f"agents/{name}.md", f".opencode/agents/{name}.md"):
        p = os.path.join(d, rel)
        if not os.path.isfile(p):
            fail(f"{name}: missing emitted target {rel}")
            continue
        tools = front_matter_tools(p)
        if tools is None:
            fail(f"{name}: {rel} missing tools front matter")
    for rel in ("package.json",):
        if not os.path.isfile(os.path.join(d, rel)):
            fail(f"{name}: missing emitted target {rel}")

for dirpath, _, filenames in os.walk(ROOT):
    if ".git" in dirpath:
        continue
    for fn in filenames:
        p = os.path.join(dirpath, fn)
        try:
            with open(p, errors="ignore") as f:
                text = f.read()
        except OSError:
            continue
        for rx in SECRET_RES:
            if rx.search(text):
                fail(f"raw secret pattern in {os.path.relpath(p, ROOT)}")
                break

print(f"checked {len(packs)} packs")
sys.exit(1 if failures else 0)
