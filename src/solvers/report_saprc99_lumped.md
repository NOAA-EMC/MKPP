# MKPP Mechanism Diagnostic Report: saprc99

## Overview
- **Total Species**: 76
- **Total Reactions**: 201

### Reaction Types Breakdown
- **ARRHENIUS**: 158
- **TROE**: 10
- **PHOTOLYSIS**: 29
- **EP2**: 1
- **EP3**: 3

### Stiffness Partitioning
- **Implicit (Stiff) Reactions**: 172
- **Explicit (Non-Stiff) Reactions**: 29
- **Graph Topology Status**: Mechanism contains cyclically dependent fast radicals. Tarjan SCC was applied.

## AMORE Auto-Lumping Summary
- **Explicit Species Collapsed**: 10
- **Surrogates Added**: 4
- **Redundant Reactions Merged**: 9

### Target Surrogates
ALK_SURR, ARO_SURR, OLE_SURR, TERP_SURR

### Lumping Mapping Table
| Explicit Species | Mapped Surrogate |
|------------------|------------------|
| `ALK1` | `ALK_SURR` |
| `ALK2` | `ALK_SURR` |
| `ALK3` | `ALK_SURR` |
| `ALK4` | `ALK_SURR` |
| `ALK5` | `ALK_SURR` |
| `ARO1` | `ARO_SURR` |
| `ARO2` | `ARO_SURR` |
| `OLE1` | `OLE_SURR` |
| `OLE2` | `OLE_SURR` |
| `TERP` | `TERP_SURR` |

### Reduced Mechanism Definitions
- Download the lumped species config: [species_saprc99_lumped.yaml](species_saprc99_lumped.yaml)
- Download the lumped reactions config: [reactions_saprc99_lumped.yaml](reactions_saprc99_lumped.yaml)

### Lumped Reaction Parameters
When explicit paths were collapsed, their kinetic parameters were aggregated into the following effective rates ($A_{eff}$):

```yaml
- type: ARRHENIUS
  reactants:
    TERP_SURR: 1.0
    OH: 1.0
  products:
    RO2_R: 0.75
    RO2_N: 0.25
    R2O2: 0.5
    HCHO: 0.276
    RCHO: 0.474
    PROD2: 0.276
  A: '1.83e-11'
  B: 0.0
  C: '-449.0'
- type: ARRHENIUS
  reactants:
    TERP_SURR: 1.0
    O3: 1.0
  products:
    OH: 0.567
    HO2: 0.033
    RO2_R: 0.031
    RO2_N: 0.18
    R2O2: 0.729
    CCO_O2: 0.123
    RCO_O2: 0.201
    CO: 0.157
    HCHO: 0.235
    RCHO: 0.205
    ACET: 0.13
    PROD2: 0.276
    GLY: 0.001
    BACL: 0.031
    HCOOH: 0.103
    RCO_OH: 0.189
  A: '1.08e-15'
  B: 0.0
  C: '821.0'
- type: ARRHENIUS
  reactants:
    TERP_SURR: 1.0
    NO3: 1.0
  products:
    NO2: 0.474
    RO2_R: 0.276
    RO2_N: 0.25
    R2O2: 0.75
    RCHO: 0.474
    RNO3: 0.276
  A: '3.66e-12'
  B: 0.0
  C: '-175.0'
- type: ARRHENIUS
  reactants:
    TERP_SURR: 1.0
    O3P: 1.0
  products:
    RCHO: 0.147
    PROD2: 0.853
  A: '3.27e-11'
- type: ARRHENIUS
  reactants:
    ALK_SURR: 1.0
    OH: 1.0
  products:
    RO2_R: 0.6940658769742309
    CCHO: 0.2522563383208645
    OH: 0.06307200748129675
    HO2: 0.031023223192019948
    RO2_N: 0.14623566084788026
    CO: 0.041331359102244385
    HCHO: 0.02809886741479634
    RCHO: 0.16864957398171238
    ACET: 0.20388045511221944
    GLY: 0.06358478802992519
    HCOOH: 0.031023223192019948
    R2O2: 0.5663815980881131
    TBU_O: 0.06246986699916874
    MEK: 0.1305803200332502
    C_O2: 0.0016990336658354115
    CCO_O2: 0.0016990336658354115
    PROD2: 0.13976231296758101
  A: ((1.37e-12) * (Temp/300.0)**(2.0) * exp(-(498.0)/Temp) + (9.87e-12) * (Temp/300.0)**(0.0)
    * exp(-(671.0)/Temp) + (1.019e-11) * (Temp/300.0)**(0.0) * exp(-(434.0)/Temp)
    + (5.946e-12) * (Temp/300.0)**(0.0) * exp(-(91.0)/Temp) + (1.112e-11) * (Temp/300.0)**(0.0)
    * exp(-(52.0)/Temp)) / 5.0
  C: '0.0'
  B: '0.0'
- type: ARRHENIUS
  reactants:
    ARO_SURR: 1.0
    OH: 1.0
  products:
    HO2: 0.18937398085785181
    RO2_R: 0.8014976958525345
    RO2_N: 0.00912832328961361
    PROD2: 0.0035288904643743352
    GLY: 0.09834739454094292
    MGLY: 0.27622084367245653
    PHEN: 0.0010907479617157038
    CRES: 0.1882832328961361
    BALD: 0.05057745480326125
    DCB1: 0.5565086848635236
    DCB2: 0.09957745480326126
    DCB3: 0.09030521091811414
    BACL: 0.08141793690180786
  A: ((1.81e-12) * (Temp/300.0)**(0.0) * exp(-(-355.0)/Temp) + (2.640e-11) * (Temp/300.0)**(0.0)
    * exp(-(0.0)/Temp)) / 2.0
  B: '0.0'
  C: '0.0'
- type: ARRHENIUS
  reactants:
    OLE_SURR: 1.0
    OH: 1.0
  products:
    RO2_R: 0.9156856269113152
    RO2_N: 0.08431437308868502
    R2O2: 0.06001651376146788
    HCHO: 0.38517675840978594
    CCHO: 0.6052880733944954
    RCHO: 0.5069498470948013
    ACET: 0.09170581039755352
    PROD2: 0.034426299694189595
    MEK: 0.051170642201834864
    BALD: 0.04335290519877676
    METHACRO: 0.01776758409785933
    ISOPROD: 0.01776758409785933
  A: ((7.095e-12) * (Temp/300.0)**(0.0) * exp(-(-451.0)/Temp) + (1.743e-11) * (Temp/300.0)**(0.0)
    * exp(-(-384.0)/Temp)) / 2.0
  B: '0.0'
  C: '0.0'
- type: ARRHENIUS
  reactants:
    OLE_SURR: 1.0
    O3: 1.0
  products:
    OH: 0.19090362913567582
    HO2: 0.04746685047448064
    RO2_R: 0.023771031033598358
    RO2_N: 0.0011610028212362144
    C_O2: 0.09548134136958195
    CO: 0.33211977430110284
    HCHO: 0.4628083482944345
    CCHO: 0.20262285201333674
    RCHO: 0.35366183636829956
    ACET: 0.008084124134393434
    PROD2: 0.18730751474737115
    HCOOH: 0.166967684021544
    CCO_OH: 0.06271922287766094
    RCO_OH: 0.13960836111823544
    R2O2: 0.022057386509361374
    CCO_O2: 0.022057386509361374
    RCO_O2: 0.0009660169274172864
    MEK: 0.004186073352141574
    BALD: 0.006762118491921005
    METHACRO: 0.004186073352141574
    MVK: 0.0030590536034880737
  A: ((2.617e-15) * (Temp/300.0)**(0.0) * exp(-(1640.0)/Temp) + (5.022e-16) * (Temp/300.0)**(0.0)
    * exp(-(461.0)/Temp)) / 2.0
  B: '0.0'
  C: '0.0'
- type: ARRHENIUS
  reactants:
    OLE_SURR: 1.0
    NO3: 1.0
  products:
    RO2_R: 0.4640619949937097
    RO2_N: 0.13831015654384396
    R2O2: 0.6981208772680699
    CCHO: 0.47823855102914287
    RCHO: 0.14441605385004475
    ACET: 0.0974951947395043
    RNO3: 0.33197324358325875
    NO2: 0.3684182197839254
    C_O2: 0.028267382592117037
    HCHO: 0.0744374408259082
    MEK: 0.0009422460864039013
    BALD: 0.014133691296058518
    MVK: 0.04522781214738726
  A: ((4.453e-14) * (Temp/300.0)**(0.0) * exp(-(376.0)/Temp) + (7.265e-13) * (Temp/300.0)**(0.0)
    * exp(-(0.0)/Temp)) / 2.0
  B: '0.0'
  C: '0.0'
- type: ARRHENIUS
  reactants:
    OLE_SURR: 1.0
    O3P: 1.0
  products:
    RCHO: 0.1985327635327635
    MEK: 0.5835242165242165
    PROD2: 0.20936277302943967
    HO2: 0.008580246913580246
    RO2_R: 0.00792022792022792
    RO2_N: 0.0006600189933523267
    CO: 0.00792022792022792
    METHACRO: 0.00792022792022792
  A: ((1.074e-11) * (Temp/300.0)**(0.0) * exp(-(234.0)/Temp) + (2.085e-11) * (Temp/300.0)**(0.0)
    * exp(-(0.0)/Temp)) / 2.0
  B: '0.0'
  C: '0.0'
```

## Generated SymPy Rate Expressions
Below are the exact algebraic AST expressions evaluated by SymPy for the Unified Jacobian.

