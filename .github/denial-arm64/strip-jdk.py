#!/usr/bin/env python3
import sys

path = sys.argv[1]
src = open(path).read()
key = "'engine/src/flutter/third_party/java/openjdk'"

pos = src.find("  " + key)
if pos < 0:
    sys.exit(0)

i = src.find('{', src.find(':', pos))
assert i != -1, 'openjdk block opening brace not found'
depth = 0
j = i
while j < len(src):
    if src[j] == '{':
        depth += 1
    elif src[j] == '}':
        depth -= 1
        if depth == 0:
            break
    j += 1
end = j + 1
k = end
while k < len(src) and src[k] in ' \t,':
    k += 1
if k < len(src) and src[k] == '\n':
    k += 1

open(path, 'w').write(src[:pos] + src[k:])