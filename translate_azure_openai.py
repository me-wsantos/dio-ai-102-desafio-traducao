import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url):
  response = requests.get(url)

  if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    for script_or_style in soup(['script', 'style']):
      script_or_style.decompose()
    
    texto = soup.get_text(separator=' ')

    #Limpar texto
    lines = (line.strip() for line in texto.splitlines())
    parts = (phrase.strip() for line in lines for phrase in line.split(" "))
    clear_text = '\n'.join(part for part in parts if part)
    return clear_text
  else:
    print(f"Failed to fetch the URL. Status code: { response.status_code}")
    return None

  #text = soup.get_text()
  #return text

extract_text_from_url('https://dev.to/azure/machine-learning-in-azure-1b84')

from langchain_openai.chat_models.azure import AzureChatOpenAI

client = AzureChatOpenAI(
    azure_endpoint="https://dio-desafio-tradutor-artigos-tecnicos-azure-openai.openai.azure.com/",
    api_key="your api key",
    api_version="2024-02-15-preview",
    deployment_name="gpt-4o-mini",
    max_retries=0
)

def translate_article(text, lang):
  messages = [
      ("system", "Você atua como tradutor de textos"),
      ("user", f"Traduza o { text } para o idioma { lang } e responda em markdown")
  ]

  response = client.invoke(messages)
  return response.content

url = "https://blogs.nvidia.com/blog/nvidia-inception-microsoft-startups-ai-healthcare/"
text = extract_text_from_url(url)
article = translate_article(text, "pt-br")
print(article)