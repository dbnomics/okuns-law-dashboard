import importlib.resources

import pandas as pd
import streamlit as st
from chart_creator import create_okun_curve
from data_loader import load_data


def filter_by_date(df, start_date, end_date):
    df["period"] = pd.to_datetime(df["period"])
    return df[(df["period"] >= start_date) & (df["period"] <= end_date)]


def main():
    package_dir = importlib.resources.files("okuns_law")
    st.set_page_config(
        page_title="DBnomics Okun's Law",
        page_icon=str(package_dir / "images/favicon.png"),
    )
    st.image(str(package_dir / "images/dbnomics.svg"), width=300)
    st.title(":blue[Okun's Law]")

    tab1, tab2 = st.tabs(["Explanations", "Charts"])

    with tab1:
        st.header(":blue[Explanations]")
        st.write(
            "\n"
            "Okun's Law was conceived in 1962 by the Keynesian American economist Arthur Okun (1928-1980).\n"
            "He was professor at Yale and advisor to Presidents Kennedy and Johnson.\n"
            "\n"
            "Okun's Law highlights a linear relationship between the economic growth rate and the change in the unemployment rate.\n"
            "Below a certain threshold of GDP growth, the unemployment rate increases.\n "
            "Beyond this same threshold, the unemployment rate decreases.\n"
            "This law thus allows for the prediction of the effects of accelerated economic growth on unemployment.\n"
            "\n"
            "Thanks to the GDP growth coefficient, it is possible to know the necessary growth for stabilizing or even reducing unemployment.\n"
            "Okun asserted that in the United States, for every 3% increase in economic growth beyond the long-term growth of an economy, the unemployment rate would decrease by 1% (and vice versa).\n"
            "This 1% variation in GDP is broken down as follows: \n"
            "- 1/3 in the form of productivity \n"
            "- 2/3 in the form of aggregated hours (employment + hours worked)\n"
            "\n"
            "There is therefore a complex relationship between the labor market and the goods and services market.\n"
            "However, this assertion became false starting from the 1970s with the beginning of the stagflation phenomenon (stagnation of economic activity, high unemployment, and rising inflation).\n"
            "\n"
            "Another major event, the Great Recession of 2007-2009, allowed for testing the validity of Okun's Law. During this period, there was an increase in productivity in the United States, which contradicts Okun's assertions: competition between companies was so strong that they were forced to maintain their productivity.\n"
            "Conversely, in France, Okun's Law is better adhered to: there was a 2% decline in French productivity. \n"
            "\n"
            "Thus, in France, the breakdown defined by Okun seems relatively respected, while it is no longer the case in the United States. This difference is due to the greater rigidity of the French labor market, which practices labor hoarding.\n"
            'Labor hoarding can be defined as "that part of labor input which is not fully utilized by a company during its production process at any given point in time".\n'
            "The management practiced in the United States renders Okun's Law obsolete. Nevertheless, during periods of increased uncertainty, Okun's Law loses its explanatory power concerning the labor market.\n"
            "\n"
        )

    with tab2:
        st.header(":blue[Okun's Law Per Country]")
        countries = ["France", "United States", "Argentina", "Japan", "Spain", "India"]
        selected_countries = st.multiselect(
            "**Select Country**", countries, default=["France"]
        )

        data = load_data()

        if selected_countries:
            all_dates = (
                pd.to_datetime(data[selected_countries[0]]["period"])
                .sort_values()
                .unique()
            )
            start_date, end_date = st.select_slider(
                "**Select Date Range**",
                options=all_dates,
                value=(all_dates[0], all_dates[-1]),
                format_func=lambda x: x.strftime("%Y"),
            )

            for country in selected_countries:
                if country in data:
                    df = data[country]
                    df_filtered = filter_by_date(df, start_date, end_date)
                    fig = create_okun_curve(df_filtered, country)
                    st.plotly_chart(fig)
        st.subheader(":blue[**DBnomics sources**]")
        st.write(
            ":blue[Unemploymant rate]: [*link*](https://db.nomics.world/ILO/UNE_DEAP_SEX_AGE_EDU_RT?tab=list)"
        )
        st.write(
            ":blue[GDP growth rate]: [*link*](https://db.nomics.world/IMF/WEO:2024-04?tab=list)"
        )


if __name__ == "__main__":
    main()
