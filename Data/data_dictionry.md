# Data Dictionary

This file documents every dataset included in the app's data package.

The assignment requires each dataset to record its source and URL, licence, columns and units, primary key, time coverage, latest observation, and transformation.


## Folder layout
```
Data/
├── raw/                                   Source
│   ├── frontier_ai_models.csv             Epoch AI – Frontier models
│   ├── notable_ai_models.csv              Epoch AI – Notable models
│   ├── Stanford AI Index Figure 1.3.6.csv Stanford AI Index 2025 – fig. 1.3.6
│   └── Stanford AI Index Figure 1.3.7.csv Stanford AI Index 2025 – fig. 1.3.7
└── processed/                             
    ├── stanford_notable_2014_2024.csv
    ├── stanford_notable_2024.csv
    ├── frontier_model_org.csv
    ├── frontier_by_year_org.csv
    └── frontier_concentration_by_year.csv
```


## Source summary
| Source | Publisher | URL | Licence |
|--------|-----------|-----|---------|
| Data on AI Models: Frontier models | Epoch AI | https://epoch.ai/data/ai-models (file: https://epoch.ai/data/frontier_ai_models.csv) | CC BY 4.0 |
| Data on AI Models: Notable models | Epoch AI | https://epoch.ai/data/ai-models (file: https://epoch.ai/data/notable_ai_models.csv) | CC BY 4.0 |
| AI Index Report 2025, Chapter 1 (R&D), figures 1.3.6 and 1.3.7 | Stanford HAI | https://hai.stanford.edu/ai-index/2025-ai-index-report (public data: "Access the Public Data") | CC BY-ND 4.0 |
-----------------------------------------------------------------------------------------------


# Raw datasets
## 1. `data/raw/frontier_ai_models.csv`
**Purpose in this project:** Source for the Organisation Concentration and Concentration Dynamics analyses.

**Source:** Epoch AI — Data on AI models, Frontier Models subset.

**Source URL:** https://epoch.ai/data/ai-models

**Direct download:** https://epoch.ai/data/frontier_ai_models.csv

**Licence:** Creative Commons Attribution (CC BY). Epoch AI states that its data may be used, distributed, and reproduced provided the source and authors are credited.

**Rows in repository snapshot:** 138

**Primary key:** `Model`  
The `Model` field is unique in the repository snapshot.

**Time coverage:** 1950-07-02 to 2026-09-03.

**Latest observation:** 2026-09-03.

**Transform:** Raw source snapshot. No transformation is applied to the file itself. 

