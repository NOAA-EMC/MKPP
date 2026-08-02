import yaml
d = yaml.safe_load(open('mechanisms/saprc99.yaml'))

surrogates = {"ALK_SURR", "ARO_SURR", "OLE_SURR", "TERP_SURR"}

def sig(r):
    react_str = ",".join(f"{k}:{v}" for k, v in sorted(r.get('reactants', {}).items()))
    has_surrogate = any(k in surrogates for k in r.get('reactants', {}).keys())
    if has_surrogate:
        return f"{r['type']}|R={react_str}"
    else:
        prod_str = ",".join(f"{k}:{v}" for k, v in sorted(r.get('products', {}).items()))
        return f"{r['type']}|R={react_str}|P={prod_str}"

for r in d['reactions']:
    for k in list(r.get('reactants', {}).keys()):
        if k in ['ALK1', 'ALK2', 'ALK3', 'ALK4', 'ALK5']:
            r['reactants']['ALK_SURR'] = r['reactants'].pop(k)
        if k in ['ARO1', 'ARO2']:
            r['reactants']['ARO_SURR'] = r['reactants'].pop(k)
        if k in ['OLE1', 'OLE2']:
            r['reactants']['OLE_SURR'] = r['reactants'].pop(k)
        if k == 'TERP':
            r['reactants']['TERP_SURR'] = r['reactants'].pop(k)

sigs = {}
for r in d['reactions']:
    if r['type'] in ("ARRHENIUS", "PHOTOLYSIS"):
        s = sig(r)
        sigs[s] = sigs.get(s, 0) + 1

for k, v in sigs.items():
    if v > 1:
        print(f"MERGED {v} times:", k)
