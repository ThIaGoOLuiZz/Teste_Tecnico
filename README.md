## Estrutura do Projeto

- `apagar_arquivos()`: Apaga a pasta `faturas` e o arquivo `resultado.csv` antes da execução para evitar dados antigos.
- `baixar_imagem(url)`: Faz download da imagem a partir da requisição da URL e salva na pasta `faturas`.
- `ocr_imagem(caminho_imagem)`: Utiliza OCR (Tesseract) para extrair texto da imagem e aplicar regex para capturar o código da fatura e a data.
- `regex_data(texto)`: Extrai e formata datas no formato `yyyy-mm-dd` ou datas escritas por extenso (ex: Jun 1, 2019).
- `regex_fatura(texto)`: Extrai o código da fatura a partir do texto extraído.
- `obter_valores_tabela()`: Usa Selenium para acessar a página, aguardar a tabela carregar, e extrair os dados da tabela.
- `criar_csv(lista)`: Cria o arquivo CSV com as colunas: `id`, `Data_Vencimento`, `Data_Fatura`, `Fatura`,`Link_Imagem`.
- `main()`: Orquestra a execução do script.

## Decisões Técnicas e Otimizações

- **Selenium com JavaScript**: Extração da tabela HTML com execução de script para capturar dados de maneira dinâmica e mais eficiente. Incluindo a manipulação do datanho do DataTable por JavaScript, aumentando ainda mais a eficiência de execução;
- **ThreadPoolExecutor**: Utilizado para baixar as imagens em paralelismo, melhorando o tempo total de download e processamento;
- **OCR com pytesseract**: Utilizado para obter os textos das Faturas. Essa escolha foi feita por conta da facilidade de integração com Python, permitindo converter imagens de faturas em texto para posterior análise via regex;
- **Regex customizado**: Para captura dos dados essenciais (datas e códigos) direto do texto extraído por OCR;

## Como executar
1. Instalar Tesseract OCR: https://digi.bib.uni-mannheim.de/tesseract/
- OBS: O código já define a PATH de ambiente ao executar, caso dê algum problema para execução, verifique se a PATH está conforme o código:
```python
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```

2. Clone o repositório:
 ```bash
git clone https://github.com/ThIaGoOLuiZz/Teste_Tecnico
cd Teste_Tecnico
```
   
3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute o script principal:
```python
python main.py
```
## Após a execução, verifique o arquivo resultado.csv gerado na raiz do projeto com os dados extraídos.