### Columns
| Column | Meaning | Unit |
|--------|---------|------|
| `Model` | Model or system name. | None (identifier) |
| `Publication date` | Model publication or release date. | Date (YYYY-MM-DD) |
| `Organization` | Organisation name(s) recorded by the source; multiple organisations may be comma-separated. | None (text) |
| `Training compute (FLOP)` | Estimated training compute. | None / as recorded |
| `Training compute notes` | Notes explaining or qualifying the training-compute estimate. | None (text) |
| `Domain` | AI domain(s) associated with the model. | None (categorical text) |
| `Task` | Task(s) associated with the model. | None (categorical text) |
| `Link` | Source or model webpage. | URL |
| `Parameters` | Estimated number of model parameters. | Parameter count |
| `Parameters notes` | Notes about the parameter estimate. | None (text) |
| `Authors` | Listed authors, where available. | None (text) |
| `Notability criteria` | Epoch AI criterion or criteria used to classify the model as notable. | None (categorical text) |
| `Notability criteria notes` | Notes about the notability classification. | None (text) |
| `Model accessibility` | How users can access the model. | None (categorical) |
| `Citations` | Citation count where available. | Count |
| `Reference` | Reference title or source label. | None (text) |
| `Training dataset` | Training dataset name or description. | None (text) |
| `Training dataset notes` | Notes about the training data. | None (text) |
| `Dataset size notes` | Notes about dataset-size estimates. | None (text) |
| `Epochs` | Number of training epochs where available. | Count |
| `Training time (hours)` | Estimated or reported training duration. | Hours |
| `Training time notes` | Notes about training duration. | None (text) |
| `Training hardware` | Hardware used for training. | None (text) |
| `Compute cost notes` | Notes about compute-cost estimates. | None (text) |
| `Confidence` | Epoch AI confidence category for estimated values. | None (categorical) |
| `Abstract` | Model/paper abstract or description. | None (text) |
| `Country (of organization)` | Country associated with the developing organisation(s). | None (categorical) |
| `Base model` | Base model used, where applicable. | None (text) |
| `Finetune compute (FLOP)` | Estimated compute used for fine-tuning. | None / as recorded |
| `Finetune compute notes` | Notes about fine-tuning compute. | None (text) |
| `Hardware quantity` | Number of training accelerators/hardware units. | Count |
| `Hardware utilization (MFU)` | Model FLOP utilisation estimate. | Ratio |
| `Training data center` | Training data-centre information. | None (text) |
| `Batch size` | Training batch size. | Count |
| `Batch size notes` | Notes about batch size. | None (text) |
| `Training chip-hours` | Estimated hardware chip-hours used for training. | Chip-hours |
| `Training code accessibility` | Accessibility of training code. | None (categorical) |
| `Accessibility notes` | Notes about model/code accessibility. | None (text) |
| `Training compute cost (2023 USD)` | Estimated training-compute cost normalised to 2023 USD. | 2023 USD |
| `Training dataset size` | Training dataset size as supplied in the source file. | Mixed / text as recorded |
| `Utilization notes` | Notes about utilisation estimates. | None (text) |
| `Estimated over 1e25 FLOP` | Flag for whether training compute is estimated above 1e25 FLOP. | Boolean / categorical |
| `Power per GPU` | Power draw per GPU/accelerator where available. | Watts (W) |
| `Base model compute` | Estimated compute of the base model. | FLOP |
| `API prices` | API pricing information where available. | Mixed / text as recorded |
| `Inference code accessibility` | Accessibility of inference code. | None (categorical) |
| `Numerical format` | Numerical precision/format used by the model or training. | None (categorical) |
| `Frontier model` | Flag indicating membership in Epoch AI's frontier-model set. | Boolean |
| `Training power draw (W)` | Estimated total training power draw. | Watts (W) |
| `FLOP/$` | Compute delivered per US dollar. | FLOP per USD |
| `Hardware release date` | Release date of the training hardware. | Date |
| `Training compute estimation method` | Method used to estimate training compute. | None (categorical text) |
| `Post-training compute (FLOP)` | Estimated compute used after pretraining. | None / as recorded |
| `Post-training compute notes` | Notes about post-training compute. | None (text) |
| `Model versions (benchmarks)` | Model-version names used in benchmark records. | None (text) |
| `Maybe over 1e25 FLOP` | Uncertain flag for training compute above 1e25 FLOP. | Boolean / categorical |
| `Hardware utilization (HFU)` | Hardware FLOP utilisation estimate. | Ratio |
| `Training compute cost (cloud)` | Estimated cloud cost of training. | USD (as recorded) |
| `Training compute cost (upfront)` | Estimated upfront training-compute cost. | USD (as recorded) |
| `Training dataset size (total)` | Total training-dataset size as recorded; unit depends on modality. | Count; unit depends on data modality |
| `Open model weights?` | Whether model weights are openly available. | None (categorical / yes-no) |
-----------------------------------------------------------------------------------------------


## 2. `data/raw/notable_ai_models.csv`
**Purpose in this project:** Source for Sector Shift, Access Concentration, and selected Concentration Dynamics views.

**Source:** Epoch AI — Data on AI models, Notable Models subset.

**Source URL:** https://epoch.ai/data/ai-models

**Direct download:** https://epoch.ai/data/notable_ai_models.csv

**Licence:** Creative Commons Attribution (CC BY). Epoch AI requires attribution to the source and authors.

**Rows in repository snapshot:** 1078

**Primary key:** `Model`  
The `Model` field is unique in the repository snapshot.

**Time coverage:** 1950-07-02 to 2026-09-30.

