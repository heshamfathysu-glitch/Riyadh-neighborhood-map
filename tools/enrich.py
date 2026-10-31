"""Builds per-district marketing metrics, the main-road layer and the metro layer
for the PLAN C Riyadh map. Inputs are archived copies of public datasets (see
SOURCES below); every number written here is computed from them, nothing is
estimated or invented. Output: data/enriched.json
"""
import sys, json, csv, math, collections, statistics
sys.path.insert(0, str(__import__('pathlib').Path(__file__).resolve().parent))
from common import norm, load_districts, in_district, dist_km, seg_dist_km, RAW, DATA

T = str(RAW) + '/'
OUT = DATA / 'enriched.json'

D = load_districts()
for d in D:
    ring = max((p[0] for p in d['polys']), key=len)
    xs = [p[0] for p in ring]; ys = [p[1] for p in ring]
    d['bbox'] = [min(xs), min(ys), max(xs), max(ys)]
    # area (km2), equirectangular at the ring's latitude, holes removed
    a = 0
    for poly in d['polys']:
        for k, r in enumerate(poly):
            lat = sum(p[1] for p in r) / len(r); kx = 111.32 * math.cos(math.radians(lat))
            s = sum(r[i][0] * r[(i + 1) % len(r)][1] - r[(i + 1) % len(r)][0] * r[i][1] for i in range(len(r)))
            a += (abs(s) * .5 * kx * 110.57) * (1 if k == 0 else -1)
    d['area'] = a
    # centroid of the largest ring
    cx = sum(xs) / len(xs); cy = sum(ys) / len(ys)
    d['center'] = [cx, cy]

def locate(pt):
    for d in D:
        b = d['bbox']
        if b[0] <= pt[0] <= b[2] and b[1] <= pt[1] <= b[3] and in_district(pt, d):
            return d['name']
    return None

M = {d['name']: {} for d in D}

# ---------- RCRC commercial services 2024 (official open data) ----------
cs = json.load(open(T + 'commercial-services-by-category-sub-municipality-and-district-2024.geojson', encoding='utf-8'))['features']
GROUP = {'محطة غاز': 'fuel', 'محطة بنزين': 'fuel', 'محل بقالة': 'grocery', 'متجر سوق': 'grocery',
         'سوبر ماركت': 'supermarket', 'هايبر ماركت': 'supermarket', 'فندق': 'hotel', 'شقق فندقية': 'hotel',
         'مجمع تجاري': 'mall', 'مركز تجاري': 'mall', 'بنك': 'bank', 'وحدات سكنية': 'residential_units'}
sector_votes = collections.defaultdict(collections.Counter)
submun_votes = collections.defaultdict(collections.Counter)
by_rcrc_name = collections.defaultdict(collections.Counter)
by_rcrc_sub = collections.defaultdict(collections.Counter)
rcrc_pts = []
rcrc_by_label = collections.defaultdict(collections.Counter)
for f in cs:
    p = f['properties']; g = p['geo_point_2d']; pt = (g['lon'], g['lat'])
    sec = p['sectorgeorrar']; sub = p['submunrrar']
    by_rcrc_name[norm(p['districtar'])][sec] += 1
    by_rcrc_sub[norm(p['districtar'])][sub] += 1
    rcrc_pts.append((pt, sec, sub))
    grp = GROUP.get(p['comcatar'], 'other')
    rcrc_by_label[norm(p['districtar'])][grp] += 1; rcrc_by_label[norm(p['districtar'])]['total'] += 1
    name = locate(pt)
    if not name: continue
    c = M[name].setdefault('rcrc_pip', collections.Counter()); c[grp] += 1; c['total'] += 1
    sector_votes[name][sec] += 1; submun_votes[name][sub] += 1
# Prefer RCRC's own district label (official assignment); fall back to point-in-polygon on the
# OSM boundary only for districts whose name does not appear in the RCRC table.
for d in D:
    k = norm(d['name']); m = M[d['name']]
    if k in rcrc_by_label: m['rcrc'] = rcrc_by_label[k]; m['rcrc_how'] = 'label'
    else: m['rcrc'] = m.get('rcrc_pip', collections.Counter()); m['rcrc_how'] = 'pip'
    m.pop('rcrc_pip', None)

# ---------- RCRC entertainment services 2024 ----------
ent_label = collections.Counter(); ent_pip = collections.Counter()
for r in csv.DictReader(open(T + 'rcrc_entertainment.csv', encoding='utf-8-sig')):
    ent_label[norm(r['districtar'])] += 1
    name = locate((float(r['lon']), float(r['lat'])))
    if name: ent_pip[name] += 1
