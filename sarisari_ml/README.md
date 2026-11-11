# 🏪 Sari-Sari Store Manager: ML for Small Businesses

One Streamlit app that shows all three machine learning paradigms on problems a
small Filipino neighborhood store really has.

| Store question | Paradigm | Algorithm | File |
|---|---|---|---|
| How much will we sell tomorrow? | Supervised | Random Forest, Linear Regression | `supervised.py` |
| Which products behave alike? | Unsupervised | KMeans | `unsupervised.py` |
| When should we restock? | Reinforcement Learning | Q-learning | `rl_agent.py` |

All data comes from `data.py` and uses a fixed seed, so results are the same every run.

## How to install and run

You need Python 3.10 or newer. Open a terminal in the `sarisari_ml` folder, then run:

```bash
pip install -r requirements.txt
```

```bash
streamlit run app.py
```

The app opens at http://localhost:8501. To test one part on its own, run
`python data.py`, `python supervised.py`, `python unsupervised.py`, or `python rl_agent.py`.

Run the app from inside the `sarisari_ml` folder, because Streamlit only finds the
colors and fonts in `.streamlit/config.toml` from there.

**How the look works.** The hand-painted store front comes from two files and has
no effect on the machine learning. `.streamlit/config.toml` sets the colors and
fonts, and `style.css` paints the sign, wire mesh, and tabs. The fonts (Bowlby One
and Barlow) load from Google Fonts, so without internet the app still works but
falls back to plainer lettering.

**Troubleshooting on Windows**

- If `streamlit` or `pip` is "not recognized", use `python -m streamlit run app.py` and `python -m pip install -r requirements.txt`.
- On the first run, Streamlit may ask for an email in the terminal. Leave it blank and press Enter.
- `requirements.txt` keeps pandas below version 3 on purpose. On a laptop with Windows Smart App Control turned on, pandas 3.1.1 failed with "An Application Control policy has blocked this file", while pandas 2.3.3 loaded normally.

- If Windows says "Python was not found", reopen the terminal. If it continues, check that Python is installed and review Settings > Apps > Advanced app settings > App execution aliases.

**Before the demo:** install and run the app on the exact laptop you will present
with, ahead of time and without relying on the venue's internet.

**During the demo:** scrolling with the mouse while the pointer is over a chart
zooms that chart. Scroll with the pointer in the margin, and double-click a chart
to reset its zoom.

## The algorithms and why we chose them

**Random Forest and Linear Regression (Supervised).** We have past days with known
sales, so this is a regression problem with labeled examples. Linear Regression is
the simple baseline: one peso amount per factor. Random Forest averages 100 decision
trees, can capture combinations of factors, and reports which inputs mattered.

**KMeans (Unsupervised).** Nobody labeled products as "fast" or "slow", so we need an
algorithm that finds groups by itself. KMeans is simple and fast, and each group has
a center we can read and name. We scale the features first because KMeans measures
distance, and price would otherwise dominate.

**Q-learning (Reinforcement Learning).** Restocking is a chain of decisions: today's
order changes tomorrow's stock. Q-learning learns from trial and error using only the
reward. With 21 states and 3 actions, the whole "brain" is a small table we can print
and explain.

## Results (seed 42)

| Model | MAE (pesos) | R² |
|---|---|---|
| Random Forest | 108.09 | 0.872 |
| Linear Regression | 95.86 | 0.903 |

KMeans inertia for k = 1 to 4 is 90.00, 25.19, 6.93, and 4.91.

| Strategy (2000 episodes, average over 200 months) | Average 30-day profit |
|---|---|
| Learned Agent | ₱385.39 |
| Random | ₱205.65 |
| Always Order 10 | ₱61.88 |

## Suggested team split

| Member | Owns | Files | Explains |
|---|---|---|---|
| 1 | Supervised | `data.py` (sales), `supervised.py` | Train/test split, MAE, R², feature importance |
| 2 | Unsupervised | `data.py` (products), `unsupervised.py` | Scaling, KMeans, elbow method, cluster naming |
| 3 | Reinforcement Learning | `rl_agent.py` | Environment, reward, Q-update, epsilon, baselines |
| 4 | App and slides | `app.py`, `style.css`, `.streamlit/config.toml`, slides | Tabs, caching, session state, theming, running the demo |

## Suggested slide outline (12 slides)

1. Title, team members
2. The problem: running a sari-sari store by gut feel
3. Three questions, three ML paradigms (the table above)
4. Our data: synthetic, how it is generated, and why
5. Supervised: inputs, target, 80/20 split
6. Supervised results: MAE and R² side by side, feature importance
7. Unsupervised: scaling, KMeans, elbow chart justifying k = 3
8. Unsupervised results: the 3 groups and the advice for each
9. RL setup: state, actions, reward, episode
10. Q-learning: the Q-table, the update rule, epsilon-greedy
11. RL results: learning curve, policy, comparison with baselines
12. Live demo, limitations, future work (real store data, more products)

## 10 likely panel questions

1. **Why use Random Forest if Linear Regression scored better?**
   Our sales rule simply adds up effects, which is exactly what Linear Regression assumes, so it wins here (MAE ₱95.86 vs ₱108.09). We kept Random Forest because real sales may contain combinations, like rain hurting a payday more, and because it gives feature importances. Comparing the two is how we know the simpler model is enough for this data.

2. **What do MAE and R² mean?**
   MAE is the average size of the error in pesos, and lower is better. R² is the share of the variation in sales the model explains, where 1.0 is perfect.

3. **Why does temperature have some importance if it is not in your sales rule?**
   Temperature does not directly change sales in our data. It is lower on rainy days, so it carries a little information about rain, and trees can also pick up small chance patterns from a column with many different values. Importance shows what a model used, not what causes sales.

4. **Why k = 3?**
   The elbow chart. Inertia falls from 90.00 to 25.19 to 6.93 for k = 1, 2, 3, then only to 4.91 at k = 4. After k = 3, more groups add little. Three groups are also easy for a store owner to act on.

5. **Why scale the features before KMeans?**
   KMeans uses distance. Price runs up to about ₱280 while margin stays under about 35, so without scaling price would count far more than margin.

6. **What is epsilon-greedy?**
   With probability epsilon the agent tries a random action, and otherwise it picks the best known action. Epsilon falls from 1.0 to 0.05, so the agent explores first and uses its knowledge later.

7. **What does gamma mean?**
   The discount factor. At 0.9, a reward tomorrow is worth 90% of the same reward today. It lets the agent accept a ₱10 delivery fee today in order to earn sales on later days.

8. **Why Q-learning instead of a bandit?**
   A bandit assumes actions do not affect the future. Here, today's order changes tomorrow's stock, so the agent has to plan across days. Q-learning includes the value of the next state, and a bandit does not.

9. **How do you know the agent really learned? Why is there an odd entry at stock 20?**
   It averages ₱385 per month against ₱206 for Random and ₱62 for Always Order 10, on the same customer demand. Its learned rule is simple: order 10 when stock is 3 or less. The default run shows "order 5" at stock 20 because high stock is rarely visited, so that row got less practice. It never matters, since this policy never holds more than 13 units.

10. **Your data is synthetic. Does this work in real life?**
    The data shows that the methods work, not that these numbers apply to a real store. We wrote the patterns ourselves, so the models are partly rediscovering our own rules. With a real store's records, we would replace `data.py` and keep the rest of the pipeline.
