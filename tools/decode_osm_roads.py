"""Decodes the OpenStreetMap main-road rows in data/raw/osm_main_roads_riyadh_source_terrain.ts
(copied from github.com/kromate/joinallworld, src/game/cities/riyadh/terrain.ts; built from the
Geofabrik GCC extract of 2026-10-11, © OpenStreetMap contributors, ODbL 1.0) into
data/raw/osm_main_roads_riyadh.json. Row format: name, major flag, first lon/lat in 1e-4 degrees,
then lon/lat steps to every next vertex."""
import json, re
from pathlib import Path
RAW = Path(__file__).resolve().parent.parent / 'data' / 'raw'
s = (RAW / 'osm_main_roads_riyadh_source_terrain.ts').read_text(encoding='utf-8')
i = s.index('roads: ['); j = s.index('\n  ]', i)
roads = []
for name, major, nums in re.findall(r'\[("(?:[^"\\]|\\.)*")\s*,\s*([01])\s*,([-\d,\s]+)\]', s[i:j]):
    n = [int(x) for x in nums.replace(' ', '').split(',') if x]
    x, y = n[0], n[1]; pts = [(x / 1e4, y / 1e4)]
    for k in range(2, len(n) - 1, 2):
        x += n[k]; y += n[k + 1]; pts.append((x / 1e4, y / 1e4))
    roads.append({'name': json.loads(name), 'major': int(major), 'pts': pts})
json.dump(roads, open(RAW / 'osm_main_roads_riyadh.json', 'w', encoding='utf-8'), ensure_ascii=False)
print(len(roads), 'road rows')
