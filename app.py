import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Load the dataset
rating_df = pd.read_csv("data/rating.csv")
kpis_df = pd.read_csv("data/kpis.csv")
last_day_stats_df = pd.read_csv("data/last_day_stats.csv")

st.set_page_config(layout="wide")

st.title("📘 Tvoj napredak u učenju engleskog")

with st.container():
    st.subheader("📈 Osnovne metrike i statistike")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Rejting", f"{rating_df['rating'].iloc[-1]}", "📈")
    col2.metric("Rešeni zadaci", f"{kpis_df['tasks_solved'].sum()}", "📊")
    col3.metric("Tačnost", f"{kpis_df['accuracy'].mean():.2%}", "✅")
    col4.metric(
        "Reseni zadaci iz gramatike",
        f"{kpis_df[kpis_df['label_1'] == 'grammar']['tasks_solved'].sum()}",
        "📚",
    )
    col5.metric(
        "Receni zadaci iz vobaculara",
        f"{kpis_df[kpis_df['label_1'] == 'vocab']['tasks_solved'].sum()}",
        "📚",
    )
    col6, col7, col8, col9, col10 = st.columns(5)
    col6.metric("Neki drugi KPI 1", "vrednost1", "⬆️")
    col7.metric("Neki drugi KPI 2", "vrednost2", "⬇️")
    col8.metric("Neki drugi KPI 3", "vrednost3", "⚡")
    col9.metric("Neki drugi KPI 4", "vrednost4", "🔥")
    col10.metric("Neki drugi KPI 5", "vrednost5", "✨")

with st.container():
    st.subheader("📅 Tvoj napredak u poslednjih 30 dana")
    fig1 = px.line(
        rating_df,
        x="date",
        y="rating",
        markers=True,
        title="Rejting po danima",
        labels={"date": "Datum", "rating": "Rejting"},
    )

    st.plotly_chart(fig1, use_container_width=True)

with st.container():
    st.subheader("📅 Tvoj napredak u danasnjem danu")

    col1, col2 = st.columns(2)

    df = last_day_stats_df.iloc[-10:].reset_index(drop=True)

    # Grafik rejtinga
    fig2 = go.Figure()

    for i in range(1, len(df)):
        color = "green" if df["rating"][i] >= df["rating"][i - 1] else "red"

        fig2.add_trace(
            go.Scatter(
                x=[df["date"][i - 1], df["date"][i]],
                y=[df["rating"][i - 1], df["rating"][i]],
                mode="lines+markers",
                line=dict(color=color, width=4, shape="spline", smoothing=1.3),
                marker=dict(
                    symbol="circle",
                    size=10,
                    color=color,
                    line=dict(width=1, color="white"),
                ),
                hoverinfo="x+y",
                showlegend=False,
            )
        )

    fig2.update_layout(
        title="📈 Rejting po danima (zadnjih 10)",
        xaxis_title="Datum",
        yaxis_title="Rejting",
        margin=dict(t=40, b=20, l=40, r=20),
        height=400,
        plot_bgcolor="#f9f9f9",
        paper_bgcolor="#f9f9f9",
    )

    with col1:
        st.plotly_chart(fig2, use_container_width=True, key="rejting_zadnjih_10")

    # Grafik rezultata (0/1)
    results = df["tasks_solved"].tolist()  # zameni 'result' sa stvarnim imenom kolone
    colors = ["green" if r == 1 else "red" for r in results]

    fig3 = go.Figure()

    icons = ["✅" if r == 1 else "❌" for r in df["tasks_solved"]]

    fig3.add_trace(
        go.Scatter(
            x=list(range(1, len(df) + 1)),
            y=[1] * len(df),
            mode="text",  # samo tekst, nema markera
            text=icons,
            textfont=dict(size=30),  # veličina ikonica
            hovertext=["Tačno" if r == 1 else "Netačno" for r in df["tasks_solved"]],
            hoverinfo="text",
            showlegend=False,
        )
    )

    fig3.update_layout(
        title="✅ Rezultati poslednjih 10 pokušaja",
        xaxis=dict(showgrid=False, zeroline=False, tickvals=list(range(1, 11))),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=120,
        margin=dict(t=40, b=20, l=40, r=20),
        plot_bgcolor="#f9f9f9",
        paper_bgcolor="#f9f9f9",
    )

    with col2:
        st.plotly_chart(fig3, use_container_width=True, key="rezultati_zadnjih_10")


with st.container():
    fig4 = px.bar(
        kpis_df.iloc[-20:],
        x="date",
        y="accuracy",
        color="label_1",
        barmode="group",
        labels={"result": "Rezultat", "count": "Broj pokušaja", "date": "Datum"},
        title="Broj tačnih i netačnih pokušaja po datumu (poslednjih 10 dana)",
    )
    st.plotly_chart(fig4, use_container_width=True)

agg_label_1 = kpis_df.groupby("label_1", as_index=False)[
    ["tasks_solved", "correct_answers"]
].sum()
agg_label_1["accuracy"] = agg_label_1["correct_answers"] / agg_label_1["tasks_solved"]


daily_streak = kpis_df.groupby("date", as_index=False).agg(
    tasks_done=("tasks_solved", "sum")
)

# Definiši boje: zeleno ako je tasks_done > 0, crveno ako nije
colors = ["green" if x > 0 else "red" for x in daily_streak["tasks_done"]]

fig5 = go.Figure()

fig5.add_trace(
    go.Bar(
        x=daily_streak["date"],
        y=[1] * len(daily_streak),  # fiksirana visina
        marker_color=colors,
        hovertext=[f"Tasks done: {x}" for x in daily_streak["tasks_done"]],
        hoverinfo="x+text",
        showlegend=False,
    )
)

fig5.update_layout(
    title="Daily Streak - Zelena ako je resio bar jedan task, crvena ako nije",
    yaxis=dict(showticklabels=False, range=[0, 1.5]),
    xaxis_title="Datum",
    plot_bgcolor="#f9f9f9",
    height=200,
    margin=dict(t=40, b=20, l=40, r=20),
)

st.plotly_chart(fig5, use_container_width=True, key="daily_streak")


fig = go.Figure()

colors = ["green" if x > 0 else "red" for x in daily_streak["tasks_done"]]
symbols = ["star" if x > 0 else "x" for x in daily_streak["tasks_done"]]

fig.add_trace(
    go.Scatter(
        x=daily_streak["date"],
        y=[1] * len(daily_streak),
        mode="markers+text",
        marker=dict(color=colors, size=20, symbol=symbols),
        text=["✅" if x > 0 else "❌" for x in daily_streak["tasks_done"]],
        textposition="middle center",
        hovertext=[f"Tasks done: {x}" for x in daily_streak["tasks_done"]],
        hoverinfo="text",
        showlegend=False,
    )
)

fig.update_layout(
    yaxis=dict(showticklabels=False, range=[0, 2]),
    xaxis_title="Datum",
    height=150,
    margin=dict(t=40, b=20, l=40, r=20),
    plot_bgcolor="#f9f9f9",
)

st.plotly_chart(fig, use_container_width=True)
