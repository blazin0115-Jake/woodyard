#!/usr/bin/env python3
"""Local deduplication + compression for tool output (ECC-style).
Reads text from stdin, deduplicates repeated lines, trims whitespace,
and compresses long repeats. Zero API calls, zero dependencies.

Usage:
    long_command | python compress_tool_output.py
"""

import sys
import re

def compress_text(text):
    lines = text.splitlines(keepends=True)
    out = []
    prev = None
    dup_count = 0

    for line in lines:
        stripped = line.strip()
        if stripped == prev:
            dup_count += 1
            continue
        else:
            if dup_count > 3:
                out.append(f"    ... ({dup_count} repeated lines)\n")
            elif dup_count > 0:
                out.extend([prev + "\n"] * dup_count)
            dup_count = 0
            prev = stripped
            out.append(line)

    # flush trailing duplicates
    if dup_count > 3:
        out.append(f"    ... ({dup_count} repeated lines)\n")
    elif dup_count > 0:
        out.extend([prev + "\n"] * dup_count)

    result = "".join(out)

    # collapse multiple blank lines
    result = re.sub(r'\n{3,}', '\n\n', result)

    # trim trailing whitespace on each line
    result = "\n".join(l.rstrip() for l in result.split("\n"))

    return result


if __name__ == "__main__":
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stdin, 'reconfigure'):
        sys.stdin.reconfigure(encoding='utf-8')

    text = sys.stdin.read()
    compressed = compress_text(text)
    sys.stdout.write(compressed)
