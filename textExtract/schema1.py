import os
import re
import unicodedata

from unidecode import unidecode

#----------------------------------------------------------------

def outAccent(string):
    s =  unidecode(string,'utf-8')
    return unicodedata.normalize('NFD', s).encode('ascii', 'ignore')

#----------------------------------------------------------------
def getTitre(text):

    flag = False

    titre = ''
    soustitre = ''
    soustitre2 = ''

    #--------------------------- Regex ------------------------------

    lettre = '[A-Z]'
    romainG = '([Il]{1,3})|^([Il]?V)|^V([Il]{1,3})|^([Il]?X)'
    titreR = "^(" + romainG + ")[.|)]?(\s[a-zA-Z\']+)+\s?$"  # text xx
    titreL = "^([A-Z])[.|)]?(\s[a-zA-Z\']+)+\s?$"  # text xx
    titreN = "^(\d)[.|)]?(\s[a-zA-Z\'’é:-]+)+\s?$"  # text xx
    soustitreR = "^(" + romainG + ")([.|)](\d|[A-Za-z]))[.|)]?(\s[a-zA-Z\']+)+\s?$"
    soustitreL = "^(" + lettre + ")[.|)](\d|[a-z])[.|)]?(\s[a-zA-Z\']+)+\s?$"
    soustitreN = "^(\d[.|)](\d|[a-z]))[.|)]?(\s[a-zA-Z\']+)+\s?$"
    soustitre2R = "^(" + romainG + ")([.|)](\d|[A-Za-z])){1,2}[.|)]?(\s[a-zA-Z\']+)+\s?$"  # text xx
    soustitre2L = "^(" + lettre + "([.|)](\d|a-z])){1,2})[.|)]?(\s[a-zA-Z\']+)+\s?$"  # text xx
    soustitre2N = "^(\d([.|)](\d|a-z])){1,2})[.|)]?(\s[a-zA-Z\']+)+\s?$"  # text xx

    #----------------------------------------------------------------------

    if titre == '':
        if re.fullmatch(titreR, text):
            titre = titreR
            soustitre = soustitreR + '|' + titreN
            soustitre2 = soustitre2R + '|' + soustitreN

            flag = True
        elif re.fullmatch(titreL, text):
            titre = titreL
            soustitre = soustitreL + '|' + titreN
            soustitre2 = soustitre2L + '|' + soustitreN

            flag = True
        elif re.fullmatch(titreN, text):
            titre = titreN
            soustitre = soustitreN
            soustitre2 = soustitre2N

            flag = True
        elif re.fullmatch(soustitreR, text):
            flag = True
        elif re.fullmatch(soustitre2R, text):
            flag = True
        elif re.fullmatch(soustitreN, text):
            flag = True
        elif re.fullmatch(soustitre2N, text):
            flag = True
        elif re.fullmatch(soustitreL, text):
            flag = True
        elif re.fullmatch(soustitre2L, text):
            flag = True


    return flag, titre, soustitre,soustitre2

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def schema1(filename):
    with open(filename) as f:

        data = {}
        block = 1
        l = 1
        contenu = ""

        lines = f.readlines()

        for line in lines:

            so = line.split()
            if line.strip() == 'INTRODUCTION' or line.strip() =='DEVELOPPEMENT' or line.strip() == 'CONCLUSION':
                if contenu != "":
                    data["contenu" + str(block)] = contenu
                    contenu = ''

                data['titre'+str(block)] = line

                block +=1

            elif len(so)>1 and ('[conn' in so[0] and 'Argument' in so[1]):
                if contenu != "":
                    data["contenu" + str(block)+str(l)] = contenu
                    contenu = ''
                data['soustitre' + str(l)] = line
                l+=1
            else:
                    contenu += line

        if contenu != "":
            data["contenu" + str(block)] = contenu
    return data

#----------------------------------------------------------------------------------------

