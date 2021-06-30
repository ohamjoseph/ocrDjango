import os
import subprocess
from pdf2image import convert_from_path

##------------------------------------------------------------------------------------
from ocrDjango.settings import BASE_DIR

def eraseFile(repertoire):
    files=os.listdir(repertoire)
    for i in range(0,len(files)):
        os.remove(repertoire+'/'+files[i])

def tesseractProcess(dir, output, idx =-1):
    """
        Extraction de text a partie d'image
        :param dir: le Dossier contenant l'image
        :param idx: le numero de la page du document en commencant la numerotation a zero
        :param output: le chemin du resultat de tesseract
        :return: null
    """
    if idx == -1:
        image = dir
    else:
        image = dir + '/page' + str(idx) + '.jpg'
    subprocess.run(['tesseract', image, output],
                   check=True, stdout=subprocess.PIPE,
                   universal_newlines=True)

#---------------------------------------------------------------------------
def addContent(text_file):
    """
        Copie le contenu de '(visio.txt)' dans le fichier passer en parametre
        :param text_file: type file ouvert en mode ajout('a+')
        :return: null
    """
    with open('visio.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            text_file.write(line)
    f.close()

#--------------------------------------------------------------------------------
def pdfToImg(file_path,image_save_path,debut =None, fin=None):
    """
        Convertie un fichier pdf en suite d'image
        :param file_path: le chemin du fichier
        :param image_save_path: le chemin ou enregistrez les fichiers image
        :return: null
    """
    eraseFile(image_save_path)
    images = convert_from_path(file_path, first_page=debut, last_page=fin)
    for i in range(len(images)):
        images[i].save(image_save_path+'/page' + str(i) + '.jpg','JPEG')
    return len(images)

def extractor(file_path,text_filename, debut, fin):
    """
    Extrait le text du fichier (pdf, image)
    :param file_path: le chemin du fichier
    :param text_filename: type file ouvert en mode ajout('a+') et contient le resultat de l'extraction
    :return: null
    """
    image_save_path =os.path.join(BASE_DIR,'textExtract/images/')
    extract_text_path = 'visio'

    filename_with_extension = os.path.basename(file_path)
    extension = os.path.splitext(filename_with_extension)[1]
    filename = os.path.splitext(filename_with_extension)[0]
    #nbPage = nbpagespdf(input_path)
    if extension.lower()=='.pdf':
        n = pdfToImg(file_path,image_save_path,debut,fin)
        print('pdf')
        for i in range(n):
            tesseractProcess(image_save_path, extract_text_path, i)
            addContent(text_filename)

    else:
        tesseractProcess(file_path, extract_text_path)
        addContent(text_filename)