FROM python:3
RUN mkdir -p /home/app
COPY . /home/app
RUN python3 -m pip install --no-cache-dir -r /home/app/requirements.txt
WORKDIR /home/app
EXPOSE 8000
CMD [ "python3","-m","uvicorn","main:app","--host","0.0.0.0"]