def schema2(filename):

    with open(filename) as f:
        data = {}
        block = 1
        l = 1
        oc = 0
        contenu = ""
        titre = "non"
        lines = f.readlines()
        arg = True
        for line in lines:
            if titre=='non':
                data['grandTitre'] = line
                titre = 'oui'
            so = line.split()

            # if arg:
            #     ligne = "Documentation de Bugzilla"
            #     if (len(so) == 2 or len(so)==3) and (ligne.split()[0] in line and ligne.split()[2] in line):
            #         if oc == 2:
            #             arg = False
            #             data['GrandTitre']=line
            #             block+=1
            #         oc+=1

            if '' in line:
                pass
            elif ('A propos' in line or line.strip() =='Guide utilisateur' or line.strip() == "Guide d'installation et de maintenance" or\
                    line.strip() == "Guide d'administration" or line.strip() == "Guide d'intégration et de personnalisation"):
                arg = False
                if contenu != "" and not arg:
                    data["contenu" + str(block)] = contenu
                    contenu = ''

                data['titre'+str(block)] = line

                block +=1

            elif line.strip() == 'Introduction' or line.strip() == 'Evaluer Bugzilla' or line.strip()=="Obtenir plus d'aide" or line.strip()=='Conventions du document' or\
                line.strip()=='Licence' or line.strip()=='Crédits':
                if contenu != "":
                    data["contenu" + str(block)+str(l)] = contenu
                    contenu = ''
                data['soustitre' + str(l)] = line
                l+=1
            elif not arg:
                    contenu += line

        if contenu != "" and not arg:
            data["contenu" + str(block)] = contenu
    return data


def schema3(filename):
    with open(filename, 'r') as bg:
        lines = bg.readlines();
        dic = {}
        prec = '\n'

        pprec = ''
        text = ''
        i = 1
        l = ''
        contenu = ''

        for line in lines:

            if len(line) > 1:
                if pprec == '':
                    pprec = line
                    continue
                elif l =='':
                    l = line
                    continue
                elif prec == '':
                    prec = line
                    continue
                text = l
                if prec == '\n' and pprec =='\n':
                    if len(text.split()) < 7:
                        if text[0].isalnum() and text[-2] != '.':
                            if len(text) > 4 and matchTitire(text):
                                if ':' not in text:
                                    list = [titre for key, titre in dic.items()]
                                    if text in list:
                                        pass
                                    else:
                                        if ':' in pprec:
                                            contenu += text
                                            pprec = ''
                                        else:
                                            if contenu != '':
                                                dic['contenu' + str(i - 1)] = contenu
                                                contenu = ''
                                            dic['titre' + str(i)] = text
                                            i += 1
                                            pprec = l
                                            l = prec
                                else:
                                    contenu += text
                    else:
                        contenu += text

                else:
                    if len(l)>1:
                        contenu +=l
                    pprec = l
                    l = prec
            prec = line
    if contenu != '':
        dic['contenu' + str(i - 1)] = contenu


    return dic

def schema4(filename):
    with open(filename, 'r') as bg:
        lines = bg.readlines();
        dic = {}
        prec = '\n'
        pprec = ''
        text = ''
        i = 1
        l = 1
        contenu = ''

        for line in lines:

            if len(line) > 1:
                text = line
                if prec != '\n':
                    contenu += text
                else:
                    if len(text.split()) < 7:
                        if text[0].isalnum() and text[-2] != '.' and ':' not in text and text[0].isupper():

                            if len(text) > 3 and matchTitire(text):
                                if ':' not in text:
                                    list = [titre for key, titre in dic.items()]
                                    if text in list:
                                        pass
                                    else:
                                        if ':' in pprec and not excluWord(text):
                                            contenu += text
                                            pprec = ''
                                        else:
                                            if contenu != '':
                                                dic['contenu' + str(i - 1)] = contenu
                                                contenu = ''
                                            dic['titre' + str(i)] = text
                                            i += 1
                                else:
                                    contenu += text
                                    pprec = text
                        else:
                            contenu += text

                    else:
                        contenu += text
                        pprec = text

            prec = line
    if contenu != '':
        dic['contenu' + str(i - 1)] = contenu
        contenu = ''

    return dic

#------------------------------------------------------------------------
def noDuplicateTitre(test_string, data):
    list = [titre for key, titre in data.items() if "titre" in key]
    return  test_string in list
#-------------------------------------------------------------------------

def matchTitire(test_string):


    pattern = '^(\d{1,2})?(\.)?((\s)?\w*)+$'

    result = re.match(pattern, test_string)

    if result:
        return True
    else:
        return False

def excluWord(word):

    list =['AVIS','NOTE','REMARQUE','N.B.','NB','N.B','N.B :']
    if word.upper() in list:
        return True
    else:
        return False

