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


def get_scatter_plot_old(this_beach):
    this_beach['dna_reading_mean'] = this_beach['dna_reading_mean']\
        .apply(lambda x: float("%.2f" % x))
    this_beach = this_beach.set_index('date')
    date_iter = this_beach.index.min()
    today = datetime.now().date()
    this_beach = this_beach.to_dict('index')
    scatter_points = []
    x_ticks = 0
    while date_iter <= today:
        dna_reading = this_beach[date_iter]['dna_reading_mean'] if date_iter in this_beach else None
        predicted_level = this_beach[date_iter]['predicted_level'] if date_iter in this_beach else None
        scatter_points.append({'date': date_iter, 'dna_reading': dna_reading, 'predicted_level': predicted_level})
        x_ticks += 1
        date_iter = date_iter + timedelta(days=1)

    scatter_plot = {'points': scatter_points, 'x_ticks': 5, 'y_ticks': 10}
    return scatter_plot
