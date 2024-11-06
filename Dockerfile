FROM python:3
WORKDIR /app 

RUN python -m pip install --upgrade pip


# 替换为国内源
RUN mkdir -p ~/.pip \
    && echo "[global]" > ~/.pip/pip.conf \
    && echo "index-url=https://mirrors.aliyun.com/pypi/simple" >> ~/.pip/pip.conf \
    && echo "trusted-host=mirrors.aliyun.com" >> ~/.pip/pip.conf


COPY . .
RUN pip install -r requirements.txt
CMD ["python3","app.py"]