def schema6(filename):
    data = {}
    flag = False
    with open(filename, 'r') as bg:
        c = 0
        lines = bg.readlines();
        data = {}
        prec = '\n'
        pprec = ''
        text = ''
        i = 0
        l = 1
        contenu = ''
        titre = ''
        soustitre = ''
        soustitre2 = ''

        for line in lines:

            if len(line) > 1:
                text = line
                if prec != '\n':
                    contenu += text
                else:
                    test_string = line
                    if not flag:
                        flag, titre, soustitre = getTitre(test_string)
                    if flag:
                        if re.fullmatch(titre, test_string):

                            if contenu != '':

                                if not isinstance(content, dict):
                                    data['contenu' + str(c)] = contenu
                                    c += 1
                                else:
                                    content['contenu' + str(c)] = contenu
                                contenu = ''
                                content = ''
                            i += 1
                            data['t' + str(i)] = line
                            data['ct' + str(i)] = {}
                            content = data['ct' + str(i)]

                            st = 1
                        elif re.fullmatch(soustitre, test_string):
                            if contenu != '':

                                if not isinstance(content, dict):
                                    data['contenu' + str(c)] = contenu
                                    c += 1
                                else:
                                    content['contenu' + str(c)] = contenu
                                contenu = ''
                                content = ''

                            data['ct' + str(i)]["st" + str(st)] = line
                            data['ct' + str(i)]['cst' + str(st)] = {}
                            content = data['ct' + str(i)]['cst' + str(st)]
                            st += 1
                            sst = 1

                    elif len(text.split()) < 7:
                        if text[0].isalnum() and text[-2] != '.' and ':' not in text and text[0].isupper():

                            if len(text) > 3 and matchTitire(text):
                                if ':' not in text:
                                    list = [titre for key, titre in data.items()]
                                    if text in list:
                                        pass
                                    else:
                                        if ':' in pprec and not excluWord(text):
                                            contenu += text
                                            pprec = ''
                                        else:
                                            if contenu != '':
                                                if not isinstance(content, dict):
                                                    data['contenu' + str(c)] = contenu
                                                    c += 1
                                                else:
                                                    content['contenu' + str(c)] = contenu
                                                contenu = ''
                                                content = ''
                                            i += 1
                                            data['t' + str(i)] = line
                                            data['ct' + str(i)] = {}
                                            content = data['ct' + str(i)]
                                            st = 1
                                else:
                                    contenu += text
                                    pprec = text
                        else:
                            contenu += text

                    else:
                        contenu += text
                        pprec = text

            prec = line
    if contenu != '':
        if not isinstance(content, dict):
            data['contenu' + str(c)] = contenu
            c += 1
        else:
            content['contenu' + str(c)] = contenu
        contenu = ''
        content = ''

    return data

def schema7(filename):
    data = {}
    flag = False
    with open(filename, 'r') as bg:
        c = 0
        lines = bg.readlines();
        data = {}
        prec = '\n'
        pprec = ''
        text = ''
        i = 0
        l = 1
        contenu = ''
        titre = ''
        soustitre = ''
        soustitre2 = ''
        part = ''
        for line in lines:

            if len(line)>3 and line[-2]=="-" and line[0]!= '.':
                part = line
            elif len(line) > 1 and line[0]!= '.':
                if part != '':
                    if line[0].isupper():
                        text = part[0:-1]+line
                    else:
                        text = part[0:-2] + line
                    part = ''
                else:
                    text = line
                f, t, s = getTitre(text)
                if prec != '\n' and not f:
                    if text[0]=='':
                        pass
                    else:
                        contenu += text
                elif True:
                    test_string = text
                    if not flag:
                        flag, titre, soustitre = getTitre(test_string)
                    if flag and f and not noDuplicateTitre(test_string,data):

                        if re.fullmatch(titre, test_string):
                            if contenu != '':
                                data['contenu' + str(i - 1)] = contenu
                                contenu = ''
                            data['titre' + str(i)] = text
                            i += 1
                        elif re.fullmatch(soustitre, test_string):
                            if contenu != '':
                                data['contenu' + str(i - 1)] = contenu
                                contenu = ''
                            data['soustitre' + str(i)] = text
                            i += 1
                    elif len(text.split()) < 7:
                        if text[0].isalnum() and text[-2] != '.' and ':' not in text and text[0].isupper():

                            if len(text) > 3 and matchTitire(text):
                                if ':' not in text:
                                    list = [titre for key, titre in data.items() if "titre" in key]

                                    if noDuplicateTitre(text,data):
                                        pass
                                    else:
                                        if ':' in pprec and not excluWord(text):
                                            contenu += text
                                            pprec = ''
                                        else:
                                            if contenu != '':
                                                data['contenu' + str(i - 1)] = contenu
                                                contenu = ''
                                            data['titre' + str(i)] = text
                                            i += 1
                                else:
                                    contenu += text
                                    pprec = text
                        else:
                            contenu += text

                    else:
                        contenu += text
                        pprec = text

            prec = line
    if contenu != '':
        data['contenu' + str(i - 1)] = contenu
        contenu = ''

    return data
