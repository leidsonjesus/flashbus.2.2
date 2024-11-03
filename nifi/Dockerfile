# Use a imagem oficial do Apache NiFi como base
FROM apache/nifi:latest

# Mudar para o usuário root para instalação
USER root

# Atualizar o sistema e instalar Python e pip
#RUN apt-get update && apt-get install -y python3 python3-pip 

# Instalar PySpark e boto3 diretamente em /usr/bin
#RUN pip3 install pyspark boto3
RUN pip install pyspark==2.4.8 
RUN pip install boto3==1.9.0 
RUN pip install requests==2.22.0
RUN pip install pyarrow==0.15.1
RUN pip install certifi==2016.2.28
# Criar diretório e alterar permissões
# Reverter para o usuário nifi
USER nifi

# Definir o diretório de trabalho (opcional)
WORKDIR /opt/nifi/nifi-current

# Comando para iniciar o NiFi (opcional, pois já está definido na imagem base)
CMD ["bin/nifi.sh", "run"]