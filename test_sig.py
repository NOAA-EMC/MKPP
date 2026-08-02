import yaml
d = yaml.safe_load(open('mechanisms/saprc99.yaml'))

surrogates = {"ALK_SURR", "ARO_SURR", "OLE_SURR", "TERP_SURR"}

def sig(r, surrogates):
    react_str = ",".join(f"{k}:{v}" for k, v in sorted(r['reactants'].items()))
    
    # If any reactant is a surrogate, we merge by reactants only to collapse explicit paths.
    has_surrogate = any(k in surrogates for k in r['reactants'].keys())
    
    if has_surrogate:
        return f"{r['type']}|R={react_str}"
    else:
        prod_str = ",".join(f"{k}:{v}" for k, v in sorted(r['products'].items()))
        return f"{r['type']}|R={react_str}|P={prod_str}"

# Substitute ALK1 -> ALK_SURR to simulate
for r in d['reactions']:
    if 'ALK1' in r.get('reactants', {}):
        r['reactants']['ALK_SURR'] = r['reactants'].pop('ALK1')
    if 'ALK2' in r.get('reactants', {}):
        r['reactants']['ALK_SURR'] = r['reactants'].pop('ALK2')

sigs = {}
for r in d['reactions']:
    s = sig(r, surrogates)
    sigs[s] = sigs.get(s, 0) + 1

for k, v in sigs.items():
    if v > 1:
        print(f"MERGED {v} times:", k)
