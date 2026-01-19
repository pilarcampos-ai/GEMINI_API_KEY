import fitz  # PyMuPDF
from docx import Document
import google.generativeai as genai
import os
import glob

# Configurar la Inteligencia Artificial
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def traducir_texto(texto):
    if not texto.strip(): return ""
    prompt = f"Traduce fielmente este manual técnico al español. Mantén estructura y términos técnicos. No resumas:\n\n{texto}"
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return texto

# Crear carpeta de salida si no existe
if not os.path.exists('salida'):
    os.makedirs('salida')

# Buscar PDFs en la carpeta de entrada
for ruta_pdf in glob.glob("entrada/*.pdf"):
    nombre_archivo = os.path.basename(ruta_pdf).replace(".pdf", ".docx")
    doc_word = Document()
    pdf = fitz.open(ruta_pdf)
    
    for pagina in pdf:
        bloques = pagina.get_text("blocks")
        for b in bloques:
            texto_es = traducir_texto(b[4])
            doc_word.add_paragraph(texto_es)
            
    doc_word.save(f"salida/TRADUCIDO_{nombre_archivo}")
