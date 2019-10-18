###         Diccionari OCR      ###

## IMPORTS ##
import unicodedata
import os
import requests

## VARIABLES ##

## FUNCTIONS ##

# Normaliza la palabra para que no de problemas en el futuro
# INPUT: String sucio     // OUTPUT: String limpio
def normalizar(w):
    word = ""
    # Separem en paraules
    w = w.split()
    for i in range(0, len(w)):
        # Llevem espais en blanc
        w[i] = w[i].rstrip()
        # Llevem accents
        w[i] = unicodedata.normalize("NFKD",w[i]).encode("ascii","ignore").decode("ascii")
        # Posem minúscules
        w[i] = w[i].lower()
        # Posem les paraules netes a word
        word += w[i]
        if (i != (len(w)-1)):
            word += " "

    return word

# Lee el .txt del cliente y pone las palabras e idiomas que este quiere
# INPUT: "buscar.txt"       // OUTPUT: words, lang
def palabras_a_buscar():
    with open('buscar.txt', 'r', encoding = 'utf-8') as f:
        lang = f.readline().rsplit(' ')     # Leemos los idiomas (Irá a la siguiente linea)
        words = f.readlines()               # Leemos las palabras

        for i in range(0, len(lang)):
            lang[i] = lang[i].rstrip("\n")
            lang[i] = traduccion("es", "en", lang[i])
            lang[i] = normalizar(lang[i])
            lang[i] = languages(lang[i])

        abbs = [""] * len(words)
        for i in range(0, len(words)):
            words[i] = words[i].rstrip("\n")
            words[i], abbs[i] = words[i].split(";")
            words[i] = normalizar(words[i])
            abbs[i] = normalizar(abbs[i])
    
        return lang, words, abbs

# Hace una llamada al traductor online de Google
# INPUT: Lenguaje del que venimos, Lenguaje al que vamos, texto a traducir
#OUTPUT: Texto traducido
def traduccion(source, target, text):
	parametros = {'sl': source, 'tl': target, 'q': text}
	cabeceras = {"Charset":"UTF-8","User-Agent":"AndroidTranslate/5.3.0.RC02.130475354-53000263 5.1 phone TRANSLATE_OPM5_TEST_1"}
	url = "https://translate.google.com/translate_a/single?client=at&dt=t&dt=ld&dt=qca&dt=rm&dt=bd&dj=1&hl=es-ES&ie=UTF-8&oe=UTF-8&inputm=2&otf=2&iid=1dd3b944-fa62-4b55-b330-74909a99969e"
	response = requests.post(url, data=parametros, headers=cabeceras)
	if response.status_code == 200:
		for x in response.json()['sentences']:
			return x['trans']
	else:
		return "Ocurrió un error"

# Mapa con los diferentes lenguajes abreviados para el OCR
# INPUT: Lenguaje // OUTPUT: Lenguaje acortado
def languages(lang):
    mapa = {"spanish" : "spa", "catalan" : "cat", "english" : "eng"}
    return mapa[lang]