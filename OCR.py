from pdf2image import convert_from_path
from subprocess import call

import PyPDF2 as pypdf
import os

TESSERACT_CMD = "tesseract.exe"


def firstPage(pdfdir, fileName):
	fr = pypdf.PdfFileReader(pdfdir + "/" + fileName, strict=False)
	
	fw = pypdf.PdfFileWriter()
	fw.addPage(fr.getPage(0))
	
	name = ".".join(fileName.split(".")[:-1]) + "_fp.pdf"
	
	with open(name, 'wb+') as f:
		fw.write(f)
	
	return name


def ejecuta_OCR(arch_pdf, arch_jpg, name_txt):
	pages = convert_from_path(arch_pdf, 300)    # Convertim pdf a jpg
	pages[0].save(arch_jpg, 'JPEG')     # Només guardem la primera pàgina

	order = TESSERACT_CMD + " " + arch_jpg + " " + name_txt + " --dpi 300 -l spa"    # Ejecuta el OCR
	call(order, shell= True)        # Pasar la imagen a texto (Leer pdf)
