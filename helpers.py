import pandas as pd

def map_text_values_to_number(df, categories_dict, countries_dict):
    categories_mapped = pd.Series(df['main_category'].map(categories_dict), name='main_category')
    countries_mapped = pd.Series(df['country'].map(countries_dict), name='country')
    df.update(categories_mapped)
    df.update(countries_mapped)

    return df
