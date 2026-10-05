#!/usr/bin/env python3
"""Rebuild the READY list in index.html: every local file that has real content.
Run after adding or removing material:  python3 tools/update-ready.py"""
import os, re, json
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ready = []
for d, _, files in os.walk(ROOT):
    if '/.git' in d or d.endswith('/tools'): continue
    for f in files:
        rel = os.path.relpath(os.path.join(d, f), ROOT)
        if rel in ('index.html', 'coming-soon.html') or not f.endswith(('.html', '.pdf')): continue
        if f.endswith('.html') and 'Content coming soon' in open(os.path.join(d, f), encoding='utf8', errors='ignore').read(4000):
            continue
        ready.append(rel)
ready.sort()
p = os.path.join(ROOT, 'index.html'); s = open(p, encoding='utf8').read()
block = '/*READY-START*/var READY = ' + json.dumps(ready) + ';/*READY-END*/'
if '/*READY-START*/' in s:
    s = re.sub(r'/\*READY-START\*/.*?/\*READY-END\*/', lambda _: block, s, flags=re.S)
else:
    s = s.replace('  /* ---------------- CONTENT', '  ' + block + '\n  function isReady(h){ return !!h && (/^https?:/.test(h) || READY.indexOf(h.split("?")[0]) >= 0); }\n\n  /* ---------------- CONTENT', 1)
open(p, 'w', encoding='utf8').write(s)
print(len(ready), 'ready files'); print('\n'.join(ready))
