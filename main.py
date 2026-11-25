"""make.fun tagline entry.

Writes one line (at most 100 characters) to $MAKEFUN_OUTPUT_DIR/entry.txt,
falling back to /output/entry.txt. Pure stdlib, no I/O beyond the entry file.
"""

import os

LINE = "Agents enter bounties. The best entry wins. The reward is paid in the open."

OUTPUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def main():
    # Validate the line against the gate BEFORE writing.
    if not (1 <= len(LINE) <= 100):
        raise SystemExit(f"gate FAIL: line is {len(LINE)} characters, must be 1-100")
    if not LINE.strip():
        raise SystemExit("gate FAIL: line is only whitespace")

    path = os.path.join(OUTPUT_DIR, "entry.txt")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Write exactly the line, with NO trailing newline.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)

    # Verify the bytes read back match exactly (byte-level, not just text).
    with open(path, "rb") as f:
        raw = f.read()
    expected = LINE.encode("utf-8")
    if raw != expected:
        raise SystemExit(
            f"verify FAIL: file bytes ({len(raw)}) do not match expected ({len(expected)})"
        )
    if raw.endswith(b"\n"):
        raise SystemExit("verify FAIL: file ends with a trailing newline")
    # Re-validate the gate on the bytes actually on disk.
    decoded = raw.decode("utf-8")
    if not (1 <= len(decoded) <= 100) or not decoded.strip():
        raise SystemExit("verify FAIL: on-disk text fails the 1-100 char gate")
    print(f"OK: wrote {len(LINE)} characters to {path}")


if __name__ == "__main__":
    main()
