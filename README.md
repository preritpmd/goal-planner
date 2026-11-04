# 💰 Goal Planner — Financial Goal Simulation

**Plan your financial goals. Simulate possible futures. Make informed decisions.**

Goal Planner is an interactive financial planning application that helps users estimate the likelihood of achieving their long-term financial goals through systematic monthly investments (SIPs).

Instead of assuming a fixed rate of return, the application uses **Monte Carlo simulation** to generate thousands of possible investment outcomes using historical Nifty 50 Total Return Index (TRI) data and configurable return assumptions.

🌐 **Live Demo:** https://goal-planner-q6rs.onrender.com/

📂 **GitHub Repository:** https://github.com/preritpmd/goal-planner

---

## 🚀 Features

### 1. Financial Goal Planning
- Create and manage multiple financial goals.
- Set target amounts and investment durations.
- Configure monthly SIP contributions.
- Include existing savings.
- Configure annual SIP step-ups.
- Account for inflation when estimating future targets.

### 2. Monte Carlo Simulation
- Generates 2,000 possible investment outcomes by default.
- Uses historical Nifty 50 TRI calendar-year returns.
- Supports historical bootstrap and normal return models.
- Estimates the probability of reaching a financial target.
- Uses reproducible random seeds for consistent simulations.

### 3. Risk-Based Asset Allocation

The application calculates an equity, debt and gold allocation based on investment duration and risk appetite.

Available risk profiles:
- Low risk
- Medium risk
- High risk

### 4. Portfolio Visualization

Understand possible investment outcomes using:
- **P10:** Lower-range outcome.
- **P50:** Median outcome.
- **P90:** Higher-range outcome.
- Portfolio projection bands.
- Financial goal target reference.

### 5. Inflation Adjustment

The application supports an assumed annual inflation rate of 6%.

Users can enable or disable inflation adjustment when calculating the future value of their financial goals.

### 6. SIP Recommendation

When the estimated probability of achieving a goal is below 80%, the application calculates an approximate monthly SIP required to reach an 80% success probability.

### 7. AI-Powered Explanation with Google Gemini

The application optionally uses Google's Gemini API to explain simulation results in simple language.

The AI explanation is designed to:
- Explain the simulation results to first-time investors.
- Describe the probability of achieving a financial goal.
- Explain the P10, P50 and P90 outcomes.
- Avoid exaggerated claims and buy/sell recommendations.
- Clarify that simulations are not guarantees.

If Gemini is unavailable or not configured, the application automatically falls back to a built-in explanation template.

---

## 🛠️ Technology Stack

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| Alternative Interface | Streamlit |
| Numerical Computation | NumPy |
| Data Processing | Pandas |
| API Validation | Pydantic |
| Historical Data | Nifty 50 TRI |
| AI Integration | Google Gemini API |
| Testing | Pytest |
| Deployment | Render |
| Version Control | Git and GitHub |

---

## 🧠 System Architecture

The application follows a client-server architecture.

```text
                 USER
                  |
                  v
          Frontend Interface
             HTML / CSS / JS
                  |
                  v
             FastAPI
            /api/simulate
                  |
                  v
          Goal Input Validation
                  |
                  v
          Asset Allocation Engine
                  |
                  v
          Monte Carlo Simulation
                  |
                  v
          Statistical Analysis
           /       |       \
          v        v        v
         P10      P50      P90
                  |
                  v
          Success Probability
                  |
                  v
          Explanation Engine
             /          \
            v            v
         Gemini       Template
             \          /
              v        v
             JSON Response
                  |
                  v
          Frontend Results
```

### Simulation Workflow

1. The user enters a financial goal, investment amount, duration and risk profile.
2. The frontend sends the inputs to the FastAPI backend.
3. The backend validates the request.
4. The allocation module calculates the equity, debt and gold proportions.
5. The simulation engine generates possible investment outcomes.
6. Statistical analysis calculates success probability and outcome percentiles.
7. The explanation engine generates a plain-language summary.
8. The frontend displays the results.

---

## 📊 Simulation Methodology

### Monte Carlo Simulation

The application models uncertainty by simulating multiple possible investment futures.

Each simulated future consists of yearly portfolio returns. Monthly SIP contributions are added throughout the investment period.

The simulation uses:
- Historical bootstrap or normal equity returns.
- Normal return assumptions for debt and gold.
- Monthly compounding.
- Annual SIP step-ups.
- Existing savings as initial capital.

### Asset Allocation

The allocation engine uses investment duration and risk appetite.

The base equity allocation depends on the investment horizon, while the selected risk profile adjusts the equity percentage.

Gold allocation is capped at 10%.

### Statistical Measures

| Metric | Explanation |
|---|---|
| P10 | 10% of simulated outcomes are at or below this value. |
| P50 | Median simulated outcome. |
| P90 | 90% of simulated outcomes are at or below this value. |
| Success Probability | Percentage of simulated outcomes reaching the target. |

### Inflation

The application uses an assumed annual inflation rate of 6% when inflation adjustment is enabled.

---

## 📁 Project Structure

