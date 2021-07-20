from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect
import os
from gtts import gTTS
import PyPDF2
import docx2txt
from googletrans import Translator

def choosefile(request):
    return render(request, 'choosefile.html')


def showresults(request):

    if request.method != 'POST':
        return redirect('choosefile')

    file      = request.FILES['filename']
    filename  = file.name
    fileSave  = os.path.abspath('.') + '/uploads/' + file.name
    extension = os.path.splitext(filename)[-1]
    nameMP3   = os.path.splitext(filename)[0] + '.mp3'
    language  = request.POST.get('language', 'es')

    traduccion  = request.POST.get('traduccion')
    #tipo =  request.POST.get('tipo')
    
    #if (tipo == "textoavoz"):

    if extension not in ['.pdf', '.txt', '.docx']:
        # error extension invalida... aqui hacer un mensaje de error..
        return redirect('choosefile')
    
    # guardo el archivo
    with open( fileSave , 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    # dependiendo de la extension creo el texto para traducir


    text = '';

    if (extension == ".pdf"):
        f = open(fileSave, "rb")
        read_pdf = PyPDF2.PdfFileReader(f)
        page     = read_pdf.getPage(0)
        text     = page.extractText()
        f.close()
        os.remove(fileSave)

    elif (extension == ".txt"):
        # lo procesamos tal como viene.
        # coding=utf-8
        f = open(fileSave, "r", encoding="utf-8")
        text = f.read().replace("\n", " ")
        f.close()
        os.remove(fileSave)
        

    elif (extension == ".docx"):
        #https://djangocentral.com/convert-a-docx-file-to-text-file/
        text = docx2txt.process(fileSave)
        os.remove(fileSave)

    if(traduccion):
        
        #requiere la traduccion a otro lenguaje
        file      = request.FILES['filename']
        filename  = file.name
        fileSave  = os.path.abspath('.') + '/uploads/' + file.name
        extension = os.path.splitext(filename)[-1]
        nameMP3   = os.path.splitext(filename)[0] + '.mp3'       
        language  = request.POST.get('lenguajedestino', 'en')
        # hacemos la conversion en si     
        #print (language)

        translater = Translator()
        out = translater.translate(text, dest=language)
        text = out.text
        
        
    #generar la traduccion y guardar el archivo mp3:
    fileMP3 = os.path.abspath('.') + '/uploads/' + nameMP3
    voz = gTTS(text=text, lang=language, slow=False)
    voz.save(fileMP3)
    


    f = open(fileMP3, 'rb')
    streamFile = f.read()
    f.close()
    os.remove(fileMP3)

    response = HttpResponse(streamFile, content_type='audio/mp3')
    response['Content-Disposition'] = 'attachment; filename=' + nameMP3
    return response

def showayuda(request):
    return render(request, 'showayuda.html')    
