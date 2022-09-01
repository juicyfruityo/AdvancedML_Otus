FROM python:3.7

RUN pip install fastapi uvicorn sklearn

RUN  mkdir WORK_REPO
RUN  cd  WORK_REPO
WORKDIR  /WORK_REPO
ADD model_application.py .
COPY model ./model

EXPOSE 8000

ENTRYPOINT ["uvicorn"]
CMD ["model_application:app", "--host", "0.0.0.0"]