```text
goal-planner/
│
├── api.py
├── app.py
├── requirements.txt
├── pytest.ini
│
├── data/
│   └── nifty50_tri_calendar_returns.csv
│
├── planner/
│   ├── __init__.py
│   ├── allocation.py
│   ├── charts.py
│   ├── data.py
│   ├── explain.py
│   └── simulation.py
│
├── static/
│   └── index.html
│
├── tests/
│   ├── test_api.py
│   └── test_simulation.py
│
├── .gitignore
├── LICENSE
└── README.md
```

### Important Modules

| File | Responsibility |
|---|---|
| `api.py` | FastAPI backend and simulation endpoint |
| `app.py` | Alternative Streamlit interface |
| `planner/allocation.py` | Risk-based asset allocation |
| `planner/simulation.py` | Monte Carlo simulation engine |
| `planner/data.py` | Historical return data and NAV utilities |
| `planner/explain.py` | Template and Gemini explanations |
| `planner/charts.py` | Portfolio visualization |
| `static/index.html` | Main web frontend |
| `tests/` | Automated tests |

---

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or newer
- Git
- VS Code (recommended)

### 1. Clone the Repository

```bash
git clone https://github.com/preritpmd/goal-planner.git

cd goal-planner
```

### 2. Create a Virtual Environment

**Windows PowerShell:**

```powershell
python -m venv .venv

.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python -m venv .venv

source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure Gemini API

Create a Gemini API key through Google AI Studio.

Set the key as an environment variable.

**Windows PowerShell:**

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"
```

Optionally configure the model:

```powershell
$env:GEMINI_MODEL="gemini-flash-latest"
```

Never commit API keys to GitHub or include them in frontend JavaScript.

### 5. Run the Application

```bash
python -m uvicorn api:app --reload
```

Open:

http://127.0.0.1:8000

### 6. Access API Documentation

FastAPI automatically provides interactive API documentation.

http://127.0.0.1:8000/docs

### 7. Run Automated Tests

```bash
pytest -q
```

---

## 🔌 API Documentation

### Simulation Endpoint

**POST** `/api/simulate`

Example request:

```json
{
  "goal": {
    "name": "House Down Payment",
    "target": 2500000,
    "years": 8,
    "sip": 25000,
    "savings": 100000,
    "step_up": 0.05,
    "inflate": true
  },
  "risk": "medium",
  "mode": "bootstrap",
  "haircut": 0.03,
  "use_ai": true
}
```

### Request Parameters

| Parameter | Description |
|---|---|
| `goal.name` | Financial goal name |
| `goal.target` | Target amount in today's rupees |
| `goal.years` | Investment duration |
| `goal.sip` | Monthly investment |
| `goal.savings` | Existing savings |
| `goal.step_up` | Annual SIP increase |
| `goal.inflate` | Whether to adjust target for inflation |
| `risk` | Low, medium or high |
| `mode` | Bootstrap or normal |
| `haircut` | Equity return adjustment |
| `use_ai` | Whether to request an AI explanation |

### Response

The API returns:
- Success probability.
- Inflation-adjusted target.
- Total invested amount.
- Asset allocation.
- P10, P50 and P90 outcomes.
- Portfolio projection bands.
- Additional goal results.
- Recommended SIP when applicable.
- Plain-language explanation.

---

## ☁️ Deployment

The application is deployed using Render.

**Live Application:** https://goal-planner-q6rs.onrender.com/

### Render Configuration

| Setting | Value |
|---|---|
| Platform | Render |
| Framework | FastAPI |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn api:app --host 0.0.0.0 --port $PORT` |

### Environment Variables

Configure the following in Render's Environment settings:

```text
GEMINI_API_KEY=your_api_key
GEMINI_MODEL=gemini-flash-latest
```

Keep API credentials private.

---

## 🧪 Testing

The project includes automated tests for simulation calculations and API behavior.

Run:

```bash
pytest -q
```

---

## ⚠️ Limitations and Disclaimer

This application is intended for educational and experimental financial planning.

Important limitations:
- Historical returns do not predict future performance.
- The simulation uses a limited historical equity dataset.
- Equity, debt and gold returns are treated as independent, simplifying real-world correlations.
- Yearly returns are spread evenly across 12 months.
- Taxes, expense ratios, exit loads and transaction costs are not included.
- Debt and gold returns rely on assumptions.
- Asset allocation is rule-based, not a personalized investment recommendation.
- AI-generated explanations may be imperfect.

**Disclaimer:** This application does not provide financial advice and does not guarantee investment outcomes. All simulation results are estimates based on assumptions and historical data.

---

## 🔮 Future Improvements

- User authentication and personalized portfolios.
- Persistent storage for financial goals.
- More historical asset-class datasets.
- Improved market correlation modeling.
- Portfolio optimization.
- Additional risk and performance metrics.
- Exportable financial planning reports.
- Enhanced interactive dashboards.

---

---

## 👨‍💻 Author

**Prerit Devashetti**

GitHub: https://github.com/preritpmd

Project: https://goal-planner-q6rs.onrender.com/

---

**Built to make financial planning more understandable through simulation, statistics and technology.**
