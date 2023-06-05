import requests
import pandas as pd

limit = 1000
token = '314d9d92c7daca89902e1edba8bcef7ccfb454b5'
headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}

def remains(date):

    """
    remains -  это остатки
    Получаю остатки на дату date_from
    """

    params = (
        ("limit", limit),
        ("filter", "stockMode=all"),
        ("filter", f"moment={date}")
    )
    url = "https://online.moysklad.ru/api/remap/1.2/report/stock/all"
    response = requests.get(url=url, headers=headers, params=params)
    result = response.json()
    assortment = pd.DataFrame(pd.json_normalize(result)['rows'][0]).sort_values('code')
    assortment.code = pd.to_numeric(assortment.code)
    return assortment[assortment.code > 10000][['code', 'name', 'quantity']]

def sold_goods(date_1, date_2):

    """
    Получаю список проданных товаров c даты date_from по дату date_to
    """

    params = (
        ('momentFrom', f'{date_1}'),
        ('momentTo', f'{date_2}')
    )
    url = "https://online.moysklad.ru/api/remap/1.2/report/profit/byproduct"
    response = requests.get(url=url, headers=headers, params=params)
    result = response.json()
    sold = pd.DataFrame(pd.json_normalize(result)['rows'][0])
    quantity = sold.sellQuantity
    sold = pd.json_normalize(sold.assortment)[['code', 'name']].sort_values('code')
    sold['quantity'] = quantity
    return sold



def assortment():

    """
    Получаю характеристики по сущности assortment
    Код, наименование, описание
    В описании ссылка на материал из которого изготавливается товар
    """

    url = "https://online.moysklad.ru/api/remap/1.2/entity/assortment"
    response = requests.get(url=url, headers=headers)
    result = pd.DataFrame(pd.json_normalize(response.json())['rows'][0])
    result.code = pd.to_numeric(result.code)
    return result[['code', 'name','description', 'weight']]



def remains_of_packs_after_shiping (date):

    """
    Остатки по пачкам, посчитанные после выполнения отгрузок
    date_to
    """

    result = remains(date)

    # Возвращаю только пачки, которых меньше 30
    return result[(result.code < 20000) & (result['quantity'] < 50)].sort_values('quantity')