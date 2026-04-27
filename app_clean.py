
import streamlit as st
import pulp
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Freelance Project Optimizer",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

html, body, [class*="css"] {
    background-color: #F7F8FA;
    color: #1C1C2E;
}

[data-testid="stSidebar"] {
    background-color: #1C1C2E !important;
    padding-top: 2rem;
}
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div {
    color: #EAEAEA !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #FFFFFF !important;
}

.page-title {
    font-size: 1.9rem;
    font-weight: 700;
    color: #1C1C2E;
    margin-bottom: 0.1rem;
}
.page-subtitle {
    font-size: 0.95rem;
    color: #6B7280;
    margin-bottom: 1.5rem;
}
.divider {
    border: none;
    border-top: 1.5px solid #E5E7EB;
    margin: 1.2rem 0;
}

.kpi-card {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 1.1rem 1.4rem;
    box-shadow: 0 1px 6px rgba(0,0,0,0.07);
}
.kpi-card .kpi-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: #9CA3AF;
    margin-bottom: 0.3rem;
}
.kpi-card .kpi-value {
    font-size: 1.75rem;
    font-weight: 700;
    color: #1C1C2E;
    line-height: 1;
}
.kpi-card .kpi-sub {
    font-size: 0.78rem;
    color: #6B7280;
    margin-top: 0.25rem;
}

