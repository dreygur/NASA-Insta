FROM python:3.7-slim

LABEL "maintainer" "Rakibul Yeasin <git+ryeasin03@gmail.com>"
LABEL "repository" "https://github.com/pypa/gh-action-pypi-publish"
LABEL "homepage" "https://github.com/pypa/gh-action-pypi-publish"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade --no-cache-dir -r requirements.txt

WORKDIR /app
COPY LICENSE.md .
COPY twine-upload.sh .

RUN chmod +x twine-upload.sh
ENTRYPOINT ["/app/twine-upload.sh"]