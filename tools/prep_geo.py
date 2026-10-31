"""Simplified district geometry + label anchors (pole of inaccessibility) for embedding."""
import sys, json, math, heapq
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
from common import load_districts, pip, KX, KY, DATA
def rdp(pts, eps):
    if len(pts) < 3: return pts
    a, b = pts[0], pts[-1]; dmax = 0; idx = 0
    ax, ay = a[0]*KX, a[1]*KY; bx, by = b[0]*KX, b[1]*KY
    for i in range(1, len(pts)-1):
        px, py = pts[i][0]*KX, pts[i][1]*KY
        dx, dy = bx-ax, by-ay; L = dx*dx+dy*dy
        t = 0 if L == 0 else max(0, min(1, ((px-ax)*dx+(py-ay)*dy)/L))
        d = math.hypot(px-(ax+t*dx), py-(ay+t*dy))
        if d > dmax: dmax, idx = d, i
    if dmax > eps: return rdp(pts[:idx+1], eps)[:-1] + rdp(pts[idx:], eps)
    return [a, b]
def ring_dist(p, ring):
    best = 1e9; inside = pip(p, ring)
    for i in range(len(ring)-1):
        a, b = ring[i], ring[i+1]
        ax, ay = (a[0]-p[0])*KX, (a[1]-p[1])*KY; bx, by = (b[0]-p[0])*KX, (b[1]-p[1])*KY
        dx, dy = bx-ax, by-ay; L = dx*dx+dy*dy
        t = 0 if L == 0 else max(0, min(1, -(ax*dx+ay*dy)/L))
        best = min(best, math.hypot(ax+t*dx, ay+t*dy))
    return best if inside else -best
def polylabel(ring, precision=0.02):
    xs = [p[0] for p in ring]; ys = [p[1] for p in ring]
    minx, miny, maxx, maxy = min(xs), min(ys), max(xs), max(ys)
    cell = min(maxx-minx, maxy-miny); h = cell/2
    if cell == 0: return [minx, miny]
    q = []
    def push(x, y, h):
        d = ring_dist((x, y), ring); heapq.heappush(q, (-(d + h*math.hypot(KX, KY)), d, x, y, h))
    x = minx
    while x < maxx:
        y = miny
        while y < maxy: push(x+h, y+h, h); y += cell
        x += cell
    cx, cy = sum(xs)/len(xs), sum(ys)/len(ys); best = (ring_dist((cx, cy), ring), cx, cy)
    while q:
        _, d, x, y, h = heapq.heappop(q)
        if d > best[0]: best = (d, x, y)
        if -_ - best[0] <= precision: continue
        h /= 2
        for dx in (-h, h):
            for dy in (-h, h): push(x+dx, y+dy, h)
    return [best[1], best[2], best[0]]
D = load_districts(); out = []; npts = 0
for d in D:
    polys = []
    for poly in d['polys']:
        rings = []
        for r in poly:
            s = rdp([p[:2] for p in r], 0.012)  # 12 m tolerance
            if len(s) >= 4: rings.append([[round(x, 5), round(y, 5)] for x, y in s]); npts += len(s)
        if rings: polys.append(rings)
    main = max((p[0] for p in d['polys']), key=lambda r: len(r))
    lx, ly, inner = polylabel([p[:2] for p in main])
    out.append({'n': d['name'], 'g': polys, 'l': [round(lx, 5), round(ly, 5)], 'r': round(inner, 3)})
json.dump(out, open(DATA / 'geo.json', 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('districts', len(out), 'points', npts, 'bytes', len(json.dumps(out, ensure_ascii=False, separators=(',', ':'))))
