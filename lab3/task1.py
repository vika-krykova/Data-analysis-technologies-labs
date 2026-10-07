import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)

YEARS = 30
LAST_FIVE_YEARS = 5

generation = np.genfromtxt(
    'global-electricity-generation.csv',
    delimiter=',', skip_header=1, usecols=range(1, 1 + YEARS),
    dtype=float, missing_values={'--', 'ie', ''}, filling_values=np.nan
)
consumption = np.genfromtxt(
    'global-electricity-consumption.csv',
    delimiter=',', skip_header=1, usecols=range(1, 1 + YEARS),
    dtype=float, missing_values={'--', 'ie', ''}, filling_values=np.nan
)
country_names = np.genfromtxt(
    'global-electricity-generation.csv',
    delimiter=',', skip_header=1, usecols=0,
    dtype=str, encoding='utf-8'
)

print("-" * 60)
print("Загружено:")
print(f" generation — {generation.shape}")
print(f" consumption — {consumption.shape}")
print(f" стран — {len(country_names)}")
print("-" * 60)

average_generation_last5  = np.nanmean(generation[:, -LAST_FIVE_YEARS:], axis=1)
average_consumption_last5 = np.nanmean(consumption[:, -LAST_FIVE_YEARS:], axis=1)

print("\n1. Суммарное потребление по годам (1992–2021):")
total_consumption_per_year = np.nansum(consumption, axis=0)
years = list(range(1992, 2022))
for year, value in zip(years, total_consumption_per_year):
    print(f" {year}: {value:10.2f}")

print("\n2. Максимум производства одной страной за один год:")
print(f" {np.nanmax(generation):.2f} млрд кВт*ч")

print("\n3. Страны с производством > 500 (в среднем за 5 лет):")
big_producers_mask = average_generation_last5 > 500
print("  " + ", ".join(country_names[big_producers_mask]))

print("\n4. Топ-10% по потреблению (в среднем за 5 лет):")
threshold_90_percent = np.nanquantile(average_consumption_last5, 0.9)
top_consumers_mask = average_consumption_last5 >= threshold_90_percent
print(f" Порог (90-й процентиль): {threshold_90_percent:.2f} млрд кВт*ч")
print(f" Всего стран: {top_consumers_mask.sum()}")
print("  " + ", ".join(country_names[top_consumers_mask]))

print("\n5. Рост производства > 10 раз (2021 к 1992):")
with np.errstate(divide='ignore', invalid='ignore'):
    generation_growth_ratio = generation[:, -1] / generation[:, 0]
fast_growth_mask = (generation_growth_ratio > 10) & np.isfinite(generation_growth_ratio)
print("  " + ", ".join(country_names[fast_growth_mask]))

print("\n6. Потратили > 100 и произвели меньше, чем потратили:")
total_consumption_per_country = np.nansum(consumption, axis=1)
total_generation_per_country = np.nansum(generation,  axis=1)
deficit_mask = (total_consumption_per_country > 100) & (total_generation_per_country < total_consumption_per_country)
print("  " + ", ".join(country_names[deficit_mask]))

print("\n7. Кто больше всех потребил в 2020:")
YEAR_2020_INDEX = -2
top_consumer_2020_index = np.nanargmax(consumption[:, YEAR_2020_INDEX])
print(f"  {country_names[top_consumer_2020_index]} — {consumption[top_consumer_2020_index, YEAR_2020_INDEX]:.2f} млрд кВт*ч")
