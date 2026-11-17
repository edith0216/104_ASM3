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

| 3 | `pages/Sector_Shift.py` | Adarsh Kumbhar | Claude | Write the Streamlit and Altair code for the sector page: classify each model as industry, academia, collaboration or other from `Organization categorization`, plot yearly shares as a 100% stacked bar, and add a training-compute scatter with an adjustable threshold | Working page code: the sector classifier, share calculation, both charts, KPI tiles and a "Trace a number" panel | Rebuilt the 2024 industry-only share by hand in Google Sheets from raw `notable_ai_models.csv`: filtered Publication date to 2024 (98 rows), then counted "Industry" (79) plus "Industry,Industry" (2) = 81, so 81/98 = 82.7%. This would have failed if the classifier mis-handled joint company models or the year filter was wrong. It matched the page metric and the trace panel exactly | Accepted. Classification rule written up in the page's "Data and method" note |

| 4 | `pages/Access_Concentration.py` | Akash | **To confirm** | **To confirm** | **To confirm** | **To confirm** | **To confirm** |
-----------------------------------------------------------------------------------------------

| 5 | `pages/Organisation_Concentration.py` | Menghan | Chat GPT | Debugging errors, unify formatting and data processing logic | Calculate CR3 and HHI, and debug errors and chart formatting in the Plotly chart | Two recounts, either of which would fail if the pipeline or chart were wrong: (1) OpenAI = 7 in 2024 matches across the raw Stanford AI Index Figure 1.3.6.csv, stanford_notable_2024.csv and chart 2; (2) the 2024 Top-3 share recomputed by hand from raw frontier_ai_models.csv gives (OpenAI 4 + Zhipu AI 2 + Anthropic 2) / 12 models = 66.7%, matching the page metric and frontier_concentration_by_year.csv | Adopted with modifications;CR3 hidden for years with ≤ 3 organisations (where it is 100% by construction)|

