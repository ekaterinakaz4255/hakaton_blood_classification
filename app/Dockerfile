FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN apt update
RUN apt install sqlite3
RUN mkdir -p database
RUN ./migrations.sh
CMD ["streamlit", "run", "str.py"]