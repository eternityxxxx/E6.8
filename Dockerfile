FROM python:3.7.6

ENV PORT 8081

WORKDIR app/

COPY ./requirements.txt ./

RUN pip install -r requirements.txt

COPY ./ .

ENTRYPOINT ["python"]

CMD ["app.py"]