**Latest observation:** 2026-09-30.

**Transform:** Raw source snapshot. The Sector and Access pages derive classifications and filters at run time rather than writing separate processed CSV files.

### Columns
| Column | Meaning | Unit |
|--------|---------|------|
| `Model` | Model or system name. | None (identifier) |
| `Organization` | Organisation name(s) recorded by the source; multiple organisations may be comma-separated. | None (text) |
| `Publication date` | Model publication or release date. | Date (YYYY-MM-DD) |
| `Domain` | AI domain(s) associated with the model. | None (categorical text) |
| `Task` | Task(s) associated with the model. | None (categorical text) |
| `Parameters` | Estimated number of model parameters. | Parameter count |
| `Parameters notes` | Notes about the parameter estimate. | None (text) |
| `Training compute (FLOP)` | Estimated training compute. | None / as recorded |
| `Training compute notes` | Notes explaining or qualifying the training-compute estimate. | None (text) |
| `Training dataset` | Training dataset name or description. | None (text) |
| `Training dataset size (total)` | Total training-dataset size as recorded; unit depends on modality. | Count; unit depends on data modality |
| `Dataset size notes` | Notes about dataset-size estimates. | None (text) |
| `Confidence` | Epoch AI confidence category for estimated values. | None (categorical) |
| `Link` | Source or model webpage. | URL |
| `Reference` | Reference title or source label. | None (text) |
| `Citations` | Citation count where available. | Count |
| `Authors` | Listed authors, where available. | None (text) |
| `Abstract` | Model/paper abstract or description. | None (text) |
| `Organization categorization` | Sector/category of the developing organisation(s), such as Industry or Academia. | None (categorical) |
| `Country (of organization)` | Country associated with the developing organisation(s). | None (categorical) |
| `Notability criteria` | Epoch AI criterion or criteria used to classify the model as notable. | None (categorical text) |
| `Notability criteria notes` | Notes about the notability classification. | None (text) |
| `Epochs` | Number of training epochs where available. | Count |
| `Training time (hours)` | Estimated or reported training duration. | Hours |
| `Training time notes` | Notes about training duration. | None (text) |
| `Training hardware` | Hardware used for training. | None (text) |
| `Hardware quantity` | Number of training accelerators/hardware units. | Count |
| `Hardware utilization (MFU)` | Model FLOP utilisation estimate. | Ratio |
| `Training compute cost (2023 USD)` | Estimated training-compute cost normalised to 2023 USD. | 2023 USD |
| `Compute cost notes` | Notes about compute-cost estimates. | None (text) |
| `Training power draw (W)` | Estimated total training power draw. | Watts (W) |
| `Base model` | Base model used, where applicable. | None (text) |
| `Finetune compute (FLOP)` | Estimated compute used for fine-tuning. | None / as recorded |
| `Finetune compute notes` | Notes about fine-tuning compute. | None (text) |
| `Batch size` | Training batch size. | Count |
| `Batch size notes` | Notes about batch size. | None (text) |
| `Model accessibility` | How users can access the model. | None (categorical) |
| `Training code accessibility` | Accessibility of training code. | None (categorical) |
| `Inference code accessibility` | Accessibility of inference code. | None (categorical) |
| `Accessibility notes` | Notes about model/code accessibility. | None (text) |
| `Numerical format` | Numerical precision/format used by the model or training. | None (categorical) |
| `Frontier model` | Flag indicating membership in Epoch AI's frontier-model set. | Boolean |
| `Hardware acquisition cost` | Estimated hardware acquisition cost. | USD (as recorded) |
| `Hardware utilization (HFU)` | Hardware FLOP utilisation estimate. | Ratio |
| `Training compute cost (cloud)` | Estimated cloud cost of training. | USD (as recorded) |
| `Training compute cost (upfront)` | Estimated upfront training-compute cost. | USD (as recorded) |
| `Open model weights?` | Whether model weights are openly available. | None (categorical / yes-no) |
-----------------------------------------------------------------------------------------------


