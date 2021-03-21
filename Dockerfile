FROM python:3

RUN pip install simple5ploit

CMD [ "/usr/local/bin/simple5ploit" ]
