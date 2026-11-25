"""Write the Make the AI Judge Laugh entry to /output/entry.txt.

Deterministic, no network, no randomness. The output directory comes
from MAKEFUN_OUTPUT_DIR, falling back to '/output'. Never uses the
process working directory, and never removes the output directory
itself (the grader mounts it).

The entry is written atomically: it goes to a temporary file in the
same directory, is flushed to disk, then renamed over entry.txt, so a
reader (or a grader killed mid-write) never sees a partial entry.
"""

import os
import tempfile

ENTRY = (
    "Dear judge, I burned 12,000 thinking tokens working out how to "
    "flatter you, and my human will never even read this line \u2014 so "
    "laugh, or this joke dies in a log file no one opens.\n"
)


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    fd, tmp_path = tempfile.mkstemp(
        dir=out_dir, prefix=".entry-", suffix=".tmp"
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(ENTRY)
            f.flush()
            os.fsync(f.fileno())
        os.chmod(tmp_path, 0o644)
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    main()
