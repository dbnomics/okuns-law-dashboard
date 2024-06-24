# chart_creator.py
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def create_okun_curve(df, country):
    df['unemployment_rate'] = pd.to_numeric(df['unemployment_rate'], errors='coerce')
    df['gdp_growth_rate'] = pd.to_numeric(df['gdp_growth_rate'], errors='coerce')

    df = df.dropna(subset=['unemployment_rate', 'gdp_growth_rate'])

    z = np.polyfit(df['unemployment_rate'], df['gdp_growth_rate'], 1)
    p = np.poly1d(z)

    x = np.linspace(df['unemployment_rate'].min(), df['unemployment_rate'].max(), 100)
    trendline = p(x)

    trend_df = pd.DataFrame({'unemployment_rate': x, 'gdp_growth_rate': trendline})

    fig = px.scatter(df, x='unemployment_rate', y='gdp_growth_rate', title=f'Okun law for {country}',
                     labels={'unemployment_rate': 'Unemployment Rate (%)', 'gdp_growth_rate': 'GDP Growth Rate (%)'},
                     hover_data={'period': True})

    fig.add_trace(go.Scatter(x=trend_df['unemployment_rate'], y=trend_df['gdp_growth_rate'], mode='lines', name='Trend',
                             line=dict(color='deeppink')))

    equation_text = f'Trendline equation: y = {z[0]:.2f}x + {z[1]:.2f}'
    fig.add_annotation(x=0.5, y=1.1, xref="paper", yref="paper",
                       text=equation_text,
                       showarrow=False,
                       font=dict(size=12, color="deeppink"),
                       align="center",
                       bordercolor="white",
                       borderwidth=2,
                       borderpad=4,
                       bgcolor="white",
                       opacity=0.8)

    return fig

if __name__ == "__main__":
    from data_loader import load_data
    data = load_data()
    for country, df in data.items():
        fig = create_okun_curve(df, country)
        fig.show()
