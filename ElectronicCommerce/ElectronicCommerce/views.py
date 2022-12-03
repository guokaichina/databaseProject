from django.shortcuts import render


def test_template(request):
    return render(request, 'admin/app_list.html')