for d in D:
    M[d['name']]['entertainment'] = ent_label[norm(d['name'])] if norm(d['name']) in rcrc_by_label else ent_pip[d['name']]

# ---------- sector / sub-municipality (RCRC official classification) ----------
for d in D:
    n = d['name']; key = norm(n)
    sec = sub = None; how = None
    if key in by_rcrc_name:
        sec = by_rcrc_name[key].most_common(1)[0][0]; sub = by_rcrc_sub[key].most_common(1)[0][0]; how = 'name'
    elif sector_votes[n]:
        sec = sector_votes[n].most_common(1)[0][0]; sub = submun_votes[n].most_common(1)[0][0]; how = 'points'
    else:
        best = min(rcrc_pts, key=lambda q: dist_km(q[0], d['center']))
        sec, sub, how = best[1], best[2], 'nearest'
    M[n]['sector'] = sec; M[n]['submun'] = sub; M[n]['sector_how'] = how

# ---------- OSM points of interest (archived extracts) ----------
for fn, key in [('riyadh_malls.csv', 'osm_malls'), ('riyadh_hospitals.csv', 'osm_hospitals'),
                ('riyadh_schools.csv', 'osm_schools'), ('riyadh_parks.csv', 'osm_parks'),
                ('riyadh_mosques.csv', 'osm_mosques')]:
    for r in csv.DictReader(open(T + fn, encoding='utf-8-sig')):
        try: pt = (float(r['longitude']), float(r['latitude']))
        except ValueError: continue
        name = locate(pt)
        if name: M[name][key] = M[name].get(key, 0) + 1

# ---------- Metro (RCRC open data 2024) ----------
st = json.load(open(T + 'metro-stations-in-riyadh-by-metro-line-and-station-type-2024.geojson', encoding='utf-8'))['features']
stations = []
for f in st:
    p = f['properties']; g = p['geo_point_2d']
    stations.append({'name': p['metro_station_desc_ar'].strip(), 'line': p['metro_line_desc_ar'].strip(),
                     'pt': (g['lon'], g['lat'])})
for d in D:
    n = d['name']
    inside = sorted({s['name'] + ' · ' + s['line'] for s in stations if in_district(s['pt'], d)})
    near = min(stations, key=lambda s: dist_km(s['pt'], d['center']))
    M[n]['metro_in'] = inside
    M[n]['metro_near'] = {'name': near['name'], 'line': near['line'],
                          'km': round(dist_km(near['pt'], d['center']), 2)}
lines = json.load(open(T + 'metro-lines-in-riyadh-2024.geojson', encoding='utf-8'))['features']
METRO = []
for f in lines:
    p = f['properties']; g = f['geometry']
    segs = [g['coordinates']] if g['type'] == 'LineString' else g['coordinates']
    METRO.append({'name': p['metrolinenamear'], 'color': p['m_linecolorcode'],
                  'ends': p.get('metroterminalstationsar'),
                  'lines': [[[round(x, 5), round(y, 5)] for x, y, *_ in s] for s in segs]})
METRO_ST = [{'n': s['name'], 'l': s['line'], 'p': [round(s['pt'][0], 5), round(s['pt'][1], 5)]} for s in stations]

# ---------- Main roads (OpenStreetMap, Geofabrik snapshot 2026-10-11) ----------
R = json.load(open(T + 'osm_main_roads_riyadh.json', encoding='utf-8'))
ROADS = [
    ('kfahd', 'طريق الملك فهد', '#FE5000', ['King Fahd Road']),
    ('kabdulaziz', 'طريق الملك عبدالعزيز', '#FFD23F', ['King Abdulaziz Road']),
    ('pturki', 'طريق الأمير تركي بن عبدالعزيز الأول', '#4ADE80', ['Prince Turki Bin Abdulaziz Al Awal Road']),
    ('kabdullah', 'طريق الملك عبدالله', '#38BDF8', ['King Abdullah Road', 'King Abdullah Rd', 'King Abdullah']),
    ('makkah', 'طريق مكة المكرمة', '#F472B6', ['Makkah Al Mukarramah Road', 'Makkah Al-Mukarramah Road']),
    ('khurais', 'طريق خريص', '#A78BFA', ['Khurais Road']),
    ('dammam', 'طريق الدمام', '#F87171', ['Dammam Road', 'Highway 40']),
    ('thumamah', 'طريق الثمامة', '#2DD4BF', ['Al Thumama', 'طريق الثمامة']),
    ('urubah', 'طريق العروبة', '#E879F9', ['Al Uaroba Road', 'Al Orouba']),
    ('ring_n', 'الدائري الشمالي', '#93C5FD', ['Northern Ring Road']),
    ('ring_e', 'الدائري الشرقي', '#FDBA74', ['Eastern Ring', 'Eastern Ring Road', 'East Ring Road']),
    ('ring_s', 'الدائري الجنوبي', '#BEF264', ['South Ring Road', 'Southern Ring Rd']),
    ('ring_w', 'الدائري الغربي', '#FCA5A5', ['Western Ring Road', 'Western Ring Rd']),
    ('jeddah', 'طريق جدة', '#C4B5FD', ['Jeddah Road', 'Jeddah Rd']),
]
ROAD_LAYER = []
for key, ar, color, osm in ROADS:
    segs = [r['pts'] for r in R if r['name'] in osm]
    # Highway 40 inside Riyadh: keep only the stretch east of the northern/eastern ring junction (Dammam road)
    if key == 'dammam':
        segs = [s for s in segs if min(p[0] for p in s) >= 46.72]
    ROAD_LAYER.append({'key': key, 'ar': ar, 'color': color, 'osm': osm,
                       'lines': [[[round(x, 4), round(y, 4)] for x, y in s] for s in segs]})
