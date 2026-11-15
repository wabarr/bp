from django.http import HttpResponseRedirect
from bp.models import Reading
from django.core.exceptions import ObjectDoesNotExist
from ipware import get_client_ip
from django.views.generic.edit import CreateView
from django.views.generic import ListView, TemplateView
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_not_required
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
import json
from django.http import HttpResponse
from django import forms
#note we need the method_decorator to use login_not_required decorator with class based views
from django.utils.decorators import method_decorator

class CreateReading(CreateView):
    model = Reading
    fields = ['systolic', 'diastolic', 'timestamp', 'AMPM']
    success_url = '/'
    template_name = 'bp/create_reading.html'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Replace an entire widget
        form.fields["timestamp"].widget = forms.DateInput(attrs={"type": "date"})
        return form

class ListReadings(ListView):
    model = Reading
    context_object_name = 'readings'
    template_name = 'bp/readings_list.html'

class ChartView(TemplateView):
    template_name = 'bp/chart.html'

def json_view(request):
    data = json.dumps(list(Reading.objects.values("diastolic", "systolic", "AMPM", "timestamp")), default=str)
    return HttpResponse(data, content_type="application/json")

#apply directly to the function based login view
@login_not_required
def login_view(request):
  if request.method == "POST":
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
      user = form.get_user()
      login(request, user)
      urlForRedirect = request.GET.get('next')
      return redirect(urlForRedirect)
  else:
    form = AuthenticationForm()

  return render(request, "bp/login.html", {"form": form})