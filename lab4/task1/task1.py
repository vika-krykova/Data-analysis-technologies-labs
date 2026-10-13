import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import warnings
warnings.filterwarnings('ignore')

import pandas as pd
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

df = pd.read_csv('athlete_events.csv', na_values=['NA'])

print("-" * 30)
print("1. Загрузка данных")
print("-" * 30)
print("Данные успешно загружены в DataFrame df")

print("\n" + "-" * 30)
print("2. Количество значений и пропуски")
print("-" * 30)
print("Количество значений по признакам:")
print(df.count())
print("\nКоличество пропусков (по убыванию):")
print(df.isna().sum().sort_values(ascending=False))

columns_with_na = list(df.columns[df.isna().any()])
column_max_na = df.isna().sum().idxmax()
print(f"\nОтвет: пропуски есть в столбцах: {columns_with_na}")
print(f"Больше всего пропусков в признаке: '{column_max_na}' "
      f"({df[column_max_na].isna().sum()} значений)")

print("\n" + "-" * 30)
print("3. Описательная статистика по Age, Height, Weight")
print("-" * 30)
stats = df[['Age', 'Height', 'Weight']].describe().T
print(stats.round(2).to_string())

print("\n" + "-" * 30)
print("4.1. Самый молодой участник ОИ 1992 года")
print("-" * 30)
olympics_1992 = df[df['Year'] == 1992]
youngest = olympics_1992.loc[olympics_1992['Age'].idxmin()]
print(f"Имя:        {youngest['Name']}")
print(f"Возраст:    {int(youngest['Age'])} лет")
print(f"Пол:        {youngest['Sex']}")
print(f"Вид спорта: {youngest['Sport']}")
print(f"Дисциплина: {youngest['Event']}")

print("\n" + "-" * 30)
print("4.2. Список всех видов спорта")
print("-" * 30)
sports = sorted(df['Sport'].unique())
print(sports)

print("\n" + "-" * 30)
print("4.3. Средний рост теннисисток на ОИ 2000")
print("-" * 30)
tennis_2000_women = df[
    (df['Sex'] == 'F') &
    (df['Sport'] == 'Tennis') &
    (df['Year'] == 2000)
]
print(f"Средний рост: {tennis_2000_women['Height'].mean():.2f} см")

print("\n" + "-" * 30)
print("4.4. Золотые медали Китая в настольном теннисе на ОИ 2008")
print("-" * 30)
gold_china_tt_2008 = df[
    (df['NOC'] == 'CHN') &
    (df['Sport'] == 'Table Tennis') &
    (df['Year'] == 2008) &
    (df['Medal'] == 'Gold')
]
print(f"Ответ: {gold_china_tt_2008['Event'].nunique()} золотых медалей")

print("\n" + "-" * 30)
print("4.5. Количество видов спорта на летних ОИ 2004 vs 1988")
print("-" * 30)
sports_1988 = df[(df['Year'] == 1988) & (df['Season'] == 'Summer')]['Sport'].nunique()
sports_2004 = df[(df['Year'] == 2004) & (df['Season'] == 'Summer')]['Sport'].nunique()
diff = sports_2004 - sports_1988
print(f"Летние ОИ 1988: {sports_1988}")
print(f"Летние ОИ 2004: {sports_2004}")
if diff > 0:
    print(f"Ответ: количество видов спорта увеличилось на {diff}")
elif diff < 0:
    print(f"Ответ: количество видов спорта уменьшилось на {-diff}")
else:
    print("Ответ: количество видов спорта не изменилось")

print("\n" + "-" * 30)
print("4.6. Гистограмма возраста мужчин-керлингистов на ОИ 2014")
print("-" * 30)
curling_men_2014 = df[
    (df['Sport'] == 'Curling') &
    (df['Sex'] == 'M') &
    (df['Year'] == 2014)
]

plt.figure(figsize=(8, 5))
plt.hist(curling_men_2014['Age'].dropna(), bins=10,
         color='steelblue', edgecolor='black')
plt.title('Возраст мужчин-керлингистов на ОИ 2014')
plt.xlabel('Возраст, лет')
plt.ylabel('Количество спортсменов')
plt.grid(alpha=0.3)
plt.savefig('curling_2014_age_hist.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n" + "-" * 30)
print("4.7. Зимние ОИ 2006: медали и средний возраст по странам")
print("-" * 30)
winter_2006 = df[(df['Year'] == 2006) & (df['Season'] == 'Winter')]
medalists_2006 = winter_2006.dropna(subset=['Medal'])

unique_medals_2006 = medalists_2006.drop_duplicates(
    subset=['NOC', 'Event', 'Medal']
)

medals_count = unique_medals_2006.groupby('NOC')['Medal'].count()
avg_age = medalists_2006.groupby('NOC')['Age'].mean()

result_47 = pd.DataFrame({
    'medals_count': medals_count,
    'avg_age': avg_age
})
result_47['avg_age'] = result_47['avg_age'].round(2)
print(result_47.to_string())

print("\n" + "-" * 30)
print("4.8. Сводная таблица медалей (Winter 2006)")
print("-" * 30)
pivot_medals = pd.pivot_table(
    unique_medals_2006,
    index='NOC',
    columns='Medal',
    values='Event',
    aggfunc='count',
    fill_value=0
)
pivot_medals = pivot_medals[['Gold', 'Silver', 'Bronze']]
print(pivot_medals.to_string())
