import pandas as pd
from pca_analyzer import PcaAnalyzer
import helpers


def configure():
    # Configure pandas to more columns than by default
    pd.set_option('display.max_columns', 10)
    pd.options.mode.chained_assignment = None  # default='warn'


def read_csv_to_dataframe(path, columns, top_rows, encoding='ISO-8859-1'):
    return pd.read_csv(path, encoding=encoding)\
             .head(top_rows)\
             .filter(columns, axis=1)


def show_stats(successful, failed):
    successful_count = len(successful.index)
    failed_count = len(failed.index)

    min_value_of_successful = successful['pledged_ratio'].min()
    max_value_of_failed = failed['pledged_ratio'].max()

    print(f'\n============ SUCCEEDED ============\n{successful}')
    print(f'\n============ FAILED ============\n{failed}')

    print(f'\n============ SUMMARY ============')
    print(f'Number of successful projects: {successful_count}')
    print(f'Number of failed projects: {failed_count}')

    print(f'Min % pledged (successful): {min_value_of_successful}')
    print(f'Max % pledged (failed): {max_value_of_failed}')


def get_all_values_from_column(df, category_name):
    categories = []
    for i in range(0, len(df[category_name])):
        category = df[category_name][i]
        if category not in categories:
            categories.append(category)

    return categories


def create_label_number_dict(names):
    normalized = {}
    for i in range(0, len(names)):
        name = names[i]
        normalized[name] = i + 1

    return normalized


def create_normalized_states_dict():
    return {
        'successful': 1,
        'failed': 2
    }


def merge_to_one_df(successful, failed):
    # Group projects by categories
    startups = successful.groupby(df['main_category']) \
        .size() \
        .reset_index(name='succeeded')
    failed_group = failed.groupby(df['main_category']) \
        .size() \
        .reset_index(name='failed')
    startups['failed'] = failed_group['failed']

    return startups


if __name__ == '__main__':
    interesting_columns = ['ID', 'main_category', 'country', 'goal', 'pledged', 'state']
    features_columns = ['main_category', 'country', 'goal', 'pledged', 'pledged_ratio']
    labels_columns = ['state']
    path = 'data/kickstarter-projects-1-filtered.csv'
    configure()

    # Read data
    df = read_csv_to_dataframe(path, interesting_columns, 1000)
    categories = get_all_values_from_column(df, 'main_category')
    countries = get_all_values_from_column(df, 'country')
    categories_dict = create_label_number_dict(categories)
    countries_dict = create_label_number_dict(countries)

    # Create new column pledged_ratio 0-100(%)
    df['pledged_ratio'] = df['pledged'].astype(float) / df['goal'].astype(float) * 100

    # PCA analysis
    features = df[features_columns]
    labels = df[labels_columns]

    # Map categories and countries to number values
    features = helpers.map_text_values_to_number(features, categories_dict, countries_dict)

    pca_analyzer = PcaAnalyzer(df, features, labels)
    pca_analyzer.perform_pca_analysis()










    # # Extract and merge data into one dataframe
    # successful = df[df['state'] == 'successful']
    # failed = df[df['state'] == 'failed']
    # startups = merge_to_one_df(successful, failed)
    #
    # # Calculate succeed to fail ratio
    # startups['succeeded_to_failed_ratio'] = startups['succeeded'].astype(float) / startups['failed'].astype(float)
    #
    # # Print results and summaries
    # show_stats(successful, failed)
    # print(f'{len(categories)} categories found')
    # print(f'{len(countries)} countries found')
    # print(f'\n============ DATA GROUPED BY CATEGORY ============\n{startups}\n')