```text
R1: ARRHENIUS | Reactants: ['O3P', 'O2', 'AIR'] | Products: ['O3'] | A: 5.68e-34
R2: ARRHENIUS | Reactants: ['O3P', 'O3'] | Products: ['O2'] | A: 8.00e-12
R3: ARRHENIUS | Reactants: ['O3P', 'NO', 'AIR'] | Products: ['NO2'] | A: 1.00e-31
R4: ARRHENIUS | Reactants: ['O3P', 'NO2'] | Products: ['NO'] | A: 6.50e-12
R5: TROE | Reactants: ['O3P', 'NO2'] | Products: ['NO3'] | A: N/A
R6: ARRHENIUS | Reactants: ['O3', 'NO'] | Products: ['NO2'] | A: 1.80e-12
R7: ARRHENIUS | Reactants: ['O3', 'NO2'] | Products: ['NO3'] | A: 1.40e-13
R8: ARRHENIUS | Reactants: ['NO', 'NO3'] | Products: ['NO2'] | A: 1.80e-11
R9: ARRHENIUS | Reactants: ['NO', 'O2'] | Products: ['NO2'] | A: 3.30e-39
R10: TROE | Reactants: ['NO2', 'NO3'] | Products: ['N2O5'] | A: N/A
R11: TROE | Reactants: ['N2O5'] | Products: ['NO2', 'NO3'] | A: N/A
R12: ARRHENIUS | Reactants: ['N2O5', 'H2O'] | Products: ['HNO3'] | A: 2.60e-22
R13: ARRHENIUS | Reactants: ['NO2', 'NO3'] | Products: ['NO', 'NO2'] | A: 4.50e-14
R14: PHOTOLYSIS | Reactants: ['NO3'] | Products: ['NO'] | A: 1.59
R15: PHOTOLYSIS | Reactants: ['NO3'] | Products: ['NO2', 'O3P'] | A: 1.50e+1
R16: PHOTOLYSIS | Reactants: ['O3'] | Products: ['O3P'] | A: 3.76e-2
R17: PHOTOLYSIS | Reactants: ['O3'] | Products: ['O1D'] | A: 4.19e-3
R18: ARRHENIUS | Reactants: ['O1D', 'H2O'] | Products: ['OH'] | A: 2.20e-10
R19: ARRHENIUS | Reactants: ['O1D', 'AIR'] | Products: ['O3P'] | A: 2.09e-11
R20: TROE | Reactants: ['OH', 'NO'] | Products: ['HONO'] | A: N/A
R21: PHOTOLYSIS | Reactants: ['HONO'] | Products: ['OH', 'NO'] | A: 1.27e-1
R22: PHOTOLYSIS | Reactants: ['HONO'] | Products: ['HO2', 'NO2'] | A: 1.60e-2
R23: ARRHENIUS | Reactants: ['OH', 'HONO'] | Products: ['NO2'] | A: 2.70e-12
R24: TROE | Reactants: ['OH', 'NO2'] | Products: ['HNO3'] | A: N/A
R25: ARRHENIUS | Reactants: ['OH', 'NO3'] | Products: ['HO2', 'NO2'] | A: 2.00e-11
R26: EP2 | Reactants: ['OH', 'HNO3'] | Products: ['NO3'] | A: N/A
R27: PHOTOLYSIS | Reactants: ['HNO3'] | Products: ['OH', 'NO2'] | A: 5.40e-5
R28: EP3 | Reactants: ['OH', 'CO'] | Products: ['HO2'] | A: N/A
R29: ARRHENIUS | Reactants: ['OH', 'O3'] | Products: ['HO2'] | A: 1.90e-12
R30: ARRHENIUS | Reactants: ['HO2', 'NO'] | Products: ['OH', 'NO2'] | A: 3.40e-12
R31: TROE | Reactants: ['HO2', 'NO2'] | Products: ['HNO4'] | A: N/A
R32: TROE | Reactants: ['HNO4'] | Products: ['HO2', 'NO2'] | A: N/A
R33: PHOTOLYSIS | Reactants: ['HNO4'] | Products: ['HO2', 'NO2', 'OH', 'NO3'] | A: 4.69e-4
R34: ARRHENIUS | Reactants: ['HNO4', 'OH'] | Products: ['NO2'] | A: 1.50e-12
R35: ARRHENIUS | Reactants: ['HO2', 'O3'] | Products: ['OH'] | A: 1.40e-14
R36: EP3 | Reactants: ['HO2'] | Products: ['H2O2'] | A: N/A
R37: EP3 | Reactants: ['HO2', 'H2O'] | Products: ['H2O2'] | A: N/A
R38: ARRHENIUS | Reactants: ['NO3', 'HO2'] | Products: ['OH', 'NO2', 'HNO3'] | A: 4.00e-12
R39: ARRHENIUS | Reactants: ['NO3'] | Products: ['NO2'] | A: 8.50e-13
R40: PHOTOLYSIS | Reactants: ['H2O2'] | Products: ['OH'] | A: 5.64e-4
R41: ARRHENIUS | Reactants: ['H2O2', 'OH'] | Products: ['HO2'] | A: 2.90e-12
R42: ARRHENIUS | Reactants: ['OH', 'HO2'] | Products: ['H2O', 'O2'] | A: 4.80e-11
R43: TROE | Reactants: ['OH', 'SO2'] | Products: ['HO2', 'H2SO4'] | A: N/A
R44: ARRHENIUS | Reactants: ['OH', 'H2'] | Products: ['HO2'] | A: 7.70e-12
R45: ARRHENIUS | Reactants: ['C_O2', 'NO'] | Products: ['NO2', 'HCHO', 'HO2'] | A: 2.80e-12
R46: ARRHENIUS | Reactants: ['C_O2', 'HO2'] | Products: ['COOH'] | A: 3.80e-13
R47: ARRHENIUS | Reactants: ['C_O2', 'NO3'] | Products: ['HCHO', 'HO2', 'NO2'] | A: 1.30e-12
R48: ARRHENIUS | Reactants: ['C_O2'] | Products: ['MEOH', 'HCHO'] | A: 2.45e-14
R49: ARRHENIUS | Reactants: ['C_O2'] | Products: ['HCHO', 'HO2'] | A: 5.90e-13
R50: ARRHENIUS | Reactants: ['RO2_R', 'NO'] | Products: ['NO2', 'HO2'] | A: 2.70e-12
R51: ARRHENIUS | Reactants: ['RO2_R', 'HO2'] | Products: ['ROOH'] | A: 1.90e-13
R52: ARRHENIUS | Reactants: ['RO2_R', 'NO3'] | Products: ['NO2', 'HO2'] | A: 2.30e-12
R53: ARRHENIUS | Reactants: ['RO2_R', 'C_O2'] | Products: ['HO2', 'HCHO', 'MEOH'] | A: 2.00e-13
R54: ARRHENIUS | Reactants: ['RO2_R'] | Products: ['HO2'] | A: 3.50e-14
R55: ARRHENIUS | Reactants: ['R2O2', 'NO'] | Products: ['NO2'] | A: 2.70e-12
R56: ARRHENIUS | Reactants: ['R2O2', 'HO2'] | Products: ['HO2'] | A: 1.90e-13
R57: ARRHENIUS | Reactants: ['R2O2', 'NO3'] | Products: ['NO2'] | A: 2.30e-12
R58: ARRHENIUS | Reactants: ['R2O2', 'C_O2'] | Products: ['C_O2'] | A: 2.00e-13
R59: ARRHENIUS | Reactants: ['R2O2', 'RO2_R'] | Products: ['RO2_R'] | A: 3.50e-14
R60: ARRHENIUS | Reactants: ['R2O2'] | Products: ['R2O2'] | A: 0.0
R61: ARRHENIUS | Reactants: ['RO2_N', 'NO'] | Products: ['RNO3'] | A: 2.70e-12
R62: ARRHENIUS | Reactants: ['RO2_N', 'HO2'] | Products: ['ROOH'] | A: 1.90e-13
R63: ARRHENIUS | Reactants: ['RO2_N', 'C_O2'] | Products: ['HO2', 'MEOH', 'MEK', 'PROD2', 'HCHO'] | A: 2.00e-13
R64: ARRHENIUS | Reactants: ['RO2_N', 'NO3'] | Products: ['NO2', 'HO2', 'MEK'] | A: 2.30e-12
R65: ARRHENIUS | Reactants: ['RO2_N', 'RO2_R'] | Products: ['HO2', 'MEK', 'PROD2'] | A: 3.50e-14
R66: ARRHENIUS | Reactants: ['RO2_N', 'R2O2'] | Products: ['RO2_N'] | A: 3.50e-14
R67: ARRHENIUS | Reactants: ['RO2_N'] | Products: ['MEK', 'HO2', 'PROD2'] | A: 3.50e-14
R68: TROE | Reactants: ['CCO_O2', 'NO2'] | Products: ['PAN'] | A: N/A
R69: TROE | Reactants: ['PAN'] | Products: ['CCO_O2', 'NO2'] | A: N/A
R70: ARRHENIUS | Reactants: ['CCO_O2', 'NO'] | Products: ['C_O2', 'NO2'] | A: 7.80e-12
R71: ARRHENIUS | Reactants: ['CCO_O2', 'HO2'] | Products: ['CCO_OOH', 'CCO_OH', 'O3'] | A: 4.30e-13
R72: ARRHENIUS | Reactants: ['CCO_O2', 'NO3'] | Products: ['C_O2', 'NO2'] | A: 4.00e-12
R73: ARRHENIUS | Reactants: ['CCO_O2', 'C_O2'] | Products: ['CCO_OH', 'HCHO'] | A: 1.80e-12
R74: ARRHENIUS | Reactants: ['CCO_O2', 'RO2_R'] | Products: ['CCO_OH'] | A: 7.50e-12
R75: ARRHENIUS | Reactants: ['CCO_O2', 'R2O2'] | Products: ['CCO_O2'] | A: 7.50e-12
R76: ARRHENIUS | Reactants: ['CCO_O2', 'RO2_N'] | Products: ['CCO_OH', 'PROD2'] | A: 7.50e-12
R77: ARRHENIUS | Reactants: ['CCO_O2'] | Products: ['C_O2'] | A: 2.90e-12
R78: ARRHENIUS | Reactants: ['RCO_O2', 'NO2'] | Products: ['PAN2'] | A: 1.20e-11
R79: ARRHENIUS | Reactants: ['PAN2'] | Products: ['RCO_O2', 'NO2'] | A: 2.00e+15
R80: ARRHENIUS | Reactants: ['RCO_O2', 'NO'] | Products: ['NO2', 'CCHO', 'RO2_R'] | A: 1.25e-11
R81: ARRHENIUS | Reactants: ['RCO_O2', 'HO2'] | Products: ['RCO_OOH', 'RCO_OH', 'O3'] | A: 4.30e-13
R82: ARRHENIUS | Reactants: ['RCO_O2', 'NO3'] | Products: ['NO2', 'CCHO', 'RO2_R'] | A: 4.00e-12
R83: ARRHENIUS | Reactants: ['RCO_O2', 'C_O2'] | Products: ['RCO_OH', 'HCHO'] | A: 1.80e-12
R84: ARRHENIUS | Reactants: ['RCO_O2', 'RO2_R'] | Products: ['RCO_OH'] | A: 7.50e-12
R85: ARRHENIUS | Reactants: ['RCO_O2', 'R2O2'] | Products: ['RCO_O2'] | A: 7.50e-12
R86: ARRHENIUS | Reactants: ['RCO_O2', 'RO2_N'] | Products: ['RCO_OH', 'PROD2'] | A: 7.50e-12
R87: ARRHENIUS | Reactants: ['RCO_O2', 'CCO_O2'] | Products: ['C_O2', 'CCHO', 'RO2_R'] | A: 2.90e-12
R88: ARRHENIUS | Reactants: ['RCO_O2'] | Products: ['CCHO', 'RO2_R'] | A: 2.90e-12
R89: ARRHENIUS | Reactants: ['BZCO_O2', 'NO2'] | Products: ['PBZN'] | A: 1.37e-11
R90: ARRHENIUS | Reactants: ['PBZN'] | Products: ['BZCO_O2', 'NO2'] | A: 7.90e+16
R91: ARRHENIUS | Reactants: ['BZCO_O2', 'NO'] | Products: ['NO2', 'BZ_O', 'R2O2'] | A: 1.25e-11
R92: ARRHENIUS | Reactants: ['BZCO_O2', 'HO2'] | Products: ['RCO_OOH', 'RCO_OH', 'O3'] | A: 4.30e-13
R93: ARRHENIUS | Reactants: ['BZCO_O2', 'NO3'] | Products: ['NO2', 'BZ_O', 'R2O2'] | A: 4.00e-12
R94: ARRHENIUS | Reactants: ['BZCO_O2', 'C_O2'] | Products: ['RCO_OH', 'HCHO'] | A: 1.80e-12
R95: ARRHENIUS | Reactants: ['BZCO_O2', 'RO2_R'] | Products: ['RCO_OH'] | A: 7.50e-12
R96: ARRHENIUS | Reactants: ['BZCO_O2', 'R2O2'] | Products: ['BZCO_O2'] | A: 7.50e-12
R97: ARRHENIUS | Reactants: ['BZCO_O2', 'RO2_N'] | Products: ['RCO_OH', 'PROD2'] | A: 7.50e-12
R98: ARRHENIUS | Reactants: ['BZCO_O2', 'CCO_O2'] | Products: ['C_O2', 'BZ_O', 'R2O2'] | A: 2.90e-12
R99: ARRHENIUS | Reactants: ['BZCO_O2', 'RCO_O2'] | Products: ['CCHO', 'RO2_R', 'BZ_O', 'R2O2'] | A: 2.90e-12
R100: ARRHENIUS | Reactants: ['BZCO_O2'] | Products: ['BZ_O', 'R2O2'] | A: 2.90e-12
R101: ARRHENIUS | Reactants: ['MA_RCO3', 'NO2'] | Products: ['MA_PAN'] | A: 1.20e-11
R102: ARRHENIUS | Reactants: ['MA_PAN'] | Products: ['MA_RCO3', 'NO2'] | A: 1.60e+16
R103: ARRHENIUS | Reactants: ['MA_RCO3', 'NO'] | Products: ['NO2', 'HCHO', 'CCO_O2'] | A: 1.25e-11
R104: ARRHENIUS | Reactants: ['MA_RCO3', 'HO2'] | Products: ['RCO_OOH', 'RCO_OH', 'O3'] | A: 4.30e-13
R105: ARRHENIUS | Reactants: ['MA_RCO3', 'NO3'] | Products: ['NO2', 'HCHO', 'CCO_O2'] | A: 4.00e-12
R106: ARRHENIUS | Reactants: ['MA_RCO3', 'C_O2'] | Products: ['RCO_OH', 'HCHO'] | A: 1.80e-12
R107: ARRHENIUS | Reactants: ['MA_RCO3', 'RO2_R'] | Products: ['RCO_OH'] | A: 7.50e-12
R108: ARRHENIUS | Reactants: ['MA_RCO3', 'R2O2'] | Products: ['MA_RCO3'] | A: 7.50e-12
R109: ARRHENIUS | Reactants: ['MA_RCO3', 'RO2_N'] | Products: ['RCO_OH'] | A: 7.50e-12
R110: ARRHENIUS | Reactants: ['MA_RCO3', 'CCO_O2'] | Products: ['C_O2', 'HCHO', 'CCO_O2'] | A: 2.90e-12
R111: ARRHENIUS | Reactants: ['MA_RCO3', 'RCO_O2'] | Products: ['HCHO', 'CCO_O2', 'CCHO', 'RO2_R'] | A: 2.90e-12
R112: ARRHENIUS | Reactants: ['MA_RCO3', 'BZCO_O2'] | Products: ['HCHO', 'CCO_O2', 'BZ_O', 'R2O2'] | A: 2.90e-12
R113: ARRHENIUS | Reactants: ['MA_RCO3'] | Products: ['HCHO', 'CCO_O2'] | A: 2.90e-12
R114: ARRHENIUS | Reactants: ['TBU_O', 'NO2'] | Products: ['RNO3'] | A: 2.40e-11
R115: ARRHENIUS | Reactants: ['TBU_O'] | Products: ['ACET', 'C_O2'] | A: 7.50e+14
R116: ARRHENIUS | Reactants: ['BZ_O', 'NO2'] | Products: ['NPHE'] | A: 2.30e-11
R117: ARRHENIUS | Reactants: ['BZ_O', 'HO2'] | Products: ['PHEN'] | A: 1.90e-13
R118: ARRHENIUS | Reactants: ['BZ_O'] | Products: ['PHEN'] | A: 1.00e-03
R119: ARRHENIUS | Reactants: ['BZNO2_O', 'NO2'] | Products: ['XN', 'XC'] | A: 7.50e+14
R120: ARRHENIUS | Reactants: ['BZNO2_O', 'HO2'] | Products: ['NPHE'] | A: 2.30e-11
R121: ARRHENIUS | Reactants: ['BZNO2_O'] | Products: ['NPHE'] | A: 1.90e-13
R122: PHOTOLYSIS | Reactants: ['HCHO'] | Products: ['HO2', 'CO'] | A: 2.32e-3
R123: PHOTOLYSIS | Reactants: ['HCHO'] | Products: ['CO'] | A: 3.15e-3
R124: ARRHENIUS | Reactants: ['HCHO', 'OH'] | Products: ['HO2', 'CO'] | A: 8.60e-12
R125: ARRHENIUS | Reactants: ['HCHO', 'HO2'] | Products: ['HOCOO'] | A: 9.70e-15
R126: ARRHENIUS | Reactants: ['HOCOO'] | Products: ['HO2', 'HCHO'] | A: 2.40e+12
R127: ARRHENIUS | Reactants: ['HOCOO', 'NO'] | Products: ['HCOOH', 'NO2', 'HO2'] | A: 2.80e-12
R128: ARRHENIUS | Reactants: ['HCHO', 'NO3'] | Products: ['HNO3', 'HO2', 'CO'] | A: 2.00e-12
R129: ARRHENIUS | Reactants: ['CCHO', 'OH'] | Products: ['CCO_O2'] | A: 5.60e-12
R130: PHOTOLYSIS | Reactants: ['CCHO'] | Products: ['CO', 'HO2', 'C_O2'] | A: 4.16e-4
R131: ARRHENIUS | Reactants: ['CCHO', 'NO3'] | Products: ['HNO3', 'CCO_O2'] | A: 1.40e-12
R132: ARRHENIUS | Reactants: ['RCHO', 'OH'] | Products: ['RO2_R', 'RO2_N', 'RCO_O2', 'CO', 'CCHO'] | A: 2.00e-11
R133: PHOTOLYSIS | Reactants: ['RCHO'] | Products: ['CCHO', 'RO2_R', 'CO', 'HO2'] | A: 1.40e-3
R134: ARRHENIUS | Reactants: ['RCHO', 'NO3'] | Products: ['HNO3', 'RCO_O2'] | A: 1.40e-12
R135: ARRHENIUS | Reactants: ['ACET', 'OH'] | Products: ['HCHO', 'CCO_O2', 'R2O2'] | A: 1.10e-12
R136: PHOTOLYSIS | Reactants: ['ACET'] | Products: ['CCO_O2', 'C_O2'] | A: 4.16e-5
R137: ARRHENIUS | Reactants: ['MEK', 'OH'] | Products: ['RO2_R', 'RO2_N', 'R2O2', 'CCO_O2', 'RCO_O2', 'HCHO', 'CCHO', 'RCHO'] | A: 1.30e-12
R138: PHOTOLYSIS | Reactants: ['MEK'] | Products: ['CCO_O2', 'CCHO', 'RO2_R'] | A: 9.49e-4*(1.50e-1*SUN/60.0)
R139: ARRHENIUS | Reactants: ['MEOH', 'OH'] | Products: ['HCHO', 'HO2'] | A: 3.10e-12
R140: ARRHENIUS | Reactants: ['COOH', 'OH'] | Products: ['HCHO', 'OH', 'C_O2'] | A: 2.90e-12
R141: PHOTOLYSIS | Reactants: ['COOH'] | Products: ['HCHO', 'HO2', 'OH'] | A: 3.94e-4
R142: ARRHENIUS | Reactants: ['ROOH', 'OH'] | Products: ['RCHO', 'RO2_R', 'OH'] | A: 1.10e-11
R143: PHOTOLYSIS | Reactants: ['ROOH'] | Products: ['RCHO', 'HO2', 'OH'] | A: 3.94e-4
R144: PHOTOLYSIS | Reactants: ['GLY'] | Products: ['CO', 'HO2'] | A: 8.93e-3
R145: PHOTOLYSIS | Reactants: ['GLY'] | Products: ['HCHO', 'CO'] | A: 1.81e-1*(6.00e-3*SUN/60.0)
R146: ARRHENIUS | Reactants: ['GLY', 'OH'] | Products: ['HO2', 'CO', 'RCO_O2'] | A: 1.10e-11
R147: ARRHENIUS | Reactants: ['GLY', 'NO3'] | Products: ['HNO3', 'HO2', 'CO', 'RCO_O2'] | A: 2.80e-12
R148: PHOTOLYSIS | Reactants: ['MGLY'] | Products: ['HO2', 'CO', 'CCO_O2'] | A: 1.10e-2
R149: ARRHENIUS | Reactants: ['MGLY', 'OH'] | Products: ['CO', 'CCO_O2'] | A: 1.50e-11
R150: ARRHENIUS | Reactants: ['MGLY', 'NO3'] | Products: ['HNO3', 'CO', 'CCO_O2'] | A: 1.40e-12
R151: PHOTOLYSIS | Reactants: ['BACL'] | Products: ['CCO_O2'] | A: 1.90e-2
R152: ARRHENIUS | Reactants: ['PHEN', 'OH'] | Products: ['BZ_O', 'RO2_R', 'GLY'] | A: 2.63e-11
R153: ARRHENIUS | Reactants: ['PHEN', 'NO3'] | Products: ['HNO3', 'BZ_O'] | A: 3.78e-12
R154: ARRHENIUS | Reactants: ['CRES', 'OH'] | Products: ['BZ_O', 'RO2_R', 'MGLY'] | A: 4.20e-11
R155: ARRHENIUS | Reactants: ['CRES', 'NO3'] | Products: ['HNO3', 'BZ_O'] | A: 1.37e-11
R156: ARRHENIUS | Reactants: ['NPHE', 'NO3'] | Products: ['HNO3', 'BZNO2_O'] | A: 3.78e-12
R157: ARRHENIUS | Reactants: ['BALD', 'OH'] | Products: ['BZCO_O2'] | A: 1.29e-11
R158: PHOTOLYSIS | Reactants: ['BALD'] | Products: ['XC'] | A: 6.22e-2*(5.00e-2*SUN/60.0)
R159: ARRHENIUS | Reactants: ['BALD', 'NO3'] | Products: ['HNO3', 'BZCO_O2'] | A: 1.40e-12
R160: ARRHENIUS | Reactants: ['METHACRO', 'OH'] | Products: ['RO2_R', 'CO', 'HCHO', 'MEK', 'MGLY', 'MA_RCO3'] | A: 1.86e-11
R161: ARRHENIUS | Reactants: ['METHACRO', 'O3'] | Products: ['HO2', 'RO2_R', 'OH', 'RCO_O2', 'CO', 'HCHO', 'MGLY', 'HCOOH'] | A: 1.36e-15
R162: ARRHENIUS | Reactants: ['METHACRO', 'NO3'] | Products: ['HNO3', 'RO2_R', 'CO', 'MA_RCO3'] | A: 1.50e-12
R163: ARRHENIUS | Reactants: ['METHACRO', 'O3P'] | Products: ['RCHO'] | A: 6.34e-12
R164: PHOTOLYSIS | Reactants: ['METHACRO'] | Products: ['HO2', 'RO2_R', 'OH', 'CCO_O2', 'CO', 'HCHO', 'MA_RCO3'] | A: 3.32e-2*(4.10e-3*SUN/60.0)
R165: ARRHENIUS | Reactants: ['MVK', 'OH'] | Products: ['RO2_R', 'RO2_N', 'R2O2', 'CCO_O2', 'HCHO', 'RCHO', 'MGLY'] | A: 4.14e-12
R166: ARRHENIUS | Reactants: ['MVK', 'O3'] | Products: ['HO2', 'RO2_R', 'OH', 'RCO_O2', 'CO', 'HCHO', 'MGLY', 'HCOOH'] | A: 7.51e-16
R167: ARRHENIUS | Reactants: ['MVK', 'O3P'] | Products: ['RCHO', 'MEK'] | A: 4.32e-12
R168: PHOTOLYSIS | Reactants: ['MVK'] | Products: ['C_O2', 'CO', 'PROD2', 'MA_RCO3'] | A: 3.32e-2*(2.10e-3*SUN/60.0)
R169: ARRHENIUS | Reactants: ['ISOPROD', 'OH'] | Products: ['RO2_R', 'RO2_N', 'MA_RCO3', 'CO', 'HCHO', 'CCHO', 'RCHO', 'MEK', 'PROD2', 'GLY', 'MGLY'] | A: 6.19e-11
R170: ARRHENIUS | Reactants: ['ISOPROD', 'O3'] | Products: ['HO2', 'RO2_R', 'RCO_O2', 'OH', 'CO', 'HCHO', 'CCHO', 'MEK', 'GLY', 'MGLY', 'HCOOH', 'RCO_OH'] | A: 4.18e-18
R171: ARRHENIUS | Reactants: ['ISOPROD', 'NO3'] | Products: ['RO2_R', 'RO2_N', 'MA_RCO3', 'CO', 'HNO3', 'HCHO', 'RCHO', 'MGLY', 'RNO3'] | A: 1.00e-13
R172: PHOTOLYSIS | Reactants: ['ISOPROD'] | Products: ['HO2', 'CCO_O2', 'RCO_O2', 'CO', 'HCHO', 'CCHO', 'MEK'] | A: 3.32e-2*(4.10e-3*SUN/60.0)
R173: ARRHENIUS | Reactants: ['PROD2', 'OH'] | Products: ['HO2', 'RO2_R', 'RO2_N', 'CCO_O2', 'RCO_O2', 'HCHO', 'CCHO', 'RCHO', 'MEK', 'PROD2'] | A: 1.50e-11
R174: PHOTOLYSIS | Reactants: ['PROD2'] | Products: ['RO2_R', 'RO2_N', 'R2O2', 'CCO_O2', 'RCO_O2', 'HCHO', 'CCHO', 'RCHO'] | A: 9.49e-4*(2.00e-2*SUN/60.0)
R175: ARRHENIUS | Reactants: ['RNO3', 'OH'] | Products: ['NO2', 'HO2', 'RO2_R', 'RO2_N', 'R2O2', 'HCHO', 'CCHO', 'RCHO', 'ACET', 'MEK', 'PROD2', 'RNO3'] | A: 7.80e-12
R176: PHOTOLYSIS | Reactants: ['RNO3'] | Products: ['NO2', 'HO2', 'RO2_R', 'RO2_N', 'R2O2', 'HCHO', 'CCHO', 'RCHO', 'ACET', 'MEK', 'PROD2'] | A: 2.35e-4
R177: ARRHENIUS | Reactants: ['DCB1', 'OH'] | Products: ['RCHO', 'RO2_R', 'CO'] | A: 5.00e-11
R178: ARRHENIUS | Reactants: ['DCB1', 'O3'] | Products: ['HO2', 'OH', 'CO', 'GLY'] | A: 2.00e-18
R179: ARRHENIUS | Reactants: ['DCB2', 'OH'] | Products: ['R2O2', 'RCHO', 'CCO_O2'] | A: 5.00e-11
R180: PHOTOLYSIS | Reactants: ['DCB2'] | Products: ['RO2_R', 'CCO_O2', 'HO2', 'CO', 'R2O2', 'GLY', 'MGLY'] | A: 2.06e-1*(3.65e-1*SUN/60.0)
R181: ARRHENIUS | Reactants: ['DCB3', 'OH'] | Products: ['R2O2', 'RCHO', 'CCO_O2'] | A: 5.00e-11
R182: PHOTOLYSIS | Reactants: ['DCB3'] | Products: ['RO2_R', 'CCO_O2', 'HO2', 'CO', 'R2O2', 'GLY', 'MGLY'] | A: 3.32e-2*(7.28*SUN/60.0)
R183: ARRHENIUS | Reactants: ['CH4', 'OH'] | Products: ['C_O2'] | A: 2.15e-12
R184: ARRHENIUS | Reactants: ['ETHENE', 'OH'] | Products: ['RO2_R', 'HCHO', 'CCHO'] | A: 1.96e-12
R185: ARRHENIUS | Reactants: ['ETHENE', 'O3'] | Products: ['OH', 'HO2', 'CO', 'HCHO', 'HCOOH'] | A: 9.14e-15
R186: ARRHENIUS | Reactants: ['ETHENE', 'NO3'] | Products: ['RO2_R', 'RCHO'] | A: 4.39e-13
R187: ARRHENIUS | Reactants: ['ETHENE', 'O3P'] | Products: ['HO2', 'RO2_R', 'C_O2', 'CO', 'HCHO', 'CCHO', 'GLY'] | A: 1.04e-11
R188: ARRHENIUS | Reactants: ['ISOPRENE', 'OH'] | Products: ['RO2_R', 'RO2_N', 'R2O2', 'HCHO', 'METHACRO', 'MVK', 'ISOPROD'] | A: 2.50e-11
R189: ARRHENIUS | Reactants: ['ISOPRENE', 'O3'] | Products: ['OH', 'RO2_R', 'RO2_N', 'R2O2', 'MA_RCO3', 'CO', 'HCHO', 'PROD2', 'METHACRO', 'MVK', 'HCOOH', 'RCO_OH'] | A: 7.86e-15
R190: ARRHENIUS | Reactants: ['ISOPRENE', 'NO3'] | Products: ['NO2', 'RO2_R', 'RO2_N', 'R2O2', 'ISOPROD'] | A: 3.03e-12
R191: ARRHENIUS | Reactants: ['ISOPRENE', 'O3P'] | Products: ['RO2_N', 'R2O2', 'C_O2', 'MA_RCO3', 'HCHO', 'PROD2'] | A: 3.60e-11
R192: ARRHENIUS | Reactants: ['TERP_SURR', 'OH'] | Products: ['RO2_R', 'RO2_N', 'R2O2', 'HCHO', 'RCHO', 'PROD2'] | A: 1.83e-11
R193: ARRHENIUS | Reactants: ['TERP_SURR', 'O3'] | Products: ['OH', 'HO2', 'RO2_R', 'RO2_N', 'R2O2', 'CCO_O2', 'RCO_O2', 'CO', 'HCHO', 'RCHO', 'ACET', 'PROD2', 'GLY', 'BACL', 'HCOOH', 'RCO_OH'] | A: 1.08e-15
R194: ARRHENIUS | Reactants: ['TERP_SURR', 'NO3'] | Products: ['NO2', 'RO2_R', 'RO2_N', 'R2O2', 'RCHO', 'RNO3'] | A: 3.66e-12
R195: ARRHENIUS | Reactants: ['TERP_SURR', 'O3P'] | Products: ['RCHO', 'PROD2'] | A: 3.27e-11
R196: ARRHENIUS | Reactants: ['ALK_SURR', 'OH'] | Products: ['RO2_R', 'CCHO', 'OH', 'HO2', 'RO2_N', 'CO', 'HCHO', 'RCHO', 'ACET', 'GLY', 'HCOOH', 'R2O2', 'TBU_O', 'MEK', 'C_O2', 'CCO_O2', 'PROD2'] | A: ((1.37e-12) * (Temp/300.0)**(2.0) * exp(-(498.0)/Temp) + (9.87e-12) * (Temp/300.0)**(0.0) * exp(-(671.0)/Temp) + (1.019e-11) * (Temp/300.0)**(0.0) * exp(-(434.0)/Temp) + (5.946e-12) * (Temp/300.0)**(0.0) * exp(-(91.0)/Temp) + (1.112e-11) * (Temp/300.0)**(0.0) * exp(-(52.0)/Temp)) / 5.0
R197: ARRHENIUS | Reactants: ['ARO_SURR', 'OH'] | Products: ['HO2', 'RO2_R', 'RO2_N', 'PROD2', 'GLY', 'MGLY', 'PHEN', 'CRES', 'BALD', 'DCB1', 'DCB2', 'DCB3', 'BACL'] | A: ((1.81e-12) * (Temp/300.0)**(0.0) * exp(-(-355.0)/Temp) + (2.640e-11) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0
R198: ARRHENIUS | Reactants: ['OLE_SURR', 'OH'] | Products: ['RO2_R', 'RO2_N', 'R2O2', 'HCHO', 'CCHO', 'RCHO', 'ACET', 'PROD2', 'MEK', 'BALD', 'METHACRO', 'ISOPROD'] | A: ((7.095e-12) * (Temp/300.0)**(0.0) * exp(-(-451.0)/Temp) + (1.743e-11) * (Temp/300.0)**(0.0) * exp(-(-384.0)/Temp)) / 2.0
R199: ARRHENIUS | Reactants: ['OLE_SURR', 'O3'] | Products: ['OH', 'HO2', 'RO2_R', 'RO2_N', 'C_O2', 'CO', 'HCHO', 'CCHO', 'RCHO', 'ACET', 'PROD2', 'HCOOH', 'CCO_OH', 'RCO_OH', 'R2O2', 'CCO_O2', 'RCO_O2', 'MEK', 'BALD', 'METHACRO', 'MVK'] | A: ((2.617e-15) * (Temp/300.0)**(0.0) * exp(-(1640.0)/Temp) + (5.022e-16) * (Temp/300.0)**(0.0) * exp(-(461.0)/Temp)) / 2.0
R200: ARRHENIUS | Reactants: ['OLE_SURR', 'NO3'] | Products: ['RO2_R', 'RO2_N', 'R2O2', 'CCHO', 'RCHO', 'ACET', 'RNO3', 'NO2', 'C_O2', 'HCHO', 'MEK', 'BALD', 'MVK'] | A: ((4.453e-14) * (Temp/300.0)**(0.0) * exp(-(376.0)/Temp) + (7.265e-13) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0
R201: ARRHENIUS | Reactants: ['OLE_SURR', 'O3P'] | Products: ['RCHO', 'MEK', 'PROD2', 'HO2', 'RO2_R', 'RO2_N', 'CO', 'METHACRO'] | A: ((1.074e-11) * (Temp/300.0)**(0.0) * exp(-(234.0)/Temp) + (2.085e-11) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0
d[O3]/dt = (IMPLICIT: -1.0*((2.617e-15) * (Temp/300.0)**(0.0) * exp(-(1640.0)/Temp) + (5.022e-16) * (Temp/300.0)**(0.0) * exp(-(461.0)/Temp)) / 2.0*C_O3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*1.08e-15*C_O3*C_TERP_SURR*(Temp/300)**0.0*exp(-821.0/Temp) - 1.0*1.36e-15*C_METHACRO*C_O3*(Temp/300)**0.0*exp(-2114.0/Temp) - 1.0*1.40e-13*C_NO2*C_O3*(Temp/300)**0.0*exp(-2470.0/Temp) - 1.0*1.40e-14*C_HO2*C_O3*(Temp/300)**0.0*exp(-600.0/Temp) - 1.0*1.80e-12*C_NO*C_O3*(Temp/300)**0.0*exp(-1370.0/Temp) - 1.0*1.90e-12*C_O3*C_OH*(Temp/300)**0.0*exp(-1000.0/Temp) - 1.0*2.00e-18*C_DCB1*C_O3*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*3.76e-2*C_O3 - 1.0*4.18e-18*C_ISOPROD*C_O3*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*4.19e-3*C_O3 + 0.25*4.30e-13*C_BZCO_O2*C_HO2*(Temp/300)**0.0*exp(--1040.0/Temp) + 0.25*4.30e-13*C_CCO_O2*C_HO2*(Temp/300)**0.0*exp(--1040.0/Temp) + 0.25*4.30e-13*C_HO2*C_MA_RCO3*(Temp/300)**0.0*exp(--1040.0/Temp) + 0.25*4.30e-13*C_HO2*C_RCO_O2*(Temp/300)**0.0*exp(--1040.0/Temp) + 1.0*5.68e-34*C_AIR*C_O2*C_O3P*(Temp/300)**-2.80*exp(-0.0/Temp) - 1.0*7.51e-16*C_MVK*C_O3*(Temp/300)**0.0*exp(-1520.0/Temp) - 1.0*7.86e-15*C_ISOPRENE*C_O3*(Temp/300)**0.0*exp(-1912.0/Temp) - 1.0*8.00e-12*C_O3*C_O3P*(Temp/300)**0.0*exp(-2060.0/Temp) - 1.0*9.14e-15*C_ETHENE*C_O3*(Temp/300)**0.0*exp(-2580.0/Temp)) + (EXPLICIT: 0)
d[H2O2]/dt = (IMPLICIT: -1.0*2.90e-12*C_H2O2*C_OH*(Temp/300)**0.0*exp(-160.0/Temp) - 1.0*5.64e-4*C_H2O2 + 1.0*C_H2O*C_HO2**2*(1000000.0*2.59e-54*exp(--3180.0/Temp) + 3.08e-34*exp(--2800.0/Temp)) + 1.0*C_HO2**2*(1000000.0*1.85e-33*exp(--980.0/Temp) + 2.20e-13*exp(--600.0/Temp))) + (EXPLICIT: 0)
d[NO]/dt = (IMPLICIT: -1000000.0*0.60**(1.0/(log(1000000.0*7.00e-31*(Temp/300)**-2.60/(3.60e-11*(Temp/300)**-0.10))**2/log(10)**2 + 1.0))*7.00e-31*C_NO*C_OH*(Temp/300)**-2.60*exp(-0.0/Temp)/(1.0 + 1000000.0*7.00e-31*(Temp/300)**-2.60/(3.60e-11*(Temp/300)**-0.10)) - 1.0*1.00e-31*C_AIR*C_NO*C_O3P*(Temp/300)**-1.60*exp(-0.0/Temp) - 1.0*1.25e-11*C_BZCO_O2*C_NO*(Temp/300)**0.0*exp(--240.0/Temp) - 1.0*1.25e-11*C_MA_RCO3*C_NO*(Temp/300)**0.0*exp(--240.0/Temp) - 1.0*1.25e-11*C_NO*C_RCO_O2*(Temp/300)**0.0*exp(--240.0/Temp) + 1.0*1.27e-1*C_HONO + 1.0*1.59*C_NO3 - 1.0*1.80e-11*C_NO*C_NO3*(Temp/300)**0.0*exp(--110.0/Temp) - 1.0*1.80e-12*C_NO*C_O3*(Temp/300)**0.0*exp(-1370.0/Temp) - 1.0*2.70e-12*C_NO*C_R2O2*(Temp/300)**0.0*exp(--360.0/Temp) - 1.0*2.70e-12*C_NO*C_RO2_N*(Temp/300)**0.0*exp(--360.0/Temp) - 1.0*2.70e-12*C_NO*C_RO2_R*(Temp/300)**0.0*exp(--360.0/Temp) - 1.0*2.80e-12*C_C_O2*C_NO*(Temp/300)**0.0*exp(--285.0/Temp) - 1.0*2.80e-12*C_HOCOO*C_NO*(Temp/300)**0.0*exp(--285.0/Temp) - 2.0*3.30e-39*C_NO**2*C_O2*(Temp/300)**0.0*exp(--530.0/Temp) - 1.0*3.40e-12*C_HO2*C_NO*(Temp/300)**0.0*exp(--270.0/Temp) + 1.0*4.50e-14*C_NO2*C_NO3*(Temp/300)**0.0*exp(-1260.0/Temp) + 1.0*6.50e-12*C_NO2*C_O3P*(Temp/300)**0.0*exp(-- 120.0/Temp) - 1.0*7.80e-12*C_CCO_O2*C_NO*(Temp/300)**0.0*exp(--300.0/Temp)) + (EXPLICIT: 0)
d[NO2]/dt = (IMPLICIT: 0.368418219783925*((4.453e-14) * (Temp/300.0)**(0.0) * exp(-(376.0)/Temp) + (7.265e-13) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_NO3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 1000000.0*0.3**(1.0/(log(1000000.0*4.90e-3*(Temp/300)**0.0*exp(-12100.0/Temp)*exp(13600.0/Temp)/(4.0e+16*(Temp/300)**0.))**2/log(10)**2 + 1.0))*4.90e-3*C_PAN*(Temp/300)**0.0*exp(-12100.0/Temp)/(1.0 + 1000000.0*4.90e-3*(Temp/300)**0.0*exp(-12100.0/Temp)*exp(13600.0/Temp)/(4.0e+16*(Temp/300)**0.)) - 1000000.0*0.30**(1.0/(log(1000000.0*2.70e-28*(Temp/300)**-7.10/(1.20e-11*(Temp/300)**-0.90))**2/log(10)**2 + 1.0))*2.70e-28*C_CCO_O2*C_NO2*(Temp/300)**-7.10*exp(-0.0/Temp)/(1.0 + 1000000.0*2.70e-28*(Temp/300)**-7.10/(1.20e-11*(Temp/300)**-0.90)) - 1000000.0*0.45**(1.0/(log(1000000.0*2.80e-30*(Temp/300)**-3.50/(2.00e-12*(Temp/300)**0.20))**2/log(10)**2 + 1.0))*2.80e-30*C_NO2*C_NO3*(Temp/300)**-3.50*exp(-0.0/Temp)/(1.0 + 1000000.0*2.80e-30*(Temp/300)**-3.50/(2.00e-12*(Temp/300)**0.20)) + 1000000.0*0.45**(1.0/(log(1000000.0*1.e-3*(Temp/300)**-3.5*exp(-11000.0/Temp)*exp(11080.0/Temp)/(9.7e+14*(Temp/300)**0.1))**2/log(10)**2 + 1.0))*1.e-3*C_N2O5*(Temp/300)**-3.5*exp(-11000.0/Temp)/(1000000.0*1.e-3*(Temp/300)**-3.5*exp(-11000.0/Temp)*exp(11080.0/Temp)/(9.7e+14*(Temp/300)**0.1) + 1.0) + 1000000.0*0.5**(1.0/(log(1000000.0*4.10e-05*exp(-10650.0/Temp)*exp(11170.0/Temp)/5.7e+15)**2/log(10)**2 + 1.0))*4.10e-05*C_HNO4*(Temp/300)**0.0*exp(-10650.0/Temp)/(1000000.0*4.10e-05*exp(-10650.0/Temp)*exp(11170.0/Temp)/5.7e+15 + 1.0) - 1000000.0*0.6**(1.0/(log(1000000.0*1.80e-31*(Temp/300)**-3.20/(4.70e-12*(Temp/300)**0.0))**2/log(10)**2 + 1.0))*1.80e-31*C_HO2*C_NO2*(Temp/300)**-3.20*exp(-0.0/Temp)/(1000000.0*1.80e-31*(Temp/300)**-3.20/(4.70e-12*(Temp/300)**0.0) + 1.0) - 1000000.0*0.60**(1.0/(log(1000000.0*2.43e-30*(Temp/300)**-3.10/(1.67e-11*(Temp/300)**-2.10))**2/log(10)**2 + 1.0))*2.43e-30*C_NO2*C_OH*(Temp/300)**-3.10*exp(-0.0/Temp)/(1.0 + 1000000.0*2.43e-30*(Temp/300)**-3.10/(1.67e-11*(Temp/300)**-2.10)) - 1000000.0*0.80**(1.0/(log(1000000.0*9.00e-32*(Temp/300)**-2.00/(2.20e-11*(Temp/300)**0.0))**2/log(10)**2 + 1.0))*9.00e-32*C_NO2*C_O3P*(Temp/300)**-2.00*exp(-0.0/Temp)/(1.0 + 1000000.0*9.00e-32*(Temp/300)**-2.00/(2.20e-11*(Temp/300)**0.0)) + 1.0*1.00e-31*C_AIR*C_NO*C_O3P*(Temp/300)**-1.60*exp(-0.0/Temp) - 1.0*1.20e-11*C_MA_RCO3*C_NO2*(Temp/300)**-0.90*exp(-0.0/Temp) - 1.0*1.20e-11*C_NO2*C_RCO_O2*(Temp/300)**-0.90*exp(-0.0/Temp) + 1.0*1.25e-11*C_BZCO_O2*C_NO*(Temp/300)**0.0*exp(--240.0/Temp) + 1.0*1.25e-11*C_MA_RCO3*C_NO*(Temp/300)**0.0*exp(--240.0/Temp) + 1.0*1.25e-11*C_NO*C_RCO_O2*(Temp/300)**0.0*exp(--240.0/Temp) + 1.0*1.30e-12*C_C_O2*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*1.37e-11*C_BZCO_O2*C_NO2*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*1.40e-13*C_NO2*C_O3*(Temp/300)**0.0*exp(-2470.0/Temp) + 1.0*1.50e+1*C_NO3 + 1.0*1.50e-12*C_HNO4*C_OH*(Temp/300)**0.0*exp(--360.0/Temp) + 1.0*1.60e+16*C_MA_PAN*(Temp/300)**0.0*exp(-13486.0/Temp) + 1.0*1.60e-2*C_HONO + 2.0*1.80e-11*C_NO*C_NO3*(Temp/300)**0.0*exp(--110.0/Temp) + 1.0*1.80e-12*C_NO*C_O3*(Temp/300)**0.0*exp(-1370.0/Temp) + 1.0*2.00e+15*C_PAN2*(Temp/300)**0.0*exp(-12800.0/Temp) + 1.0*2.00e-11*C_NO3*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*2.30e-11*C_BZ_O*C_NO2*(Temp/300)**0.0*exp(--150.0/Temp) + 1.0*2.30e-12*C_NO3*C_R2O2*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*2.30e-12*C_NO3*C_RO2_N*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*2.30e-12*C_NO3*C_RO2_R*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*2.35e-4*C_RNO3 - 1.0*2.40e-11*C_NO2*C_TBU_O*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*2.70e-12*C_HONO*C_OH*(Temp/300)**0.0*exp(--260.0/Temp) + 1.0*2.70e-12*C_NO*C_R2O2*(Temp/300)**0.0*exp(--360.0/Temp) + 1.0*2.70e-12*C_NO*C_RO2_R*(Temp/300)**0.0*exp(--360.0/Temp) + 1.0*2.80e-12*C_C_O2*C_NO*(Temp/300)**0.0*exp(--285.0/Temp) + 1.0*2.80e-12*C_HOCOO*C_NO*(Temp/300)**0.0*exp(--285.0/Temp) + 0.187*3.03e-12*C_ISOPRENE*C_NO3*(Temp/300)**0.0*exp(-448.0/Temp) + 2.0*3.30e-39*C_NO**2*C_O2*(Temp/300)**0.0*exp(--530.0/Temp) + 1.0*3.40e-12*C_HO2*C_NO*(Temp/300)**0.0*exp(--270.0/Temp) + 0.474*3.66e-12*C_NO3*C_TERP_SURR*(Temp/300)**0.0*exp(--175.0/Temp) + 1.0*4.00e-12*C_BZCO_O2*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*4.00e-12*C_CCO_O2*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) + 0.8*4.00e-12*C_HO2*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*4.00e-12*C_MA_RCO3*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*4.00e-12*C_NO3*C_RCO_O2*(Temp/300)**0.0*exp(-0.0/Temp) + 0.61*4.69e-4*C_HNO4 + 1.0*5.40e-5*C_HNO3 - 1.0*6.50e-12*C_NO2*C_O3P*(Temp/300)**0.0*exp(-- 120.0/Temp) - 1.0*7.50e+14*C_BZNO2_O*C_NO2*(Temp/300)**0.0*exp(-8152.0/Temp) + 1.0*7.80e-12*C_CCO_O2*C_NO*(Temp/300)**0.0*exp(--300.0/Temp) + 0.338*7.80e-12*C_OH*C_RNO3*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*7.90e+16*C_PBZN*(Temp/300)**0.0*exp(-14000.0/Temp) + 2.0*8.50e-13*C_NO3**2*(Temp/300)**0.0*exp(-2450.0/Temp)) + (EXPLICIT: 0)
d[NO3]/dt = (IMPLICIT: -1.0*((4.453e-14) * (Temp/300.0)**(0.0) * exp(-(376.0)/Temp) + (7.265e-13) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_NO3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) - 1000000.0*0.45**(1.0/(log(1000000.0*2.80e-30*(Temp/300)**-3.50/(2.00e-12*(Temp/300)**0.20))**2/log(10)**2 + 1.0))*2.80e-30*C_NO2*C_NO3*(Temp/300)**-3.50*exp(-0.0/Temp)/(1.0 + 1000000.0*2.80e-30*(Temp/300)**-3.50/(2.00e-12*(Temp/300)**0.20)) + 1000000.0*0.45**(1.0/(log(1000000.0*1.e-3*(Temp/300)**-3.5*exp(-11000.0/Temp)*exp(11080.0/Temp)/(9.7e+14*(Temp/300)**0.1))**2/log(10)**2 + 1.0))*1.e-3*C_N2O5*(Temp/300)**-3.5*exp(-11000.0/Temp)/(1000000.0*1.e-3*(Temp/300)**-3.5*exp(-11000.0/Temp)*exp(11080.0/Temp)/(9.7e+14*(Temp/300)**0.1) + 1.0) + 1000000.0*0.80**(1.0/(log(1000000.0*9.00e-32*(Temp/300)**-2.00/(2.20e-11*(Temp/300)**0.0))**2/log(10)**2 + 1.0))*9.00e-32*C_NO2*C_O3P*(Temp/300)**-2.00*exp(-0.0/Temp)/(1.0 + 1000000.0*9.00e-32*(Temp/300)**-2.00/(2.20e-11*(Temp/300)**0.0)) - 1.0*1.00e-13*C_ISOPROD*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*1.30e-12*C_C_O2*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*1.37e-11*C_CRES*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*1.40e-12*C_BALD*C_NO3*(Temp/300)**0.0*exp(-1872.0/Temp) - 1.0*1.40e-12*C_CCHO*C_NO3*(Temp/300)**0.0*exp(-1860.0/Temp) - 1.0*1.40e-12*C_MGLY*C_NO3*(Temp/300)**0.0*exp(-1895.0/Temp) - 1.0*1.40e-12*C_NO3*C_RCHO*(Temp/300)**0.0*exp(-1771.0/Temp) + 1.0*1.40e-13*C_NO2*C_O3*(Temp/300)**0.0*exp(-2470.0/Temp) - 1.0*1.50e+1*C_NO3 - 1.0*1.50e-12*C_METHACRO*C_NO3*(Temp/300)**0.0*exp(-1726.0/Temp) - 1.0*1.59*C_NO3 - 1.0*1.80e-11*C_NO*C_NO3*(Temp/300)**0.0*exp(--110.0/Temp) - 1.0*2.00e-11*C_NO3*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*2.00e-12*C_HCHO*C_NO3*(Temp/300)**0.0*exp(-2431.0/Temp) - 1.0*2.30e-12*C_NO3*C_R2O2*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*2.30e-12*C_NO3*C_RO2_N*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*2.30e-12*C_NO3*C_RO2_R*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*2.80e-12*C_GLY*C_NO3*(Temp/300)**0.0*exp(-2376.0/Temp) - 1.0*3.03e-12*C_ISOPRENE*C_NO3*(Temp/300)**0.0*exp(-448.0/Temp) - 1.0*3.66e-12*C_NO3*C_TERP_SURR*(Temp/300)**0.0*exp(--175.0/Temp) - 1.0*3.78e-12*C_NO3*C_NPHE*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*3.78e-12*C_NO3*C_PHEN*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*4.00e-12*C_BZCO_O2*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*4.00e-12*C_CCO_O2*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*4.00e-12*C_HO2*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*4.00e-12*C_MA_RCO3*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*4.00e-12*C_NO3*C_RCO_O2*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*4.39e-13*C_ETHENE*C_NO3*(Temp/300)**2.0*exp(-2282.0/Temp) - 1.0*4.50e-14*C_NO2*C_NO3*(Temp/300)**0.0*exp(-1260.0/Temp) + 0.39*4.69e-4*C_HNO4 - 2.0*8.50e-13*C_NO3**2*(Temp/300)**0.0*exp(-2450.0/Temp) + 1.0*C_HNO3*C_OH*(1000000.0*1.90e-33*exp(--725.0/Temp)/(1000000.0*1.90e-33*exp(-1440.0/Temp)*exp(--725.0/Temp)/4.10e-16 + 1.0) + 7.20e-15*exp(--785.0/Temp))) + (EXPLICIT: 0)
d[N2O5]/dt = (IMPLICIT: 1000000.0*0.45**(1.0/(log(1000000.0*2.80e-30*(Temp/300)**-3.50/(2.00e-12*(Temp/300)**0.20))**2/log(10)**2 + 1.0))*2.80e-30*C_NO2*C_NO3*(Temp/300)**-3.50*exp(-0.0/Temp)/(1.0 + 1000000.0*2.80e-30*(Temp/300)**-3.50/(2.00e-12*(Temp/300)**0.20)) - 1000000.0*0.45**(1.0/(log(1000000.0*1.e-3*(Temp/300)**-3.5*exp(-11000.0/Temp)*exp(11080.0/Temp)/(9.7e+14*(Temp/300)**0.1))**2/log(10)**2 + 1.0))*1.e-3*C_N2O5*(Temp/300)**-3.5*exp(-11000.0/Temp)/(1000000.0*1.e-3*(Temp/300)**-3.5*exp(-11000.0/Temp)*exp(11080.0/Temp)/(9.7e+14*(Temp/300)**0.1) + 1.0) - 1.0*2.60e-22*C_H2O*C_N2O5*(Temp/300)**0.0*exp(-0.0/Temp)) + (EXPLICIT: 0)
d[HONO]/dt = (IMPLICIT: 1000000.0*0.60**(1.0/(log(1000000.0*7.00e-31*(Temp/300)**-2.60/(3.60e-11*(Temp/300)**-0.10))**2/log(10)**2 + 1.0))*7.00e-31*C_NO*C_OH*(Temp/300)**-2.60*exp(-0.0/Temp)/(1.0 + 1000000.0*7.00e-31*(Temp/300)**-2.60/(3.60e-11*(Temp/300)**-0.10)) - 1.0*1.27e-1*C_HONO - 1.0*1.60e-2*C_HONO - 1.0*2.70e-12*C_HONO*C_OH*(Temp/300)**0.0*exp(--260.0/Temp)) + (EXPLICIT: 0)
d[HNO3]/dt = (IMPLICIT: 1000000.0*0.60**(1.0/(log(1000000.0*2.43e-30*(Temp/300)**-3.10/(1.67e-11*(Temp/300)**-2.10))**2/log(10)**2 + 1.0))*2.43e-30*C_NO2*C_OH*(Temp/300)**-3.10*exp(-0.0/Temp)/(1.0 + 1000000.0*2.43e-30*(Temp/300)**-3.10/(1.67e-11*(Temp/300)**-2.10)) + 0.15*1.00e-13*C_ISOPROD*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*1.37e-11*C_CRES*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*1.40e-12*C_BALD*C_NO3*(Temp/300)**0.0*exp(-1872.0/Temp) + 1.0*1.40e-12*C_CCHO*C_NO3*(Temp/300)**0.0*exp(-1860.0/Temp) + 1.0*1.40e-12*C_MGLY*C_NO3*(Temp/300)**0.0*exp(-1895.0/Temp) + 1.0*1.40e-12*C_NO3*C_RCHO*(Temp/300)**0.0*exp(-1771.0/Temp) + 0.5*1.50e-12*C_METHACRO*C_NO3*(Temp/300)**0.0*exp(-1726.0/Temp) + 1.0*2.00e-12*C_HCHO*C_NO3*(Temp/300)**0.0*exp(-2431.0/Temp) + 2.0*2.60e-22*C_H2O*C_N2O5*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*2.80e-12*C_GLY*C_NO3*(Temp/300)**0.0*exp(-2376.0/Temp) + 1.0*3.78e-12*C_NO3*C_NPHE*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*3.78e-12*C_NO3*C_PHEN*(Temp/300)**0.0*exp(-0.0/Temp) + 0.2*4.00e-12*C_HO2*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*5.40e-5*C_HNO3 - 1.0*C_HNO3*C_OH*(1000000.0*1.90e-33*exp(--725.0/Temp)/(1000000.0*1.90e-33*exp(-1440.0/Temp)*exp(--725.0/Temp)/4.10e-16 + 1.0) + 7.20e-15*exp(--785.0/Temp))) + (EXPLICIT: 0)
d[HNO4]/dt = (IMPLICIT: -1000000.0*0.5**(1.0/(log(1000000.0*4.10e-05*exp(-10650.0/Temp)*exp(11170.0/Temp)/5.7e+15)**2/log(10)**2 + 1.0))*4.10e-05*C_HNO4*(Temp/300)**0.0*exp(-10650.0/Temp)/(1000000.0*4.10e-05*exp(-10650.0/Temp)*exp(11170.0/Temp)/5.7e+15 + 1.0) + 1000000.0*0.6**(1.0/(log(1000000.0*1.80e-31*(Temp/300)**-3.20/(4.70e-12*(Temp/300)**0.0))**2/log(10)**2 + 1.0))*1.80e-31*C_HO2*C_NO2*(Temp/300)**-3.20*exp(-0.0/Temp)/(1000000.0*1.80e-31*(Temp/300)**-3.20/(4.70e-12*(Temp/300)**0.0) + 1.0) - 1.0*1.50e-12*C_HNO4*C_OH*(Temp/300)**0.0*exp(--360.0/Temp) - 1.0*4.69e-4*C_HNO4) + (EXPLICIT: 0)
d[SO2]/dt = (IMPLICIT: -1000000.0*0.45**(1.0/(log(1000000.0*4.00e-31*(Temp/300)**-3.30/(2.00e-12*(Temp/300)**0.0))**2/log(10)**2 + 1.0))*4.00e-31*C_OH*C_SO2*(Temp/300)**-3.30*exp(-0.0/Temp)/(1.0 + 1000000.0*4.00e-31*(Temp/300)**-3.30/(2.00e-12*(Temp/300)**0.0))) + (EXPLICIT: 0)
d[H2SO4]/dt = (IMPLICIT: 1000000.0*0.45**(1.0/(log(1000000.0*4.00e-31*(Temp/300)**-3.30/(2.00e-12*(Temp/300)**0.0))**2/log(10)**2 + 1.0))*4.00e-31*C_OH*C_SO2*(Temp/300)**-3.30*exp(-0.0/Temp)/(1.0 + 1000000.0*4.00e-31*(Temp/300)**-3.30/(2.00e-12*(Temp/300)**0.0))) + (EXPLICIT: 0)
d[CO]/dt = (IMPLICIT: 0.00792022792022792*((1.074e-11) * (Temp/300.0)**(0.0) * exp(-(234.0)/Temp) + (2.085e-11) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_O3P*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.0413313591022444*((1.37e-12) * (Temp/300.0)**(2.0) * exp(-(498.0)/Temp) + (9.87e-12) * (Temp/300.0)**(0.0) * exp(-(671.0)/Temp) + (1.019e-11) * (Temp/300.0)**(0.0) * exp(-(434.0)/Temp) + (5.946e-12) * (Temp/300.0)**(0.0) * exp(-(91.0)/Temp) + (1.112e-11) * (Temp/300.0)**(0.0) * exp(-(52.0)/Temp)) / 5.0*C_ALK_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.332119774301103*((2.617e-15) * (Temp/300.0)**(0.0) * exp(-(1640.0)/Temp) + (5.022e-16) * (Temp/300.0)**(0.0) * exp(-(461.0)/Temp)) / 2.0*C_O3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.572*1.00e-13*C_ISOPROD*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) + 0.491*1.04e-11*C_ETHENE*C_O3P*(Temp/300)**0.0*exp(-792.0/Temp) + 0.157*1.08e-15*C_O3*C_TERP_SURR*(Temp/300)**0.0*exp(-821.0/Temp) + 1.26*1.10e-11*C_GLY*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*1.10e-2*C_MGLY + 0.45*1.36e-15*C_METHACRO*C_O3*(Temp/300)**0.0*exp(-2114.0/Temp) + 1.0*1.40e-12*C_MGLY*C_NO3*(Temp/300)**0.0*exp(-1895.0/Temp) + 1.0*1.40e-3*C_RCHO + 1.0*1.50e-11*C_MGLY*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.5*1.50e-12*C_METHACRO*C_NO3*(Temp/300)**0.0*exp(-1726.0/Temp) + 1.0*1.81e-1*(6.00e-3*SUN/60.0)*C_GLY + 0.416*1.86e-11*C_METHACRO*C_OH*(Temp/300)**0.0*exp(--176.0/Temp) + 0.034*2.00e-11*C_OH*C_RCHO*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*2.00e-12*C_HCHO*C_NO3*(Temp/300)**0.0*exp(-2431.0/Temp) + 1.5*2.00e-18*C_DCB1*C_O3*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*2.06e-1*(3.65e-1*SUN/60.0)*C_DCB2 + 1.0*2.32e-3*C_HCHO + 1.26*2.80e-12*C_GLY*C_NO3*(Temp/300)**0.0*exp(-2376.0/Temp) + 1.0*3.15e-3*C_HCHO + 0.7*3.32e-2*(2.10e-3*SUN/60.0)*C_MVK + 1.233*3.32e-2*(4.10e-3*SUN/60.0)*C_ISOPROD + 0.67*3.32e-2*(4.10e-3*SUN/60.0)*C_METHACRO + 1.0*3.32e-2*(7.28*SUN/60.0)*C_DCB3 + 1.0*4.16e-4*C_CCHO + 0.498*4.18e-18*C_ISOPROD*C_O3*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*5.00e-11*C_DCB1*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.336*6.19e-11*C_ISOPROD*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.475*7.51e-16*C_MVK*C_O3*(Temp/300)**0.0*exp(-1520.0/Temp) + 0.275*7.86e-15*C_ISOPRENE*C_O3*(Temp/300)**0.0*exp(-1912.0/Temp) + 1.0*8.60e-12*C_HCHO*C_OH*(Temp/300)**0.0*exp(--20.0/Temp) + 2.0*8.93e-3*C_GLY + 0.5*9.14e-15*C_ETHENE*C_O3*(Temp/300)**0.0*exp(-2580.0/Temp) - 1.0*C_CO*C_OH*(1.30e-13*exp(-0.0/Temp) + 1000000.0*3.19e-33*exp(-0.0/Temp))) + (EXPLICIT: 0)
d[HCHO]/dt = (IMPLICIT: 0.0280988674147963*((1.37e-12) * (Temp/300.0)**(2.0) * exp(-(498.0)/Temp) + (9.87e-12) * (Temp/300.0)**(0.0) * exp(-(671.0)/Temp) + (1.019e-11) * (Temp/300.0)**(0.0) * exp(-(434.0)/Temp) + (5.946e-12) * (Temp/300.0)**(0.0) * exp(-(91.0)/Temp) + (1.112e-11) * (Temp/300.0)**(0.0) * exp(-(52.0)/Temp)) / 5.0*C_ALK_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.462808348294435*((2.617e-15) * (Temp/300.0)**(0.0) * exp(-(1640.0)/Temp) + (5.022e-16) * (Temp/300.0)**(0.0) * exp(-(461.0)/Temp)) / 2.0*C_O3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.0744374408259082*((4.453e-14) * (Temp/300.0)**(0.0) * exp(-(376.0)/Temp) + (7.265e-13) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_NO3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.385176758409786*((7.095e-12) * (Temp/300.0)**(0.0) * exp(-(-451.0)/Temp) + (1.743e-11) * (Temp/300.0)**(0.0) * exp(-(-384.0)/Temp)) / 2.0*C_OH*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.227*1.00e-13*C_ISOPROD*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) + 0.191*1.04e-11*C_ETHENE*C_O3P*(Temp/300)**0.0*exp(-792.0/Temp) + 0.235*1.08e-15*C_O3*C_TERP_SURR*(Temp/300)**0.0*exp(-821.0/Temp) + 1.0*1.10e-12*C_ACET*C_OH*(Temp/300)**0.0*exp(-520.0/Temp) + 1.0*1.25e-11*C_MA_RCO3*C_NO*(Temp/300)**0.0*exp(--240.0/Temp) + 1.0*1.30e-12*C_C_O2*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) + 0.115*1.30e-12*C_MEK*C_OH*(Temp/300)**2.0*exp(-25.0/Temp) + 0.2*1.36e-15*C_METHACRO*C_O3*(Temp/300)**0.0*exp(-2114.0/Temp) + 0.213*1.50e-11*C_OH*C_PROD2*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*1.80e-12*C_BZCO_O2*C_C_O2*(Temp/300)**0.0*exp(--500.0/Temp) + 1.0*1.80e-12*C_CCO_O2*C_C_O2*(Temp/300)**0.0*exp(--500.0/Temp) + 1.0*1.80e-12*C_C_O2*C_MA_RCO3*(Temp/300)**0.0*exp(--500.0/Temp) + 1.0*1.80e-12*C_C_O2*C_RCO_O2*(Temp/300)**0.0*exp(--500.0/Temp) + 1.0*1.81e-1*(6.00e-3*SUN/60.0)*C_GLY + 0.276*1.83e-11*C_OH*C_TERP_SURR*(Temp/300)**0.0*exp(--449.0/Temp) + 0.084*1.86e-11*C_METHACRO*C_OH*(Temp/300)**0.0*exp(--176.0/Temp) + 1.61*1.96e-12*C_ETHENE*C_OH*(Temp/300)**0.0*exp(--438.0/Temp) - 1.0*2.00e-12*C_HCHO*C_NO3*(Temp/300)**0.0*exp(-2431.0/Temp) + 0.75*2.00e-13*C_C_O2*C_RO2_N*(Temp/300)**0.0*exp(-0.0/Temp) + 0.75*2.00e-13*C_C_O2*C_RO2_R*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*2.32e-3*C_HCHO + 0.134*2.35e-4*C_RNO3 + 1.0*2.40e+12*C_HOCOO*(Temp/300)**0.0*exp(-7000.0/Temp) + 1.0*2.45e-14*C_C_O2**2*(Temp/300)**0.0*exp(--710.0/Temp) + 0.624*2.50e-11*C_ISOPRENE*C_OH*(Temp/300)**0.0*exp(--408.0/Temp) + 1.0*2.80e-12*C_C_O2*C_NO*(Temp/300)**0.0*exp(--285.0/Temp) + 1.0*2.90e-12*C_BZCO_O2*C_MA_RCO3*(Temp/300)**0.0*exp(--500.0/Temp) + 1.0*2.90e-12*C_CCO_O2*C_MA_RCO3*(Temp/300)**0.0*exp(--500.0/Temp) + 0.35*2.90e-12*C_COOH*C_OH*(Temp/300)**0.0*exp(--190.0/Temp) + 2.0*2.90e-12*C_MA_RCO3**2*(Temp/300)**0.0*exp(--500.0/Temp) + 1.0*2.90e-12*C_MA_RCO3*C_RCO_O2*(Temp/300)**0.0*exp(--500.0/Temp) + 1.0*3.10e-12*C_MEOH*C_OH*(Temp/300)**2.0*exp(-360.0/Temp) - 1.0*3.15e-3*C_HCHO + 0.3*3.32e-2*(4.10e-3*SUN/60.0)*C_ISOPROD + 0.67*3.32e-2*(4.10e-3*SUN/60.0)*C_METHACRO + 0.24*3.60e-11*C_ISOPRENE*C_O3P*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*3.94e-4*C_COOH + 1.0*4.00e-12*C_MA_RCO3*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) + 0.3*4.14e-12*C_MVK*C_OH*(Temp/300)**0.0*exp(--453.0/Temp) + 0.125*4.18e-18*C_ISOPROD*C_O3*(Temp/300)**0.0*exp(-0.0/Temp) + 2.0*5.90e-13*C_C_O2**2*(Temp/300)**0.0*exp(-509.0/Temp) + 0.055*6.19e-11*C_ISOPROD*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.1*7.51e-16*C_MVK*C_O3*(Temp/300)**0.0*exp(-1520.0/Temp) + 0.01*7.80e-12*C_OH*C_RNO3*(Temp/300)**0.0*exp(-0.0/Temp) + 0.592*7.86e-15*C_ISOPRENE*C_O3*(Temp/300)**0.0*exp(-1912.0/Temp) - 1.0*8.60e-12*C_HCHO*C_OH*(Temp/300)**0.0*exp(--20.0/Temp) + 1.0*9.14e-15*C_ETHENE*C_O3*(Temp/300)**0.0*exp(-2580.0/Temp) + 0.506*9.49e-4*(2.00e-2*SUN/60.0)*C_PROD2 - 1.0*9.70e-15*C_HCHO*C_HO2*(Temp/300)**0.0*exp(--625.0/Temp)) + (EXPLICIT: 0)
d[CCHO]/dt = (IMPLICIT: 0.252256338320865*((1.37e-12) * (Temp/300.0)**(2.0) * exp(-(498.0)/Temp) + (9.87e-12) * (Temp/300.0)**(0.0) * exp(-(671.0)/Temp) + (1.019e-11) * (Temp/300.0)**(0.0) * exp(-(434.0)/Temp) + (5.946e-12) * (Temp/300.0)**(0.0) * exp(-(91.0)/Temp) + (1.112e-11) * (Temp/300.0)**(0.0) * exp(-(52.0)/Temp)) / 5.0*C_ALK_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.202622852013337*((2.617e-15) * (Temp/300.0)**(0.0) * exp(-(1640.0)/Temp) + (5.022e-16) * (Temp/300.0)**(0.0) * exp(-(461.0)/Temp)) / 2.0*C_O3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.478238551029143*((4.453e-14) * (Temp/300.0)**(0.0) * exp(-(376.0)/Temp) + (7.265e-13) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_NO3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.605288073394495*((7.095e-12) * (Temp/300.0)**(0.0) * exp(-(-451.0)/Temp) + (1.743e-11) * (Temp/300.0)**(0.0) * exp(-(-384.0)/Temp)) / 2.0*C_OH*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.25*1.04e-11*C_ETHENE*C_O3P*(Temp/300)**0.0*exp(-792.0/Temp) + 1.0*1.25e-11*C_NO*C_RCO_O2*(Temp/300)**0.0*exp(--240.0/Temp) + 0.482*1.30e-12*C_MEK*C_OH*(Temp/300)**2.0*exp(-25.0/Temp) - 1.0*1.40e-12*C_CCHO*C_NO3*(Temp/300)**0.0*exp(-1860.0/Temp) + 1.0*1.40e-3*C_RCHO + 0.084*1.50e-11*C_OH*C_PROD2*(Temp/300)**0.0*exp(-0.0/Temp) + 0.195*1.96e-12*C_ETHENE*C_OH*(Temp/300)**0.0*exp(--438.0/Temp) + 0.034*2.00e-11*C_OH*C_RCHO*(Temp/300)**0.0*exp(-0.0/Temp) + 0.431*2.35e-4*C_RNO3 + 1.0*2.90e-12*C_BZCO_O2*C_RCO_O2*(Temp/300)**0.0*exp(--500.0/Temp) + 1.0*2.90e-12*C_CCO_O2*C_RCO_O2*(Temp/300)**0.0*exp(--500.0/Temp) + 1.0*2.90e-12*C_MA_RCO3*C_RCO_O2*(Temp/300)**0.0*exp(--500.0/Temp) + 2.0*2.90e-12*C_RCO_O2**2*(Temp/300)**0.0*exp(--500.0/Temp) + 0.467*3.32e-2*(4.10e-3*SUN/60.0)*C_ISOPROD + 1.0*4.00e-12*C_NO3*C_RCO_O2*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*4.16e-4*C_CCHO + 0.047*4.18e-18*C_ISOPROD*C_O3*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*5.60e-12*C_CCHO*C_OH*(Temp/300)**0.0*exp(--310.0/Temp) + 0.129*6.19e-11*C_ISOPROD*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.439*7.80e-12*C_OH*C_RNO3*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*9.49e-4*(1.50e-1*SUN/60.0)*C_MEK + 0.246*9.49e-4*(2.00e-2*SUN/60.0)*C_PROD2) + (EXPLICIT: 0)
d[RCHO]/dt = (IMPLICIT: 0.198532763532764*((1.074e-11) * (Temp/300.0)**(0.0) * exp(-(234.0)/Temp) + (2.085e-11) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_O3P*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.168649573981712*((1.37e-12) * (Temp/300.0)**(2.0) * exp(-(498.0)/Temp) + (9.87e-12) * (Temp/300.0)**(0.0) * exp(-(671.0)/Temp) + (1.019e-11) * (Temp/300.0)**(0.0) * exp(-(434.0)/Temp) + (5.946e-12) * (Temp/300.0)**(0.0) * exp(-(91.0)/Temp) + (1.112e-11) * (Temp/300.0)**(0.0) * exp(-(52.0)/Temp)) / 5.0*C_ALK_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.3536618363683*((2.617e-15) * (Temp/300.0)**(0.0) * exp(-(1640.0)/Temp) + (5.022e-16) * (Temp/300.0)**(0.0) * exp(-(461.0)/Temp)) / 2.0*C_O3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.144416053850045*((4.453e-14) * (Temp/300.0)**(0.0) * exp(-(376.0)/Temp) + (7.265e-13) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_NO3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.506949847094801*((7.095e-12) * (Temp/300.0)**(0.0) * exp(-(-451.0)/Temp) + (1.743e-11) * (Temp/300.0)**(0.0) * exp(-(-384.0)/Temp)) / 2.0*C_OH*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.218*1.00e-13*C_ISOPROD*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) + 0.205*1.08e-15*C_O3*C_TERP_SURR*(Temp/300)**0.0*exp(-821.0/Temp) + 1.0*1.10e-11*C_OH*C_ROOH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.37*1.30e-12*C_MEK*C_OH*(Temp/300)**2.0*exp(-25.0/Temp) - 1.0*1.40e-12*C_NO3*C_RCHO*(Temp/300)**0.0*exp(-1771.0/Temp) - 1.0*1.40e-3*C_RCHO + 0.558*1.50e-11*C_OH*C_PROD2*(Temp/300)**0.0*exp(-0.0/Temp) + 0.474*1.83e-11*C_OH*C_TERP_SURR*(Temp/300)**0.0*exp(--449.0/Temp) - 1.0*2.00e-11*C_OH*C_RCHO*(Temp/300)**0.0*exp(-0.0/Temp) + 0.147*2.35e-4*C_RNO3 + 0.147*3.27e-11*C_O3P*C_TERP_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.474*3.66e-12*C_NO3*C_TERP_SURR*(Temp/300)**0.0*exp(--175.0/Temp) + 1.0*3.94e-4*C_ROOH + 0.675*4.14e-12*C_MVK*C_OH*(Temp/300)**0.0*exp(--453.0/Temp) + 0.45*4.32e-12*C_MVK*C_O3P*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*4.39e-13*C_ETHENE*C_NO3*(Temp/300)**2.0*exp(-2282.0/Temp) + 1.0*5.00e-11*C_DCB1*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*5.00e-11*C_DCB2*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*5.00e-11*C_DCB3*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.013*6.19e-11*C_ISOPROD*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*6.34e-12*C_METHACRO*C_O3P*(Temp/300)**0.0*exp(-0.0/Temp) + 0.213*7.80e-12*C_OH*C_RNO3*(Temp/300)**0.0*exp(-0.0/Temp) + 0.71*9.49e-4*(2.00e-2*SUN/60.0)*C_PROD2) + (EXPLICIT: 0)
d[ACET]/dt = (IMPLICIT: 0.203880455112219*((1.37e-12) * (Temp/300.0)**(2.0) * exp(-(498.0)/Temp) + (9.87e-12) * (Temp/300.0)**(0.0) * exp(-(671.0)/Temp) + (1.019e-11) * (Temp/300.0)**(0.0) * exp(-(434.0)/Temp) + (5.946e-12) * (Temp/300.0)**(0.0) * exp(-(91.0)/Temp) + (1.112e-11) * (Temp/300.0)**(0.0) * exp(-(52.0)/Temp)) / 5.0*C_ALK_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.00808412413439343*((2.617e-15) * (Temp/300.0)**(0.0) * exp(-(1640.0)/Temp) + (5.022e-16) * (Temp/300.0)**(0.0) * exp(-(461.0)/Temp)) / 2.0*C_O3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.0974951947395043*((4.453e-14) * (Temp/300.0)**(0.0) * exp(-(376.0)/Temp) + (7.265e-13) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_NO3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.0917058103975535*((7.095e-12) * (Temp/300.0)**(0.0) * exp(-(-451.0)/Temp) + (1.743e-11) * (Temp/300.0)**(0.0) * exp(-(-384.0)/Temp)) / 2.0*C_OH*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.13*1.08e-15*C_O3*C_TERP_SURR*(Temp/300)**0.0*exp(-821.0/Temp) - 1.0*1.10e-12*C_ACET*C_OH*(Temp/300)**0.0*exp(-520.0/Temp) + 0.02*2.35e-4*C_RNO3 - 1.0*4.16e-5*C_ACET + 1.0*7.50e+14*C_TBU_O*(Temp/300)**0.0*exp(-8152.0/Temp) + 0.006*7.80e-12*C_OH*C_RNO3*(Temp/300)**0.0*exp(-0.0/Temp)) + (EXPLICIT: 0)
d[MEK]/dt = (IMPLICIT: 0.583524216524216*((1.074e-11) * (Temp/300.0)**(0.0) * exp(-(234.0)/Temp) + (2.085e-11) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_O3P*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.13058032003325*((1.37e-12) * (Temp/300.0)**(2.0) * exp(-(498.0)/Temp) + (9.87e-12) * (Temp/300.0)**(0.0) * exp(-(671.0)/Temp) + (1.019e-11) * (Temp/300.0)**(0.0) * exp(-(434.0)/Temp) + (5.946e-12) * (Temp/300.0)**(0.0) * exp(-(91.0)/Temp) + (1.112e-11) * (Temp/300.0)**(0.0) * exp(-(52.0)/Temp)) / 5.0*C_ALK_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.00418607335214157*((2.617e-15) * (Temp/300.0)**(0.0) * exp(-(1640.0)/Temp) + (5.022e-16) * (Temp/300.0)**(0.0) * exp(-(461.0)/Temp)) / 2.0*C_O3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.000942246086403901*((4.453e-14) * (Temp/300.0)**(0.0) * exp(-(376.0)/Temp) + (7.265e-13) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_NO3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.0511706422018349*((7.095e-12) * (Temp/300.0)**(0.0) * exp(-(-451.0)/Temp) + (1.743e-11) * (Temp/300.0)**(0.0) * exp(-(-384.0)/Temp)) / 2.0*C_OH*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*1.30e-12*C_MEK*C_OH*(Temp/300)**2.0*exp(-25.0/Temp) + 0.115*1.50e-11*C_OH*C_PROD2*(Temp/300)**0.0*exp(-0.0/Temp) + 0.416*1.86e-11*C_METHACRO*C_OH*(Temp/300)**0.0*exp(--176.0/Temp) + 0.5*2.00e-13*C_C_O2*C_RO2_N*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*2.30e-12*C_NO3*C_RO2_N*(Temp/300)**0.0*exp(-0.0/Temp) + 0.243*2.35e-4*C_RNO3 + 0.233*3.32e-2*(4.10e-3*SUN/60.0)*C_ISOPROD + 1.0*3.50e-14*C_RO2_N**2*(Temp/300)**0.0*exp(-0.0/Temp) + 0.5*3.50e-14*C_RO2_N*C_RO2_R*(Temp/300)**0.0*exp(-0.0/Temp) + 0.21*4.18e-18*C_ISOPROD*C_O3*(Temp/300)**0.0*exp(-0.0/Temp) + 0.55*4.32e-12*C_MVK*C_O3P*(Temp/300)**0.0*exp(-0.0/Temp) + 0.15*6.19e-11*C_ISOPROD*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.177*7.80e-12*C_OH*C_RNO3*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*9.49e-4*(1.50e-1*SUN/60.0)*C_MEK) + (EXPLICIT: 0)
d[HCOOH]/dt = (IMPLICIT: 0.0310232231920199*((1.37e-12) * (Temp/300.0)**(2.0) * exp(-(498.0)/Temp) + (9.87e-12) * (Temp/300.0)**(0.0) * exp(-(671.0)/Temp) + (1.019e-11) * (Temp/300.0)**(0.0) * exp(-(434.0)/Temp) + (5.946e-12) * (Temp/300.0)**(0.0) * exp(-(91.0)/Temp) + (1.112e-11) * (Temp/300.0)**(0.0) * exp(-(52.0)/Temp)) / 5.0*C_ALK_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.166967684021544*((2.617e-15) * (Temp/300.0)**(0.0) * exp(-(1640.0)/Temp) + (5.022e-16) * (Temp/300.0)**(0.0) * exp(-(461.0)/Temp)) / 2.0*C_O3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.103*1.08e-15*C_O3*C_TERP_SURR*(Temp/300)**0.0*exp(-821.0/Temp) + 0.333*1.36e-15*C_METHACRO*C_O3*(Temp/300)**0.0*exp(-2114.0/Temp) + 1.0*2.80e-12*C_HOCOO*C_NO*(Temp/300)**0.0*exp(--285.0/Temp) + 0.1*4.18e-18*C_ISOPROD*C_O3*(Temp/300)**0.0*exp(-0.0/Temp) + 0.351*7.51e-16*C_MVK*C_O3*(Temp/300)**0.0*exp(-1520.0/Temp) + 0.204*7.86e-15*C_ISOPRENE*C_O3*(Temp/300)**0.0*exp(-1912.0/Temp) + 0.37*9.14e-15*C_ETHENE*C_O3*(Temp/300)**0.0*exp(-2580.0/Temp)) + (EXPLICIT: 0)
d[MEOH]/dt = (IMPLICIT: 0.25*2.00e-13*C_C_O2*C_RO2_N*(Temp/300)**0.0*exp(-0.0/Temp) + 0.25*2.00e-13*C_C_O2*C_RO2_R*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*2.45e-14*C_C_O2**2*(Temp/300)**0.0*exp(--710.0/Temp) - 1.0*3.10e-12*C_MEOH*C_OH*(Temp/300)**2.0*exp(-360.0/Temp)) + (EXPLICIT: 0)
d[CCO_OH]/dt = (IMPLICIT: 0.0627192228776609*((2.617e-15) * (Temp/300.0)**(0.0) * exp(-(1640.0)/Temp) + (5.022e-16) * (Temp/300.0)**(0.0) * exp(-(461.0)/Temp)) / 2.0*C_O3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*1.80e-12*C_CCO_O2*C_C_O2*(Temp/300)**0.0*exp(--500.0/Temp) + 0.25*4.30e-13*C_CCO_O2*C_HO2*(Temp/300)**0.0*exp(--1040.0/Temp) + 1.0*7.50e-12*C_CCO_O2*C_RO2_N*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*7.50e-12*C_CCO_O2*C_RO2_R*(Temp/300)**0.0*exp(-0.0/Temp)) + (EXPLICIT: 0)
d[RCO_OH]/dt = (IMPLICIT: 0.139608361118235*((2.617e-15) * (Temp/300.0)**(0.0) * exp(-(1640.0)/Temp) + (5.022e-16) * (Temp/300.0)**(0.0) * exp(-(461.0)/Temp)) / 2.0*C_O3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.189*1.08e-15*C_O3*C_TERP_SURR*(Temp/300)**0.0*exp(-821.0/Temp) + 1.0*1.80e-12*C_BZCO_O2*C_C_O2*(Temp/300)**0.0*exp(--500.0/Temp) + 1.0*1.80e-12*C_C_O2*C_MA_RCO3*(Temp/300)**0.0*exp(--500.0/Temp) + 1.0*1.80e-12*C_C_O2*C_RCO_O2*(Temp/300)**0.0*exp(--500.0/Temp) + 0.372*4.18e-18*C_ISOPROD*C_O3*(Temp/300)**0.0*exp(-0.0/Temp) + 0.25*4.30e-13*C_BZCO_O2*C_HO2*(Temp/300)**0.0*exp(--1040.0/Temp) + 0.25*4.30e-13*C_HO2*C_MA_RCO3*(Temp/300)**0.0*exp(--1040.0/Temp) + 0.25*4.30e-13*C_HO2*C_RCO_O2*(Temp/300)**0.0*exp(--1040.0/Temp) + 1.0*7.50e-12*C_BZCO_O2*C_RO2_N*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*7.50e-12*C_BZCO_O2*C_RO2_R*(Temp/300)**0.0*exp(-0.0/Temp) + 2.0*7.50e-12*C_MA_RCO3*C_RO2_N*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*7.50e-12*C_MA_RCO3*C_RO2_R*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*7.50e-12*C_RCO_O2*C_RO2_N*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*7.50e-12*C_RCO_O2*C_RO2_R*(Temp/300)**0.0*exp(-0.0/Temp) + 0.15*7.86e-15*C_ISOPRENE*C_O3*(Temp/300)**0.0*exp(-1912.0/Temp)) + (EXPLICIT: 0)
d[GLY]/dt = (IMPLICIT: 0.0635847880299252*((1.37e-12) * (Temp/300.0)**(2.0) * exp(-(498.0)/Temp) + (9.87e-12) * (Temp/300.0)**(0.0) * exp(-(671.0)/Temp) + (1.019e-11) * (Temp/300.0)**(0.0) * exp(-(434.0)/Temp) + (5.946e-12) * (Temp/300.0)**(0.0) * exp(-(91.0)/Temp) + (1.112e-11) * (Temp/300.0)**(0.0) * exp(-(52.0)/Temp)) / 5.0*C_ALK_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.0983473945409429*((1.81e-12) * (Temp/300.0)**(0.0) * exp(-(-355.0)/Temp) + (2.640e-11) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_ARO_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.009*1.04e-11*C_ETHENE*C_O3P*(Temp/300)**0.0*exp(-792.0/Temp) + 0.001*1.08e-15*C_O3*C_TERP_SURR*(Temp/300)**0.0*exp(-821.0/Temp) - 1.0*1.10e-11*C_GLY*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*1.81e-1*(6.00e-3*SUN/60.0)*C_GLY + 1.0*2.00e-18*C_DCB1*C_O3*(Temp/300)**0.0*exp(-0.0/Temp) + 0.5*2.06e-1*(3.65e-1*SUN/60.0)*C_DCB2 + 0.23*2.63e-11*C_OH*C_PHEN*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*2.80e-12*C_GLY*C_NO3*(Temp/300)**0.0*exp(-2376.0/Temp) + 0.5*3.32e-2*(7.28*SUN/60.0)*C_DCB3 + 0.023*4.18e-18*C_ISOPROD*C_O3*(Temp/300)**0.0*exp(-0.0/Temp) + 0.15*6.19e-11*C_ISOPROD*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*8.93e-3*C_GLY) + (EXPLICIT: 0)
d[MGLY]/dt = (IMPLICIT: 0.276220843672457*((1.81e-12) * (Temp/300.0)**(0.0) * exp(-(-355.0)/Temp) + (2.640e-11) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_ARO_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.008*1.00e-13*C_ISOPROD*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*1.10e-2*C_MGLY + 0.9*1.36e-15*C_METHACRO*C_O3*(Temp/300)**0.0*exp(-2114.0/Temp) - 1.0*1.40e-12*C_MGLY*C_NO3*(Temp/300)**0.0*exp(-1895.0/Temp) - 1.0*1.50e-11*C_MGLY*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.084*1.86e-11*C_METHACRO*C_OH*(Temp/300)**0.0*exp(--176.0/Temp) + 0.5*2.06e-1*(3.65e-1*SUN/60.0)*C_DCB2 + 0.5*3.32e-2*(7.28*SUN/60.0)*C_DCB3 + 0.3*4.14e-12*C_MVK*C_OH*(Temp/300)**0.0*exp(--453.0/Temp) + 0.742*4.18e-18*C_ISOPROD*C_O3*(Temp/300)**0.0*exp(-0.0/Temp) + 0.23*4.20e-11*C_CRES*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.174*6.19e-11*C_ISOPROD*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.95*7.51e-16*C_MVK*C_O3*(Temp/300)**0.0*exp(-1520.0/Temp)) + (EXPLICIT: 0)
d[BACL]/dt = (IMPLICIT: 0.0814179369018079*((1.81e-12) * (Temp/300.0)**(0.0) * exp(-(-355.0)/Temp) + (2.640e-11) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_ARO_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.031*1.08e-15*C_O3*C_TERP_SURR*(Temp/300)**0.0*exp(-821.0/Temp) - 1.0*1.90e-2*C_BACL) + (EXPLICIT: 0)
d[CRES]/dt = (IMPLICIT: 0.188283232896136*((1.81e-12) * (Temp/300.0)**(0.0) * exp(-(-355.0)/Temp) + (2.640e-11) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_ARO_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*1.37e-11*C_CRES*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*4.20e-11*C_CRES*C_OH*(Temp/300)**0.0*exp(-0.0/Temp)) + (EXPLICIT: 0)
d[BALD]/dt = (IMPLICIT: 0.0505774548032613*((1.81e-12) * (Temp/300.0)**(0.0) * exp(-(-355.0)/Temp) + (2.640e-11) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_ARO_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.006762118491921*((2.617e-15) * (Temp/300.0)**(0.0) * exp(-(1640.0)/Temp) + (5.022e-16) * (Temp/300.0)**(0.0) * exp(-(461.0)/Temp)) / 2.0*C_O3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.0141336912960585*((4.453e-14) * (Temp/300.0)**(0.0) * exp(-(376.0)/Temp) + (7.265e-13) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_NO3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.0433529051987768*((7.095e-12) * (Temp/300.0)**(0.0) * exp(-(-451.0)/Temp) + (1.743e-11) * (Temp/300.0)**(0.0) * exp(-(-384.0)/Temp)) / 2.0*C_OH*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*1.29e-11*C_BALD*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*1.40e-12*C_BALD*C_NO3*(Temp/300)**0.0*exp(-1872.0/Temp)) + (EXPLICIT: -1.0*6.22e-2*(5.00e-2*SUN/60.0)*C_BALD)
d[ISOPROD]/dt = (IMPLICIT: 0.0177675840978593*((7.095e-12) * (Temp/300.0)**(0.0) * exp(-(-451.0)/Temp) + (1.743e-11) * (Temp/300.0)**(0.0) * exp(-(-384.0)/Temp)) / 2.0*C_OH*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*1.00e-13*C_ISOPROD*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) + 0.357*2.50e-11*C_ISOPRENE*C_OH*(Temp/300)**0.0*exp(--408.0/Temp) + 0.936*3.03e-12*C_ISOPRENE*C_NO3*(Temp/300)**0.0*exp(-448.0/Temp) - 1.0*3.32e-2*(4.10e-3*SUN/60.0)*C_ISOPROD - 1.0*4.18e-18*C_ISOPROD*C_O3*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*6.19e-11*C_ISOPROD*C_OH*(Temp/300)**0.0*exp(-0.0/Temp)) + (EXPLICIT: 0)
d[METHACRO]/dt = (IMPLICIT: 0.00792022792022792*((1.074e-11) * (Temp/300.0)**(0.0) * exp(-(234.0)/Temp) + (2.085e-11) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_O3P*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.00418607335214157*((2.617e-15) * (Temp/300.0)**(0.0) * exp(-(1640.0)/Temp) + (5.022e-16) * (Temp/300.0)**(0.0) * exp(-(461.0)/Temp)) / 2.0*C_O3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.0177675840978593*((7.095e-12) * (Temp/300.0)**(0.0) * exp(-(-451.0)/Temp) + (1.743e-11) * (Temp/300.0)**(0.0) * exp(-(-384.0)/Temp)) / 2.0*C_OH*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*1.36e-15*C_METHACRO*C_O3*(Temp/300)**0.0*exp(-2114.0/Temp) - 1.0*1.50e-12*C_METHACRO*C_NO3*(Temp/300)**0.0*exp(-1726.0/Temp) - 1.0*1.86e-11*C_METHACRO*C_OH*(Temp/300)**0.0*exp(--176.0/Temp) + 0.23*2.50e-11*C_ISOPRENE*C_OH*(Temp/300)**0.0*exp(--408.0/Temp) - 1.0*3.32e-2*(4.10e-3*SUN/60.0)*C_METHACRO - 1.0*6.34e-12*C_METHACRO*C_O3P*(Temp/300)**0.0*exp(-0.0/Temp) + 0.39*7.86e-15*C_ISOPRENE*C_O3*(Temp/300)**0.0*exp(-1912.0/Temp)) + (EXPLICIT: 0)
d[MVK]/dt = (IMPLICIT: 0.00305905360348807*((2.617e-15) * (Temp/300.0)**(0.0) * exp(-(1640.0)/Temp) + (5.022e-16) * (Temp/300.0)**(0.0) * exp(-(461.0)/Temp)) / 2.0*C_O3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.0452278121473873*((4.453e-14) * (Temp/300.0)**(0.0) * exp(-(376.0)/Temp) + (7.265e-13) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_NO3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.32*2.50e-11*C_ISOPRENE*C_OH*(Temp/300)**0.0*exp(--408.0/Temp) - 1.0*3.32e-2*(2.10e-3*SUN/60.0)*C_MVK - 1.0*4.14e-12*C_MVK*C_OH*(Temp/300)**0.0*exp(--453.0/Temp) - 1.0*4.32e-12*C_MVK*C_O3P*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*7.51e-16*C_MVK*C_O3*(Temp/300)**0.0*exp(-1520.0/Temp) + 0.16*7.86e-15*C_ISOPRENE*C_O3*(Temp/300)**0.0*exp(-1912.0/Temp)) + (EXPLICIT: 0)
d[PROD2]/dt = (IMPLICIT: 0.20936277302944*((1.074e-11) * (Temp/300.0)**(0.0) * exp(-(234.0)/Temp) + (2.085e-11) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_O3P*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.139762312967581*((1.37e-12) * (Temp/300.0)**(2.0) * exp(-(498.0)/Temp) + (9.87e-12) * (Temp/300.0)**(0.0) * exp(-(671.0)/Temp) + (1.019e-11) * (Temp/300.0)**(0.0) * exp(-(434.0)/Temp) + (5.946e-12) * (Temp/300.0)**(0.0) * exp(-(91.0)/Temp) + (1.112e-11) * (Temp/300.0)**(0.0) * exp(-(52.0)/Temp)) / 5.0*C_ALK_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.00352889046437434*((1.81e-12) * (Temp/300.0)**(0.0) * exp(-(-355.0)/Temp) + (2.640e-11) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_ARO_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.187307514747371*((2.617e-15) * (Temp/300.0)**(0.0) * exp(-(1640.0)/Temp) + (5.022e-16) * (Temp/300.0)**(0.0) * exp(-(461.0)/Temp)) / 2.0*C_O3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.0344262996941896*((7.095e-12) * (Temp/300.0)**(0.0) * exp(-(-451.0)/Temp) + (1.743e-11) * (Temp/300.0)**(0.0) * exp(-(-384.0)/Temp)) / 2.0*C_OH*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.276*1.08e-15*C_O3*C_TERP_SURR*(Temp/300)**0.0*exp(-821.0/Temp) - 0.671*1.50e-11*C_OH*C_PROD2*(Temp/300)**0.0*exp(-0.0/Temp) + 0.276*1.83e-11*C_OH*C_TERP_SURR*(Temp/300)**0.0*exp(--449.0/Temp) + 0.5*2.00e-13*C_C_O2*C_RO2_N*(Temp/300)**0.0*exp(-0.0/Temp) + 0.435*2.35e-4*C_RNO3 + 0.853*3.27e-11*C_O3P*C_TERP_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.7*3.32e-2*(2.10e-3*SUN/60.0)*C_MVK + 1.0*3.50e-14*C_RO2_N**2*(Temp/300)**0.0*exp(-0.0/Temp) + 0.5*3.50e-14*C_RO2_N*C_RO2_R*(Temp/300)**0.0*exp(-0.0/Temp) + 0.75*3.60e-11*C_ISOPRENE*C_O3P*(Temp/300)**0.0*exp(-0.0/Temp) + 0.332*6.19e-11*C_ISOPROD*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*7.50e-12*C_BZCO_O2*C_RO2_N*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*7.50e-12*C_CCO_O2*C_RO2_N*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*7.50e-12*C_RCO_O2*C_RO2_N*(Temp/300)**0.0*exp(-0.0/Temp) + 0.048*7.80e-12*C_OH*C_RNO3*(Temp/300)**0.0*exp(-0.0/Temp) + 0.1*7.86e-15*C_ISOPRENE*C_O3*(Temp/300)**0.0*exp(-1912.0/Temp) - 1.0*9.49e-4*(2.00e-2*SUN/60.0)*C_PROD2) + (EXPLICIT: 0)
d[DCB1]/dt = (IMPLICIT: 0.556508684863524*((1.81e-12) * (Temp/300.0)**(0.0) * exp(-(-355.0)/Temp) + (2.640e-11) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_ARO_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*2.00e-18*C_DCB1*C_O3*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*5.00e-11*C_DCB1*C_OH*(Temp/300)**0.0*exp(-0.0/Temp)) + (EXPLICIT: 0)
d[DCB2]/dt = (IMPLICIT: 0.0995774548032613*((1.81e-12) * (Temp/300.0)**(0.0) * exp(-(-355.0)/Temp) + (2.640e-11) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_ARO_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*2.06e-1*(3.65e-1*SUN/60.0)*C_DCB2 - 1.0*5.00e-11*C_DCB2*C_OH*(Temp/300)**0.0*exp(-0.0/Temp)) + (EXPLICIT: 0)
d[DCB3]/dt = (IMPLICIT: 0.0903052109181141*((1.81e-12) * (Temp/300.0)**(0.0) * exp(-(-355.0)/Temp) + (2.640e-11) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_ARO_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*3.32e-2*(7.28*SUN/60.0)*C_DCB3 - 1.0*5.00e-11*C_DCB3*C_OH*(Temp/300)**0.0*exp(-0.0/Temp)) + (EXPLICIT: 0)
d[ETHENE]/dt = (IMPLICIT: -1.0*1.04e-11*C_ETHENE*C_O3P*(Temp/300)**0.0*exp(-792.0/Temp) - 1.0*1.96e-12*C_ETHENE*C_OH*(Temp/300)**0.0*exp(--438.0/Temp) - 1.0*4.39e-13*C_ETHENE*C_NO3*(Temp/300)**2.0*exp(-2282.0/Temp) - 1.0*9.14e-15*C_ETHENE*C_O3*(Temp/300)**0.0*exp(-2580.0/Temp)) + (EXPLICIT: 0)
d[ISOPRENE]/dt = (IMPLICIT: -1.0*2.50e-11*C_ISOPRENE*C_OH*(Temp/300)**0.0*exp(--408.0/Temp) - 1.0*3.03e-12*C_ISOPRENE*C_NO3*(Temp/300)**0.0*exp(-448.0/Temp) - 1.0*3.60e-11*C_ISOPRENE*C_O3P*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*7.86e-15*C_ISOPRENE*C_O3*(Temp/300)**0.0*exp(-1912.0/Temp)) + (EXPLICIT: 0)
d[ALK_SURR]/dt = (IMPLICIT: -1.0*((1.37e-12) * (Temp/300.0)**(2.0) * exp(-(498.0)/Temp) + (9.87e-12) * (Temp/300.0)**(0.0) * exp(-(671.0)/Temp) + (1.019e-11) * (Temp/300.0)**(0.0) * exp(-(434.0)/Temp) + (5.946e-12) * (Temp/300.0)**(0.0) * exp(-(91.0)/Temp) + (1.112e-11) * (Temp/300.0)**(0.0) * exp(-(52.0)/Temp)) / 5.0*C_ALK_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp)) + (EXPLICIT: 0)
d[ARO_SURR]/dt = (IMPLICIT: -1.0*((1.81e-12) * (Temp/300.0)**(0.0) * exp(-(-355.0)/Temp) + (2.640e-11) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_ARO_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp)) + (EXPLICIT: 0)
d[OLE_SURR]/dt = (IMPLICIT: -1.0*((1.074e-11) * (Temp/300.0)**(0.0) * exp(-(234.0)/Temp) + (2.085e-11) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_O3P*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*((2.617e-15) * (Temp/300.0)**(0.0) * exp(-(1640.0)/Temp) + (5.022e-16) * (Temp/300.0)**(0.0) * exp(-(461.0)/Temp)) / 2.0*C_O3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*((4.453e-14) * (Temp/300.0)**(0.0) * exp(-(376.0)/Temp) + (7.265e-13) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_NO3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*((7.095e-12) * (Temp/300.0)**(0.0) * exp(-(-451.0)/Temp) + (1.743e-11) * (Temp/300.0)**(0.0) * exp(-(-384.0)/Temp)) / 2.0*C_OH*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp)) + (EXPLICIT: 0)
d[TERP_SURR]/dt = (IMPLICIT: -1.0*1.08e-15*C_O3*C_TERP_SURR*(Temp/300)**0.0*exp(-821.0/Temp) - 1.0*1.83e-11*C_OH*C_TERP_SURR*(Temp/300)**0.0*exp(--449.0/Temp) - 1.0*3.27e-11*C_O3P*C_TERP_SURR*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*3.66e-12*C_NO3*C_TERP_SURR*(Temp/300)**0.0*exp(--175.0/Temp)) + (EXPLICIT: 0)
d[RNO3]/dt = (IMPLICIT: 0.331973243583259*((4.453e-14) * (Temp/300.0)**(0.0) * exp(-(376.0)/Temp) + (7.265e-13) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_NO3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.572*1.00e-13*C_ISOPROD*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*2.35e-4*C_RNO3 + 1.0*2.40e-11*C_NO2*C_TBU_O*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*2.70e-12*C_NO*C_RO2_N*(Temp/300)**0.0*exp(--360.0/Temp) + 0.276*3.66e-12*C_NO3*C_TERP_SURR*(Temp/300)**0.0*exp(--175.0/Temp) - 0.69*7.80e-12*C_OH*C_RNO3*(Temp/300)**0.0*exp(-0.0/Temp)) + (EXPLICIT: 0)
d[NPHE]/dt = (IMPLICIT: 1.0*1.90e-13*C_BZNO2_O*(Temp/300)**0.0*exp(--1300.0/Temp) + 1.0*2.30e-11*C_BZNO2_O*C_HO2*(Temp/300)**0.0*exp(--150.0/Temp) + 1.0*2.30e-11*C_BZ_O*C_NO2*(Temp/300)**0.0*exp(--150.0/Temp) - 1.0*3.78e-12*C_NO3*C_NPHE*(Temp/300)**0.0*exp(-0.0/Temp)) + (EXPLICIT: 0)
d[PHEN]/dt = (IMPLICIT: 0.0010907479617157*((1.81e-12) * (Temp/300.0)**(0.0) * exp(-(-355.0)/Temp) + (2.640e-11) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_ARO_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*1.00e-03*C_BZ_O*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*1.90e-13*C_BZ_O*C_HO2*(Temp/300)**0.0*exp(--1300.0/Temp) - 1.0*2.63e-11*C_OH*C_PHEN*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*3.78e-12*C_NO3*C_PHEN*(Temp/300)**0.0*exp(-0.0/Temp)) + (EXPLICIT: 0)
d[PAN]/dt = (IMPLICIT: -1000000.0*0.3**(1.0/(log(1000000.0*4.90e-3*(Temp/300)**0.0*exp(-12100.0/Temp)*exp(13600.0/Temp)/(4.0e+16*(Temp/300)**0.))**2/log(10)**2 + 1.0))*4.90e-3*C_PAN*(Temp/300)**0.0*exp(-12100.0/Temp)/(1.0 + 1000000.0*4.90e-3*(Temp/300)**0.0*exp(-12100.0/Temp)*exp(13600.0/Temp)/(4.0e+16*(Temp/300)**0.)) + 1000000.0*0.30**(1.0/(log(1000000.0*2.70e-28*(Temp/300)**-7.10/(1.20e-11*(Temp/300)**-0.90))**2/log(10)**2 + 1.0))*2.70e-28*C_CCO_O2*C_NO2*(Temp/300)**-7.10*exp(-0.0/Temp)/(1.0 + 1000000.0*2.70e-28*(Temp/300)**-7.10/(1.20e-11*(Temp/300)**-0.90))) + (EXPLICIT: 0)
d[PAN2]/dt = (IMPLICIT: 1.0*1.20e-11*C_NO2*C_RCO_O2*(Temp/300)**-0.90*exp(-0.0/Temp) - 1.0*2.00e+15*C_PAN2*(Temp/300)**0.0*exp(-12800.0/Temp)) + (EXPLICIT: 0)
d[PBZN]/dt = (IMPLICIT: 1.0*1.37e-11*C_BZCO_O2*C_NO2*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*7.90e+16*C_PBZN*(Temp/300)**0.0*exp(-14000.0/Temp)) + (EXPLICIT: 0)
d[MA_PAN]/dt = (IMPLICIT: 1.0*1.20e-11*C_MA_RCO3*C_NO2*(Temp/300)**-0.90*exp(-0.0/Temp) - 1.0*1.60e+16*C_MA_PAN*(Temp/300)**0.0*exp(-13486.0/Temp)) + (EXPLICIT: 0)
d[CCO_OOH]/dt = (IMPLICIT: 0.75*4.30e-13*C_CCO_O2*C_HO2*(Temp/300)**0.0*exp(--1040.0/Temp)) + (EXPLICIT: 0)
d[RCO_O2]/dt = (IMPLICIT: 0.000966016927417286*((2.617e-15) * (Temp/300.0)**(0.0) * exp(-(1640.0)/Temp) + (5.022e-16) * (Temp/300.0)**(0.0) * exp(-(461.0)/Temp)) / 2.0*C_O3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.201*1.08e-15*C_O3*C_TERP_SURR*(Temp/300)**0.0*exp(-821.0/Temp) + 0.37*1.10e-11*C_GLY*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*1.20e-11*C_NO2*C_RCO_O2*(Temp/300)**-0.90*exp(-0.0/Temp) - 1.0*1.25e-11*C_NO*C_RCO_O2*(Temp/300)**0.0*exp(--240.0/Temp) + 0.096*1.30e-12*C_MEK*C_OH*(Temp/300)**2.0*exp(-25.0/Temp) + 0.1*1.36e-15*C_METHACRO*C_O3*(Temp/300)**0.0*exp(-2114.0/Temp) + 1.0*1.40e-12*C_NO3*C_RCHO*(Temp/300)**0.0*exp(-1771.0/Temp) + 0.049*1.50e-11*C_OH*C_PROD2*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*1.80e-12*C_C_O2*C_RCO_O2*(Temp/300)**0.0*exp(--500.0/Temp) + 1.0*2.00e+15*C_PAN2*(Temp/300)**0.0*exp(-12800.0/Temp) + 0.965*2.00e-11*C_OH*C_RCHO*(Temp/300)**0.0*exp(-0.0/Temp) + 0.37*2.80e-12*C_GLY*C_NO3*(Temp/300)**0.0*exp(-2376.0/Temp) - 1.0*2.90e-12*C_BZCO_O2*C_RCO_O2*(Temp/300)**0.0*exp(--500.0/Temp) - 1.0*2.90e-12*C_CCO_O2*C_RCO_O2*(Temp/300)**0.0*exp(--500.0/Temp) - 1.0*2.90e-12*C_MA_RCO3*C_RCO_O2*(Temp/300)**0.0*exp(--500.0/Temp) - 2.0*2.90e-12*C_RCO_O2**2*(Temp/300)**0.0*exp(--500.0/Temp) + 0.3*3.32e-2*(4.10e-3*SUN/60.0)*C_ISOPROD - 1.0*4.00e-12*C_NO3*C_RCO_O2*(Temp/300)**0.0*exp(-0.0/Temp) + 0.048*4.18e-18*C_ISOPROD*C_O3*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*4.30e-13*C_HO2*C_RCO_O2*(Temp/300)**0.0*exp(--1040.0/Temp) - 1.0*7.50e-12*C_RCO_O2*C_RO2_N*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*7.50e-12*C_RCO_O2*C_RO2_R*(Temp/300)**0.0*exp(-0.0/Temp) + 0.05*7.51e-16*C_MVK*C_O3*(Temp/300)**0.0*exp(-1520.0/Temp) + 0.333*9.49e-4*(2.00e-2*SUN/60.0)*C_PROD2) + (EXPLICIT: 0)
d[RCO_OOH]/dt = (IMPLICIT: 0.75*4.30e-13*C_BZCO_O2*C_HO2*(Temp/300)**0.0*exp(--1040.0/Temp) + 0.75*4.30e-13*C_HO2*C_MA_RCO3*(Temp/300)**0.0*exp(--1040.0/Temp) + 0.75*4.30e-13*C_HO2*C_RCO_O2*(Temp/300)**0.0*exp(--1040.0/Temp)) + (EXPLICIT: 0)
d[XN]/dt = (IMPLICIT: 2.0*7.50e+14*C_BZNO2_O*C_NO2*(Temp/300)**0.0*exp(-8152.0/Temp)) + (EXPLICIT: 0)
d[XC]/dt = (IMPLICIT: 6.0*7.50e+14*C_BZNO2_O*C_NO2*(Temp/300)**0.0*exp(-8152.0/Temp)) + (EXPLICIT: 7.0*6.22e-2*(5.00e-2*SUN/60.0)*C_BALD)
d[O3P]/dt = (IMPLICIT: -1.0*((1.074e-11) * (Temp/300.0)**(0.0) * exp(-(234.0)/Temp) + (2.085e-11) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_O3P*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) - 1000000.0*0.80**(1.0/(log(1000000.0*9.00e-32*(Temp/300)**-2.00/(2.20e-11*(Temp/300)**0.0))**2/log(10)**2 + 1.0))*9.00e-32*C_NO2*C_O3P*(Temp/300)**-2.00*exp(-0.0/Temp)/(1.0 + 1000000.0*9.00e-32*(Temp/300)**-2.00/(2.20e-11*(Temp/300)**0.0)) - 1.0*1.00e-31*C_AIR*C_NO*C_O3P*(Temp/300)**-1.60*exp(-0.0/Temp) - 1.0*1.04e-11*C_ETHENE*C_O3P*(Temp/300)**0.0*exp(-792.0/Temp) + 1.0*1.50e+1*C_NO3 + 1.0*2.09e-11*C_AIR*C_O1D*(Temp/300)**0.0*exp(--95.0/Temp) - 1.0*3.27e-11*C_O3P*C_TERP_SURR*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*3.60e-11*C_ISOPRENE*C_O3P*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*3.76e-2*C_O3 - 1.0*4.32e-12*C_MVK*C_O3P*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*5.68e-34*C_AIR*C_O2*C_O3P*(Temp/300)**-2.80*exp(-0.0/Temp) - 1.0*6.34e-12*C_METHACRO*C_O3P*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*6.50e-12*C_NO2*C_O3P*(Temp/300)**0.0*exp(-- 120.0/Temp) - 1.0*8.00e-12*C_O3*C_O3P*(Temp/300)**0.0*exp(-2060.0/Temp)) + (EXPLICIT: 0)
d[O1D]/dt = (IMPLICIT: -1.0*2.09e-11*C_AIR*C_O1D*(Temp/300)**0.0*exp(--95.0/Temp) - 1.0*2.20e-10*C_H2O*C_O1D*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*4.19e-3*C_O3) + (EXPLICIT: 0)
d[OH]/dt = (IMPLICIT: -0.936927992518703*((1.37e-12) * (Temp/300.0)**(2.0) * exp(-(498.0)/Temp) + (9.87e-12) * (Temp/300.0)**(0.0) * exp(-(671.0)/Temp) + (1.019e-11) * (Temp/300.0)**(0.0) * exp(-(434.0)/Temp) + (5.946e-12) * (Temp/300.0)**(0.0) * exp(-(91.0)/Temp) + (1.112e-11) * (Temp/300.0)**(0.0) * exp(-(52.0)/Temp)) / 5.0*C_ALK_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*((1.81e-12) * (Temp/300.0)**(0.0) * exp(-(-355.0)/Temp) + (2.640e-11) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_ARO_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.190903629135676*((2.617e-15) * (Temp/300.0)**(0.0) * exp(-(1640.0)/Temp) + (5.022e-16) * (Temp/300.0)**(0.0) * exp(-(461.0)/Temp)) / 2.0*C_O3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*((7.095e-12) * (Temp/300.0)**(0.0) * exp(-(-451.0)/Temp) + (1.743e-11) * (Temp/300.0)**(0.0) * exp(-(-384.0)/Temp)) / 2.0*C_OH*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) - 1000000.0*0.45**(1.0/(log(1000000.0*4.00e-31*(Temp/300)**-3.30/(2.00e-12*(Temp/300)**0.0))**2/log(10)**2 + 1.0))*4.00e-31*C_OH*C_SO2*(Temp/300)**-3.30*exp(-0.0/Temp)/(1.0 + 1000000.0*4.00e-31*(Temp/300)**-3.30/(2.00e-12*(Temp/300)**0.0)) - 1000000.0*0.60**(1.0/(log(1000000.0*2.43e-30*(Temp/300)**-3.10/(1.67e-11*(Temp/300)**-2.10))**2/log(10)**2 + 1.0))*2.43e-30*C_NO2*C_OH*(Temp/300)**-3.10*exp(-0.0/Temp)/(1.0 + 1000000.0*2.43e-30*(Temp/300)**-3.10/(1.67e-11*(Temp/300)**-2.10)) - 1000000.0*0.60**(1.0/(log(1000000.0*7.00e-31*(Temp/300)**-2.60/(3.60e-11*(Temp/300)**-0.10))**2/log(10)**2 + 1.0))*7.00e-31*C_NO*C_OH*(Temp/300)**-2.60*exp(-0.0/Temp)/(1.0 + 1000000.0*7.00e-31*(Temp/300)**-2.60/(3.60e-11*(Temp/300)**-0.10)) + 0.567*1.08e-15*C_O3*C_TERP_SURR*(Temp/300)**0.0*exp(-821.0/Temp) - 1.0*1.10e-11*C_GLY*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) - 0.34*1.10e-11*C_OH*C_ROOH*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*1.10e-12*C_ACET*C_OH*(Temp/300)**0.0*exp(-520.0/Temp) + 1.0*1.27e-1*C_HONO - 1.0*1.29e-11*C_BALD*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*1.30e-12*C_MEK*C_OH*(Temp/300)**2.0*exp(-25.0/Temp) + 0.208*1.36e-15*C_METHACRO*C_O3*(Temp/300)**0.0*exp(-2114.0/Temp) + 1.0*1.40e-14*C_HO2*C_O3*(Temp/300)**0.0*exp(-600.0/Temp) - 1.0*1.50e-11*C_MGLY*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*1.50e-11*C_OH*C_PROD2*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*1.50e-12*C_HNO4*C_OH*(Temp/300)**0.0*exp(--360.0/Temp) - 1.0*1.83e-11*C_OH*C_TERP_SURR*(Temp/300)**0.0*exp(--449.0/Temp) - 1.0*1.86e-11*C_METHACRO*C_OH*(Temp/300)**0.0*exp(--176.0/Temp) - 1.0*1.90e-12*C_O3*C_OH*(Temp/300)**0.0*exp(-1000.0/Temp) - 1.0*1.96e-12*C_ETHENE*C_OH*(Temp/300)**0.0*exp(--438.0/Temp) - 1.0*2.00e-11*C_NO3*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*2.00e-11*C_OH*C_RCHO*(Temp/300)**0.0*exp(-0.0/Temp) + 0.5*2.00e-18*C_DCB1*C_O3*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*2.15e-12*C_CH4*C_OH*(Temp/300)**0.0*exp(-1735.0/Temp) + 2.0*2.20e-10*C_H2O*C_O1D*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*2.50e-11*C_ISOPRENE*C_OH*(Temp/300)**0.0*exp(--408.0/Temp) - 1.0*2.63e-11*C_OH*C_PHEN*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*2.70e-12*C_HONO*C_OH*(Temp/300)**0.0*exp(--260.0/Temp) - 0.65*2.90e-12*C_COOH*C_OH*(Temp/300)**0.0*exp(--190.0/Temp) - 1.0*2.90e-12*C_H2O2*C_OH*(Temp/300)**0.0*exp(-160.0/Temp) - 1.0*3.10e-12*C_MEOH*C_OH*(Temp/300)**2.0*exp(-360.0/Temp) + 0.33*3.32e-2*(4.10e-3*SUN/60.0)*C_METHACRO + 1.0*3.40e-12*C_HO2*C_NO*(Temp/300)**0.0*exp(--270.0/Temp) + 1.0*3.94e-4*C_COOH + 1.0*3.94e-4*C_ROOH + 0.8*4.00e-12*C_HO2*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*4.14e-12*C_MVK*C_OH*(Temp/300)**0.0*exp(--453.0/Temp) + 0.285*4.18e-18*C_ISOPROD*C_O3*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*4.20e-11*C_CRES*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.39*4.69e-4*C_HNO4 - 1.0*4.80e-11*C_HO2*C_OH*(Temp/300)**0.0*exp(--250.0/Temp) - 1.0*5.00e-11*C_DCB1*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*5.00e-11*C_DCB2*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*5.00e-11*C_DCB3*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*5.40e-5*C_HNO3 - 1.0*5.60e-12*C_CCHO*C_OH*(Temp/300)**0.0*exp(--310.0/Temp) + 2.0*5.64e-4*C_H2O2 - 1.0*6.19e-11*C_ISOPROD*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.164*7.51e-16*C_MVK*C_O3*(Temp/300)**0.0*exp(-1520.0/Temp) - 1.0*7.70e-12*C_H2*C_OH*(Temp/300)**0.0*exp(-2100.0/Temp) - 1.0*7.80e-12*C_OH*C_RNO3*(Temp/300)**0.0*exp(-0.0/Temp) + 0.266*7.86e-15*C_ISOPRENE*C_O3*(Temp/300)**0.0*exp(-1912.0/Temp) - 1.0*8.60e-12*C_HCHO*C_OH*(Temp/300)**0.0*exp(--20.0/Temp) + 0.12*9.14e-15*C_ETHENE*C_O3*(Temp/300)**0.0*exp(-2580.0/Temp) - 1.0*C_CO*C_OH*(1.30e-13*exp(-0.0/Temp) + 1000000.0*3.19e-33*exp(-0.0/Temp)) - 1.0*C_HNO3*C_OH*(1000000.0*1.90e-33*exp(--725.0/Temp)/(1000000.0*1.90e-33*exp(-1440.0/Temp)*exp(--725.0/Temp)/4.10e-16 + 1.0) + 7.20e-15*exp(--785.0/Temp))) + (EXPLICIT: 0)
d[HO2]/dt = (IMPLICIT: 0.00858024691358025*((1.074e-11) * (Temp/300.0)**(0.0) * exp(-(234.0)/Temp) + (2.085e-11) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_O3P*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.0310232231920199*((1.37e-12) * (Temp/300.0)**(2.0) * exp(-(498.0)/Temp) + (9.87e-12) * (Temp/300.0)**(0.0) * exp(-(671.0)/Temp) + (1.019e-11) * (Temp/300.0)**(0.0) * exp(-(434.0)/Temp) + (5.946e-12) * (Temp/300.0)**(0.0) * exp(-(91.0)/Temp) + (1.112e-11) * (Temp/300.0)**(0.0) * exp(-(52.0)/Temp)) / 5.0*C_ALK_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.189373980857852*((1.81e-12) * (Temp/300.0)**(0.0) * exp(-(-355.0)/Temp) + (2.640e-11) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_ARO_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.0474668504744806*((2.617e-15) * (Temp/300.0)**(0.0) * exp(-(1640.0)/Temp) + (5.022e-16) * (Temp/300.0)**(0.0) * exp(-(461.0)/Temp)) / 2.0*C_O3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 1000000.0*0.45**(1.0/(log(1000000.0*4.00e-31*(Temp/300)**-3.30/(2.00e-12*(Temp/300)**0.0))**2/log(10)**2 + 1.0))*4.00e-31*C_OH*C_SO2*(Temp/300)**-3.30*exp(-0.0/Temp)/(1.0 + 1000000.0*4.00e-31*(Temp/300)**-3.30/(2.00e-12*(Temp/300)**0.0)) + 1000000.0*0.5**(1.0/(log(1000000.0*4.10e-05*exp(-10650.0/Temp)*exp(11170.0/Temp)/5.7e+15)**2/log(10)**2 + 1.0))*4.10e-05*C_HNO4*(Temp/300)**0.0*exp(-10650.0/Temp)/(1000000.0*4.10e-05*exp(-10650.0/Temp)*exp(11170.0/Temp)/5.7e+15 + 1.0) - 1000000.0*0.6**(1.0/(log(1000000.0*1.80e-31*(Temp/300)**-3.20/(4.70e-12*(Temp/300)**0.0))**2/log(10)**2 + 1.0))*1.80e-31*C_HO2*C_NO2*(Temp/300)**-3.20*exp(-0.0/Temp)/(1000000.0*1.80e-31*(Temp/300)**-3.20/(4.70e-12*(Temp/300)**0.0) + 1.0) + 0.5*1.04e-11*C_ETHENE*C_O3P*(Temp/300)**0.0*exp(-792.0/Temp) + 0.033*1.08e-15*C_O3*C_TERP_SURR*(Temp/300)**0.0*exp(-821.0/Temp) + 0.63*1.10e-11*C_GLY*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*1.10e-2*C_MGLY + 1.0*1.30e-12*C_C_O2*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) + 0.008*1.36e-15*C_METHACRO*C_O3*(Temp/300)**0.0*exp(-2114.0/Temp) - 1.0*1.40e-14*C_HO2*C_O3*(Temp/300)**0.0*exp(-600.0/Temp) + 1.0*1.40e-3*C_RCHO + 0.379*1.50e-11*C_OH*C_PROD2*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*1.60e-2*C_HONO + 1.0*1.90e-12*C_O3*C_OH*(Temp/300)**0.0*exp(-1000.0/Temp) - 1.0*1.90e-13*C_BZ_O*C_HO2*(Temp/300)**0.0*exp(--1300.0/Temp) - 1.0*1.90e-13*C_HO2*C_RO2_N*(Temp/300)**0.0*exp(--1300.0/Temp) - 1.0*1.90e-13*C_HO2*C_RO2_R*(Temp/300)**0.0*exp(--1300.0/Temp) + 1.0*2.00e-11*C_NO3*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*2.00e-12*C_HCHO*C_NO3*(Temp/300)**0.0*exp(-2431.0/Temp) + 1.0*2.00e-13*C_C_O2*C_RO2_N*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*2.00e-13*C_C_O2*C_RO2_R*(Temp/300)**0.0*exp(-0.0/Temp) + 1.5*2.00e-18*C_DCB1*C_O3*(Temp/300)**0.0*exp(-0.0/Temp) + 0.5*2.06e-1*(3.65e-1*SUN/60.0)*C_DCB2 - 1.0*2.30e-11*C_BZNO2_O*C_HO2*(Temp/300)**0.0*exp(--150.0/Temp) + 1.0*2.30e-12*C_NO3*C_RO2_N*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*2.30e-12*C_NO3*C_RO2_R*(Temp/300)**0.0*exp(-0.0/Temp) + 2.0*2.32e-3*C_HCHO + 0.341*2.35e-4*C_RNO3 + 1.0*2.40e+12*C_HOCOO*(Temp/300)**0.0*exp(-7000.0/Temp) + 1.0*2.70e-12*C_NO*C_RO2_R*(Temp/300)**0.0*exp(--360.0/Temp) + 1.0*2.80e-12*C_C_O2*C_NO*(Temp/300)**0.0*exp(--285.0/Temp) + 0.63*2.80e-12*C_GLY*C_NO3*(Temp/300)**0.0*exp(-2376.0/Temp) + 1.0*2.80e-12*C_HOCOO*C_NO*(Temp/300)**0.0*exp(--285.0/Temp) + 1.0*2.90e-12*C_H2O2*C_OH*(Temp/300)**0.0*exp(-160.0/Temp) + 1.0*3.10e-12*C_MEOH*C_OH*(Temp/300)**2.0*exp(-360.0/Temp) + 1.233*3.32e-2*(4.10e-3*SUN/60.0)*C_ISOPROD + 0.34*3.32e-2*(4.10e-3*SUN/60.0)*C_METHACRO + 0.5*3.32e-2*(7.28*SUN/60.0)*C_DCB3 - 1.0*3.40e-12*C_HO2*C_NO*(Temp/300)**0.0*exp(--270.0/Temp) + 1.0*3.50e-14*C_RO2_N**2*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*3.50e-14*C_RO2_N*C_RO2_R*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*3.50e-14*C_RO2_R**2*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*3.80e-13*C_C_O2*C_HO2*(Temp/300)**0.0*exp(--780.0/Temp) + 1.0*3.94e-4*C_COOH + 1.0*3.94e-4*C_ROOH - 1.0*4.00e-12*C_HO2*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*4.16e-4*C_CCHO + 0.4*4.18e-18*C_ISOPROD*C_O3*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*4.30e-13*C_BZCO_O2*C_HO2*(Temp/300)**0.0*exp(--1040.0/Temp) - 1.0*4.30e-13*C_CCO_O2*C_HO2*(Temp/300)**0.0*exp(--1040.0/Temp) - 1.0*4.30e-13*C_HO2*C_MA_RCO3*(Temp/300)**0.0*exp(--1040.0/Temp) - 1.0*4.30e-13*C_HO2*C_RCO_O2*(Temp/300)**0.0*exp(--1040.0/Temp) + 0.61*4.69e-4*C_HNO4 - 1.0*4.80e-11*C_HO2*C_OH*(Temp/300)**0.0*exp(--250.0/Temp) + 2.0*5.90e-13*C_C_O2**2*(Temp/300)**0.0*exp(-509.0/Temp) + 0.064*7.51e-16*C_MVK*C_O3*(Temp/300)**0.0*exp(-1520.0/Temp) + 1.0*7.70e-12*C_H2*C_OH*(Temp/300)**0.0*exp(-2100.0/Temp) + 0.113*7.80e-12*C_OH*C_RNO3*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*8.60e-12*C_HCHO*C_OH*(Temp/300)**0.0*exp(--20.0/Temp) + 2.0*8.93e-3*C_GLY + 0.12*9.14e-15*C_ETHENE*C_O3*(Temp/300)**0.0*exp(-2580.0/Temp) - 1.0*9.70e-15*C_HCHO*C_HO2*(Temp/300)**0.0*exp(--625.0/Temp) + 1.0*C_CO*C_OH*(1.30e-13*exp(-0.0/Temp) + 1000000.0*3.19e-33*exp(-0.0/Temp)) - 2.0*C_H2O*C_HO2**2*(1000000.0*2.59e-54*exp(--3180.0/Temp) + 3.08e-34*exp(--2800.0/Temp)) - 2.0*C_HO2**2*(1000000.0*1.85e-33*exp(--980.0/Temp) + 2.20e-13*exp(--600.0/Temp))) + (EXPLICIT: 0)
d[C_O2]/dt = (IMPLICIT: 0.00169903366583541*((1.37e-12) * (Temp/300.0)**(2.0) * exp(-(498.0)/Temp) + (9.87e-12) * (Temp/300.0)**(0.0) * exp(-(671.0)/Temp) + (1.019e-11) * (Temp/300.0)**(0.0) * exp(-(434.0)/Temp) + (5.946e-12) * (Temp/300.0)**(0.0) * exp(-(91.0)/Temp) + (1.112e-11) * (Temp/300.0)**(0.0) * exp(-(52.0)/Temp)) / 5.0*C_ALK_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.0954813413695819*((2.617e-15) * (Temp/300.0)**(0.0) * exp(-(1640.0)/Temp) + (5.022e-16) * (Temp/300.0)**(0.0) * exp(-(461.0)/Temp)) / 2.0*C_O3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.028267382592117*((4.453e-14) * (Temp/300.0)**(0.0) * exp(-(376.0)/Temp) + (7.265e-13) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_NO3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.3*1.04e-11*C_ETHENE*C_O3P*(Temp/300)**0.0*exp(-792.0/Temp) - 1.0*1.30e-12*C_C_O2*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*1.80e-12*C_BZCO_O2*C_C_O2*(Temp/300)**0.0*exp(--500.0/Temp) - 1.0*1.80e-12*C_CCO_O2*C_C_O2*(Temp/300)**0.0*exp(--500.0/Temp) - 1.0*1.80e-12*C_C_O2*C_MA_RCO3*(Temp/300)**0.0*exp(--500.0/Temp) - 1.0*1.80e-12*C_C_O2*C_RCO_O2*(Temp/300)**0.0*exp(--500.0/Temp) - 1.0*2.00e-13*C_C_O2*C_RO2_N*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*2.00e-13*C_C_O2*C_RO2_R*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*2.15e-12*C_CH4*C_OH*(Temp/300)**0.0*exp(-1735.0/Temp) - 2.0*2.45e-14*C_C_O2**2*(Temp/300)**0.0*exp(--710.0/Temp) - 1.0*2.80e-12*C_C_O2*C_NO*(Temp/300)**0.0*exp(--285.0/Temp) + 1.0*2.90e-12*C_BZCO_O2*C_CCO_O2*(Temp/300)**0.0*exp(--500.0/Temp) + 2.0*2.90e-12*C_CCO_O2**2*(Temp/300)**0.0*exp(--500.0/Temp) + 1.0*2.90e-12*C_CCO_O2*C_MA_RCO3*(Temp/300)**0.0*exp(--500.0/Temp) + 1.0*2.90e-12*C_CCO_O2*C_RCO_O2*(Temp/300)**0.0*exp(--500.0/Temp) + 0.65*2.90e-12*C_COOH*C_OH*(Temp/300)**0.0*exp(--190.0/Temp) + 0.3*3.32e-2*(2.10e-3*SUN/60.0)*C_MVK + 0.25*3.60e-11*C_ISOPRENE*C_O3P*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*3.80e-13*C_C_O2*C_HO2*(Temp/300)**0.0*exp(--780.0/Temp) + 1.0*4.00e-12*C_CCO_O2*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*4.16e-4*C_CCHO + 1.0*4.16e-5*C_ACET - 2.0*5.90e-13*C_C_O2**2*(Temp/300)**0.0*exp(-509.0/Temp) + 1.0*7.50e+14*C_TBU_O*(Temp/300)**0.0*exp(-8152.0/Temp) + 1.0*7.80e-12*C_CCO_O2*C_NO*(Temp/300)**0.0*exp(--300.0/Temp)) + (EXPLICIT: 0)
d[COOH]/dt = (IMPLICIT: -1.0*2.90e-12*C_COOH*C_OH*(Temp/300)**0.0*exp(--190.0/Temp) + 1.0*3.80e-13*C_C_O2*C_HO2*(Temp/300)**0.0*exp(--780.0/Temp) - 1.0*3.94e-4*C_COOH) + (EXPLICIT: 0)
d[ROOH]/dt = (IMPLICIT: -1.0*1.10e-11*C_OH*C_ROOH*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*1.90e-13*C_HO2*C_RO2_N*(Temp/300)**0.0*exp(--1300.0/Temp) + 1.0*1.90e-13*C_HO2*C_RO2_R*(Temp/300)**0.0*exp(--1300.0/Temp) - 1.0*3.94e-4*C_ROOH) + (EXPLICIT: 0)
d[RO2_R]/dt = (IMPLICIT: 0.00792022792022792*((1.074e-11) * (Temp/300.0)**(0.0) * exp(-(234.0)/Temp) + (2.085e-11) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_O3P*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.694065876974231*((1.37e-12) * (Temp/300.0)**(2.0) * exp(-(498.0)/Temp) + (9.87e-12) * (Temp/300.0)**(0.0) * exp(-(671.0)/Temp) + (1.019e-11) * (Temp/300.0)**(0.0) * exp(-(434.0)/Temp) + (5.946e-12) * (Temp/300.0)**(0.0) * exp(-(91.0)/Temp) + (1.112e-11) * (Temp/300.0)**(0.0) * exp(-(52.0)/Temp)) / 5.0*C_ALK_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.801497695852534*((1.81e-12) * (Temp/300.0)**(0.0) * exp(-(-355.0)/Temp) + (2.640e-11) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_ARO_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.0237710310335984*((2.617e-15) * (Temp/300.0)**(0.0) * exp(-(1640.0)/Temp) + (5.022e-16) * (Temp/300.0)**(0.0) * exp(-(461.0)/Temp)) / 2.0*C_O3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.46406199499371*((4.453e-14) * (Temp/300.0)**(0.0) * exp(-(376.0)/Temp) + (7.265e-13) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_NO3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.915685626911315*((7.095e-12) * (Temp/300.0)**(0.0) * exp(-(-451.0)/Temp) + (1.743e-11) * (Temp/300.0)**(0.0) * exp(-(-384.0)/Temp)) / 2.0*C_OH*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.799*1.00e-13*C_ISOPROD*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) + 0.2*1.04e-11*C_ETHENE*C_O3P*(Temp/300)**0.0*exp(-792.0/Temp) + 0.031*1.08e-15*C_O3*C_TERP_SURR*(Temp/300)**0.0*exp(-821.0/Temp) + 0.34*1.10e-11*C_OH*C_ROOH*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*1.25e-11*C_NO*C_RCO_O2*(Temp/300)**0.0*exp(--240.0/Temp) + 0.37*1.30e-12*C_MEK*C_OH*(Temp/300)**2.0*exp(-25.0/Temp) + 0.1*1.36e-15*C_METHACRO*C_O3*(Temp/300)**0.0*exp(-2114.0/Temp) + 1.0*1.40e-3*C_RCHO + 0.473*1.50e-11*C_OH*C_PROD2*(Temp/300)**0.0*exp(-0.0/Temp) + 0.5*1.50e-12*C_METHACRO*C_NO3*(Temp/300)**0.0*exp(-1726.0/Temp) + 0.75*1.83e-11*C_OH*C_TERP_SURR*(Temp/300)**0.0*exp(--449.0/Temp) + 0.5*1.86e-11*C_METHACRO*C_OH*(Temp/300)**0.0*exp(--176.0/Temp) - 1.0*1.90e-13*C_HO2*C_RO2_R*(Temp/300)**0.0*exp(--1300.0/Temp) + 1.0*1.96e-12*C_ETHENE*C_OH*(Temp/300)**0.0*exp(--438.0/Temp) + 0.034*2.00e-11*C_OH*C_RCHO*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*2.00e-13*C_C_O2*C_RO2_R*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*2.06e-1*(3.65e-1*SUN/60.0)*C_DCB2 - 1.0*2.30e-12*C_NO3*C_RO2_R*(Temp/300)**0.0*exp(-0.0/Temp) + 0.564*2.35e-4*C_RNO3 + 0.907*2.50e-11*C_ISOPRENE*C_OH*(Temp/300)**0.0*exp(--408.0/Temp) + 0.76*2.63e-11*C_OH*C_PHEN*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*2.70e-12*C_NO*C_RO2_R*(Temp/300)**0.0*exp(--360.0/Temp) + 1.0*2.90e-12*C_BZCO_O2*C_RCO_O2*(Temp/300)**0.0*exp(--500.0/Temp) + 1.0*2.90e-12*C_CCO_O2*C_RCO_O2*(Temp/300)**0.0*exp(--500.0/Temp) + 1.0*2.90e-12*C_MA_RCO3*C_RCO_O2*(Temp/300)**0.0*exp(--500.0/Temp) + 2.0*2.90e-12*C_RCO_O2**2*(Temp/300)**0.0*exp(--500.0/Temp) + 0.749*3.03e-12*C_ISOPRENE*C_NO3*(Temp/300)**0.0*exp(-448.0/Temp) + 0.33*3.32e-2*(4.10e-3*SUN/60.0)*C_METHACRO + 1.0*3.32e-2*(7.28*SUN/60.0)*C_DCB3 - 1.0*3.50e-14*C_RO2_N*C_RO2_R*(Temp/300)**0.0*exp(-0.0/Temp) - 2.0*3.50e-14*C_RO2_R**2*(Temp/300)**0.0*exp(-0.0/Temp) + 0.276*3.66e-12*C_NO3*C_TERP_SURR*(Temp/300)**0.0*exp(--175.0/Temp) + 1.0*4.00e-12*C_NO3*C_RCO_O2*(Temp/300)**0.0*exp(-0.0/Temp) + 0.3*4.14e-12*C_MVK*C_OH*(Temp/300)**0.0*exp(--453.0/Temp) + 0.048*4.18e-18*C_ISOPROD*C_O3*(Temp/300)**0.0*exp(-0.0/Temp) + 0.76*4.20e-11*C_CRES*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*4.39e-13*C_ETHENE*C_NO3*(Temp/300)**2.0*exp(-2282.0/Temp) + 1.0*5.00e-11*C_DCB1*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.67*6.19e-11*C_ISOPROD*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*7.50e-12*C_BZCO_O2*C_RO2_R*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*7.50e-12*C_CCO_O2*C_RO2_R*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*7.50e-12*C_MA_RCO3*C_RO2_R*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*7.50e-12*C_RCO_O2*C_RO2_R*(Temp/300)**0.0*exp(-0.0/Temp) + 0.05*7.51e-16*C_MVK*C_O3*(Temp/300)**0.0*exp(-1520.0/Temp) + 0.376*7.80e-12*C_OH*C_RNO3*(Temp/300)**0.0*exp(-0.0/Temp) + 0.066*7.86e-15*C_ISOPRENE*C_O3*(Temp/300)**0.0*exp(-1912.0/Temp) + 1.0*9.49e-4*(1.50e-1*SUN/60.0)*C_MEK + 0.96*9.49e-4*(2.00e-2*SUN/60.0)*C_PROD2) + (EXPLICIT: 0)
d[R2O2]/dt = (IMPLICIT: 0.566381598088113*((1.37e-12) * (Temp/300.0)**(2.0) * exp(-(498.0)/Temp) + (9.87e-12) * (Temp/300.0)**(0.0) * exp(-(671.0)/Temp) + (1.019e-11) * (Temp/300.0)**(0.0) * exp(-(434.0)/Temp) + (5.946e-12) * (Temp/300.0)**(0.0) * exp(-(91.0)/Temp) + (1.112e-11) * (Temp/300.0)**(0.0) * exp(-(52.0)/Temp)) / 5.0*C_ALK_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.0220573865093614*((2.617e-15) * (Temp/300.0)**(0.0) * exp(-(1640.0)/Temp) + (5.022e-16) * (Temp/300.0)**(0.0) * exp(-(461.0)/Temp)) / 2.0*C_O3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.69812087726807*((4.453e-14) * (Temp/300.0)**(0.0) * exp(-(376.0)/Temp) + (7.265e-13) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_NO3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.0600165137614679*((7.095e-12) * (Temp/300.0)**(0.0) * exp(-(-451.0)/Temp) + (1.743e-11) * (Temp/300.0)**(0.0) * exp(-(-384.0)/Temp)) / 2.0*C_OH*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.729*1.08e-15*C_O3*C_TERP_SURR*(Temp/300)**0.0*exp(-821.0/Temp) + 1.0*1.10e-12*C_ACET*C_OH*(Temp/300)**0.0*exp(-520.0/Temp) + 1.0*1.25e-11*C_BZCO_O2*C_NO*(Temp/300)**0.0*exp(--240.0/Temp) + 0.616*1.30e-12*C_MEK*C_OH*(Temp/300)**2.0*exp(-25.0/Temp) + 0.5*1.83e-11*C_OH*C_TERP_SURR*(Temp/300)**0.0*exp(--449.0/Temp) - 1.0*1.90e-13*C_HO2*C_R2O2*(Temp/300)**0.0*exp(--1300.0/Temp) - 1.0*2.00e-13*C_C_O2*C_R2O2*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*2.06e-1*(3.65e-1*SUN/60.0)*C_DCB2 - 1.0*2.30e-12*C_NO3*C_R2O2*(Temp/300)**0.0*exp(-0.0/Temp) + 0.152*2.35e-4*C_RNO3 + 0.079*2.50e-11*C_ISOPRENE*C_OH*(Temp/300)**0.0*exp(--408.0/Temp) - 1.0*2.70e-12*C_NO*C_R2O2*(Temp/300)**0.0*exp(--360.0/Temp) + 2.0*2.90e-12*C_BZCO_O2**2*(Temp/300)**0.0*exp(--500.0/Temp) + 1.0*2.90e-12*C_BZCO_O2*C_CCO_O2*(Temp/300)**0.0*exp(--500.0/Temp) + 1.0*2.90e-12*C_BZCO_O2*C_MA_RCO3*(Temp/300)**0.0*exp(--500.0/Temp) + 1.0*2.90e-12*C_BZCO_O2*C_RCO_O2*(Temp/300)**0.0*exp(--500.0/Temp) + 0.187*3.03e-12*C_ISOPRENE*C_NO3*(Temp/300)**0.0*exp(-448.0/Temp) + 1.0*3.32e-2*(7.28*SUN/60.0)*C_DCB3 - 1.0*3.50e-14*C_R2O2*C_RO2_N*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*3.50e-14*C_R2O2*C_RO2_R*(Temp/300)**0.0*exp(-0.0/Temp) + 0.24*3.60e-11*C_ISOPRENE*C_O3P*(Temp/300)**0.0*exp(-0.0/Temp) + 0.75*3.66e-12*C_NO3*C_TERP_SURR*(Temp/300)**0.0*exp(--175.0/Temp) + 1.0*4.00e-12*C_BZCO_O2*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) + 0.675*4.14e-12*C_MVK*C_OH*(Temp/300)**0.0*exp(--453.0/Temp) + 1.0*5.00e-11*C_DCB2*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*5.00e-11*C_DCB3*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*7.50e-12*C_BZCO_O2*C_R2O2*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*7.50e-12*C_CCO_O2*C_R2O2*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*7.50e-12*C_MA_RCO3*C_R2O2*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*7.50e-12*C_R2O2*C_RCO_O2*(Temp/300)**0.0*exp(-0.0/Temp) + 0.596*7.80e-12*C_OH*C_RNO3*(Temp/300)**0.0*exp(-0.0/Temp) + 0.126*7.86e-15*C_ISOPRENE*C_O3*(Temp/300)**0.0*exp(-1912.0/Temp) + 0.515*9.49e-4*(2.00e-2*SUN/60.0)*C_PROD2) + (EXPLICIT: 0)
d[RO2_N]/dt = (IMPLICIT: 0.000660018993352327*((1.074e-11) * (Temp/300.0)**(0.0) * exp(-(234.0)/Temp) + (2.085e-11) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_O3P*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.14623566084788*((1.37e-12) * (Temp/300.0)**(2.0) * exp(-(498.0)/Temp) + (9.87e-12) * (Temp/300.0)**(0.0) * exp(-(671.0)/Temp) + (1.019e-11) * (Temp/300.0)**(0.0) * exp(-(434.0)/Temp) + (5.946e-12) * (Temp/300.0)**(0.0) * exp(-(91.0)/Temp) + (1.112e-11) * (Temp/300.0)**(0.0) * exp(-(52.0)/Temp)) / 5.0*C_ALK_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.00912832328961361*((1.81e-12) * (Temp/300.0)**(0.0) * exp(-(-355.0)/Temp) + (2.640e-11) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_ARO_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.00116100282123621*((2.617e-15) * (Temp/300.0)**(0.0) * exp(-(1640.0)/Temp) + (5.022e-16) * (Temp/300.0)**(0.0) * exp(-(461.0)/Temp)) / 2.0*C_O3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.138310156543844*((4.453e-14) * (Temp/300.0)**(0.0) * exp(-(376.0)/Temp) + (7.265e-13) * (Temp/300.0)**(0.0) * exp(-(0.0)/Temp)) / 2.0*C_NO3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.084314373088685*((7.095e-12) * (Temp/300.0)**(0.0) * exp(-(-451.0)/Temp) + (1.743e-11) * (Temp/300.0)**(0.0) * exp(-(-384.0)/Temp)) / 2.0*C_OH*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 0.051*1.00e-13*C_ISOPROD*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) + 0.18*1.08e-15*C_O3*C_TERP_SURR*(Temp/300)**0.0*exp(-821.0/Temp) + 0.042*1.30e-12*C_MEK*C_OH*(Temp/300)**2.0*exp(-25.0/Temp) + 0.07*1.50e-11*C_OH*C_PROD2*(Temp/300)**0.0*exp(-0.0/Temp) + 0.25*1.83e-11*C_OH*C_TERP_SURR*(Temp/300)**0.0*exp(--449.0/Temp) - 1.0*1.90e-13*C_HO2*C_RO2_N*(Temp/300)**0.0*exp(--1300.0/Temp) + 0.001*2.00e-11*C_OH*C_RCHO*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*2.00e-13*C_C_O2*C_RO2_N*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*2.30e-12*C_NO3*C_RO2_N*(Temp/300)**0.0*exp(-0.0/Temp) + 0.095*2.35e-4*C_RNO3 + 0.093*2.50e-11*C_ISOPRENE*C_OH*(Temp/300)**0.0*exp(--408.0/Temp) - 1.0*2.70e-12*C_NO*C_RO2_N*(Temp/300)**0.0*exp(--360.0/Temp) + 0.064*3.03e-12*C_ISOPRENE*C_NO3*(Temp/300)**0.0*exp(-448.0/Temp) - 2.0*3.50e-14*C_RO2_N**2*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*3.50e-14*C_RO2_N*C_RO2_R*(Temp/300)**0.0*exp(-0.0/Temp) + 0.01*3.60e-11*C_ISOPRENE*C_O3P*(Temp/300)**0.0*exp(-0.0/Temp) + 0.25*3.66e-12*C_NO3*C_TERP_SURR*(Temp/300)**0.0*exp(--175.0/Temp) + 0.025*4.14e-12*C_MVK*C_OH*(Temp/300)**0.0*exp(--453.0/Temp) + 0.041*6.19e-11*C_ISOPROD*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*7.50e-12*C_BZCO_O2*C_RO2_N*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*7.50e-12*C_CCO_O2*C_RO2_N*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*7.50e-12*C_MA_RCO3*C_RO2_N*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*7.50e-12*C_RCO_O2*C_RO2_N*(Temp/300)**0.0*exp(-0.0/Temp) + 0.173*7.80e-12*C_OH*C_RNO3*(Temp/300)**0.0*exp(-0.0/Temp) + 0.008*7.86e-15*C_ISOPRENE*C_O3*(Temp/300)**0.0*exp(-1912.0/Temp) + 0.04*9.49e-4*(2.00e-2*SUN/60.0)*C_PROD2) + (EXPLICIT: 0)
d[HOCOO]/dt = (IMPLICIT: -1.0*2.40e+12*C_HOCOO*(Temp/300)**0.0*exp(-7000.0/Temp) - 1.0*2.80e-12*C_HOCOO*C_NO*(Temp/300)**0.0*exp(--285.0/Temp) + 1.0*9.70e-15*C_HCHO*C_HO2*(Temp/300)**0.0*exp(--625.0/Temp)) + (EXPLICIT: 0)
d[CCO_O2]/dt = (IMPLICIT: 0.00169903366583541*((1.37e-12) * (Temp/300.0)**(2.0) * exp(-(498.0)/Temp) + (9.87e-12) * (Temp/300.0)**(0.0) * exp(-(671.0)/Temp) + (1.019e-11) * (Temp/300.0)**(0.0) * exp(-(434.0)/Temp) + (5.946e-12) * (Temp/300.0)**(0.0) * exp(-(91.0)/Temp) + (1.112e-11) * (Temp/300.0)**(0.0) * exp(-(52.0)/Temp)) / 5.0*C_ALK_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.0220573865093614*((2.617e-15) * (Temp/300.0)**(0.0) * exp(-(1640.0)/Temp) + (5.022e-16) * (Temp/300.0)**(0.0) * exp(-(461.0)/Temp)) / 2.0*C_O3*C_OLE_SURR*(Temp/300)**0.0*exp(-0.0/Temp) + 1000000.0*0.3**(1.0/(log(1000000.0*4.90e-3*(Temp/300)**0.0*exp(-12100.0/Temp)*exp(13600.0/Temp)/(4.0e+16*(Temp/300)**0.))**2/log(10)**2 + 1.0))*4.90e-3*C_PAN*(Temp/300)**0.0*exp(-12100.0/Temp)/(1.0 + 1000000.0*4.90e-3*(Temp/300)**0.0*exp(-12100.0/Temp)*exp(13600.0/Temp)/(4.0e+16*(Temp/300)**0.)) - 1000000.0*0.30**(1.0/(log(1000000.0*2.70e-28*(Temp/300)**-7.10/(1.20e-11*(Temp/300)**-0.90))**2/log(10)**2 + 1.0))*2.70e-28*C_CCO_O2*C_NO2*(Temp/300)**-7.10*exp(-0.0/Temp)/(1.0 + 1000000.0*2.70e-28*(Temp/300)**-7.10/(1.20e-11*(Temp/300)**-0.90)) + 0.123*1.08e-15*C_O3*C_TERP_SURR*(Temp/300)**0.0*exp(-821.0/Temp) + 1.0*1.10e-12*C_ACET*C_OH*(Temp/300)**0.0*exp(-520.0/Temp) + 1.0*1.10e-2*C_MGLY + 1.0*1.25e-11*C_MA_RCO3*C_NO*(Temp/300)**0.0*exp(--240.0/Temp) + 0.492*1.30e-12*C_MEK*C_OH*(Temp/300)**2.0*exp(-25.0/Temp) + 1.0*1.40e-12*C_CCHO*C_NO3*(Temp/300)**0.0*exp(-1860.0/Temp) + 1.0*1.40e-12*C_MGLY*C_NO3*(Temp/300)**0.0*exp(-1895.0/Temp) + 1.0*1.50e-11*C_MGLY*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 0.029*1.50e-11*C_OH*C_PROD2*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*1.80e-12*C_CCO_O2*C_C_O2*(Temp/300)**0.0*exp(--500.0/Temp) + 2.0*1.90e-2*C_BACL + 0.5*2.06e-1*(3.65e-1*SUN/60.0)*C_DCB2 - 1.0*2.90e-12*C_BZCO_O2*C_CCO_O2*(Temp/300)**0.0*exp(--500.0/Temp) + 1.0*2.90e-12*C_BZCO_O2*C_MA_RCO3*(Temp/300)**0.0*exp(--500.0/Temp) - 2.0*2.90e-12*C_CCO_O2**2*(Temp/300)**0.0*exp(--500.0/Temp) - 1.0*2.90e-12*C_CCO_O2*C_RCO_O2*(Temp/300)**0.0*exp(--500.0/Temp) + 2.0*2.90e-12*C_MA_RCO3**2*(Temp/300)**0.0*exp(--500.0/Temp) + 1.0*2.90e-12*C_MA_RCO3*C_RCO_O2*(Temp/300)**0.0*exp(--500.0/Temp) + 0.467*3.32e-2*(4.10e-3*SUN/60.0)*C_ISOPROD + 0.67*3.32e-2*(4.10e-3*SUN/60.0)*C_METHACRO + 0.5*3.32e-2*(7.28*SUN/60.0)*C_DCB3 - 1.0*4.00e-12*C_CCO_O2*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*4.00e-12*C_MA_RCO3*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) + 0.675*4.14e-12*C_MVK*C_OH*(Temp/300)**0.0*exp(--453.0/Temp) + 1.0*4.16e-5*C_ACET - 1.0*4.30e-13*C_CCO_O2*C_HO2*(Temp/300)**0.0*exp(--1040.0/Temp) + 1.0*5.00e-11*C_DCB2*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*5.00e-11*C_DCB3*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*5.60e-12*C_CCHO*C_OH*(Temp/300)**0.0*exp(--310.0/Temp) - 1.0*7.50e-12*C_CCO_O2*C_RO2_N*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*7.50e-12*C_CCO_O2*C_RO2_R*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*7.80e-12*C_CCO_O2*C_NO*(Temp/300)**0.0*exp(--300.0/Temp) + 1.0*9.49e-4*(1.50e-1*SUN/60.0)*C_MEK + 0.667*9.49e-4*(2.00e-2*SUN/60.0)*C_PROD2) + (EXPLICIT: 0)
d[BZCO_O2]/dt = (IMPLICIT: -1.0*1.25e-11*C_BZCO_O2*C_NO*(Temp/300)**0.0*exp(--240.0/Temp) + 1.0*1.29e-11*C_BALD*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*1.37e-11*C_BZCO_O2*C_NO2*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*1.40e-12*C_BALD*C_NO3*(Temp/300)**0.0*exp(-1872.0/Temp) - 1.0*1.80e-12*C_BZCO_O2*C_C_O2*(Temp/300)**0.0*exp(--500.0/Temp) - 2.0*2.90e-12*C_BZCO_O2**2*(Temp/300)**0.0*exp(--500.0/Temp) - 1.0*2.90e-12*C_BZCO_O2*C_CCO_O2*(Temp/300)**0.0*exp(--500.0/Temp) - 1.0*2.90e-12*C_BZCO_O2*C_MA_RCO3*(Temp/300)**0.0*exp(--500.0/Temp) - 1.0*2.90e-12*C_BZCO_O2*C_RCO_O2*(Temp/300)**0.0*exp(--500.0/Temp) - 1.0*4.00e-12*C_BZCO_O2*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*4.30e-13*C_BZCO_O2*C_HO2*(Temp/300)**0.0*exp(--1040.0/Temp) - 1.0*7.50e-12*C_BZCO_O2*C_RO2_N*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*7.50e-12*C_BZCO_O2*C_RO2_R*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*7.90e+16*C_PBZN*(Temp/300)**0.0*exp(-14000.0/Temp)) + (EXPLICIT: 0)
d[BZNO2_O]/dt = (IMPLICIT: -1.0*1.90e-13*C_BZNO2_O*(Temp/300)**0.0*exp(--1300.0/Temp) - 1.0*2.30e-11*C_BZNO2_O*C_HO2*(Temp/300)**0.0*exp(--150.0/Temp) + 1.0*3.78e-12*C_NO3*C_NPHE*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*7.50e+14*C_BZNO2_O*C_NO2*(Temp/300)**0.0*exp(-8152.0/Temp)) + (EXPLICIT: 0)
d[BZ_O]/dt = (IMPLICIT: -1.0*1.00e-03*C_BZ_O*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*1.25e-11*C_BZCO_O2*C_NO*(Temp/300)**0.0*exp(--240.0/Temp) + 1.0*1.37e-11*C_CRES*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*1.90e-13*C_BZ_O*C_HO2*(Temp/300)**0.0*exp(--1300.0/Temp) - 1.0*2.30e-11*C_BZ_O*C_NO2*(Temp/300)**0.0*exp(--150.0/Temp) + 0.24*2.63e-11*C_OH*C_PHEN*(Temp/300)**0.0*exp(-0.0/Temp) + 2.0*2.90e-12*C_BZCO_O2**2*(Temp/300)**0.0*exp(--500.0/Temp) + 1.0*2.90e-12*C_BZCO_O2*C_CCO_O2*(Temp/300)**0.0*exp(--500.0/Temp) + 1.0*2.90e-12*C_BZCO_O2*C_MA_RCO3*(Temp/300)**0.0*exp(--500.0/Temp) + 1.0*2.90e-12*C_BZCO_O2*C_RCO_O2*(Temp/300)**0.0*exp(--500.0/Temp) + 1.0*3.78e-12*C_NO3*C_PHEN*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*4.00e-12*C_BZCO_O2*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) + 0.24*4.20e-11*C_CRES*C_OH*(Temp/300)**0.0*exp(-0.0/Temp)) + (EXPLICIT: 0)
d[MA_RCO3]/dt = (IMPLICIT: 0.15*1.00e-13*C_ISOPROD*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*1.20e-11*C_MA_RCO3*C_NO2*(Temp/300)**-0.90*exp(-0.0/Temp) - 1.0*1.25e-11*C_MA_RCO3*C_NO*(Temp/300)**0.0*exp(--240.0/Temp) + 0.5*1.50e-12*C_METHACRO*C_NO3*(Temp/300)**0.0*exp(-1726.0/Temp) + 1.0*1.60e+16*C_MA_PAN*(Temp/300)**0.0*exp(-13486.0/Temp) - 1.0*1.80e-12*C_C_O2*C_MA_RCO3*(Temp/300)**0.0*exp(--500.0/Temp) + 0.5*1.86e-11*C_METHACRO*C_OH*(Temp/300)**0.0*exp(--176.0/Temp) - 1.0*2.90e-12*C_BZCO_O2*C_MA_RCO3*(Temp/300)**0.0*exp(--500.0/Temp) - 1.0*2.90e-12*C_CCO_O2*C_MA_RCO3*(Temp/300)**0.0*exp(--500.0/Temp) - 2.0*2.90e-12*C_MA_RCO3**2*(Temp/300)**0.0*exp(--500.0/Temp) - 1.0*2.90e-12*C_MA_RCO3*C_RCO_O2*(Temp/300)**0.0*exp(--500.0/Temp) + 0.3*3.32e-2*(2.10e-3*SUN/60.0)*C_MVK + 0.33*3.32e-2*(4.10e-3*SUN/60.0)*C_METHACRO + 0.24*3.60e-11*C_ISOPRENE*C_O3P*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*4.00e-12*C_MA_RCO3*C_NO3*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*4.30e-13*C_HO2*C_MA_RCO3*(Temp/300)**0.0*exp(--1040.0/Temp) + 0.289*6.19e-11*C_ISOPROD*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*7.50e-12*C_MA_RCO3*C_RO2_N*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*7.50e-12*C_MA_RCO3*C_RO2_R*(Temp/300)**0.0*exp(-0.0/Temp) + 0.192*7.86e-15*C_ISOPRENE*C_O3*(Temp/300)**0.0*exp(-1912.0/Temp)) + (EXPLICIT: 0)
d[TBU_O]/dt = (IMPLICIT: 0.0624698669991687*((1.37e-12) * (Temp/300.0)**(2.0) * exp(-(498.0)/Temp) + (9.87e-12) * (Temp/300.0)**(0.0) * exp(-(671.0)/Temp) + (1.019e-11) * (Temp/300.0)**(0.0) * exp(-(434.0)/Temp) + (5.946e-12) * (Temp/300.0)**(0.0) * exp(-(91.0)/Temp) + (1.112e-11) * (Temp/300.0)**(0.0) * exp(-(52.0)/Temp)) / 5.0*C_ALK_SURR*C_OH*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*2.40e-11*C_NO2*C_TBU_O*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*7.50e+14*C_TBU_O*(Temp/300)**0.0*exp(-8152.0/Temp)) + (EXPLICIT: 0)
d[AIR]/dt = (IMPLICIT: -1.0*1.00e-31*C_AIR*C_NO*C_O3P*(Temp/300)**-1.60*exp(-0.0/Temp) - 1.0*2.09e-11*C_AIR*C_O1D*(Temp/300)**0.0*exp(--95.0/Temp) - 1.0*5.68e-34*C_AIR*C_O2*C_O3P*(Temp/300)**-2.80*exp(-0.0/Temp)) + (EXPLICIT: 0)
d[O2]/dt = (IMPLICIT: -1.0*3.30e-39*C_NO**2*C_O2*(Temp/300)**0.0*exp(--530.0/Temp) + 1.0*4.80e-11*C_HO2*C_OH*(Temp/300)**0.0*exp(--250.0/Temp) - 1.0*5.68e-34*C_AIR*C_O2*C_O3P*(Temp/300)**-2.80*exp(-0.0/Temp) + 2.0*8.00e-12*C_O3*C_O3P*(Temp/300)**0.0*exp(-2060.0/Temp)) + (EXPLICIT: 0)
d[H2O]/dt = (IMPLICIT: -1.0*2.20e-10*C_H2O*C_O1D*(Temp/300)**0.0*exp(-0.0/Temp) - 1.0*2.60e-22*C_H2O*C_N2O5*(Temp/300)**0.0*exp(-0.0/Temp) + 1.0*4.80e-11*C_HO2*C_OH*(Temp/300)**0.0*exp(--250.0/Temp) - 1.0*C_H2O*C_HO2**2*(1000000.0*2.59e-54*exp(--3180.0/Temp) + 3.08e-34*exp(--2800.0/Temp))) + (EXPLICIT: 0)
d[H2]/dt = (IMPLICIT: -1.0*7.70e-12*C_H2*C_OH*(Temp/300)**0.0*exp(-2100.0/Temp)) + (EXPLICIT: 0)
d[CH4]/dt = (IMPLICIT: -1.0*2.15e-12*C_CH4*C_OH*(Temp/300)**0.0*exp(-1735.0/Temp)) + (EXPLICIT: 0)
d[M]/dt = (IMPLICIT: 0) + (EXPLICIT: 0)
d[N2]/dt = (IMPLICIT: 0) + (EXPLICIT: 0)
d[RO2]/dt = (IMPLICIT: 0) + (EXPLICIT: 0)
```

## Performance & Stiffness Diagnostics
The following species are the most heavily coupled (densest Jacobian rows). These dictate the performance ceiling of the Dense LU / ROS2 implicit solver block:

| Species | Non-Zero Dependencies |
|---------|-----------------------|
| HO2 | 45 |
| OH | 43 |
| NO2 | 33 |
| NO3 | 33 |
| RO2_R | 32 |

### Warnings
- ⚠️ Mechanism exceeds 50 species. Consider running with `--lump` to auto-reduce.
- ⚠️ Mechanism contains complex pressure-dependent or empirical falloff rates which expand the AST depth significantly.
