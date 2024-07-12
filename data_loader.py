# data_loader.py
import pandas as pd
from dbnomics import fetch_series

def load_data():
    df_unemploy = fetch_series([
        'ILO/UNE_DEAP_SEX_AGE_EDU_RT/USA.BA_453.AGE_YTHADULT_YGE15.EDU_AGGREGATE_TOTAL.SEX_T.A',
        'ILO/UNE_DEAP_SEX_AGE_EDU_RT/FRA.BA_148.AGE_YTHADULT_YGE15.EDU_AGGREGATE_TOTAL.SEX_T.A',
        'ILO/UNE_DEAP_SEX_AGE_EDU_RT/ARG.BA_150.AGE_YTHADULT_YGE15.EDU_AGGREGATE_TOTAL.SEX_T.A',
        'ILO/UNE_DEAP_SEX_AGE_EDU_RT/JPN.BA_259.AGE_YTHADULT_YGE15.EDU_AGGREGATE_TOTAL.SEX_T.A',
        'ILO/UNE_DEAP_SEX_AGE_EDU_RT/ESP.BA_2244.AGE_YTHADULT_YGE15.EDU_AGGREGATE_TOTAL.SEX_T.A',
        'ILO/UNE_DEAP_SEX_AGE_EDU_RT/IND.BA_14121.AGE_YTHADULT_YGE15.EDU_AGGREGATE_TOTAL.SEX_T.A',
    ])

    df_gdp = fetch_series([
        'IMF/WEO:2024-04/USA.NGDP_RPCH.pcent_change',
        'IMF/WEO:2024-04/FRA.NGDP_RPCH.pcent_change',
        'IMF/WEO:2024-04/ARG.NGDP_RPCH.pcent_change',
        'IMF/WEO:2024-04/JPN.NGDP_RPCH.pcent_change',
        'IMF/WEO:2024-04/ESP.NGDP_RPCH.pcent_change',
        'IMF/WEO:2024-04/IND.NGDP_RPCH.pcent_change'
    ])

    col_em = ['original_period', 'original_value', 'Reference area']
    col_gdp = ['original_period', 'original_value', 'WEO Country']

    df_unemploy = df_unemploy.rename(columns={'original_value': 'unemployment_rate'})
    df_gdp = df_gdp.rename(columns={'original_value': 'gdp_growth_rate'})

    def create_country_df(df, country, col, col_name):
        return df[df[col] == country][['original_period', col_name]].rename(
            columns={'original_period': 'period', col_name: col_name})

    countries = ['France', 'United States', 'Argentina', 'Japan', 'Spain', 'India']
    df_dict = {}

    for country in countries:
        df_em = create_country_df(df_unemploy, country, 'Reference area', 'unemployment_rate')
        df_gdp_ctry = create_country_df(df_gdp, country, 'WEO Country', 'gdp_growth_rate')
        df_merged = pd.merge(df_em, df_gdp_ctry, on='period')
        df_dict[country] = df_merged

    return df_dict


if __name__ == "__main__":
    data = load_data()
    for country, df in data.items():
        print(f"{country} Data:")
        print(df.head())
