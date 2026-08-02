from src.mkpp.model import ReactionDefinition
from src.mkpp.amore import apply_amore_lumping
import yaml

with open('mechanisms/saprc99.yaml') as f:
    data = yaml.safe_load(f)
    
rules = {"ALK1_SURR": ["ALK1", "ALK2", "ALK3"]}

def sig(r):
    react_str = ",".join(f"{k}:{v}" for k, v in sorted(r['reactants'].items()))
    prod_str = ",".join(f"{k}:{v}" for k, v in sorted(r['products'].items()))
    return f"{r['type']}|R={react_str}|P={prod_str}"

for r in data['reactions']:
    if 'ALK1' in r.get('reactants', {}) or 'ALK2' in r.get('reactants', {}):
        print("Explicit Reaction:", r)
        # Manually apply rules
        new_reacts = {}
        for k, v in r.get('reactants', {}).items():
            mapped = rules.get("ALK1_SURR", [])
            new_k = "ALK1_SURR" if k in mapped else k
            new_reacts[new_k] = new_reacts.get(new_k, 0) + v
            
        new_prods = {}
        for k, v in r.get('products', {}).items():
            mapped = rules.get("ALK1_SURR", [])
            new_k = "ALK1_SURR" if k in mapped else k
            new_prods[new_k] = new_prods.get(new_k, 0) + v
            
        r['reactants'] = new_reacts
        r['products'] = new_prods
        print("Substituted Reaction:", r)
        print("Signature:", sig(r))
        print("---")
