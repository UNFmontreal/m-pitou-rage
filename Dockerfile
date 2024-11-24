#
# Build wheel
#
FROM ghcr.io/astral-sh/uv:python3.12-alpine AS src
RUN apk add gcc \
  g++ \
  libc-dev \
  make \
  cmake
COPY . /src
RUN pip install virtualenv

RUN virtualenv --system-site-packages /opt/venv \
	&& source /opt/venv/bin/activate \
	&& pip install /src

FROM python:3.12-alpine

COPY --from=src /opt/venv /opt/venv

ENTRYPOINT /opt/venv/bin/unpitou_rage
