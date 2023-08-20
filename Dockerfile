FROM python:latest


RUN git clone https://github.com/dyler2/mediaall.git /mediaall
WORKDIR /mediaall
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r mediaall/requirements.txt
CMD python3 mediaall.py

