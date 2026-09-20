# Run Keepers of Akasha

## Prerequisites

- Python 3
- Project dependencies installed
- A `.env` file containing the required OpenRouter API key for live AI evaluation
- Ports `8501` and `8502` available

## Run the demo

From the repository root, run:

```bash
python run_demo.py
```

On Windows, this equivalent command can also be used:

```powershell
py run_demo.py
```

The launcher starts both Streamlit interfaces:

- Student interface: `http://localhost:8501`
- Professor dashboard: `http://localhost:8502`

The student interface opens automatically in the default browser. Use the **Professor dashboard ↗** control in the student sidebar to open the professor view.

Press `Ctrl+C` in the launcher terminal to stop both servers.

## Network behavior

Live reasoning evaluation requires network access to the configured model provider.

If model evaluation cannot be completed, the student interface does not present fallback text as AI-generated feedback. It displays:

> Evaluation couldn't be made  
> Servers might be busy or check your network connection.

The local Streamlit interface and persisted SQLite learning records remain available.
