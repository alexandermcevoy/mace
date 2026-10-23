# OpenHeights: CH-UH spending vs. poverty-similar Ohio districts.
# Usage: python3 -I spending_peers.py <report-card spend json (2025-26, all districts)> <residuals_2025-26.csv> <CCD directory json> <Census elsec24.xlsx> <out.csv>
# Inputs: Ohio report card finance data; DEW/SAIPE merged file from build of adjusted-outcomes page; NCES CCD directory (IRN<->LEAID); Census Annual Survey of School System Finances FY2024.
import json, csv, sys, statistics as st
import pandas as pd, numpy as np
spend_f, resid_f, ccd_f, census_f = sys.argv[1:5]
sp = {r['irn']: r for r in json.load(open(spend_f))}
res = {}
with open(resid_f) as f:
    for r in csv.DictReader(f): res[r['irn']] = r
ccd = json.load(open(ccd_f))['results']
irn2lea = {c['state_leaid'].split('-')[-1]: str(c['leaid']) for c in ccd if c.get('state_leaid')}
cen = pd.read_excel(census_f, sheet_name=0, dtype={'NCESID': str, 'FIPST': str})
cen = cen[cen.FIPST == '39'].set_index('NCESID')

rows = []
for irn, r in res.items():
    s = sp.get(irn)
    if not s or not s.get('ExpndPerEquivPupilAmt'): continue
    ep = s['ExpndPerEquivPupilAmt']; pct = s['ExpndPctClsrm']
    d = dict(irn=irn, name=r['name'], typ=int(r['typ']), enr=float(r['enr']), ed=float(r['ed']), swd=float(r['swd']),
             cpov=float(r['cpov']), pi=float(r['pi']), epep=ep, pct=pct, cls=ep * pct / 100, non=ep * (1 - pct / 100))
    lea = irn2lea.get(irn)
    if lea in cen.index:
        c = cen.loc[lea]; m = c['V33']
        if m and m > 0:
            k = 1000 / m
            d.update(mem=m, cur=c['TCURELSC'] * k, inst=c['TCURINST'] * k, pupil=c['E17'] * k, istaff=c['E07'] * k,
                     genadm=c['E08'] * k, schadm=c['E09'] * k, ops=c['V40'] * k, trans=c['V45'] * k,
                     other=(c['V90'] + c['V85']) * k, food=c['E11'] * k)
    rows.append(d)
D = pd.DataFrame(rows)
me = D[D.irn == '043794'].iloc[0]
print("CH-UH:", me[['enr','ed','swd','cpov','epep','pct','cls','non']].to_dict())
def pctile(s, v): return round(100 * (s < v).mean(), 1)
groups = {
  'All 607': D,
  'Child poverty 15-23% (SAIPE)': D[(D.cpov >= 14.9) & (D.cpov <= 22.9)],
  'Child poverty 15-23%, enrollment >=2,500': D[(D.cpov >= 14.9) & (D.cpov <= 22.9) & (D.enr >= 2500)],
  'Child poverty >=15% (as poor or poorer)': D[D.cpov >= 14.9],
  'Econ-disadv flag >=95%': D[D.ed >= 95],
  'Typology 5 (CH-UH group)': D[D.typ == 5],
  'Typology 7-8 urban': D[D.typ >= 7],
}
for g, G in groups.items():
    print(f"\n## {g}: n={len(G)}")
    for col, lab in [('epep','Spend/equiv pupil'),('cls','Classroom $/equiv'),('non','Non-classroom $/equiv'),('pct','Classroom %')]:
        print(f"  {lab:22s} CH-UH {me[col]:>9.1f}  median {G[col].median():>9.1f}  CH-UH pctile {pctile(G[col], me[col])}")
# regression: EPEP on cpov, swd, log enr
Dn = D.dropna(subset=['epep'])
X = np.column_stack([np.ones(len(Dn)), Dn.cpov, Dn.swd, np.log(Dn.enr)])
for col in ['epep','non','cls']:
    b,*_ = np.linalg.lstsq(X, Dn[col], rcond=None); pred = X @ b; resid = Dn[col] - pred
    i = list(Dn.irn).index('043794')
    r2 = 1 - ((Dn[col]-pred)**2).sum()/((Dn[col]-Dn[col].mean())**2).sum()
    print(f"\nOLS {col} ~ cpov+swd+log(enr): R2={r2:.2f}; CH-UH actual {Dn[col].iloc[i]:.0f}, predicted {pred[i]:.0f}, resid {resid.iloc[i]:+.0f}, resid pctile {pctile(resid, resid.iloc[i])}")
# census function breakdown
C = D.dropna(subset=['cur'])
peer = C[(C.cpov >= 14.9) & (C.cpov <= 22.9) & (C.enr >= 2500)]
print(f"\nCensus FY2024 per-pupil by function (peers: poverty 15-23%, enr>=2500, n={len(peer)}); state = all-district median")
mec = C[C.irn == '043794'].iloc[0]
for col, lab in [('cur','Total current'),('inst','Instruction'),('pupil','Pupil support'),('istaff','Instructional staff support'),('genadm','General (district) admin'),('schadm','School admin'),('ops','Operations & maintenance'),('trans','Transportation'),('other','Business/central/other'),('food','Food service')]:
    print(f"  {lab:28s} CH-UH {mec[col]:>7.0f}  peer median {peer[col].median():>7.0f}  all median {C[col].median():>7.0f}  diff vs peers {mec[col]-peer[col].median():>+6.0f}  pctile(all) {pctile(C[col], mec[col])}")
print("\nPeers list:", ", ".join(sorted(peer.name)))
D.to_csv(sys.argv[5], index=False)
