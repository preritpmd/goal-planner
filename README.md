# 💰 Goal Planner — Financial Goal Simulation

**Plan your financial goals. Simulate possible futures. Make informed decisions.**

Goal Planner is an interactive financial planning application that helps users understand how likely they are to achieve their financial goals through monthly investments (SIPs).

Instead of assuming a fixed rate of return, the application uses **Monte Carlo simulation** to generate thousands of possible investment outcomes using historical Nifty 50 Total Return Index (TRI) data and configurable return assumptions.

Users can explore different investment amounts, time horizons, risk profiles and portfolio allocations to understand the uncertainty associated with long-term financial planning.

🌐 **Live Demo:** https://goal-planner-q6rs.onrender.com/

📂 **GitHub Repository:** https://github.com/preritpmd/goal-planner

---

## 🚀 Features

### 1. Interactive Financial Goal Planning
- Create and manage multiple financial goals.
- Set target amounts and investment horizons.
- Configure monthly SIP contributions.
- Include existing savings.
- Set annual SIP step-ups.

### 2. Monte Carlo Simulation
- Simulates 2,000 possible investment futures by default.
- Uses historical Nifty 50 TRI calendar-year returns.
- Supports historical bootstrap and normal return models.
- Estimates the probability of achieving a financial goal.
- Uses a fixed random seed for reproducible simulations.

### 3. Risk-Based Asset Allocation

The application suggests an equity, debt and gold allocation based on:
- Investment duration.
- User's risk appetite.
- Portfolio allocation rules.

Users can select:
- Low risk
- Medium risk
- High risk

### 4. Interactive Portfolio Visualization

Visualizes projected portfolio growth through:
- Median portfolio projection (P50).
- 10th percentile (P10).
- 90th percentile (P90).
- Middle 50% outcome range.
- Target amount reference line.

### 5. Inflation Adjustment

Supports an assumed annual inflation rate of 6%.

The application adjusts the future target amount to account for inflation.

### 6. SIP Recommendation

If the simulated probability of achieving the goal is below 80%, the application estimates the monthly SIP required to reach approximately 80% simulated success probability.

### 7. Plain-Language Explanations

Provides understandable explanations of simulation results.

Optionally supports Claude-generated explanations when an Anthropic API key is configured. Otherwise, it uses a built-in explanation template.

---

## 🛠️ Technology Stack

| Component | Technologies |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, FastAPI |
| Alternative UI | Streamlit |
| Simulation | NumPy |
| Data Processing | Pandas |
| Visualization | Matplotlib, SVG |
| Validation | Pydantic |
| Testing | Pytest |
| Deployment | Render |
| Version Control | Git, GitHub |
| Optional AI | Anthropic Claude API |

---

## 🧠 How It Works

Goal Planner follows a client-server architecture.

1. **User Input:** The user enters financial goals, investment amount, duration, savings and risk appetite.
2. **API Request:** The frontend sends the information to the FastAPI backend through a REST API.
3. **Asset Allocation:** The allocation module determines the equity, debt and gold proportions.
4. **Simulation Engine:** The Monte Carlo engine generates 2,000 possible investment scenarios.
5. **Statistical Analysis:** The application calculates success probability and portfolio percentiles.
6. **Visualization:** The frontend displays the results through interactive charts and probability indicators.
7. **Explanation:** The application generates a plain-language summary of the results.

### Application Architecture

```text
                 USER
                  |
                  v
          Frontend (HTML/CSS/JS)
                  |
                  v
           FastAPI REST API
             /api/simulate
                  |
                  v
          Asset Allocation
                  |
                  v
         Monte Carlo Engine
                  |
          +-------+-------+
          |       |       |
          v       v       v
        Equity   Debt    Gold
          |       |       |
          +-------+-------+
                  |
                  v
          Statistical Analysis
                  |
          +-------+-------+
          |       |       |
          v       v       v
        P10      P50     P90
                  |
                  v
          Explanation Engine
                  |
                  v
          JSON Response
                  |
                  v
          Frontend Visualization
```

---

## 📊 Simulation Methodology

The application uses Monte Carlo simulation to model uncertainty in future investment returns.

### Historical Equity Returns

The default model uses Nifty 50 TRI calendar-year returns from 2006–2024.

Each simulated year randomly selects a historical equity return, with an adjustable return haircut.

### Debt and Gold

Debt and gold returns are modeled using configurable normal distributions.