# Short gaps left by the simplified extract (e.g. at interchanges) are bridged with a
# straight connector that the page draws dashed, so it is never mistaken for mapped geometry.
for r in ROAD_LAYER:
    L = r['lines']; n = len(L); par = list(range(n))
    def find(x):
        while par[x] != x: par[x] = par[par[x]]; x = par[x]
        return x
    for i in range(n):
        for j in range(i + 1, n):
            if min(dist_km(p, q) for p in L[i] for q in L[j]) < 0.06: par[find(i)] = find(j)
    r['bridges'] = []
    while True:
        comps = {}
        for i in range(n): comps.setdefault(find(i), []).append(i)
        cs = list(comps.values()); best = None
        for a in range(len(cs)):
            for b in range(a + 1, len(cs)):
                for i in cs[a]:
                    for j in cs[b]:
                        for p in (L[i][0], L[i][-1]):
                            for q in (L[j][0], L[j][-1]):
                                d = dist_km(p, q)
                                if best is None or d < best[0]: best = (d, p, q, i, j)
        if not best or best[0] > 2.0: break
        r['bridges'].append([best[1], best[2]]); par[find(best[3])] = find(best[4])
# Riyadh–Qassim road: since 2023 officially an extension of King Fahd Road; its rural
# geometry lies outside the bundled OSM extract, so only the exit point is marked.
kf_north = max((p for s in ROAD_LAYER[0]['lines'] for p in s), key=lambda p: p[1])
QASSIM = {'key': 'qassim', 'ar': 'طريق الرياض–القصيم', 'color': '#FDE68A', 'exit': kf_north}

def densify(line, step=0.1):
    out = []
    for a, b in zip(line, line[1:]):
        n = max(1, int(dist_km(a, b) / step))
        for k in range(n): out.append((a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n))
    out.append(tuple(line[-1])); return out

ROAD_SAMPLES = {r['key']: [p for l in r['lines'] for p in densify(l)] for r in ROAD_LAYER}
for d in D:
    ring = max((p[0] for p in d['polys']), key=len)
    b = d['bbox']; pad = 0.004
    hits = []
    for r in ROAD_LAYER:
        hit = False
        for p in ROAD_SAMPLES[r['key']]:
            if not (b[0] - pad <= p[0] <= b[2] + pad and b[1] - pad <= p[1] <= b[3] + pad): continue
            if in_district(p, d) or min(seg_dist_km(p, ring[i], ring[i + 1]) for i in range(len(ring) - 1)) < 0.25:
                hit = True; break
        if hit: hits.append(r['key'])
    M[d['name']]['roads'] = hits

# ---------- Real estate transactions (Ministry of Justice, 2025 Q1–Q3) ----------
ALIAS = {norm('المغرزات'): norm('مغرزات'), norm('العريجاء الوسطى'): norm('العريجاءالاوسط'),
         norm('العريجاء الغربية'): norm('العريجاءالغربي'), norm('السكيرينه'): norm('سكيرينه'),
         norm('الوسيطا'): norm('الوسيطاء'), norm('المنصوره'): norm('المنصوره(خنشليله)')}
