#!/usr/bin/env python3
"""Generate CATALOG.json for all mirrored docs repos.

Scans sibling `*-docs-llm-agents` repos (or dirs given as args), reads
INDEX.md / llms-full.txt / LAST-SYNC.txt / .llms-mirror / git, and writes
a machine-readable manifest. Stdlib only.
"""

import argparse
import json
import pathlib
import re
import subprocess
from datetime import datetime, timezone

NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git(args, cwd):
    try:
        return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()
    except Exception:
        return ""


ARTIFACTS = {"README.md", "INDEX.md", "NOTICE.md", "LAST-SYNC.txt"}


def pages_in(repo):
    return sum(
        1
        for p in repo.rglob("*.md")
        if ".git" not in p.parts and p.name not in ARTIFACTS
    )


KNOWN_SOURCES = {
    "clerk.com": "https://clerk.com/docs/llms.txt",
    "docs.midtrans.com": "https://docs.midtrans.com/llms.txt",
    "docs.xendit.co": "https://docs.xendit.co/llms.txt",
    "docs.stripe.com": "https://docs.stripe.com/llms.txt",
    "razorpay.com": "https://razorpay.com/docs/llms.txt",
}


def source_url(repo):
    meta = repo / ".llms-mirror"
    if meta.exists():
        url = meta.read_text(errors="ignore").strip()
        if url:
            return url
    txt = repo / "llms.txt"
    if txt.exists():
        for m in re.finditer(r"https?://[^\s)\]]+", txt.read_text(errors="ignore")):
            netloc = m.group(0).split("/")[2]
            if netloc in KNOWN_SOURCES:
                return KNOWN_SOURCES[netloc]
    return None


def last_sync(repo):
    sync = repo / "LAST-SYNC.txt"
    if sync.exists():
        m = re.search(r"synced:\s*(\S+)", sync.read_text(errors="ignore"))
        if m:
            return m.group(1)
    stamp = git(["log", "-1", "--format=%cI"], repo)
    return stamp or None


def scan(base, dirs):
    mirrors = []
    for name in sorted(dirs):
        repo = base / name
        if not repo.is_dir() or not (repo / "INDEX.md").exists():
            continue
        full = repo / "llms-full.txt"
        remote = git(["remote", "get-url", "origin"], repo) or ""
        mirrors.append(
            {
                "name": name,
                "repo": remote.removesuffix(".git") if remote else None,
                "source": source_url(repo),
                "pages": pages_in(repo),
                "bytes": full.stat().st_size if full.exists() else 0,
                "last_sync": last_sync(repo),
            }
        )
    return mirrors


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("dirs", nargs="*", help="mirror repo dirs (default: sibling *-docs-llm-agents)")
    ap.add_argument("--out", default="CATALOG.json")
    args = ap.parse_args()

    root = pathlib.Path(__file__).resolve().parent
    dirs = args.dirs or sorted(
        d.name for d in root.parent.glob("*-docs-llm-agents") if d.is_dir()
    )

    mirrors = scan(root.parent, dirs)
    manifest = {
        "generated": NOW,
        "total_pages": sum(m["pages"] for m in mirrors),
        "total_bytes": sum(m["bytes"] for m in mirrors),
        "mirrors": mirrors,
    }
    out = root / args.out
    out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out} ({len(mirrors)} mirrors, {manifest['total_pages']} pages)")


if __name__ == "__main__":
    main()
