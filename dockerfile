FROM python:3.11
COPY . ./app
WORKDIR /app
COPY ./requirements.txt ./
COPY ./migrations.sh ./
RUN pip install --no-cache-dir -r requirements.txt
RUN apt update
RUN  apt install sqlite3
RUN run app/migrations.sh
CMD ["streamlit", " run", "str.py"]