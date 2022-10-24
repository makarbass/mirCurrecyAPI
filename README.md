# mirCurrencyAPI
API курсов валют системы МИР

Для обновления курсов в БД запустить файл `check_rates.py` (добавить в crontab с желаемым промежутком обновления)

## Получение курсов на данный момент

```GET``` /rate - актуальные курсы валют на данный момент

Пример ответа:
```json
{
"rate": [
    {
      "currency": 1,
      "value": 0.16096,
      "name": "Армянский драм",
      "ticker": "AMD"
    },
  ]
}
```

```GET``` /rate?currency={CURRENCY_ID} - курсы за последние 7 дней по определенной валюте
```GET``` /rate?currency={CURRENCY_ID}&beginDate=YYYY-MM-DD - c какой даты до сегодняшнего дня
```GET``` /rate?currency={CURRENCY_ID}&endDate=YYYY-MM-DD - 7 дней до какой даты
```GET``` /rate?currency={CURRENCY_ID}&beginDate=YYYY-MM-DD&endDate=YYYY-MM-DD - с какой по какую дату


Пример ответа:
```json
{
"beginDate": "2022-10-17 00:00:00",
"endDate": "2022-10-24 23:59:59.999999",
"name": "Армянский драм",
"ticker": "AMD",
"values": [
    {
      "date": "2022-10-18 09:00:00",
      "rate": 0.16199
    },
  ]
}
```




