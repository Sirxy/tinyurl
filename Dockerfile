FROM python:3.7-alpine

RUN mkdir -p /tinyurl

COPY requirements.txt ./
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . /tinyurl

WORKDIR /tinyurl

EXPOSE 5010

CMD ["python", "app.py"]
