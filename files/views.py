import os.path

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.core import serializers
from .forms import FileForm
from .models import File
from django import http
import json
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


def upload(request):
    if request.method == 'POST':
        file = request.FILES['document'] if 'document' in request.FILES else None
        if file:
            fss = FileSystemStorage()
            fss.save(file.name, file)
        return JsonResponse(data={"message": 1})
    return JsonResponse(data={"message": 0})


def file_download(request, name):
    file = File.objects.get(name=name)
    if file:
        d_file = file.file
        response = http.HttpResponse(json.dumps(file.file).encode("utf-8"),
                                     content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=%s' % d_file
        return response


def file_js(request):
    files = File.objects.all()
    data = []
    for file in files:
        record = {"name": file.name, "size": file.file.size // 2 ** 20}
        data.append(record)

    return JsonResponse(data={"data": data})


def file_list(request):
    files = File.objects.all()

    return JsonResponse(data={"data": [str(f) for f in files]})


@csrf_exempt
def file_upload(request):
    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)
        form = FileForm(request.POST, request.FILES)
        print(form.is_valid())
        if form.is_valid():
            form.save()
            return redirect('list')
    else:
        form = FileForm()
    return JsonResponse({"massage": "Work"})


def file_delete(request, pk):
    if request.method == 'POST':
        file = File.objects.get(pk=pk)
        file.delete()
        return JsonResponse(data={"massage": "Work"})

    return JsonResponse(data={"massage": "Nope"})
