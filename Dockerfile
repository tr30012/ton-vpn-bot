FROM snakepacker/python:all as builder

RUN python3.9 -m venv /usr/share/python3/app
RUN /usr/share/python3/app/bin/pip install -U pip

COPY requirements.txt /mnt/
RUN /usr/share/python3/app/bin/pip install -Ur /mnt/requirements.txt

COPY ./dist/ /mnt/dist/
RUN /usr/share/python3/app/bin/pip install /mnt/dist/* \
    && /usr/share/python3/app/bin/pip check

FROM snakepacker/python:3.9 as api

COPY --from=builder /usr/share/python3/app /usr/share/python3/app

RUN ln -snf /usr/share/python3/app/bin/vpnbot /usr/local/bin/

# Устанавливаем выполняемую при запуске контейнера команду по умолчанию
CMD ["vpnbot"]