import os
import subprocess
import yaml
import re
from pathlib import Path
import glob

def generate_kpp_baseline(mech_name, kpp_dir, out_dir):
    run_dir = Path(f"kpp_run_{mech_name}")
    run_dir.mkdir(exist_ok=True)
    
    with open(run_dir / f"{mech_name}.def", "w") as f:
        f.write(f"#INCLUDE {mech_name}.spc\n")
        f.write(f"#INCLUDE {mech_name}.eqn\n")
        f.write("#LANGUAGE C\n")
        f.write("#DOUBLE ON\n")
        f.write("#INTEGRATOR rosenbrock\n")
        f.write("#DRIVER general\n")
        
    if mech_name == "chapman":
        subprocess.run(["cp", f"tests/integration/e2e_validation/data/chapman.spc", str(run_dir)])
        subprocess.run(["cp", f"tests/integration/e2e_validation/data/chapman.eqn", str(run_dir)])
    else:
        subprocess.run(["cp", f"{kpp_dir}/models/{mech_name}.spc", str(run_dir)])
        subprocess.run(["cp", f"{kpp_dir}/models/{mech_name}.eqn", str(run_dir)])
        subprocess.run(["cp", f"{kpp_dir}/models/atoms", str(run_dir)])
        subprocess.run(["cp", f"{kpp_dir}/models/atoms.kpp", str(run_dir)])
    
    kpp_bin = os.path.abspath(f"{kpp_dir}/bin/kpp")
    env = os.environ.copy()
    env["KPP_HOME"] = os.path.abspath(kpp_dir)
    res = subprocess.run([kpp_bin, f"{mech_name}.def"], cwd=str(run_dir), env=env, capture_output=True, text=True)
    
    yaml_path = f"mechanisms/{mech_name}.yaml" if mech_name != "chapman" else "tests/integration/e2e_validation/data/chapman.yaml"
    with open(yaml_path, "r") as f:
        mech = yaml.safe_load(f)
    mkpp_species = [s["name"] for s in mech["species"]]
    n_spec = len(mkpp_species)
    
    with open(run_dir / f"{mech_name}_Monitor.c", "r") as f:
        monitor_c = f.read()
    
    match = re.search(r'SPC_NAMES\[\]\s*=\s*\{([^{}]+)\};', monitor_c)
    kpp_spc_str = match.group(1).replace('"', '').replace('\n', '').replace(' ', '')
    kpp_species = [s.strip() for s in kpp_spc_str.split(',') if s.strip()]
    
    mkpp_to_kpp = []
    for sp in mkpp_species:
        if sp in kpp_species:
            mkpp_to_kpp.append(kpp_species.index(sp))
        else:
            mkpp_to_kpp.append(-1)
            
    c_map_str = "int mkpp_to_kpp[] = {" + ",".join(map(str, mkpp_to_kpp)) + "};"
    c_inv_str = "int kpp_to_mkpp[] = {" + ",".join([str(mkpp_species.index(s)) if s in mkpp_species else "-1" for s in kpp_species]) + "};"
    
    c_driver = f"""#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include "{mech_name}_Parameters.h"
#include "{mech_name}_Global.h"
#include "{mech_name}_Sparse.h"

double C[NSPEC];
double * VAR = & C[0];
double * FIX = & C[NVAR];
double RCONST[NREACT];
double TIME;
double SUN;
double TEMP;
double TSTART;
double TEND;
double DT;
double ATOL[NVAR];
double RTOL[NVAR];
double STEPMIN;
double STEPMAX;
double CFACTOR;

void Initialize();
void Update_RCONST();
void Jac_SP(double V[], double F[], double RCT[], double JVS[]);
void INTEGRATE(double TIN, double TOUT);

int main() {{
    TSTART = 0.0;
    TEND = 3600.0;
    DT = 3600.0;
    TEMP = 300.0;
    SUN = 1.0;
    CFACTOR = 1.0;
    TIME = TSTART;
    
    Initialize();
    
    {c_map_str}
    
    double mkpp_conc[{n_spec}];
    for(int i=0; i<{n_spec}; i++) {{
        mkpp_conc[i] = 1.0e2; // safe minimal non-zero concentration
    }}


    
    for(int i=0; i<{n_spec}; i++) {{
        if(mkpp_to_kpp[i] != -1) {{
            C[mkpp_to_kpp[i]] = mkpp_conc[i];
        }}
    }}

    for(int i = 0; i < NVAR; i++) {{
        RTOL[i] = 1.0e-6;
        ATOL[i] = 1.0e-12;
    }}
    STEPMIN = 0.0;
    STEPMAX = 900.0;

    Update_RCONST();

    double JVS[LU_NONZERO];
    Jac_SP(VAR, FIX, RCONST, JVS);
    
    double Jac_FULL[NSPEC][NSPEC];
    for(int i=0; i<NSPEC; i++) for(int j=0; j<NSPEC; j++) Jac_FULL[i][j] = 0.0;
    
    for(int k=0; k<LU_NONZERO; k++) {{
        int r = LU_IROW[k];
        int c = LU_ICOL[k];
        Jac_FULL[r][c] = JVS[k];
    }}

    FILE* f = fopen("../tests/integration/e2e_validation/data/kpp_baseline_{mech_name}.csv", "w");
    fprintf(f, "time_step,species_name,concentration,jacobian_sparsity_row,jacobian_sparsity_col,jacobian_value\\n");
    
    for (int mkpp_r=0; mkpp_r<{n_spec}; mkpp_r++) {{
        for (int mkpp_c=0; mkpp_c<{n_spec}; mkpp_c++) {{
            int kpp_r = mkpp_to_kpp[mkpp_r];
            int kpp_c = mkpp_to_kpp[mkpp_c];
            if (kpp_r != -1 && kpp_c != -1 && Jac_FULL[kpp_r][kpp_c] != 0.0) {{
                fprintf(f, ",,,%d,%d,%.16e\\n", mkpp_r, mkpp_c, Jac_FULL[kpp_r][kpp_c]);
            }}
        }}
    }}
    
    INTEGRATE(TSTART, TEND);
    
    for(int i=0; i<{n_spec}; i++) {{
        if(mkpp_to_kpp[i] != -1) {{
            fprintf(f, "1,%s,%.16e,,,\\n", "{mech_name}", C[mkpp_to_kpp[i]]); // Will fix name lookup later if needed
        }}
    }}
    fclose(f);
    
    return 0;
}}
"""
    with open(run_dir / "driver.c", "w") as f:
        f.write(c_driver)
        
    import glob
    c_files = glob.glob(str(run_dir / "*.c"))
    c_files = [c for c in c_files if "Main" not in c and "mex" not in c]
    
    
    import glob
    for c_file in c_files:
        with open(c_file, "r") as f:
            c_text = f.read()
        # Fix Fortran double precision suffixes leaking into C code
        c_text = re.sub(r'(\d+\.\d+)d([+-]\d+)', r'\1e\2', c_text, flags=re.IGNORECASE)
        c_text = re.sub(r'(\d+\.\d+)d0', r'\1e0', c_text, flags=re.IGNORECASE)
        c_text = re.sub(r'(\d+)d([+-]\d+)', r'\1.0e\2', c_text, flags=re.IGNORECASE)
        c_text = c_text.replace("EXP(", "exp(")
        with open(c_file, "w") as f:
            f.write(c_text)
            
    res = subprocess.run(["gcc", "-c"] + [os.path.basename(c) for c in c_files], cwd=str(run_dir), capture_output=True, text=True)
    o_files = glob.glob(str(run_dir / "*.o"))
    res = subprocess.run(["gcc"] + [os.path.basename(o) for o in o_files] + ["-o", "generator", "-lm"], cwd=str(run_dir), capture_output=True, text=True)
    subprocess.run(["./generator"], cwd=str(run_dir))
    print(f"Generated baseline for {mech_name}")

if __name__ == "__main__":
    out_dir = "tests/integration/e2e_validation/data"
    generate_kpp_baseline("small_strato", "../KPP", out_dir)
    generate_kpp_baseline("carbon", "../KPP", out_dir)
    generate_kpp_baseline("saprc99", "../KPP", out_dir)
    generate_kpp_baseline("saprcnov", "../KPP", out_dir)
