FROM python:3.11-slim

# Instala pacotes básicos e dependências do Chrome para conseguirmos executar o Kaleido (geração de PDF com imagens)
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    curl \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    xdg-utils \
    libu2f-udev \
    libvulkan1 \
    && rm -rf /var/lib/apt/lists/*

# Instala o Google Chrome (versão estável)
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*
    
# Diretório de trabalho na pasta app (padrão p deploy com docker)
WORKDIR /app

# Instala dependências Python (libs necessárias)
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copia o código do meu PC para a imagem do docker
COPY . .

# Expõe a porta padrão do Google Cloud Run
EXPOSE 8080

# Comando para iniciar o app web via Streamlit
CMD ["streamlit", "run", "index_code.py", "--server.port=8080", "--server.address=0.0.0.0"]