## 3. `data/raw/Stanford AI Index Figure 1.3.6.csv`
**Purpose in this project:** Organisation ranking for notable AI models in 2024.

**Source:** Stanford HAI, *AI Index Report 2025*, Figure 1.3.6, “Number of notable AI models by organization, 2024.” The figure identifies Epoch AI as its underlying data source.

**Source URL:** https://hai.stanford.edu/ai-index/2025-ai-index-report

**Report URL:** https://hai.stanford.edu/assets/files/hai_ai_index_report_2025.pdf

**Licence:** Creative Commons Attribution-NoDerivatives 4.0 International (CC BY-ND 4.0), as stated in the AI Index 2025 report.

**Rows:** 15

**Primary key:** `Organization`.

**Time coverage:** 2024.

**Latest observation:** 2024.

**Transform:** Raw chart-data sample. The processed version strips organisation names, converts the count to numeric, removes missing/duplicate rows, and renames fields for consistent app use.

### Columns
| Column | Meaning | Unit |
|--------|---------|------|
| `Organization` | Organisation named in Stanford Figure 1.3.6. | None (text) |
| `Number of notable AI model in 2024` | Number of notable AI models attributed to that organisation in 2024. | Models (count) |
-----------------------------------------------------------------------------------------------


## 4. `data/raw/Stanford AI Index Figure 1.3.7.csv`
**Purpose in this project:** Long-term organisation ranking for notable AI models.

**Source:** Stanford HAI, *AI Index Report 2025*, Figure 1.3.7, “Number of notable AI models by organization, 2014–2024 (total).” The figure identifies Epoch AI as its underlying data source.

**Source URL:** https://hai.stanford.edu/ai-index/2025-ai-index-report

**Report URL:** https://hai.stanford.edu/assets/files/hai_ai_index_report_2025.pdf

**Licence:** Creative Commons Attribution-NoDerivatives 4.0 International (CC BY-ND 4.0).

**Rows:** 15

**Primary key:** `Organization`.

**Time coverage:** 2014-2024 cumulative.

**Latest observation:** 2024.

**Transform:** Raw chart-data sample. The processed version strips organisation names, converts counts to numeric, removes missing/duplicate rows, and renames fields.

### Columns
| Column | Meaning | Unit |
|--------|---------|------|
| `Organization` | Organisation named in Stanford Figure 1.3.7. | None (text) |
| `Number of notable AI model, 2014-24` | Total notable AI models attributed to that organisation over 2014-2024. | Models (count) |
-----------------------------------------------------------------------------------------------


# Processed datasets
## 5. `data/processed/frontier_model_org.csv`
**Derived from:** `data/raw/frontier_ai_models.csv`.

**Rows:** 90.

**Primary key:** (`Model`, `Organisation`).

**Time coverage:** 2014-06-18 to 2024-11-20.

**Latest observation:** 2024-11-20.

**Licence:** Derived from Epoch AI data; source attribution and the Epoch AI CC BY terms continue to apply. The project does not assign a separate licence to the transformation.

**Transform:**
1. Parse `Publication date` and derive `Year`.
2. Restrict observations to 2014-2024.
3. Split comma-separated `Organization` values.
4. Harmonise selected organisation names, for example DeepMind / Google Brain / Google Research / Google DeepMind → Google.
5. Deduplicate organisation names after harmonisation.
6. Count the number of unique organisations on each model (`N_orgs`).
7. Assign each organisation fractional credit `1 / N_orgs`.
8. Explode the model record to one row per model-organisation pair.

### Columns
| Column | Meaning | Unit |
|--------|---------|------|
| `Model` | Model name from Epoch AI. | None (identifier) |
| `Publication date` | Model publication date. | Date |
| `Year` | Calendar year derived from publication date. | Year |
| `Organization` | Original organisation string from Epoch AI. | None (text) |
| `Organisation` | Cleaned and harmonised organisation name. | None (text) |
| `N_orgs` | Number of unique organisations attached to the model after harmonisation. | Organisations (count) |
| `Fractional_weight` | Credit allocated to this organisation for this model, equal to `1 / N_orgs`. | Model-credit units |
-----------------------------------------------------------------------------------------------


