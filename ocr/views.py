import os

#import pytesseract as pytesseract
from django.contrib.auth import authenticate, login
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.http import HttpResponse
from django.shortcuts import render, redirect
from pymongo import MongoClient
from pdf2image import convert_from_path, convert_from_bytes


# Create your views here.
from ocr.forms import FormUploadPDF, SearchForm, LoginForm
from ocrDjango.settings import BASE_DIR

from textExtract.extractor import extractor
from textExtract.schema1 import schema2, schema1, schema3, schema4, schema5, juridiqueSch

from bson.objectid import ObjectId

def connexion(request):
    context = {}
    if request.method == 'POST':
        print(0)
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        print(form.errors)
        if form.is_valid():
            print(1)
            user = authenticate(request, username=username, password=password)
            if user:
                print(2)
                login(request, user=user)
                # permettre plutot une redirectin vers next=
                return redirect('ocr:acceuil')
            else:
                context['errors'] = True
                context['form'] = form
        else:
            context['errors'] = True
            context['form'] = form
    else:
        context['form'] = LoginForm()
    return render(request, 'login.html', context)

def inscription(request):
    context = {'register':True}
    if request.method == 'POST':
        print(0)
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        print(form.errors)
        if form.is_valid():
            print(1)
            user = authenticate(request, username=username, password=password)
            if user:
                print(2)
                login(request, user=user)
                # permettre plutot une redirectin vers next=
                return redirect('ocr:acceuil')
            else:
                context['errors'] = True
                context['form'] = form
        else:
            context['errors'] = True
            context['form'] = form
    else:
        context['form'] = LoginForm()
    return render(request, 'login.html', context)

def read(request,data):
    client = MongoClient()
    print(type(data))
    print(2)

    document = client.ocr_db.documents.find_one({'_id': ObjectId(data)})
    print(document['doc'])
    if document['doc'] == 'doc':
        return render(request, 'index.html', context={'data':document['data']})
    elif document['doc'] == '' or document['doc'] == 'loi':
        return render(request, 'indexJuridique.html', context={'data':document['data']})


def index(request):
    client = MongoClient()

    db = client.ocr_db
    collection = db.documents

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            searchTerm = form.cleaned_data['searchTerm']

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
    print(context['data'])
    return render(request, 'acceuil.html',context=context)

def upload3(request):
    texts = []
    if request.method == 'POST':
        form = FormUploadPDF(request.POST, request.FILES)
        if form.is_valid():

            file_obj = request.FILES.get('name', None)
            debut = request.POST["debut"]
            fin = request.POST["fin"]
            pdf = form.save()
            filename_with_extension = os.path.basename(pdf.name.path)
            extension = os.path.splitext(filename_with_extension)[1]
            filename = os.path.splitext(filename_with_extension)[0]

            text_file = os.path.join(BASE_DIR,'media','text',filename+'.txt')
            fp = open(text_file,'a+')

            extractor(pdf.name.path,fp,int(debut),int(fin))
            fp.close()
            if extension.lower() == ".pdf":
                data = schema5(text_file)
            else:
                data = schema5(text_file)
            # print(pdf.name.path)

            #images = convert_from_path(pdf.name.path,dpi=200)
            #images = convert_from_path(file_obj.,poppler_path=r"D:\Documents\ZEP\Projet\poppler-20.12.1\Library\bin")
            # for idx,image in enumerate(images):
            #     image.save('image' + str(idx) + '.jpg', 'JPEG')
            #     text = transcript(image)
            #     texts.append(text)
            # for i in range(len(images)):
            #      print("Page N°" + str(i + 1) + "\n")
            #      text = pytesseract.image_to_string(images[i])
            #      texts.append(text)
            #     #print()

            document = {}
            document['livre'] = filename
            document['doc'] = 'doc'
            document['data'] = data
            from pymongo import MongoClient
            client = MongoClient()

            db = client.new_your
            collection = db.restaurants
            rs =collection.insert_one(document).inserted_id

            context = {
                'data': collection.find_one(
                    {'_id': rs},
                    {'data': 1, '_id': 0}
                )
            }

            return render(request,'index.html',context=context['data'])

    form = FormUploadPDF()
    return render(request, 'upload2.html', {'form': form})

# 12 / 04 / 2021
def upload(request):
    doc = ''
    if request.method == 'POST':
        form = FormUploadPDF(request.POST, request.FILES)
        if form.is_valid():

            debut = request.POST["debut"]
            fin = request.POST["fin"]
            loi = (request.POST["loi"] or False)

            pdf = form.save()

            print(pdf.name)

            # filename_with_extension = os.path.basename(pdf.name.path)
            # extension = os.path.splitext(filename_with_extension)[1]
            # filename = os.path.splitext(filename_with_extension)[0]

            
            # data = {
            #     "path":pdf.name.path,
            #     "debut":debut,
            #     "fin":fin,
            #     "loi":loi
            # }
            # text_file = os.path.join(BASE_DIR,'media','text',filename+'.txt')
            # fp = open(text_file,'a+')

            # extractor(pdf.name.path,fp,int(debut),int(fin))
            # fp.close()
            # if extension.lower() == ".pdf":
            #     if loi == str(2):
            #         template = 'indexJuridique.html'
            #         data = juridiqueSch(text_file)
            #     else:
            #         template = 'index.html'
            #         data = schema5(text_file)

            # else:
            #     if loi == str(2):
            #         doc = "loi"
            #         template = 'indexJuridique.html'
            #         data = juridiqueSch(text_file)
            #     else:
            #         doc = "doc"
            #         template = 'index.html'
            #         data = schema5(text_file)

            # document = {}
            # document['livre'] = filename
            # document['doc'] = doc
            # document['data'] = data

            # client = MongoClient()

            # db = client.ocr_db
            # collection = db.documents
            # rs =collection.insert_one(document).inserted_id

            # context = {

            #     'data': collection.find_one(
            #         {'_id': rs},
            #         {'data': 1, '_id': 0}
            #     )
            # }

            return redirect("extract", lien = pdf.name, debut = debut, fin = fin, loi = loi)

    form = FormUploadPDF()
    return render(request, 'upload2.html', {'form': form})

def upload2(pdf):
    import PyPDF2
    texts =[]
    pdfFileObj = open(pdf,'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    print(pdfReader.numPages)

    pageObj = pdfReader.getPage(0)
    texts.append(pageObj.extractText())



    pdfFileObj.close()

    return texts

def extractTextDoc(request, lien, debut, fin,loi):

    filename_with_extension = os.path.basename(lien.path)
    extension = os.path.splitext(filename_with_extension)[1]
    filename = os.path.splitext(filename_with_extension)[0]

    text_file = os.path.join(BASE_DIR,'media','text',filename+'.txt')
    fp = open(text_file,'a+')

    extractor(lien.path,fp,int(debut),int(fin))
    fp.close()
    if extension.lower() == ".pdf":
        if loi == str(2):
            doc = "loi"
            #template = 'indexJuridique.html'
            data = juridiqueSch(text_file)
        else:
            doc = "doc"
            #template = 'index.html'
            data = schema5(text_file)

    else:
        if loi == str(2):
            doc = "loi"
           # template = 'indexJuridique.html'
            data = juridiqueSch(text_file)
        else:
            doc = "doc"
            #template = 'index.html'
            data = schema5(text_file)

    document = {}
    document['livre'] = filename
    document['doc'] = doc
    document['data'] = data

    client = MongoClient()

    db = client.ocr_db
    collection = db.documents
    rs =collection.insert_one(document).inserted_id

    return redirect('read', data=rs)