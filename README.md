# freelance-optimizer
A Streamlit dashboard that picks the best mix of freelance projects to maximize weekly earnings, using a 0-1 Integer Program solved with HiGHS via AMPL.
Run locally
pip install -r requirements.txt
streamlit run app_clean.py
Deploy on Streamlit Cloud

Push this repo to GitHub
Go to share.streamlit.io
Click Create app, point it to this repo, main file is app_clean.py
Deploy

Model

Decision variables: x_j in {0,1} for each project j
Objective: maximize total revenue
Constraints: time budget, minimum revenue, max projects accepted
