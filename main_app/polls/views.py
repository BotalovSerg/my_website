from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def index(request):
    return HttpResponse("Hello, my frends. You are at the poll index")


def detail(request, question_id):
    return HttpResponse("You're looking at questions %s." % question_id)

def results(request, question_id):
    response = "You're looking at the result of questions %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting at questions %s." % question_id)