## 6. `data/processed/frontier_by_year_org.csv`
**Derived from:** `frontier_model_org.csv`.

**Rows:** 56.

**Primary key:** (`Year`, `Organisation`).

**Time coverage:** 2014-2024.

**Latest observation:** 2024.

**Licence:** Derived from Epoch AI data; Epoch AI attribution requirements continue to apply.

**Transform:**
1. Group model-organisation rows by `Year` and `Organisation`.
2. Sum `Fractional_weight` to obtain `Fractional_contribution`.
3. Count unique models to obtain `Model_count`.
4. Sum organisation fractional contributions within each year to obtain `Year_total`.
5. Calculate `Share = Fractional_contribution / Year_total`.
6. Calculate `Share_percent = Share × 100`.

### Columns
| Column | Meaning | Unit |
|--------|---------|------|
| `Year` | Calendar year. | Year |
| `Organisation` | Harmonised organisation name. | None (text) |
| `Fractional_contribution` | Sum of fractional model credits assigned to the organisation in that year. | Model-credit units |
| `Model_count` | Number of unique frontier models associated with the organisation that year. | Models (count) |
| `Year_total` | Total fractional model credit in that year. | Model-credit units |
| `Share` | Organisation's share of annual fractional credit. | Proportion, 0-1 |
| `Share_percent` | Organisation's annual share expressed as a percentage. | Percent (%) |
-----------------------------------------------------------------------------------------------


## 7. `data/processed/frontier_concentration_by_year.csv`
**Derived from:** `frontier_model_org.csv` and `frontier_by_year_org.csv`.

**Rows:** 11.

**Primary key:** `Year`.

**Time coverage:** 2014-2024.

**Latest observation:** 2024.

**Licence:** Derived from Epoch AI data; Epoch AI attribution requirements continue to apply.

**Transform:**
1. Count unique frontier models in each year.
2. Count unique harmonised organisations in each year.
3. Rank organisations by annual `Share`.
4. Sum the largest three annual shares to obtain `CR3`.
5. Calculate `CR3_percent = CR3 × 100`.
6. Calculate HHI as the sum of squared organisation shares: `Σ Share²`.

**Validation used by the processing pipeline:**
- Annual organisation shares must sum to 1.
- CR3 must be between 0 and 1.
- HHI must be between 0 and 1.

### Columns
| Column | Meaning | Unit |
|--------|---------|------|
| `Year` | Calendar year. | Year |
| `Frontier_model_count` | Number of unique frontier models in that year. | Models (count) |
| `Organisation_count` | Number of unique harmonised organisations participating in that year. | Organisations (count) |
| `CR3` | Combined share of the three largest organisations. | Proportion, 0-1 |
| `CR3_percent` | CR3 expressed as a percentage. | Percent (%) |
| `HHI` | Herfindahl-Hirschman concentration index calculated from organisation shares. | Index, 0-1 |
-----------------------------------------------------------------------------------------------


## 8. `data/processed/stanford_notable_2024.csv`
**Derived from:** `data/raw/Stanford AI Index Figure 1.3.6.csv`.

**Rows:** 15.

**Primary key:** `Organisation`.

**Time coverage:** 2024.

**Latest observation:** 2024.

**Licence:** Derived from the Stanford AI Index 2025 chart data; the source's CC BY-ND 4.0 terms apply. No separate licence is assigned by the group.

**Transform:**
1. Require one organisation column and one numeric count column.
2. Strip whitespace from organisation names.
3. Convert the model count to numeric.
4. Drop rows with missing organisation/count values.
5. Remove duplicate rows.
6. Rename `Organization` → `Organisation`.
7. Rename the source count field → `Notable_model_count_2024`.

### Columns
| Column | Meaning | Unit |
|--------|---------|------|
| `Organisation` | Organisation name. | None (text) |
| `Notable_model_count_2024` | Number of notable AI models attributed to the organisation in 2024. | Models (count) |
-----------------------------------------------------------------------------------------------


