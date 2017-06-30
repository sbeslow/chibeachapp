from django.shortcuts import render
from beach.chi_portal import get_beach_days_2017
from beach.beach_days import find_failed_tests, get_scatter_points


def index(request):
    beach_days = get_beach_days_2017()
    ret_val = {}
    ret_val['failed_tests'] = find_failed_tests(beach_days)
    return render(request, 'index.html', ret_val)


def show_beach(request, beach_name):
    beach_days = get_beach_days_2017()
    this_beach = beach_days.loc[beach_days['beach_name'] == beach_name]
    ret_val = {}
    ret_val['scatter_points'] = get_scatter_points(this_beach)
    return render(request, 'show_beach.html', ret_val)
