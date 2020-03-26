FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./load_manifests.py" ]

# Running
# docker build -t my-python-app .
# docker run -it --rm --name my-running-app -v "$PWD":/usr/src/myapp -w /usr/src/myapp my-python-app