def schema5(filename):
    data = {}
    flag = False
    with open(filename, 'r') as bg:
        c = 0
        lines = bg.readlines();
        data = {}
        prec = '\n'
        pprec = ''
        text = ''
        i = 0
        l = 1
        contenu = ''
        titre = ''
        soustitre = ''
        soustitre2 = ''
        part = ''
        for line in lines:

            if len(line)>3 and line[-2]=="-" and line[0]!= '.':
                part = line
            elif len(line) > 1 and line[0]!= '.':

                if part != '':
                    if line[0].isupper():
                        text = part[0:-1]+line
                    else:
                        text = part[0:-2] + line
                    part = ''
                else:
                    text = line

                f, t, s, s2 = getTitre(text)

                if prec != '\n' and not f:

                    if text[0]=='':
                        pass
                    else:
                        contenu += text
                else:
                    test_string = text
                    if not flag:
                        flag, titre, soustitre, soustitre2 = getTitre(test_string)

                    if flag and f and not noDuplicateTitre(test_string,data):

                        if re.fullmatch(titre, test_string):
                            if contenu != '':
                                data['contenu' + str(i - 1)] = contenu
                                contenu = ''
                            data['titre' + str(i)] = text
                            i += 1
                        elif re.fullmatch(soustitre, test_string):
                            if contenu != '':
                                data['contenu' + str(i - 1)] = contenu
                                contenu = ''
                            data['soustitre' + str(i)] = text
                            i += 1
                        elif re.fullmatch(soustitre2, test_string):
                            if contenu != '':
                                data['contenu' + str(i - 1)] = contenu
                                contenu = ''
                            data['soussoustitre' + str(i)] = text
                            i += 1

                    elif len(text.split()) < 7:
                        if text[0].isalnum() and text[-2] != '.' and ':' not in text and text[0].isupper():

                            if len(text) > 3 and matchTitire(text):
                                if ':' not in text:
                                    list = [titre for key, titre in data.items() if "titre" in key]

                                    if noDuplicateTitre(text,data):
                                        pass
                                    else:
                                        if ':' in pprec and not excluWord(text):
                                            contenu += text
                                            pprec = ''
                                        else:
                                            if contenu != '':
                                                data['contenu' + str(i - 1)] = contenu
                                                contenu = ''
                                            data['titre' + str(i)] = text
                                            i += 1
                                else:
                                    contenu += text
                                    pprec = text
                        else:
                            contenu += text

                    else:
                        contenu += text
                        pprec = text

            prec = line
    if contenu != '':
        data['contenu' + str(i - 1)] = contenu
        contenu = ''

    return data


def definitionFonction(line):
    df = False
    if len(line)>2:
        if line[0] == "-" and ":" in line:
            tabline = line.split(':')
            definitio = tabline[0]+':'
            contenueDef = tabline[1]
            if line[-2] == ";":
                df = True
            return [True,definitio,contenueDef,df]
        else:
            return [False]
    else:
        return [False]

