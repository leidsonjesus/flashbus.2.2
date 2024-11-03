import requests
from org.apache.nifi.processor.io import StreamCallback
from java.io import OutputStream

class WriteToS3(StreamCallback):
    def __init__(self, url):
        self.url = url

    def write(self, outputStream):
        response = requests.get(self.url, stream=True)
        
        if response.status_code == 200:
            outputStream.write(response.content)
            print "Arquivo enviado para o S3 com sucesso."
        else:
            print "Erro ao acessar a URL: {}".format(response.status_code)

# URL que você deseja acessar
url = "https://www.sptrans.com.br/umbraco/Surface/PerfilDesenvolvedor/BaixarGTFS?memberName=teste"

# Instanciando o callback para escrever no fluxo
writeToS3 = WriteToS3(url)

# Acessando o fluxo de saída
flowFile = session.get()
if flowFile is not None:
    # Adicionando conteúdo ao flowfile
    flowFile = session.write(flowFile, writeToS3)
    # Definindo atributos, se necessário
    flowFile = session.putAttribute(flowFile, "filename", "gtfs_files.zip")
    
    # Transferindo para o próximo processador
    session.transfer(flowFile, REL_SUCCESS)
