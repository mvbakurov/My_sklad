import pandas as pd
from calculate import *
from get_data import *

# Даты от и до какого числа производится рассчет
date_from = "2023-06-08 00:00:00"  # дата начала
date_to = "2023-06-08 23:59:59"    # дата конца

# Поучаем базу по товарам
# BASE = assortment()
# BASE.to_csv('BASE.csv')
BASE = pd.read_csv('BASE.csv')
BASE.code = pd.to_numeric(BASE.code)

# Датафреймы для хранения данных на печать и для закупки товаров
print_data = pd.DataFrame()
work_base = pd.DataFrame()



#### Пачки для фасовки. И материалы для этого


for_packing = remains_of_packs_after_shiping(date_to).merge(BASE)

print_data = for_packing[['code', 'name']].sort_values('code')
print_data.loc[:, 'quantity'] = 100

# * 100 / 1000 = /10
work_base['code'] = pd.to_numeric(for_packing.description)
work_base = work_base.merge(BASE[['code', 'name']], on='code')
work_base['quantity'] = for_packing.weight / 10

# Для фасовки на 100 пачек нужно вес * 100 / 1000, чтобы перевести в кг
for_packing['weight'] = for_packing['weight'] / 10



### Стаканчики для фасовки

glasses = sold_goods(date_from, date_to)
glasses.code = pd.to_numeric(glasses.code)
glasses = glasses[
              (glasses.code > 20000)
              & (glasses.code < 30000)
              & (glasses.code != 25069)
              & (glasses.code != 25071)
              & (glasses.code != 25072)
    ]

glasses.to_csv('3.csv')



print_data[['code', 'name', 'quantity']].rename(columns={'name': 'Фасовка', 'quantity': 'пачек'}).to_csv('1.csv')
print_data.to_csv('1.csv')

work_base.to_csv('2.csv')