Default assumptions:

- Debt: 7% mean annual return, 2.5% standard deviation.
- Gold: 8% mean annual return, 13% standard deviation.

### Portfolio Allocation

The allocation depends on investment duration and risk appetite.

The application uses simple rule-based allocation rather than claiming to provide an optimized investment portfolio.

### Statistical Measures

| Metric | Meaning |
|---|---|
| P10 | 10th percentile outcome |
| P50 | Median outcome |
| P90 | 90th percentile outcome |
| Success Probability | Percentage of simulated futures reaching the target |

**Important:** These are model-based estimates, not guaranteed investment returns.

---

## 📁 Project Structure

```text
goal-planner/
│
├── api.py
│
├── app.py
│
├── requirements.txt
│
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

- `api.py` — FastAPI backend and simulation endpoint.
- `app.py` — Alternative Streamlit interface.
- `planner/allocation.py` — Risk-based asset allocation.
- `planner/simulation.py` — Monte Carlo simulation engine.
- `planner/data.py` — Historical returns and mutual fund NAV data.
- `planner/explain.py` — Plain-language and optional AI explanations.
- `planner/charts.py` — Portfolio visualization.
- `static/index.html` — Main interactive web frontend.
- `tests/` — Automated API and simulation tests.

---

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or newer.
- Git.
- VS Code (recommended).

### 1. Clone the Repository

```bash
git clone https://github.com/preritpmd/goal-planner.git

cd goal-planner
```

### 2. Create a Virtual Environment

**Windows:**

```powershell
python -m venv venv

venv\Scripts\activate
```

**macOS/Linux:**

```bash
python -m venv venv

source venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Run the FastAPI Application

```bash
uvicorn api:app --reload
```

Open your browser:

http://localhost:8000

### 5. Run the Alternative Streamlit Application

```bash
streamlit run app.py
```

### 6. Run Automated Tests

```bash
pytest -q
```

---

## 🔌 API Documentation

The application exposes a REST API through FastAPI.

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
  "use_ai": false
}
```

The API returns:
- Success probability.
- Adjusted target.
- Total invested amount.
- Asset allocation.
- P10, P50 and P90 values.
- Portfolio projection bands.
- SIP recommendation when required.
- Plain-language explanation.

### Interactive API Documentation

Once the backend is running, visit:

http://localhost:8000/docs

---

## 🧪 Testing

The project includes automated tests for:

- Monte Carlo simulation calculations.
- SIP future-value calculations.
- Annual SIP step-up calculations.
- Reproducibility using random seeds.
- Asset allocation constraints.
- Probability monotonicity with increasing SIP.
- API response structure.
- Invalid request validation.
- Frontend availability.

Run the test suite:

```bash
pytest -q
```

---

## ☁️ Deployment

The application is deployed using Render.

**Live Application:**

https://goal-planner-q6rs.onrender.com/

Deployment configuration:

| Setting | Value |
|---|---|
| Platform | Render |
| Repository | GitHub |
| Framework | FastAPI |
| Build Command | `pip install -r requirements.txt` |
| Start Command | `uvicorn api:app --host 0.0.0.0 --port $PORT` |

---

## ⚠️ Limitations and Assumptions

This application is designed for educational and experimental financial planning.

Some limitations include:

- Historical equity returns do not predict future performance.
- Only 19 calendar years of bundled equity history are available.
- Asset classes are modeled as independent, which simplifies real market correlations.
- Yearly returns are spread evenly across 12 months.
- Taxes, expense ratios, exit loads and transaction costs are not included.
- Debt and gold returns are assumptions rather than sourced historical datasets.
- The allocation strategy is rule-based and not a personalized investment recommendation.

**Disclaimer:** This application is for educational purposes only. It does not provide financial advice or guarantee investment outcomes.

---

## 🔮 Future Improvements

Potential enhancements include:

- User authentication and personalized portfolios.
- Persistent storage for financial goals.
- More historical asset-class datasets.
- Portfolio optimization.
- Improved market correlation modeling.
- Additional investment performance metrics.
- Exportable financial planning reports.
- Enhanced interactive dashboards.

---

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## 👨‍💻 Author

**Prerit Devashetti**

GitHub: https://github.com/preritpmd

Project: [Goal Planner](https://goal-planner-q6rs.onrender.com/)

---

**Built to make financial planning more understandable through simulation, statistics and technology.**
