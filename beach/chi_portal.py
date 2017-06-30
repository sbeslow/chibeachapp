import pandas as pd


def get_beach_days_2017():
    predictions = get_predictions_from_portal()
    lab_results = get_lab_results_from_portal()
    beach_days = lab_results.merge(predictions, how='left', on=['beach_name', 'date'])
    return beach_days


def get_predictions_from_portal():
    query = ('https://data.cityofchicago.org/resource/ct72-a55e.json?$limit=50000')
    predictions = pd.read_json(query)
    cols_to_delete = [_ for _ in predictions.columns if _.startswith(':@')]
    predictions = predictions.drop(cols_to_delete, axis=1)
    predictions = predictions.drop(['recordid', 'prediction_source', 'latitude', 'longitude', 'location'], axis=1)
    predictions['date'] = predictions['date'].dt.date
    return predictions


def get_lab_results_from_portal():
    query = "https://data.cityofchicago.org/resource/awhh-mb2r.json?" + \
            "$where=dna_sample_timestamp%20%3E%20%222017-01-01T00:00:00%22&" + \
            "$order=dna_sample_timestamp%20desc&$limit=50000"
    lab_results = pd.read_json(query)

    lab_results = lab_results[['beach', 'dna_reading_mean', 'dna_sample_timestamp', 'dna_test_id', 'location']]
    lab_results['dna_sample_timestamp'] = pd.to_datetime(lab_results['dna_sample_timestamp'])
    lab_results['date'] = lab_results['dna_sample_timestamp'].dt.date
    lab_results['beach_name'] = lab_results['beach']
    del lab_results['beach']
    return lab_results
