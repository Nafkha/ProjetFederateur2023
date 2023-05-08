from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from django.http import Http404

from .models import JobOffer
def index(request):
    jobs  = JobOffer.objects.order_by('-Date')[:5]
    template = loader.get_template("joboffers/index.html")
    context = {
        "jobs":jobs
    }
    return render(request,"joboffers/index.html",context)
def joblist(request):
    jobs  = JobOffer.objects.order_by('-Date')
    template = loader.get_template("joboffers/job-list.html")
    context = {
        "jobs":jobs
    }
    return render(request,"joboffers/job-list.html",context)

def detail(request,offer_id):
    print(offer_id)
    try:
        j = JobOffer.objects.get(pk=offer_id)
    except JobOffer.DoesNotExist:
        raise Http404("Job Not Found")
    print(j)
    return render(request, "joboffers/job-detail.html", {"j": j})
