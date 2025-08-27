from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime
import requests
import os
from concurrent.futures import ThreadPoolExecutor
import shutil
from PIL import Image
import pytesseract
import re
import csv
import time

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe" ## Definir variavel de ambiente do tesseract

def apagar_arquivos():
  if os.path.exists("faturas"):
    shutil.rmtree("faturas")
  os.makedirs("faturas")

  if os.path.exists("resultado.csv"):
    os.remove("resultado.csv")

def baixar_imagem(url):
  response = requests.get(url)
  nome_imagem = url.split("/")[-1]

  if response.status_code == 200:
    with open(f"faturas/{nome_imagem}","wb") as f:
        f.write(response.content)
  else:
     print(f"Erro na requisição: {response.content}")

def ocr_imagem(caminho_imagem):
  imagem = Image.open(caminho_imagem)
  texto = pytesseract.image_to_string(imagem)
  fatura = regex_fatura(texto)
  data_fatura = regex_data(texto)
  valores = [fatura, data_fatura]
  return valores

def regex_data(texto):
  match_data_formatada = re.search(r"\b(\d{4})-(\d{2})-(\d{2})\b", texto)
  match_data_extenso = re.search(r"\b([A-Za-z]{3})\s+(\d{1,2}),\s+(\d{4})", texto)

  if match_data_formatada:
        data_str = match_data_formatada.group(0)
        data_obj = datetime.strptime(data_str, "%Y-%m-%d")
        return data_obj.strftime("%d/%m/%Y")

  if match_data_extenso:
        mes_abrev = match_data_extenso.group(1)
        dia = int(match_data_extenso.group(2))
        ano = int(match_data_extenso.group(3))

        data_str = f"{mes_abrev} {dia}, {ano}"
        data_obj = datetime.strptime(data_str, "%b %d, %Y")
        return data_obj.strftime("%d-%m-%Y")
  return None

def regex_fatura(texto):
  padrao = r"#\s*(\w+)"
  match = re.search(padrao, texto)
  if match:
      codigo = match.group(1)
      return codigo
  else:
      return None
  
def obter_valores_tabela():
  driver = webdriver.Chrome()
  driver.get("https://rpachallengeocr.azurewebsites.net/")

  WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "start")))
  driver.execute_script("$('#tableSandbox').DataTable().page.len(12).draw();")

  script_retorno_matriz = """
  return [...document.querySelectorAll("#tableSandbox tr")]
    .map(tr => [...tr.querySelectorAll("th,td")]
      .map(td => td.querySelector("a")?.href || td.innerText.trim())
    );
  """

  matriz = driver.execute_script(script_retorno_matriz)
  dados = matriz[1:]
  driver.close()
  return dados

def criar_csv(lista):
   with open("resultado.csv", mode="w", newline="", encoding="utf-8") as arquivo:
      writer = csv.writer(arquivo)
      writer.writerow(["id","Data_Vencimento","Data_Fatura","Fatura"])
      writer.writerows(lista)

def main():
  apagar_arquivos()

  urls = []
  lista = []
  dados = obter_valores_tabela()

  start = time.time() ## Inicio do cronometro

  for linha in dados:
      id = linha[1]
      data_venc = datetime.strptime(linha[2], "%d-%m-%Y").date()
      link_img = linha[3]

      if data_venc >= datetime.today().date():
        valores = [id,data_venc,link_img]

        urls.append(link_img)
        lista.append(valores)

  with ThreadPoolExecutor(max_workers=12) as executor:
    executor.map(baixar_imagem, urls)

  lista_csv = []
  for linha in lista:
    id = linha[0]
    data_venc = linha[1]
    nome_arquivo = linha[2].split("/")[-1]

    caminho = f"faturas/{nome_arquivo}"
    valores_ocr = ocr_imagem(caminho)

    fatura = valores_ocr[0]
    data_fatura = valores_ocr[1]

    lista_csv.append([id,data_venc,data_fatura,fatura])

  criar_csv(lista_csv)
  
  end = time.time() ## Final do cronometro
  print(f"Tempo de execução: {end - start:.2f} segundos")

if __name__ == "__main__":
  main()