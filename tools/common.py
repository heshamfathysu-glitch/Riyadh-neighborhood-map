import json,re,math,csv
from pathlib import Path
RAW=Path(__file__).resolve().parent.parent/'data'/'raw'
DATA=Path(__file__).resolve().parent.parent/'data'
def norm(s):
    s=str(s or '').strip()
    s=re.sub(r'^حي\s+','',s)
    s=re.sub('[إأآا]','ا',s).replace('ة','ه').replace('ى','ي').replace('ـ','')
    s=re.sub(r'\s+','',s)
    return s
def load_districts():
    D=json.load(open(RAW/'riyadh_districts_osm.geojson',encoding='utf-8'))
    out=[]
    for i,f in enumerate(D['features']):
        g=f['geometry']
        polys=[g['coordinates']] if g['type']=='Polygon' else g['coordinates']
        name=re.sub(r'^حي\s+','',f['properties'].get('name_ar') or f['properties'].get('name','')).strip()
        name={'At Turayf Al Jadid':'الطريف الجديد'}.get(name,name)  # OSM feature has only a Latin name
        out.append({'name':name,'polys':polys,'props':f['properties']})
    return out
def pip(pt,ring):
    x,y=pt;ins=False;n=len(ring);j=n-1
    for i in range(n):
        xi,yi=ring[i][:2];xj,yj=ring[j][:2]
        if (yi>y)!=(yj>y) and x<(xj-xi)*(y-yi)/(yj-yi)+xi: ins=not ins
        j=i
    return ins
def in_district(pt,d):
    for poly in d['polys']:
        if pip(pt,poly[0]) and not any(pip(pt,h) for h in poly[1:]): return True
    return False
KX=111.32*math.cos(math.radians(24.72));KY=110.57
def dist_km(a,b): return math.hypot((a[0]-b[0])*KX,(a[1]-b[1])*KY)
def seg_dist_km(p,a,b):
    ax,ay=(a[0]-p[0])*KX,(a[1]-p[1])*KY;bx,by=(b[0]-p[0])*KX,(b[1]-p[1])*KY
    dx,dy=bx-ax,by-ay;L=dx*dx+dy*dy
    t=0 if L==0 else max(0,min(1,-(ax*dx+ay*dy)/L))
    return math.hypot(ax+t*dx,ay+t*dy)
