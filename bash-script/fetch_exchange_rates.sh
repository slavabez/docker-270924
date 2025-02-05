#!/bin/bash

# Скачиваем данные об обменных курсах относительно USD
curl -o /app/data/currencies.json https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/usd.json

# Выводим сообщение о успешной загрузке данных
echo "Currency data saved to currencies.json"