from datetime import datetime, timedelta


def find_failed_tests(beach_days):
    # Get the last five days
    today = datetime.now().date()
    print(datetime.now())
    five_days_ago = today - timedelta(days=7)
    failed_tests = beach_days.loc[(beach_days['date'] >= five_days_ago) &
                                  (beach_days['dna_reading_mean'] >= 1000)]
    failed_tests = failed_tests.sort_values(['date', 'dna_reading_mean'], ascending=False)
    failed_tests['dna_reading_mean'] = failed_tests['dna_reading_mean']\
        .apply(lambda x: "%.2f" % x + ' cfu')
    print(today)
    print(failed_tests['date'])
    failed_tests['is_today'] = failed_tests['date'] == today
    return failed_tests.to_dict('records')
