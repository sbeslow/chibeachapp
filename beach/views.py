from django.shortcuts import render
from beach.chi_portal import get_beach_days_2017
from beach.beach_days import find_failed_tests, get_scatter_plot


def index(request):
    beach_days = get_beach_days_2017()
    ret_val = {'beaches': list(beach_days['beach_name'].unique())}
    ret_val['failed_tests'] = find_failed_tests(beach_days)
    return render(request, 'index.html', ret_val)


def show_beach(request, beach_name):
    beach_days = get_beach_days_2017()
    this_beach = beach_days.loc[beach_days['beach_name'] == beach_name]
    ret_val = {'beaches': list(beach_days['beach_name'].unique())}
    ret_val['scatter_plot'] = get_scatter_plot(this_beach)
    return render(request, 'show_beach.html', ret_val)
