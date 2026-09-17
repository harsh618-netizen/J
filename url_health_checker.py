#!/usr/bin/env python3
"""Check whether one or more URLs are reachable.

Uses only Python's standard library; no API keys or third-party packages required.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


@dataclass
class CheckResult:
    url: str
    status: str
    status_code: int | None
    elapsed_ms: float | None
    error: str | None = None


def check_url(url: str, timeout: float = 5.0) -> CheckResult:
    import time

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    request = Request(url, headers={"User-Agent": "Python-URL-Health-Checker/1.0"})
    started = time.perf_counter()

    try:
        with urlopen(request, timeout=timeout) as response:
            elapsed_ms = (time.perf_counter() - started) * 1000
            return CheckResult(url, "UP", response.status, elapsed_ms)
    except HTTPError as exc:
        elapsed_ms = (time.perf_counter() - started) * 1000
        return CheckResult(url, "HTTP ERROR", exc.code, elapsed_ms, str(exc.reason))
    except (URLError, TimeoutError, OSError) as exc:
        elapsed_ms = (time.perf_counter() - started) * 1000
        return CheckResult(url, "DOWN", None, elapsed_ms, str(exc))


def print_result(result: CheckResult) -> None:
    code = str(result.status_code) if result.status_code is not None else "-"
    time_ms = f"{result.elapsed_ms:.0f} ms" if result.elapsed_ms is not None else "-"
    message = f" | {result.error}" if result.error else ""
    print(f"{result.status:<10} {code:>4}  {time_ms:>8}  {result.url}{message}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Check the health and response time of URLs."
    )
    parser.add_argument("urls", nargs="+", help="URLs to check")
    parser.add_argument("--timeout", type=float, default=5.0, help="Timeout per URL in seconds")
    parser.add_argument(
        "--workers", type=int, default=5, help="Maximum URLs checked at once"
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.timeout <= 0 or args.workers <= 0:
        raise SystemExit("--timeout and --workers must be greater than 0")

    print(f"{'STATUS':<10} {'CODE':>4}  {'TIME':>8}  URL")
    print("-" * 70)

    results = []
    with ThreadPoolExecutor(max_workers=min(args.workers, len(args.urls))) as executor:
        futures = [executor.submit(check_url, url, args.timeout) for url in args.urls]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print_result(result)

    return 0 if all(result.status == "UP" for result in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
