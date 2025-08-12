FROM python:3.11-slim

# diretório de trabalho
WORKDIR /app

# copiar arquivo de dependências
COPY requirements.txt .

# instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# copiar código da aplicação
COPY . .

EXPOSE 5001

# comando para rodar a aplicação
CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]