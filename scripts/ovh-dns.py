#!/usr/bin/env python3
"""
ovh-dns.py — gestión de registros DNS en OVH por API (firma HMAC-SHA1).

Usa las credenciales del `.env` del repo `cluster` (OVH_APPLICATION_KEY,
OVH_APPLICATION_SECRET, OVH_CONSUMER_KEY). No imprime secretos.

    python3 ovh-dns.py list  <zona>
    python3 ovh-dns.py ls    <zona> <campo> <subdominio>
    python3 ovh-dns.py add   <zona> <campo> <subdominio> <destino> [ttl]
    python3 ovh-dns.py del   <zona> <id>

Ejemplos
--------
    python3 ovh-dns.py ls  jimenezgomez.org AAAA blog
    python3 ovh-dns.py add jimenezgomez.org AAAA blog 2001:41d0:301:4::21
    python3 ovh-dns.py add jimenezgomez.org A    blog 87.98.230.241

⚠️ `add` es idempotente: si ya existe un registro igual, no lo duplica.
   Tras modificar, llama a refresh (lo hace solo) para propagar.
"""

from __future__ import annotations

import hashlib
import json
import os
import sys
import urllib.request
from pathlib import Path

CLUSTER_ENV = Path.home() / "data" / "repo" / "cluster" / ".env"
BASE = "https://eu.api.ovh.com/1.0"   # ⚠️ NO es ovh-eu.api.ovh.com


def creds() -> dict[str, str]:
    """Lee solo las 3 claves OVH del .env (sin `source`: hay líneas con [ ])."""
    out = {}
    for line in CLUSTER_ENV.read_text(encoding="utf-8").splitlines():
        for k in ("OVH_APPLICATION_KEY", "OVH_APPLICATION_SECRET", "OVH_CONSUMER_KEY"):
            if line.startswith(f"{k}="):
                out[k] = line.split("=", 1)[1].strip().strip('"').strip("'")
    missing = {"OVH_APPLICATION_KEY", "OVH_APPLICATION_SECRET", "OVH_CONSUMER_KEY"} - set(out)
    if missing:
        sys.exit(f"✗ Faltan credenciales en {CLUSTER_ENV}: {', '.join(sorted(missing))}")
    return out


class OVH:
    def __init__(self) -> None:
        self.c = creds()
        self.ts = json.load(urllib.request.urlopen(f"{BASE}/auth/time", timeout=20))

    def call(self, method: str, path: str, body: dict | None = None):
        url = BASE + path
        raw = json.dumps(body) if body is not None else ""
        s = f"{self.c['OVH_APPLICATION_SECRET']}+{self.c['OVH_CONSUMER_KEY']}+{method}+{url}+{raw}+{self.ts}"
        sig = "$1$" + hashlib.sha1(s.encode()).hexdigest()
        req = urllib.request.Request(
            url, data=raw.encode() if body is not None else None, method=method,
            headers={
                "Content-Type": "application/json",
                "X-Ovh-Application": self.c["OVH_APPLICATION_KEY"],
                "X-Ovh-Timestamp": str(self.ts),
                "X-Ovh-Signature": sig,
                "X-Ovh-Consumer": self.c["OVH_CONSUMER_KEY"],
            },
        )
        return json.load(urllib.request.urlopen(req, timeout=25))

    def refresh(self, zone: str) -> None:
        self.call("POST", f"/domain/zone/{zone}/refresh")


def find(api: OVH, zone: str, field: str, sub: str) -> list[dict]:
    ids = api.call("GET", f"/domain/zone/{zone}/record?fieldType={field}&subDomain={sub}")
    return [api.call("GET", f"/domain/zone/{zone}/record/{i}") for i in ids]


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    cmd, zone = sys.argv[1], sys.argv[2]
    api = OVH()

    if cmd == "list":
        ids = api.call("GET", f"/domain/zone/{zone}/record")
        for rid in ids:
            r = api.call("GET", f"/domain/zone/{zone}/record/{rid}")
            sub = r["subDomain"] or "@"
            print(f"{r['fieldType']:6} {sub:28} {r.get('target',''):56} id={r['id']}")
        return 0

    if cmd == "ls":
        field, sub = sys.argv[3], sys.argv[4]
        for r in find(api, zone, field, sub):
            print(f"{r['fieldType']} {r['subDomain']} -> {r['target']} (id={r['id']})")
        return 0

    if cmd == "add":
        field, sub, target = sys.argv[3], sys.argv[4], sys.argv[5]
        ttl = int(sys.argv[6]) if len(sys.argv) > 6 else 0
        for r in find(api, zone, field, sub):
            if r["target"] == target:
                print(f"= ya existe: {field} {sub} -> {target} (id={r['id']}), no se toca")
                return 0
        res = api.call("POST", f"/domain/zone/{zone}/record", {
            "fieldType": field, "subDomain": sub, "target": target, "ttl": ttl,
        })
        api.refresh(zone)
        print(f"✓ creado: {field} {sub} -> {target} (id={res['id']})")
        return 0

    if cmd == "del":
        rid = sys.argv[3]
        api.call("DELETE", f"/domain/zone/{zone}/record/{rid}")
        api.refresh(zone)
        print(f"✓ borrado id={rid}")
        return 0

    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
