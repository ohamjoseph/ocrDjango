import os
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from pymongo import MongoClient

# Create your views here.
from ocr.forms import FormUploadPDF, SearchForm, LoginForm, RegisterForm
from ocrDjango.settings import BASE_DIR

from textExtract.extractor import extractor
from textExtract.schema1 import schema5, juridiqueSch

from bson.objectid import ObjectId

@login_required
def connexion(request):
    context = {'form2':RegisterForm()}
    if request.user.is_authenticated:
        return redirect('acceuil')
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        if form.is_valid():

            user = authenticate(request, username=username, password=password)
            if user:

                login(request, user=user)
                # permettre plutot une redirectin vers next=
                return redirect('acceuil')
            else:
                context['errors'] = True
                context['form'] = form
        else:
            context['errors'] = True
            context['form'] = form
    else:
        context['form'] = LoginForm()
    return render(request, 'login.html', context)

@login_required
def deconnexion(request):
    logout(request)
    return redirect("login")

@login_required
def inscription(request):
    context = {'register':True,
               'form': LoginForm()}

    if request.method == 'POST':
        form2 = RegisterForm(request.POST)
        if form2.is_valid():


            username = form2.cleaned_data.get('username')
            email = form2.cleaned_data.get('email')
            raw_password = form2.cleaned_data.get('password')

            User.objects.create_user(username,email,raw_password)

            user = authenticate(username=username, password=raw_password)
            if user:
                login(request, user=user)
                # permettre plutot une redirectin vers next=
                return redirect('acceuil')
            else:
                context['error'] = True
                context['form2'] = form2
        else:
            context['error'] = True
            context['form2'] = form2
    else:
        context['form2'] = RegisterForm()
    return render(request, 'login.html', context)

@login_required
def read(request, data):
    client = MongoClient()

    document = client.ocr_db.documents.find_one({'_id': ObjectId(data)})

    if document['doc'] == 'doc':
        return render(request, 'index.html', context={'data':document['data'],'id':data})
    elif document['doc'] == '' or document['doc'] == 'loi':
        return render(request, 'indexJuridique.html', context={'data':document['data'], 'id':data})

@login_required
def delete(request, data):
    client = MongoClient()
    document = client.ocr_db.documents.delete_one({'_id': ObjectId(data)})
    if document:
        return redirect('acceuil')
    else:
        return redirect('read',data)

@login_required
def index(request):
    client = MongoClient()

    db = client.ocr_db
    collection = db.documents

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            searchTerm = form.cleaned_data['searchterm']

            data = collection.find({"$text": {"$search": searchTerm}},
                                    { "_id": 0,
                                      "id": "$_id",
                                      "data": 1,
                                      "livre": 1
                                        },
                                   )
                                        #, {"score": {"$meta": "textScore"}}).sort({"score": {"$meta": "textScore"}})

        else:
            data = collection.aggregate([

                {"$project": {
                    "_id": 0,
                    "id": "$_id",
                    "data": 1,
                    "livre": 1

                }},
            ])
    else:
        data = collection.aggregate([

            {"$project": {
                "_id": 0,
                "id": "$_id",
                "data": 1,
                "livre": 1

            }}
        ])
    form = SearchForm()


    context = {
        'data': data,
        'form':form
    }
    return render(request, 'acceuil.html',context=context)

# 12 / 04 / 2021
@login_required
def upload(request):
    doc = ''
    if request.method == 'POST':
        form = FormUploadPDF(request.POST, request.FILES)
        if form.is_valid():

            debut = int(request.POST["debut"]) if request.POST["debut"] else None
            fin = int(request.POST["fin"]) if request.POST["fin"] else None
            loi = (request.POST["loi"] or False)

            pdf = form.save()

            filename_with_extension = os.path.basename(pdf.name.path)
            extension = os.path.splitext(filename_with_extension)[1]
            filename = os.path.splitext(filename_with_extension)[0]

            text_file = os.path.join(BASE_DIR,'media','text',filename+'.txt')
            fp = open(text_file,'a+')

            extractor(pdf.name.path,fp,debut,fin)
            fp.close()
            if extension.lower() == ".pdf":
                if loi == str(2):
                    template = 'indexJuridique.html'
                    data = juridiqueSch(text_file)
                else:
                    template = 'index.html'
                    data = schema5(text_file)

            else:
                if loi == str(2):
                    doc = "loi"
                    data = juridiqueSch(text_file)
                else:
                    doc = "doc"
                    data = schema5(text_file)

            document = {}
            document['livre'] = filename
            document['doc'] = doc
            document['data'] = data

            client = MongoClient()

            db = client.ocr_db
            collection = db.documents
            collection.insert_one(document).inserted_id



            return redirect('acceuil')

    form = FormUploadPDF()
    return render(request, 'upload2.html', {'form': form})
