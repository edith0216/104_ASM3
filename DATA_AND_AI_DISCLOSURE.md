# Data and AI disclosure statement

Group 17, 36104 Data Visualisation and Narratives, Assignment 3 Part 2.
Members: Aarushi Kohli, Adarsh Kumbhar, Akash Tomar, Menghan Sun.

## Data

**Sources.** Every number in the app comes from public data. We did not collect, purchase or invent any data.

| Dataset | Publisher | Licence | Used for |
|---|---|---|---|
| Notable AI models (`data/raw/notable_ai_models.csv`) | Epoch AI, *Data on AI Models* | CC BY 4.0 | Summary, Sector Shift and Access pages |
| Frontier AI models (`data/raw/frontier_ai_models.csv`) | Epoch AI, *Data on AI Models* | CC BY 4.0 | Concentration Dynamics and Organisation Concentration pages |
| AI Index Figures 1.3.6 and 1.3.7 (`data/raw/`) | Stanford HAI, *AI Index Report* | CC BY-ND 4.0 | Organisation Concentration page |

Retrieval dates, columns, units, primary keys and time coverage are in `data/data_dictionary.md`.

**What we did to the data.** Source files are stored unchanged in `data/raw/`. Processed files in `data/processed/` are rebuilt from them by the transforms documented in the data dictionary. We filtered by year, grouped labels (for example, Epoch's accessibility labels into open, closed and unreleased) and counted models. We did not impute missing values or edit any row by hand.

**Personal data.** None. The datasets describe AI models and organisations, not individuals.

**Limits of the data.** The datasets are curated lists of models that Epoch or Stanford judged notable, not every model released. Each model counts once, whatever its size or use. Training-compute estimates are missing for many models, and more often for closed models, so views filtered by compute are not a fair sample. These limits are also stated on screen.

## AI use

**Tools.** Members used Claude (Anthropic) and ChatGPT (OpenAI).

**What the group decided without AI.** The question, the persona, the user stories and which angle each member took were agreed by the group.

**What AI was used for.** Drafting and debugging Streamlit and pandas code, checking calculations, and drafting documentation text. The extent varied by member. In some parts AI wrote most of the code. Every substantive use is recorded, with who, tool, prompt, output and check, in the AI provenance matrix.

**How AI output was checked.** No number on screen was taken from an AI answer. Every displayed number is computed from the files in `data/raw/` and `data/processed/`. Members verified AI-written code by running it, tracing displayed numbers back to the source rows, and recounting figures by hand from the raw files in a spreadsheet. Each provenance row names a check that could have failed. One check did change a result: on the Access page, a count of compute estimates by access type showed that the high-compute view over-represents open-weights models (70% of them publish an estimate against 37% of closed models), so we withdrew a claim that open weights were prominent among high-compute models and added this as a stated limitation.

**Responsibility.** We have reviewed the app and documentation, and we take responsibility for every claim in them, including those first drafted with AI help.
