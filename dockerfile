FROM python:3.11-slim-buster

# 設置工作目錄
WORKDIR /app

# 將 requirements.txt 複製到容器中
COPY requirements.txt .

# 安裝所需的 Python 庫
RUN pip install --no-cache-dir -r requirements.txt

# 將應用程序代碼複製到容器中
COPY . .

# 公開 5000 端口，用於外部訪問
EXPOSE 5000

# 定義啟動命令
CMD ["python", "app.py"]