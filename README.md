# AI Concentration Explorer

**36104 Data Visualisation and Narratives — Assignment 3, Spring 2026**

Deployed app: https://104asm3-jns5mux863yavglqhfdkn5.streamlit.app/

## Question

Is influential AI model development concentrated in fewer organisations?

## Persona

**Technology policy analyst** advising government on AI. The analyst needs to decide whether AI capability is pooling in a small number of organisations, sectors or access models closely enough to justify a policy response (for example, competition review or funding for public and open research), and whether that answer holds up when the way of counting changes.

## User stories

1. **As a** technology policy analyst, **I want** to see what share of frontier AI models the top few organisations produce each year, **so that** I can judge whether development is concentrated among a handful of labs.
   *Walkthrough:* Summary → **Organisation Concentration**. Move the year slider and change the Top-N selector to see the leading organisations' share.

2. **As a** technology policy analyst, **I want** to know whether notable AI development has moved from universities into industry, **so that** I can decide whether public research capacity needs support.
   *Walkthrough:* Summary → **Sector Shift**. Use the year-range slider on the stacked bar chart, then change the high-compute threshold to see who builds the largest models. Open "Trace a number back to the source" to check any share.

3. **As a** technology policy analyst, **I want** to check whether access to AI models is shifting behind company APIs, and whether the concentration answer survives different counting choices, **so that** my advice does not rest on one way of measuring.
   *Walkthrough:* Summary → **Access Concentration**. Turn on the high-compute toggle and compare the open-weight and closed shares. Then go to **Concentration Dynamics** and change the model set, Top-N, window and parent roll-up.

## App structure

| Page | Question it answers | Primary contributor |
|---|---|---|
| `Summary.py` | Overall answer, key findings, limitations | Menghan |
| `pages/Organisation_Concentration.py` | Do a few organisations account for most frontier models? | Menghan |
| `pages/Sector_Shift.py` | Has notable development shifted from academia to industry? | Adarsh Kumbhar |
| `pages/Access_Concentration.py` | Is access concentrating behind company APIs? | Akash |
| `pages/Concentration_Dynamics.py` | How does concentration change with time and counting choices? | Aarushi |

## Data

All data are committed snapshots in `Data/raw/` (source files) and `Data/processed/` (files the app reads). See the data dictionary for sources, licences, columns, coverage and transforms.

- Epoch AI, *Notable AI Models* and *Frontier AI Models* (CC BY 4.0), snapshot 25 October 2026
- Stanford HAI, *AI Index Report 2025*, Figures 1.3.6 and 1.3.7

## AI use

Each member's AI use is recorded in [`AI_PROVENANCE.md`](AI_PROVENANCE.md).

## Run locally

```bash
pip install -r requirements.txt
streamlit run Summary.py
```
