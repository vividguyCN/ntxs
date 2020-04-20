FROM python:3.7

COPY ./novelspider ./novelspider

RUN pip3 install --default-timeout=100 -r novelspider/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple


ENTRYPOINT ["python","novelspider/main.py"]