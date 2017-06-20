from django.shortcuts import render
import pandas as pd
from chibeachapp.settings import BASE_DIR
import pdb
import os


from django.http import HttpResponse


def index(request):
    lab_results = pd.read_csv(os.path.join(BASE_DIR, 'data', 'lab_results_cleaned_20170606.csv'))
    beach_names = lab_results['beach_name'].unique()
    return render(request, 'index.html', {'beach_names': beach_names})


def show_beach(request, beach_name):

    lab_results = pd.read_csv(os.path.join(BASE_DIR, 'data', 'lab_results_cleaned_20170606.csv'))
    lab_results = lab_results.loc[lab_results['beach_name'] == beach_name]
    if len(lab_results) == 0:
        return HttpResponse("Beach not found")

    lab_results['dna_sample_timestamp'] = pd.to_datetime(lab_results['dna_sample_timestamp'])
    # lab_results['culture_sample_1_timestamp'] = pd.to_datetime(lab_results['culture_sample_1_timestamp'])

    most_recent_sample = lab_results.sort_values(['dna_sample_timestamp'], ascending=False).iloc[0]

    ret_val = {'beach_name': beach_name, 'most_recent_sample': {'date': most_recent_sample['date'],
               'reading': most_recent_sample['dna_reading_mean']}}

    lab_results['date'] = lab_results['date'].apply(lambda x: pd.to_datetime(x).date().strftime('%b %d, %Y'))
    lab_results['year'] = lab_results['year'].astype(str)

    accept_levels = ['acceptable', 'above_235', 'above_1000']

    sample_levels = {level: {year: 0 for year in lab_results['year'].unique() for level in accept_levels}
                     for level in ['above_1000', 'above_235', 'acceptable']}

    for lab_result in lab_results.to_dict('records'):
        for sample_type in ['dna_reading_mean', 'culture_reading_mean']:
            if str(lab_result[sample_type]) != 'nan':
                if lab_result[sample_type] >= 1000:
                    sample_levels['above_1000'][lab_result['year']] += 1
                elif lab_result[sample_type] >= 235:
                    sample_levels['above_235'][lab_result['year']] += 1
                else:
                    sample_levels['acceptable'][lab_result['year']] += 1

    years = sorted(lab_results['year'].unique())

    ret_val['samples_by_year'] = {'years': years,
                                  'series': [{'name': level.replace('_', ' ').title(),
                                              'data': [sample_levels[level][year] for year in years]}
                                             for level in accept_levels]}
    results_by_date = {year: {'dna': [], 'culture': []} for year in years}
    lab_results = lab_results.set_index('date').to_dict('index')
    for date in sorted(lab_results.keys()):
        lab_result = lab_results[date]
        if str(lab_result['dna_reading_mean']) != 'nan':
            results_by_date[lab_result['year']]['dna'].append([date, lab_result['dna_reading_mean']])
        if str(lab_result['culture_reading_mean']) != 'nan':
            results_by_date[lab_result['year']]['culture'].append([date, lab_result['culture_reading_mean']])
    ret_val['results_by_date'] = results_by_date

    return render(request, 'show_beach.html', ret_val)
