# Use a imagem base do Python
FROM python:3.12.3

# Defina o diretório de trabalho
WORKDIR /app

# Copie o conteúdo do diretório atual para o contêiner
COPY . .

# Atualize e instale as dependências necessárias
RUN apt-get update && \
    apt-get install -y git gcc libpoppler-cpp-dev pkg-config python3-dev && \
    curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash && \
    apt-get install -y git-lfs && \
    git lfs install

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r configure/requirements.txt

# Comando de entrada (entrypoint)
CMD ["uvicorn", "application:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]                                               