from django.shortcuts import render
from app1.utils.generate import (
    create_max_receipt,
    gen_daily_all_data,
    get_selected_users)


def testing(request):
    return render(request, 'app1/testing.html', {})


def main(request):
    return render(request, 'app1/main.html', {})


def how_to_use(request):
    return render(request, 'app1/how_to_use.html', {})


def demo(request):
    return render(request, 'app1/demo.html', {})


def benefits(request):
    return render(request,
                  'app1/benefits.html', {})


def our_story(request):
    return render(request,
                  'app1/our_story.html', {})


def gen_max_receipt(request):
    create_max_receipt()
    return render(request, 'app1/gen_max_receipt.html', {})


def daily_all_data(request):
    data = gen_daily_all_data()
    return render(request, 'app1/daily_all_data.html', {'data': data})


def users_joined_in_a_date(request, **kwargs):
    a_date = kwargs['date_joined']
    data = get_selected_users(a_date)
    return render(request, 'app1/selected_users.html', {'data': data})
