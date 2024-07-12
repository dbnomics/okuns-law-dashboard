import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression


def create_okun_curve(df, country):
    df["unemployment_rate"] = pd.to_numeric(df["unemployment_rate"], errors="coerce")
    df["gdp_growth_rate"] = pd.to_numeric(df["gdp_growth_rate"], errors="coerce")

    df = df.dropna(subset=["unemployment_rate", "gdp_growth_rate"])

    z = np.polyfit(df["gdp_growth_rate"], df["unemployment_rate"], 1)
    p = np.poly1d(z)

    x = np.linspace(df["gdp_growth_rate"].min(), df["gdp_growth_rate"].max(), 100)
    trendline = p(x)

    trend_df = pd.DataFrame({"gdp_growth_rate": x, "unemployment_rate": trendline})

    fig = px.scatter(
        df,
        x="gdp_growth_rate",
        y="unemployment_rate",
        title=f"Okun's Law for {country}",
        labels={
            "gdp_growth_rate": "GDP Growth Rate (%)",
            "unemployment_rate": "Unemployment Rate (%)",
        },
        hover_data={"period": True},
    )
    fig.add_trace(
        go.Scatter(
            x=trend_df["gdp_growth_rate"],
            y=trend_df["unemployment_rate"],
            mode="lines",
            name="Trend",
            line=dict(color="deeppink"),
        )
    )

    equation_text = f"Trendline equation: y = {z[0]:.2f}x + {z[1]:.2f}"
    fig.add_annotation(
        x=0.5,
        y=1.1,
        xref="paper",
        yref="paper",
        text=equation_text,
        showarrow=False,
        font=dict(size=12, color="deeppink"),
        align="center",
        bordercolor="white",
        borderwidth=2,
        borderpad=4,
        bgcolor="white",
        opacity=0.8,
    )

    return fig


def create_example_okun():
    np.random.seed(0)
    years = np.arange(2000, 2024)
    gdp_growth = np.random.normal(2, 1, len(years))
    unemployment_rate_change = -0.5 * gdp_growth + np.random.normal(0, 0.5, len(years))

    data = pd.DataFrame(
        {
            "Year": years,
            "GDP Growth rate (%)": gdp_growth,
            "Unemployment rate change (%)": unemployment_rate_change,
        }
    )

    X = data["GDP Growth rate (%)"].values.reshape(-1, 1)
    y = data["Unemployment rate change (%)"].values

    model = LinearRegression()
    model.fit(X, y)

    predictions = model.predict(X)

    coef = model.coef_[0]
    intercept = model.intercept_

    scatter_trace = go.Scatter(
        x=data["GDP Growth rate (%)"],
        y=data["Unemployment rate change (%)"],
        mode="markers",
        name="Fake Data",
    )

    line_trace = go.Scatter(
        x=data["GDP Growth rate (%)"],
        y=predictions,
        mode="lines",
        name="Linear Regression",
    )

    layout = go.Layout(
        title="Okun's Law in theory",
        xaxis_title="GDP Growth rate (%)",
        yaxis_title="Unemployment rate change (%)",
        showlegend=True,
    )

    fig = go.Figure(data=[scatter_trace, line_trace], layout=layout)

    return fig