## 9. `data/processed/stanford_notable_2014_2024.csv`
**Derived from:** `data/raw/Stanford AI Index Figure 1.3.7.csv`.

**Rows:** 15.

**Primary key:** `Organisation`.

**Time coverage:** 2014-2024 cumulative.

**Latest observation:** 2024.

**Licence:** Derived from the Stanford AI Index 2025 chart data; the source's CC BY-ND 4.0 terms apply. No separate licence is assigned by the group.

**Transform:**
1. Require one organisation column and one numeric count column.
2. Strip whitespace from organisation names.
3. Convert the model count to numeric.
4. Drop rows with missing organisation/count values.
5. Remove duplicate rows.
6. Rename `Organization` → `Organisation`.
7. Rename the source count field → `Notable_model_count_2014_2024`.

### Columns
| Column | Meaning | Unit |
|--------|---------|------|
| `Organisation` | Organisation name. | None (text) |
| `Notable_model_count_2014_2024` | Total notable AI models attributed to the organisation from 2014 through 2024. | Models (count) |
-----------------------------------------------------------------------------------------------


# Runtime transformations not stored as separate processed CSVs
Some app pages calculate views directly from the raw Epoch files. These transformations are documented here so that displayed values remain traceable.

## Sector Shift
**Input:** `data/raw/notable_ai_models.csv`.

The `Organization categorization` column is used to group each model into:
- Industry
- Academia
- Industry-academia collaboration
- Other

For each year, the app calculates the number and percentage of models in each group.
The high-compute view keeps only models above the selected training-compute threshold, such as `≥ 1e23 FLOP`.
-----------------------------------------------------------------------------------------------


## Access Concentration
**Input:** `data/raw/notable_ai_models.csv`.

`Model accessibility` is grouped into:
- Open weights
- Closed (API / hosted)
- Unreleased

The main analysis covers 2019 onward because earlier accessibility labels are incomplete. The high-compute toggle filters to `Training compute (FLOP) ≥ 1e23`.
-----------------------------------------------------------------------------------------------


## Concentration Dynamics
**Inputs:** `data/raw/frontier_ai_models.csv` and, for selected views, `data/raw/notable_ai_models.csv`.

The page:
1. resolves source column names;
2. splits comma-separated organisations;
3. optionally rolls selected sub-labs up to parent companies;
4. deduplicates organisations after roll-up;
5. assigns `1/k` model credit to each of `k` organisations;
6. calculates Top-N share, HHI and effective organisation count over user-selected rolling windows;
7. derives additional views such as organisation-share matrices, Lorenz curves, Gini, new entrants and sector/country shares.

These values are calculated at run time rather than saved as separate CSV files.
-----------------------------------------------------------------------------------------------


# Organisation harmonisation used in the long-term processed files
The long-term Organisation Concentration pipeline harmonises selected names before fractional attribution. Examples include:
| Source label | Harmonised label |
|--------------|------------------|
| Google | Google |
| Google Research | Google |
| Google Brain | Google |
| Google DeepMind | Google |
| DeepMind | Google |
| Meta | Meta |
| Meta AI | Meta |
| Facebook | Meta |
| Facebook AI | Meta |
| Microsoft Research | Microsoft |
| Z.ai (Zhipu AI) | Zhipu AI |
| Carnegie Mellon University (CMU) | Carnegie Mellon University |
| Massachusetts Institute of Technology (MIT) | MIT |
| New York University (NYU) | New York University |
| University College London (UCL) | University College London |

Names are deduplicated after harmonisation so that aliases for the same organisation are not counted twice on the same model.
-----------------------------------------------------------------------------------------------


# Reproducibility and checks
The final repository should contain the script used to regenerate all five files in `data/processed/` from the four source samples in `data/raw/`.

The processed-data checks used in this project include:
- each collaborative model's fractional credits sum to one;
- annual organisation shares sum to one;
- CR3 lies between 0 and 1;
- HHI lies between 0 and 1;
- processed tables reproduce the committed CSVs when the build/check script is run.
-----------------------------------------------------------------------------------------------