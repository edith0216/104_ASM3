# AI Provenance Matrix

Each row records one important use of AI in the project.

Each group member must have at least one row.

The verification must name a check that could have failed.

| # | Artefact / section | Who | AI tool | What was asked | What AI produced | How it was checked | Outcome |
-----------------------------------------------------------------------------------------------

| 1 | `Summary.py` | Menghan | Claude & Chat GPT| Replace hard-coded 88%, 83% and 44% values with values calculated from the data | Code that calculates the three headline figures from the data package | Compared the output with manual recounts: frontier 2025–26 = 7/8 = 87.5%; industry-only 2024 = 81/98 = 82.7%; closed access 2024 = 43/98 = 43.9%. | Accepted; hard-coded values removed |
-----------------------------------------------------------------------------------------------

| 2 | `concentration.py` / `pages/Concentration_Dynamics.py` | Aarushi | **To confirm** | **To confirm** | **To confirm** | **To confirm** | **To confirm** |
-----------------------------------------------------------------------------------------------

| 3 | `pages/Sector_Shift.py` | Adarsh Kumbhar | **To confirm** | **To confirm** | **To confirm** | **To confirm** | **To confirm** |
-----------------------------------------------------------------------------------------------

| 4 | `pages/Access_Concentration.py` | Akash | **To confirm** | **To confirm** | **To confirm** | **To confirm** | **To confirm** |
-----------------------------------------------------------------------------------------------

| 5 | `pages/Organisation_Concentration.py` | Menghan | Chat GPT | Debugging errors, unify formatting and data processing logic | Calculate CR3 and HHI, and debug errors and chart formatting in the Plotly chart | Two recounts, either of which would fail if the pipeline or chart were wrong: (1) OpenAI = 7 in 2024 matches across the raw Stanford AI Index Figure 1.3.6.csv, stanford_notable_2024.csv and chart 2; (2) the 2024 Top-3 share recomputed by hand from raw frontier_ai_models.csv gives (OpenAI 4 + Zhipu AI 2 + Anthropic 2) / 12 models = 66.7%, matching the page metric and frontier_concentration_by_year.csv | Adopted with modifications;CR3 hidden for years with ≤ 3 organisations (where it is 100% by construction)|

