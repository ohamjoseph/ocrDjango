# ocrDjango
## Preinstalations

* [Tesseract-ocr](https://github.com/tesseract-ocr/tesseract)
* [MongoDB](https://www.mongodb.com/try/download/community)
* [Django](https://www.djangoproject.com/)

## Architecture

```
ocrDjango/
---manage.py
---media/
------pdf/
------text
---ocr/
------__init__.py
------models.py
------urls.py
------view.py
---ocrDjango/
------__init__.py
------settings.py
------urls.py
------asgi.py
---textExtract/
------images/
------extractor.py
------schema1.py
---visio.txt
---wsgi.py
```

### Le module ocr
ocr est une application django, il contient les vues, les models et les urls. C’est lui qui se charge de la communication entre les utilisateurs et le coeur de l’application (textExtract)
### Le module textExtract
Cet module regroupe l’ensemble des fonctions d'extraction et de structuration.
### /images
Le dossiers /images reçoit les pages du document pdf.
### Package extractor.py
Le package extractor.py recoit le dossiers /images et passe chaque pages a tesseract-ocr et retourne le chemin du fichier .txt contenant les données du document.
### Le package shema1.py
shema1.py regroupe plusieurs fonctions de structuration. Chaque fonction reçoit le chemin du fichier .txt et retourne une variable data. La variable data est un dictionnaire qui retrace la mise en page initiale du document pdf chargé.
Chaque fonction du package shema1.py est appeller depuis ocr/views selon le type de document chargé. Pour un document juridique c’est la fonction schéma1.juridiqueSch() qui sera appelée.
