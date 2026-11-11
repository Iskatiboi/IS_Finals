# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Primary audience: the panel grading a machine learning final lab, watching a live demo on Nov 17, 2026. Presenters: a team of 4 students who operate the app and explain the code line by line in Q&A. The imagined end user is a Filipino sari-sari store owner.

## Product Purpose

Show all three machine learning paradigms solving three decisions a neighborhood store owner really makes: expected sales, which products need attention, and when to restock. Success means the panel remembers a tool that solves a real problem, with the ML in service of that problem.

## Positioning

Each ML paradigm is tied to one concrete store decision, not shown as a detached algorithm demo.

## Operating Context

Runs locally with `streamlit run app.py` during a live class presentation. The display setup is undecided, so text and charts should stay readable on a projector. It may run without venue internet.

## Capabilities and Constraints

- Python, numpy, pandas, scikit-learn, Streamlit. Streamlit built-in charts only, no extra chart libraries.
- One app with 4 tabs: Home, Sales Prediction (Supervised), Product Groups (Unsupervised), Restock Agent (Reinforcement Learning).
- Code must stay simple enough for 4 students to explain line by line.
- Data is synthetic, generated with a fixed seed, and must be labeled as synthetic.

## Brand Commitments

- Name: Sari-Sari Store Manager.
- Title: "🏪 Sari-Sari Store Manager: ML for Small Businesses".
- The app shows the team members' names, kept in the TEAM list in `app.py`.

## Evidence on Hand

Only synthetic data and the measured model results. There are no real store customers, testimonials, or deployments, and none may be implied.

## Product Principles

1. The store decision comes first and the algorithm second.
2. Every result is stated in plain language a store owner would understand.
3. Honest numbers: show what the models really scored, even when the simpler model wins.
4. Nothing on screen should be harder to explain than the ML itself.
