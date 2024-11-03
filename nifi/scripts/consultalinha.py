from org.apache.nifi.processor.io import StreamCallback
import csv
import json
import requests

class CSVProcessor(StreamCallback):
    def __init__(self):
        self.auth_token = self.authenticate()  # Chama a função de autenticação

    def authenticate(self):
        url = "http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar?token=4dce59f8ee6f8f22167f9ef33b230a93d6c0f76ce3be7e1b87d29ed61f81e078"
        response = requests.post(url)
        if response.status_code == 200:
            return response.json().post('token')  # Supondo que o token esteja na chave 'token'
        else:
            raise Exception("Falha na autenticação: {}".format(response.status_code))

    def process(self, inputStream, outputStream):
        # Lê o conteúdo do inputStream como bytes
        input_data = inputStream.read()
        
        if isinstance(input_data, int):
            raise ValueError("Esperado bytes, mas recebeu um inteiro.")

        input_data = input_data.decode('utf-8')

        if not input_data.strip():
            outputStream.write(json.dumps([]).encode('utf-8'))
            return

        reader = csv.DictReader(input_data.splitlines())
        results = []

        for row in reader:
            route_id = row['route_id']
            headers = {'Authorization': 'Bearer {}'.format(self.auth_token)}  # Adiciona o cabeçalho de autenticação
            response = requests.get("http://api.olhovivo.sptrans.com.br/v2.1/Linha/Buscar?termosBusca={}".format(route_id), headers=headers)
            
            if response.status_code == 200:
                results.append({
                    'route_id': route_id,
                    'data': response.json()
                })
            else:
                results.append({
                    'route_id': route_id,
                    'error': response.status_code
                })

        outputStream.write(json.dumps(results).encode('utf-8'))

# Registra o callback
flowFile = session.get()
if flowFile is not None:
    processor = CSVProcessor()
    session.write(flowFile, processor)
    session.transfer(flowFile, REL_SUCCESS)
