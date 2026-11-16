from django.http import HttpResponseRedirect
from bp.models import Reading, Annotations
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
from django.contrib.messages.views import SuccessMessageMixin
from django.utils import formats
from django.db import IntegrityError

class CreateReading(SuccessMessageMixin, CreateView):
    model = Reading
    fields = ['systolic', 'diastolic', 'timestamp', 'AMPM']
    success_url = '/'
    template_name = 'bp/create_reading.html'

    def get_success_message(self, cleaned_data):
        date = cleaned_data['timestamp']
        formatted_date = formats.date_format(date, "m/d/Y")
        return f'Added {formatted_date} - {cleaned_data["AMPM"]} - ({cleaned_data["systolic"]})/{cleaned_data["diastolic"]}'

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Replace an entire widget
        form.fields["timestamp"].widget = forms.DateInput(attrs={"type": "date"})
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last10'] = Reading.objects.all().order_by('-timestamp')[:10]
        return context

    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except IntegrityError:
            form.add_error(None, "An entry for this date and time already exists.")
            return self.form_invalid(form)

class ListReadings(ListView):
    model = Reading
    context_object_name = 'readings'
    template_name = 'bp/readings_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['annotations'] = Annotations.objects.all()
        return context

class ChartView(TemplateView):
    template_name = 'bp/chart.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['annotations'] = Annotations.objects.all()
        return context

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