#!/usr/bin/env python3
"""Create the optional local Qdrant collection for Manager OpenBrain."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ENV_FILE = ROOT / ".env.qdrant"
DEFAULT_URL = "http://127.0.0.1:6333"
DEFAULT_COLLECTION = "manager_openbrain_memory_v1"
DEFAULT_VECTOR_SIZE = 384
DEFAULT_DISTANCE = "Cosine"


def parse_env_file(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, raw_value = line.split("=", 1)
        key = key.strip().removeprefix("export ").strip()
        values[key] = raw_value.strip().strip("'").strip('"')
    return values


def request_json(
    method: str,
    url: str,
    qdrant_token: str,
    body: dict[str, object] | None = None,
) -> tuple[int, str]:
    data = None
    headers = {"api-key": qdrant_token}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = Request(url, data=data, headers=headers, method=method)
    try:
        with urlopen(request, timeout=10) as response:
            return response.status, response.read().decode("utf-8", errors="replace")
    except HTTPError as exc:
        return exc.code, exc.read().decode("utf-8", errors="replace")
    except (TimeoutError, URLError, OSError) as exc:
        raise RuntimeError(str(exc)) from exc


def create_collection(args: argparse.Namespace) -> int:
    env_file = Path(args.env_file).expanduser()
    values = parse_env_file(env_file)

    base_url = args.url or os.environ.get("QDRANT_URL") or values.get("QDRANT_URL") or DEFAULT_URL
    base_url = base_url.rstrip("/")
    collection = (
        args.collection
        or os.environ.get("MANAGER_OPENBRAIN_MEMORY_COLLECTION")
        or values.get("MANAGER_OPENBRAIN_MEMORY_COLLECTION")
        or DEFAULT_COLLECTION
    )
    token = os.environ.get("QDRANT_API_KEY") or values.get("QDRANT_API_KEY")
    vector_size = int(
        args.vector_size
        or os.environ.get("MANAGER_OPENBRAIN_VECTOR_SIZE")
        or values.get("MANAGER_OPENBRAIN_VECTOR_SIZE")
        or DEFAULT_VECTOR_SIZE
    )
    distance = (
        args.distance
        or os.environ.get("MANAGER_OPENBRAIN_VECTOR_DISTANCE")
        or values.get("MANAGER_OPENBRAIN_VECTOR_DISTANCE")
        or DEFAULT_DISTANCE
    )

    if not env_file.exists():
        print(f"Missing env file: {env_file}", file=sys.stderr)
        print("Copy templates/env/qdrant.env.example to .env.qdrant first.", file=sys.stderr)
        return 1
    if not token:
        print("QDRANT_API_KEY is missing in the env file or environment.", file=sys.stderr)
        return 1

    try:
        status, _ = request_json("GET", f"{base_url}/healthz", token)
    except RuntimeError as exc:
        print(f"Qdrant health check failed: {exc}", file=sys.stderr)
        return 1
    if status != 200:
        print(f"Qdrant health check returned HTTP {status}", file=sys.stderr)
        return 1

    try:
        status, _ = request_json("GET", f"{base_url}/collections/{collection}", token)
    except RuntimeError as exc:
        print(f"Collection check failed: {exc}", file=sys.stderr)
        return 1

    if status == 200:
        print(f"Collection already exists: {collection}")
        return 0
    if status != 404:
        print(f"Collection check returned HTTP {status}", file=sys.stderr)
        return 1

    body = {"vectors": {"size": vector_size, "distance": distance}}
    try:
        status, response = request_json("PUT", f"{base_url}/collections/{collection}", token, body)
    except RuntimeError as exc:
        print(f"Collection creation failed: {exc}", file=sys.stderr)
        return 1

    if status not in {200, 201}:
        print(f"Collection creation returned HTTP {status}: {response}", file=sys.stderr)
        return 1

    print(f"Created collection: {collection}")
    print(f"Vector size: {vector_size}")
    print(f"Distance: {distance}")
    print("No memory items were inserted.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Create the optional local Qdrant collection.")
    parser.add_argument("--env-file", default=str(DEFAULT_ENV_FILE), help="Path to local Qdrant env file.")
    parser.add_argument("--url", help="Qdrant base URL.")
    parser.add_argument("--collection", help="Collection name.")
    parser.add_argument("--vector-size", type=int, help="Vector size for the collection.")
    parser.add_argument("--distance", choices=["Cosine", "Dot", "Euclid", "Manhattan"], help="Vector distance.")
    return create_collection(parser.parse_args())


if __name__ == "__main__":
    sys.exit(main())
