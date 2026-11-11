# 🏪 Sari-Sari Store Manager: ML for Small Businesses

A Streamlit app that uses all three machine learning paradigms to help a Filipino
neighborhood store owner make three everyday decisions.

| Store question | Paradigm | Algorithm |
|---|---|---|
| How much will we sell tomorrow? | Supervised Learning | Random Forest and Linear Regression |
| Which products behave alike? | Unsupervised Learning | KMeans clustering |
| When should we restock, and how much? | Reinforcement Learning | Q-learning, written from scratch |

**Team:** Condesa, John Brence S. · De Castro, Carl Andre A. · Maher, Scott Franklin T. · Murillo, Marlon Jr. V.

## Features

- **Sales Prediction:** trains two models on a year of daily sales, compares their error side by side, shows which factors matter most, and predicts sales for any day you describe.
- **Product Groups:** groups 30 store products by price, weekly sales, and profit margin, uses the elbow method to justify 3 groups, and gives plain-language advice for each group.
- **Restock Agent:** trains an agent by trial and error to decide when to reorder Pancit Canton, then compares its profit against random ordering and always ordering 10 units.

All data is synthetic and generated with a fixed random seed, so every run gives the same results.

## Results

| Sales model | Average error (MAE) | R² |
|---|---|---|
| Linear Regression | ₱95.86 | 0.903 |
| Random Forest | ₱108.09 | 0.872 |

| Restock strategy | Average profit per 30 days |
|---|---|
| Learned Q-learning agent | ₱385 |
| Random ordering | ₱206 |
| Always order 10 | ₱62 |

Linear Regression wins because our synthetic sales rule adds its effects together, which is exactly what Linear Regression assumes. The Q-learning agent lands within about ₱1 of the best possible policy.

## Getting started

You need Python 3.10 or newer.

```bash
git clone https://github.com/Iskatiboi/IS_Finals.git
cd IS_Finals/sarisari_ml
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The app opens at http://localhost:8501. Run it from inside the `sarisari_ml` folder so the app's theme loads.

## Project structure

```
sarisari_ml/
├── app.py              # Streamlit app with 4 tabs
├── data.py             # Synthetic sales and product data
├── supervised.py       # Sales prediction models
├── unsupervised.py     # Product clustering and elbow method
├── rl_agent.py         # Restocking environment and Q-learning agent
├── style.css           # Store front styling
├── .streamlit/
│   └── config.toml     # Theme colors and fonts
├── requirements.txt
└── README.md           # Full guide: algorithms, team split, slides, Q&A
```

Each module can also be tested on its own, for example `python rl_agent.py`.

## Built with

Python · NumPy · pandas · scikit-learn · Streamlit

## More details

See [sarisari_ml/README.md](sarisari_ml/README.md) for how each algorithm works, why we chose it, troubleshooting tips, the team split, the slide outline, and likely panel questions with answers.
