from django.shortcuts import render
from beach.chi_portal import get_beach_days_2017
from beach.beach_days import find_failed_tests, get_scatter_plot, find_total_stats, per_beach_stats
from datetime import datetime


def index(request):
    beach_days = get_beach_days_2017()
    ret_val = {'beaches': sorted(list(beach_days['beach_name'].unique())),
               'stats': find_total_stats(beach_days)}
    ret_val['failed_tests'] = find_failed_tests(beach_days)
    ret_val['per_beach_stats'] = per_beach_stats(beach_days)

    last_sample_date = beach_days.sort_values("dna_sample_timestamp", ascending=False).head()\
        .iloc[0]['dna_sample_timestamp'].date()
    today = datetime.now().date()
    ret_val['last_sample'] = last_sample_date.strftime('%m/%d/%Y') if last_sample_date != today else None

    return render(request, 'index.html', ret_val)


def show_beach(request, beach_name):
    beach_days = get_beach_days_2017()
    this_beach = beach_days.loc[beach_days['beach_name'] == beach_name]

    ret_val = {'beaches': sorted(list(beach_days['beach_name'].unique()))}

    predictions = this_beach.loc[~this_beach['predicted_level'].isnull()]
    ret_val['beach'] = {'beach_name': beach_name, 'samples_taken': len(this_beach),
                        'failed_samples': len(this_beach.loc[this_beach['dna_reading_mean'] >= 1000]),
                        'is_predicted': len(predictions) > 0,
                        'num_predictions': len(predictions),
                        'num_predictions_failed': len(predictions.loc[predictions['predicted_level'] >= 1000])}
    ret_val['scatter_plot'] = get_scatter_plot(this_beach)
    this_beach = this_beach[['date', 'dna_reading_mean', 'predicted_level']]
    this_beach['date'] = this_beach['date'].apply(lambda x: x.strftime('%m/%d/%Y'))
    ret_val['samples'] = this_beach.fillna(-1).to_dict('records')
    import pdb
    # pdb.set_trace()
    return render(request, 'show_beach.html', ret_val)


def chicago(request):
    ret_val = {}
    return render(request, 'chicago.html', ret_val)
