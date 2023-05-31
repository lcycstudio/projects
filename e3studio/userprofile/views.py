from django.shortcuts import render
# from django.http import HttpResponse
# import datetime
# from .forms import NameForm


# def get_name(request):
#     if request.method == 'POST':
#         # create a form instance and populate it with data from the request:
#         form = NameForm(request.POST)
#         # check whether it's valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required
#             # ...
#             # redirect to a new URL:
#             print(form.cleaned_data.get('your_name'))
#             return render(request, 'name.html', {'thanks': 'thanks'})

#     # if a GET (or any other method) we'll create a blank form
#     else:
#         form = NameForm()
#     return render(request, 'name.html', {'form': form, 'thanks': ""})
