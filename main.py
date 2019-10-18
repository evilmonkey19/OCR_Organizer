from search import search
from Diccionari_OCR import palabras_a_buscar, normalizar
from OCR import ejecuta_OCR, firstPage

import shutil
import os
import Language

langs, words, abbs = palabras_a_buscar()
pdf_dir = "examenes"

for archivo_pdf in os.listdir(pdf_dir):
    if os.path.isdir(archivo_pdf):
        continue
    
    if not archivo_pdf.endswith(".pdf"):
        print(archivo_pdf)
        continue
    
    archivo_pdffp = firstPage(pdf_dir, archivo_pdf)
    ejecuta_OCR(archivo_pdffp, ".".join(archivo_pdffp.split(".")[:-1]) + ".jpg", "test")
    
    vec_probs_cat = Language.lang_coincidence("test", "cat")
    vec_probs_eng = Language.lang_coincidence("test", "eng")
    vec_probs_esp = Language.lang_coincidence("test", "esp")
    if (sum(vec_probs_esp) > sum(vec_probs_cat) and sum(vec_probs_esp) > sum(vec_probs_eng)):
        print("El idioma es castellano:", sum(vec_probs_esp))
    if (sum(vec_probs_cat) > sum(vec_probs_esp) and sum(vec_probs_cat) > sum(vec_probs_eng)):
        print("L'idioma és català:", sum(vec_probs_cat))
    if (sum(vec_probs_eng) > sum(vec_probs_cat) and sum(vec_probs_eng) > sum(vec_probs_esp)):
        print("The language is English:", sum(vec_probs_eng))
    
    for i in range(len(words)):
        
        # traduccion aqui
        if search(words[i], "test.txt"):
            shutil.copy("test.txt", "text/" + archivo_pdf + "_test.txt")
            if not os.path.isdir(pdf_dir + "/" + abbs[i]):
                os.mkdir(pdf_dir + "/" + abbs[i])
            shutil.copy(pdf_dir + "/" + archivo_pdf, pdf_dir + "/" + abbs[i])
#                
#            except FileExistsError:
#                pass
#            finally:
#                os.remove(pdf_dir + "/" + archivo_pdffp)
#        
