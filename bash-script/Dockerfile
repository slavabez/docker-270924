# Дебиан слим как база
FROM debian:12-slim

# Установка curl
RUN apt-get update && apt-get install -y curl && mkdir /app && mkdir /app/data

# Переход в рабочую директорию
WORKDIR /app

# Копирование скрипта в рабочую директорию
COPY fetch_exchange_rates.sh .

# Установка исполняемости скрипта
RUN chmod +x fetch_exchange_rates.sh

# Запуск скрипта при старте контейнера
CMD ["./fetch_exchange_rates.sh"]

# Говорим Docker, что мы хотим использовать данную папку как том (volume)
VOLUME /app/data