# 12 / 03 / 2021
def juridiqueSch2(filename):
    data = {}
    t = 1
    a = 1
    c = 1
    l = 1
    cl = 1
    ct = 1
    dn = 1
    s = 1
    df = False

    contenue = ''

    romainG = '([IlT]{1,3}|([IlT]?[V|X|L|M])|([V|X|L|M][IlT]{1,3}))'

    livre = '^(LIVRE)\s?([IlT]{1,3}|([IlT]?[V|X|L|M])|([V|X|L|M][IlT]{1,3}))\s?[:;]?\s?([a-zA-Z,\']+\s?)+$'
    titre = '^(TITRE)\s?([IlT]{1,3}|([IlT]?[V|X|L|M])|([V|X|L|M][IlT]{1,3}))\s?[:;]?\s?([a-zA-Z\']+\s?)+$'
    capitre = '^(CHAPITRE)\s?(\d|'+romainG+')\s?[:;]?\s?([a-zA-Z\']+\s?)+$'
    article = '^(Article)\s?\d+(-\d)?\s?[:;]?\s?(([a-zA-Z\']+\s?)+)?$'
    section = '^(Section)\s?\d+(-\d)?\s?[:;]?\s?(([a-zA-Zèêé\']+\s?)+)?$'
    definition = r"^(\s?-(\s?[a-zA-Zèêé\',]+)+)\s?[:;]?\s?([a-zA-Zèêé\'\,]+\s?)+(;)?$"

    with open(filename, 'r') as bg:
        prec = "\n"
        lines = bg.readlines();
        i = 0
        for line in lines:

            if line[0] == '':

                line = line[1:]
            if i == 0:
                if len(line)>1:
                    data['code'] = line;
                    i += 1
            elif df:
                contenueDf += line
                if contenueDf[-2] == ';' or contenueDf[-2] == '.':
                    data["defcontenu" + str(dn)] = contenueDf
                    dn += 1
                    contenueDf = ''
                    df = False

            elif re.fullmatch(livre, line):

                if contenue != '':
                    data['contenu' + str(cl)] = contenue
                    contenue = ''
                    cl += 1

                data['livre' + str(l)] = line
                t += 1
            elif re.fullmatch(titre, line):

                if contenue != '':
                    data['contenu' + str(ct)] = contenue
                    contenue = ''
                    ct += 1

                data['titre' + str(t)] = line
                t += 1

            elif re.fullmatch(article, line):

                if contenue != '':
                    data['contenu' + str(ct)] = contenue
                    contenue = ''
                    ct += 1

                data['article' + str(a)] = line
                a += 1

            elif re.fullmatch(capitre, line):

                if contenue != '':
                    data['contenu' + str(ct)] = contenue
                    contenue = ''
                    ct += 1
                data['chapitre' + str(c)] = line
                c += 1

            elif re.fullmatch(section, line):

                if contenue != '':
                    data['contenu' + str(ct)] = contenue
                    contenue = ''
                    ct += 1
                data['section' + str(s)] = line
                s += 1

            elif definitionFonction(line)[0]:

                if contenue != '':
                    data['contenu' + str(ct)] = contenue
                    contenue = ''
                    ct += 1

                data['definition' + str(dn)] = definitionFonction(line)[1]
                if definitionFonction(line)[3]:
                    data["defcontenu" + str(dn)] = definitionFonction(line)[2]
                    dn += 1
                    df = False
                else:
                    contenueDf = definitionFonction(line)[2]
                    df = True

            else:

                contenue += line
            prec = line
        if contenue != '':
            data['contenu' + str(ct)] = contenue

    return data