agg = collections.defaultdict(lambda: collections.defaultdict(lambda: [0, 0.0, 0]))  # deeds, sum(n*avg_ppm), n with avg
quarters = set()
for fn in ['sales_riyadh_2025_Q1.csv', 'sales_riyadh_2025_Q2.csv', 'sales_riyadh_2025_Q3.csv']:
    for r in csv.DictReader(open(T + fn, encoding='utf-8-sig')):
        if r['المدينة'].strip() != 'الرياض': continue
        quarters.add(r['الربع'])
        k = norm(r['الحي']); typ = r['نوع العقار'].strip(); cls = r['تصنيف العقار'].strip()
        try: n = int(float(r['عدد الصكوك ']))
        except ValueError: continue
        try: avg = float(r['متوسط سعر المتر'])
        except ValueError: avg = None   # MOJ publishes NULL for small groups
        bucket = {'أرض': 'land', 'فيلا': 'villa', 'شقة': 'apartment'}.get(typ, 'other')
        if cls != 'سكني': bucket = bucket + '_nonres'
        for b in (bucket, 'all'):
            x = agg[k][b]; x[0] += n
            if avg is not None and b != 'all': x[1] += n * avg; x[2] += n
MIN_DEEDS = 5
land_ppm = []
for d in D:
    k = norm(d['name']); k = k if k in agg else ALIAS.get(k, k)
    if k not in agg: M[d['name']]['moj'] = None; continue
    out = {'deeds': agg[k]['all'][0]}
    for b in ('land', 'villa', 'apartment'):
        n, s_, nw = agg[k][b]
        if nw >= MIN_DEEDS: out[b] = {'ppm': round(s_ / nw), 'deeds': n}
        elif n: out[b] = {'ppm': None, 'deeds': n}
    M[d['name']]['moj'] = out
    if out.get('land', {}).get('ppm'): land_ppm.append(out['land']['ppm'])
qs = statistics.quantiles(land_ppm, n=4)
for d in D:
    m = M[d['name']].get('moj')
    p = m and m.get('land', {}).get('ppm')
    M[d['name']]['tier'] = None if not p else (0 if p < qs[0] else 1 if p < qs[1] else 2 if p < qs[2] else 3)

# ---------- geometry-derived ----------
QASR = (46.7134, 24.6312)  # Qasr Al-Hukm, historic centre
TOT = sum(d['area'] for d in D)
CITY_C = (statistics.median(d['center'][0] for d in D), statistics.median(d['center'][1] for d in D))  # median of district centres
def sector4(pt):
    ang = math.degrees(math.atan2((pt[0] - CITY_C[0]) * 0.908, pt[1] - CITY_C[1]))  # 0 = north, 90 = east
    return 'الشمال' if -45 <= ang < 45 else 'الشرق' if 45 <= ang < 135 else 'الغرب' if -135 <= ang < -45 else 'الجنوب'
for d in D:
    m = M[d['name']]
    m['area'] = round(d['area'], 3)
    m['center_km'] = round(dist_km(d['center'], QASR), 1)
    m['sector4'] = sector4(d['center'])
    c = m.get('rcrc', {})
    m['rcrc'] = dict(c) if c else {}
    m['rcrc_density'] = round(c.get('total', 0) / d['area'], 2) if d['area'] > 0.05 else None

out = {'districts': M, 'roads': ROAD_LAYER, 'qassim': QASSIM, 'metro': METRO, 'metro_stations': METRO_ST,
       'city_centre': [round(CITY_C[0], 4), round(CITY_C[1], 4)], 'land_quartiles': [round(x) for x in qs], 'moj_quarters': sorted(quarters)}
json.dump(out, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))

# ---------- report ----------
print('districts', len(M), 'land price quartiles', [round(x) for x in qs], 'quarters', sorted(quarters))
print('city centre', CITY_C, collections.Counter(m['sector4'] for m in M.values()))
print('sector', collections.Counter(m['sector'] for m in M.values()))
print('sector_how', collections.Counter(m['sector_how'] for m in M.values()))
print('with moj', sum(1 for m in M.values() if m.get('moj')), 'with land ppm', len(land_ppm))
print('with rcrc points', sum(1 for m in M.values() if m['rcrc']), 'total pts', sum(m['rcrc'].get('total', 0) for m in M.values()))
print('with roads', sum(1 for m in M.values() if m['roads']))
for n in ['الملقا', 'العليا', 'النسيم الشرقي', 'السويدي', 'الياسمين', 'الملز']:
    print(n, json.dumps(M.get(n), ensure_ascii=False)[:600])
print('bridges', {r['key']: [round(dist_km(*b), 2) for b in r['bridges']] for r in ROAD_LAYER})
print('road segments', {r['key']: len(r['lines']) for r in ROAD_LAYER}, 'qassim exit', kf_north)
print('bytes', len(json.dumps(out, ensure_ascii=False, separators=(',', ':'))))
