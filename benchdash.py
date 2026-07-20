#!/usr/bin/env python3
"""BenchDash CLI: collect system info and print a report."""
import json
import sys

import collector.system_info as system_info


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if argv and argv[0] in ("-h", "--help"):
        print("Usage: python3 benchdash.py [collect|show]")
        print("  collect  re-scan host and write system_info.json (default)")
        print("  show     print last collected profile as JSON")
        return 0
    cmd = argv[0] if argv else "collect"
    if cmd == "show":
        info = system_info.collect()
    else:
        info = system_info.save()
    print(json.dumps(info, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