.accept-row {
    background: #F0FDF4;
    border-left: 3px solid #22C55E;
    border-radius: 8px;
    padding: 0.65rem 1rem;
    margin-bottom: 0.45rem;
}
.reject-row {
    background: #FFF7F7;
    border-left: 3px solid #EF4444;
    border-radius: 8px;
    padding: 0.65rem 1rem;
    margin-bottom: 0.45rem;
}
.row-title { font-size: 0.88rem; font-weight: 600; color: #1C1C2E; }
.row-meta  { font-size: 0.78rem; color: #6B7280; margin-top: 0.1rem; }
.badge {
    display: inline-block;
    padding: 0.12rem 0.55rem;
    border-radius: 20px;
    font-size: 0.68rem;
    font-weight: 600;
    margin-right: 0.3rem;
}
.badge-green  { background: #DCFCE7; color: #166534; }
.badge-red    { background: #FEE2E2; color: #991B1B; }
.badge-blue   { background: #DBEAFE; color: #1E40AF; }

.stButton > button {
    background-color: #1C1C2E !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.6rem 2rem !important;
    font-size: 0.92rem !important;
    font-weight: 600 !important;
    width: 100% !important;
    letter-spacing: 0.02em !important;
    transition: background 0.2s !important;
}
.stButton > button:hover {
    background-color: #2D2D44 !important;
}

#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("### Settings")
    st.markdown("---")
    total_hours  = st.slider("Available hours per week", 5, 80, 40)
    min_revenue  = st.slider("Minimum earnings target ($)", 0, 2000, 150, step=25)
    max_projects = st.number_input("Maximum number of projects", min_value=1, max_value=20, value=5, step=1)
    st.markdown("---")
    st.markdown("**Model Type:** 0-1 Integer Program")
    st.markdown("**Solver:** CBC via PuLP")
    st.markdown("---")
    st.markdown("**Constraints:**")
    st.markdown("- Total hours <= capacity")
    st.markdown("- Total revenue >= minimum")
    st.markdown("- Projects accepted <= max limit")

# HEADER
st.markdown('<p class="page-title">Freelance Project Optimizer</p>', unsafe_allow_html=True)
st.markdown('<p class="page-subtitle">Find the optimal set of projects to maximize your weekly earnings using Integer Programming.</p>', unsafe_allow_html=True)
st.markdown('<hr class="divider">', unsafe_allow_html=True)

# TABS
tab1, tab2, tab3 = st.tabs(["Projects", "Results", "Model"])

# TAB 1, PROJECTS
with tab1:
    st.markdown("#### Available Projects")
    st.caption("Edit the table below. You can add or remove rows.")

    default_data = pd.DataFrame([
        {"Project Name": "SolidWorks CAD Assembly",    "Revenue ($)": 120, "Hours": 8,  "Skill": "CAD"},
        {"Project Name": "AnyLogic Simulation Model",  "Revenue ($)": 180, "Hours": 14, "Skill": "Simulation"},
        {"Project Name": "AutoCAD Floor Plan",         "Revenue ($)": 70,  "Hours": 5,  "Skill": "CAD"},
        {"Project Name": "Arena Simulation Report",    "Revenue ($)": 150, "Hours": 11, "Skill": "Simulation"},
        {"Project Name": "3D Product Rendering",       "Revenue ($)": 90,  "Hours": 6,  "Skill": "Design"},
        {"Project Name": "Injection Mold Design",      "Revenue ($)": 200, "Hours": 16, "Skill": "CAD"},
        {"Project Name": "Supply Chain Consulting",    "Revenue ($)": 130, "Hours": 9,  "Skill": "Consulting"},
        {"Project Name": "Simio Factory Layout",       "Revenue ($)": 160, "Hours": 13, "Skill": "Simulation"},
        {"Project Name": "Logo & Branding Pack",       "Revenue ($)": 55,  "Hours": 4,  "Skill": "Design"},
        {"Project Name": "Process Improvement Report", "Revenue ($)": 110, "Hours": 8,  "Skill": "Consulting"},
    ])

    edited_df = st.data_editor(
        default_data,
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Project Name": st.column_config.TextColumn("Project Name", width="large"),
            "Revenue ($)":  st.column_config.NumberColumn("Revenue ($)", min_value=0, format="$%d"),
            "Hours":        st.column_config.NumberColumn("Hours Required", min_value=1),
            "Skill":        st.column_config.SelectboxColumn("Skill Type", options=["CAD","Simulation","Design","Consulting"]),
        },
        hide_index=True,
    )

    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    n = len(edited_df)
    total_rev_all = int(edited_df["Revenue ($)"].sum())
    total_hrs_all = int(edited_df["Hours"].sum())
    avg_rate = round((edited_df["Revenue ($)"] / edited_df["Hours"]).mean(), 1)

    for col, label, val, sub in [
        (c1, "TOTAL PROJECTS",    str(n),              "in your list"),
        (c2, "TOTAL HOURS",       f"{total_hrs_all}",  "if all accepted"),
        (c3, "MAX POSSIBLE ($)",  f"${total_rev_all}", "if all accepted"),
        (c4, "AVG RATE",          f"${avg_rate}/hr",   "across all projects"),
    ]:
        with col:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{val}</div>
                <div class="kpi-sub">{sub}</div>
            </div>""", unsafe_allow_html=True)

# TAB 2, RESULTS
with tab2:
    st.markdown("#### Run Optimization")
    st.caption("Click Solve to find the best combination of projects.")
    solve_btn = st.button("Solve")

    if solve_btn:
        df = edited_df.dropna(subset=["Project Name","Revenue ($)","Hours"]).reset_index(drop=True)
        df = df[df["Project Name"].str.strip() != ""]

        if len(df) == 0:
            st.error("No valid projects found. Please add projects in the Projects tab.")
        else:
            try:
                names    = list(df["Project Name"])
                revenues = dict(zip(df["Project Name"], df["Revenue ($)"].astype(float)))
                hours    = dict(zip(df["Project Name"], df["Hours"].astype(float)))

                # Build the 0-1 Integer Program with PuLP
                prob = pulp.LpProblem("FreelanceOptimizer", pulp.LpMaximize)
                x = {j: pulp.LpVariable(f"x_{i}", cat="Binary") for i, j in enumerate(names)}

                # Objective: maximize total revenue
                prob += pulp.lpSum(revenues[j] * x[j] for j in names), "TotalRevenue"

                # Constraints
                prob += pulp.lpSum(hours[j]    * x[j] for j in names) <= float(total_hours),  "TimeLimit"
                prob += pulp.lpSum(revenues[j] * x[j] for j in names) >= float(min_revenue),  "MinRevenue"
                prob += pulp.lpSum(x[j]                for j in names) <= float(max_projects), "ProjectCap"

                # Solve with CBC (bundled with PuLP, no external solver needed)
                prob.solve(pulp.PULP_CBC_CMD(msg=0))
                status = pulp.LpStatus[prob.status]

                if status != "Optimal":
                    st.error(f"No feasible solution. Try lowering minimum earnings or increasing available hours. (Status: {status})")
                else:
                    result  = {j: x[j].value() for j in names}
                    obj_val = pulp.value(prob.objective)

                    selected     = [j for j in names if result[j] > 0.5]
                    not_selected = [j for j in names if result[j] <= 0.5]
                    hrs_used     = sum(hours[j] for j in selected)
                    hrs_left     = total_hours - hrs_used
                    eff_rate     = round(obj_val / hrs_used, 1) if hrs_used > 0 else 0

                    # KPIs
                    st.markdown('<hr class="divider">', unsafe_allow_html=True)
                    k1, k2, k3, k4 = st.columns(4)
                    for col, label, val, sub in [
                        (k1, "OPTIMAL REVENUE",   f"${int(obj_val)}",    "maximized"),
                        (k2, "PROJECTS ACCEPTED", str(len(selected)),    f"of {len(names)} total"),
                        (k3, "HOURS USED",        f"{int(hrs_used)}",    f"of {total_hours} available"),
                        (k4, "EFFECTIVE RATE",    f"${eff_rate}/hr",     "optimized $/hr"),
                    ]:
                        with col:
                            st.markdown(f"""
                            <div class="kpi-card">
                                <div class="kpi-label">{label}</div>
                                <div class="kpi-value">{val}</div>
                                <div class="kpi-sub">{sub}</div>
                            </div>""", unsafe_allow_html=True)

                    st.markdown('<hr class="divider">', unsafe_allow_html=True)

                    # Project decisions side by side
                    r1, r2 = st.columns(2)
                    with r1:
                        st.markdown("**Accepted Projects**")
                        for j in selected:
                            rate = round(revenues[j]/hours[j],1)
                            skill = df[df["Project Name"]==j]["Skill"].values[0]
                            st.markdown(f"""
                            <div class="accept-row">
                                <div class="row-title">
                                    <span class="badge badge-green">Accept</span>
                                    <span class="badge badge-blue">{skill}</span>
                                    {j}
                                </div>
                                <div class="row-meta">${int(revenues[j])} revenue &nbsp;|&nbsp; {int(hours[j])} hrs &nbsp;|&nbsp; ${rate}/hr</div>
                            </div>""", unsafe_allow_html=True)

                    with r2:
                        st.markdown("**Skipped Projects**")
                        for j in not_selected:
                            rate = round(revenues[j]/hours[j],1)
                            skill = df[df["Project Name"]==j]["Skill"].values[0]
                            st.markdown(f"""
                            <div class="reject-row">
                                <div class="row-title">
                                    <span class="badge badge-red">Skip</span>
                                    <span class="badge badge-blue">{skill}</span>
                                    {j}
                                </div>
                                <div class="row-meta">${int(revenues[j])} revenue &nbsp;|&nbsp; {int(hours[j])} hrs &nbsp;|&nbsp; ${rate}/hr</div>
                            </div>""", unsafe_allow_html=True)

                    st.markdown('<hr class="divider">', unsafe_allow_html=True)
                    st.markdown("**Visual Summary**")

                    ch1, ch2 = st.columns(2)

                    with ch1:
                        bar_df = pd.DataFrame({
                            "Project": selected,
                            "Revenue": [int(revenues[j]) for j in selected]
                        }).sort_values("Revenue", ascending=True)
                        fig1 = px.bar(bar_df, x="Revenue", y="Project", orientation="h",
                                      color="Revenue",
                                      color_continuous_scale=["#93C5FD","#1C1C2E"],
                                      title="Revenue per Accepted Project",
                                      text="Revenue")
                        fig1.update_traces(texttemplate="$%{text}", textposition="outside")
                        fig1.update_layout(
                            plot_bgcolor="white", paper_bgcolor="white",
                            coloraxis_showscale=False,
                            title_font=dict(size=13, color="#1C1C2E"),
                            margin=dict(l=10,r=30,t=40,b=10),
                            xaxis=dict(showgrid=True, gridcolor="#F3F4F6"),
                            yaxis=dict(showgrid=False),
                            font=dict(color="#1C1C2E")
                        )
                        st.plotly_chart(fig1, use_container_width=True)

                    with ch2:
                        pie_df = pd.DataFrame({
                            "Status": ["Hours Used", "Hours Free"],
                            "Hours":  [hrs_used, max(hrs_left,0)]
                        })
                        fig2 = px.pie(pie_df, names="Status", values="Hours",
                                      title="Hours Utilization",
                                      color="Status",
                                      color_discrete_map={"Hours Used":"#1C1C2E","Hours Free":"#E5E7EB"},
                                      hole=0.45)
                        fig2.update_layout(
                            plot_bgcolor="white", paper_bgcolor="white",
                            title_font=dict(size=13, color="#1C1C2E"),
                            margin=dict(l=10,r=10,t=40,b=10),
                            legend=dict(orientation="h", y=-0.1),
                            font=dict(color="#1C1C2E")
                        )
                        st.plotly_chart(fig2, use_container_width=True)

                    # Full solution table
                    st.markdown("**Full Solution Table**")
                    summary = df.copy()
                    summary["Decision"] = summary["Project Name"].apply(
                        lambda x: "Accept" if x in selected else "Skip"
                    )
                    summary["Rate ($/hr)"] = (summary["Revenue ($)"] / summary["Hours"]).round(1)
                    summary = summary[["Project Name","Skill","Revenue ($)","Hours","Rate ($/hr)","Decision"]]
                    st.dataframe(summary, use_container_width=True, hide_index=True)

            except Exception as e:
                st.error(f"Solver error: {e}")

    else:
        st.info("Configure your settings in the sidebar, enter projects in the Projects tab, then click Solve.")

# TAB 3, MODEL
with tab3:
    st.markdown("#### Mathematical Formulation")
    st.markdown(r"""
**Decision Variables**

Let J = set of all available projects.

$$x_j \in \{0,1\} \quad \forall j \in J$$

$x_j = 1$ means project $j$ is accepted. $x_j = 0$ means rejected.

---

**Objective Function, Maximize Total Revenue**

$$\text{Maximize} \quad Z = \sum_{j \in J} \text{rev}_j \cdot x_j$$

---

**Constraints**

Time Budget:
$$\sum_{j \in J} \text{hrs}_j \cdot x_j \leq H$$

Minimum Earnings:
$$\sum_{j \in J} \text{rev}_j \cdot x_j \geq R$$

Project Cap:
$$\sum_{j \in J} x_j \leq N_{max}$$

Binary Domain:
$$x_j \in \{0,1\} \quad \forall j \in J$$

---

**Model Type:** 0-1 Integer Program (IP). Projects cannot be partially accepted, fractional values have no real-world meaning. This makes IP the correct model, not LP.

**Solver:** CBC via PuLP

| Symbol | Meaning |
|--------|---------|
| $\text{rev}_j$ | Revenue from project $j$ |
| $\text{hrs}_j$ | Hours required for project $j$ |
| $H$ | Weekly hour capacity |
| $R$ | Minimum revenue target |
| $N_{max}$ | Maximum projects to accept |
    """)
