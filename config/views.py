from django.contrib import admin
from django.urls import path 
from django.shortcuts import render
def main(request):
    
    return render(request, "main.html")