def juridiqueSch(filename):
    data = {}

    t = 1
    a = 1
    c = 1
    p = 1
    l = 1
    cl = 1
    ct = 1
    dn = 1
    an = 1
    s = 1
    df = False
    ar = False

    contenue = ''
    contenueAr = ''


    romainG = '([IlT]{1,3}|([IlT]?[V|X|L|M])|([V|X|L|M][IlT]{1,3}))'

    livre = '^(LIVRE)\s?([IlT]{1,3}|([IlT]?[V|X|L|M])|([V|X|L|M][IlT]{1,3}))\s?[:;]?\s?([a-zA-Z,\']+\s?)+$'
    titre = '^(TITRE)\s?([IlT]{1,3}|([IlT]?[V|X|L|M])|([V|X|L|M][IlT]{1,3}))\s?[:;]?\s?([a-zA-Z\']+\s?)+$'
    capitre = '^(CHAPITRE)\s?(\d|' + romainG + ')\s?[:;]?\s?([a-zA-Z\']+\s?)+$'
    article = '^(Article)\s?\d+(-\d)?\s?[:;]?\s?(([a-zA-Z\']+\s?)+)?$'
    section = '^(Section)\s?\d+(-\d)?\s?[:;]?\s?(([a-zA-Zèêé\']+\s?)+)?$'
    definition = r"^(\s?-(\s?[a-zA-Zèêé\',]+)+)\s?[:;]?\s?([a-zA-Zèêé\'\,]+\s?)+(;)?$"

    with open(filename, 'r') as bg:
        prec = "\n"
        lines = bg.readlines();
        i = 0
        for line in lines:

            if line[0] == '':

                line = line[1:]
            if i == 0:
                if len(line) > 1:
                    data['code'] = line;
                    i += 1
            elif df:
                contenueDf += line
                if contenueDf[-2] == ';' or contenueDf[-2] == '.':
                    data["defcontenu" + str(dn)] = contenueDf
                    dn += 1
                    contenueDf = ''
                    df = False

            elif re.fullmatch(livre, line):

                if ar:
                    data['Artcontenu' + str(an)] = contenueAr
                    contenueAr = ''
                    ar = False
                    an += 1

                if contenue != '':
                    data['contenu' + str(cl)] = contenue
                    contenue = ''
                    cl += 1

                data['livre' + str(l)] = line
                t += 1
            elif re.fullmatch(titre, line):

                if ar:
                    data['Artcontenu' + str(an)] = contenueAr
                    contenueAr = ''
                    ar = False
                    an += 1

                if contenue != '':
                    data['contenu' + str(ct)] = contenue
                    contenue = ''
                    ct += 1

                data['titre' + str(t)] = line
                t += 1

            elif re.fullmatch(article, line):

                if ar:
                    data['Artcontenu' + str(an)] = contenueAr
                    contenueAr = ''
                    ar = False
                    an += 1

                if contenue != '':
                    data['contenu' + str(ct)] = contenue
                    contenue = ''
                    ar = False
                    ct += 1

                data['article' + str(a)] = line
                a += 1

            elif re.fullmatch(capitre, line):

                if ar:
                    data['Artcontenu' + str(an)] = contenueAr
                    contenueAr = ''
                    ar = False
                    an += 1

                if contenue != '':
                    data['contenu' + str(ct)] = contenue
                    contenue = ''
                    ct += 1
                data['chapitre' + str(c)] = line
                c += 1

            elif re.fullmatch(section, line):

                if ar:
                    data['Artcontenu' + str(an)] = contenueAr
                    contenueAr = ''
                    ar = False
                    an += 1

                if contenue != '':
                    data['contenu' + str(ct)] = contenue
                    contenue = ''
                    ct += 1
                data['section' + str(s)] = line
                s += 1
            elif 'PARTIE' in line:
                if line.split(' ')[1] == 'PARTIE':
                    if ar:
                        data['Artcontenu' + str(an)] = contenueAr
                        contenueAr = ''
                        ar = False
                        an += 1

                    if contenue != '':
                        data['contenu' + str(ct)] = contenue
                        contenue = ''
                        ct += 1
                    data['partie' + str(p)] = line
                    p += 1

            elif definitionFonction(line)[0]:

                if ar:
                    data['Artcontenu' + str(an)] = contenueAr
                    contenueAr = ''
                    an += 1

                if contenue != '':
                    data['contenu' + str(ct)] = contenue
                    contenue = ''
                    ct += 1

                data['definition' + str(dn)] = definitionFonction(line)[1]
                if definitionFonction(line)[3]:
                    data["defcontenu" + str(dn)] = definitionFonction(line)[2]
                    dn += 1
                    df = False
                else:
                    contenueDf = definitionFonction(line)[2]
                    df = True
            elif articleFonction(line)[0]:

                if ar:
                    data['Artcontenu' + str(an)] = contenueAr
                    contenueAr = ''
                    an += 1

                if contenue != '':
                    data['contenu' + str(ct)] = contenue
                    contenue = ''
                    ct += 1

                data['dArticle'+str(a)] = articleFonction(line)[1]
                contenueAr = articleFonction(line)[2]
                ar = True
                a += 1

            elif ar:
                contenueAr += line

            else:

                contenue += line
            prec = line
        if contenue != '':
            data['contenu' + str(ct)] = contenue
        elif ar:
            data['Artcontenu' + str(an)] = contenueAr



    return data

def articleFonction(line):
    a = False
    regex = r"^(Article \d+.)"
    position = re.match(regex, line, re.MULTILINE)
    if len(line) == 0:
        return [False]
    elif position:
        article = line[position.start():position.end()]
        contenueArt = line[position.end()+1:]
        return [True,article,contenueArt,a]
    else:
        return [False]

def miseEnForme(data, contenuAr, contenue, ca, ct):

    if contenuAr != '':
        data['contenueAr' + str(ca)] = contenuAr

        ca += 1
    if contenue != '':
        data['contenu' + str(ct)] = contenue
        ct += 1
    return False
