from django.shortcuts import render
from django.http import HttpResponse
 
def index(request):
    return HttpResponse(u"Hello world.")



# def switch_page(request):





