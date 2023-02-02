# 选择buster版本镜像
FROM python:3.9.12-buster as builder-image
# 安装包,不缓存
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 选择slim最小包
FROM python:3.9.12-slim-buster
# 把第一阶段安装的包复制出来
COPY --from=builder-image /usr/local/bin /usr/local/bin
COPY --from=builder-image /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# 设定目录, 拷贝本地代码
WORKDIR /backend/
COPY . ./backend


#ENV PYTHONPATH=/backend

# 暴露端口
EXPOSE 80
CMD ["uvicorn", "main:app","--reload","--host", "0.0.0.0", "--port", "80"]