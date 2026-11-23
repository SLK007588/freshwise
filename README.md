# FreshWise

Prose word count: 193

## Status
A Streamlit prototype for pantry tracking and explainable recipe recommendations. Implemented: date flags, add/edit/remove pantry entries, a fixed five-recipe catalogue, rule-based ranking, explanation toggle and session-only dismissal. Recommendation and date logic is simulated with explicit rules; no trained AI model or food-safety assessment is used. Pantry data is not saved permanently.

## Technology
- Python and Streamlit: interactive web dashboard.
- pandas: pantry overview table.
- OpenAI ChatGPT/Codex: assisted code and report drafting; suggestions were reviewed through interactive checks and screenshots.

## Run
1. Install Python 3.10 or later.
2. Install dependencies: `pip install streamlit pandas`.
3. From this folder run: `streamlit run app.py`.

## Development record
- Stage 1: built the pantry overview, entered-date flags and add/remove controls; checked these in the browser.
- Stage 2: added fixed recipes, ingredient matching, urgency ranking, explanations, correction and dismissal controls; walked through the interactions and captured screenshots.
- Stage 3: prepared a report with the system flow and interaction examples.

## AI assistance
ChatGPT/Codex helped propose and implement rule-based recommendation code, draft report prose, and organise diagram/storyboard content.
## Additional files
The report is `FreshWise_A2_Report.pdf`. Interface screenshots are stored alongside `app.py`.

