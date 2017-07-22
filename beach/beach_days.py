from datetime import datetime, timedelta
import pandas as pd


def find_failed_tests(beach_days):
    # Get the last five days
    today = datetime.now().date()
    five_days_ago = today - timedelta(days=7)
    failed_tests = beach_days.loc[(beach_days['date'] >= five_days_ago) &
                                  (beach_days['dna_reading_mean'] >= 1000)]
    failed_tests = failed_tests.sort_values(['date', 'dna_reading_mean'], ascending=False)
    failed_tests['dna_reading_mean'] = failed_tests['dna_reading_mean']\
        .apply(lambda x: "%.2f" % x + ' cfu')
    failed_tests['is_today'] = failed_tests['date'] == today
    return failed_tests.to_dict('records')


def find_total_stats(beach_days):
    samples = beach_days.loc[~beach_days['dna_reading_mean'].isnull()]
    predictions = samples.loc[~samples['predicted_level'].isnull()]

    return {'num_samples': len(samples),
            'failed_samples': len(samples.loc[samples['dna_reading_mean'] >= 1000]),
            'predicted_failed': len(predictions.loc[predictions['predicted_level'] >= 1000])
            }


def per_beach_stats(beach_days):
    samples = beach_days.loc[~beach_days['dna_reading_mean'].isnull()]
    num_samples = samples.groupby('beach_name').count()['dna_test_id']
    # df.columns = ['num_samples']
    num_failed = samples.loc[samples['dna_reading_mean'] >= 1000].groupby('beach_name').count()['dna_test_id']
    df = pd.concat([num_samples, num_failed], axis=1).fillna(0).astype(int)
    df.columns = ['num_samples', 'num_failed']
    df['beach_name'] = df.index.values
    return df.to_dict('records')


def get_scatter_plot(this_beach):
    this_beach['dna_reading_mean'] = this_beach['dna_reading_mean']\
        .apply(lambda x: float("%.2f" % x))

    readings, predictions = [], []
    this_beach = this_beach.set_index('date')
    date_iter = this_beach.index.min()
    today = datetime.now().date()
    this_beach = this_beach.to_dict('index')

    while date_iter <= today:
        if date_iter in this_beach:
            dna_reading = this_beach[date_iter]['dna_reading_mean'] if date_iter in this_beach else None
            readings.append([date_iter.strftime('%B %d, %Y'), dna_reading])

            if str(this_beach[date_iter]['predicted_level']).lower() != 'nan':
                predictions.append([date_iter.strftime('%B %d, %Y'), this_beach[date_iter]['predicted_level']])
        date_iter = date_iter + timedelta(days=1)

    ret_val = {'readings': readings, 'predictions': predictions}
    return ret_val
