from pathlib import Path
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

cols = [
    'State', 'Area code', 'International plan', 'Number vmail messages',
    'Total day minutes', 'Total day calls',
    'Total eve minutes', 'Total eve calls',
    'Total night minutes', 'Total night calls',
    'Customer service calls', 'Churn'
]

csv_path = Path(__file__).parent / 'telecom_churn.csv'
df = pd.read_csv(csv_path, usecols=cols)

sep = "-" * 30

print("1. Общая информация о датафрейме:")
print(df.info())
print(df.describe(include='all').to_string())
missing = df.isna().sum().sum()
print("\n" + f"Есть ли отсутствующие данные? {'Да' if missing > 0 else 'Нет'} (всего пропусков: {missing})")

print("\n" + sep)

print("\n2. Распределение клиентов по оттоку:")
counts = df['Churn'].value_counts()
percent = df['Churn'].value_counts(normalize=True) * 100
print(counts.to_string())
print(percent.round(2).to_string())
print(f"Активных: {counts[False]} ({percent[False]:.2f}%), потерянных: {counts[True]} ({percent[True]:.2f}%)")

df['avg_call_duration'] = (
    df['Total day minutes'] + df['Total eve minutes'] + df['Total night minutes']
) / (
    df['Total day calls'] + df['Total eve calls'] + df['Total night calls']
)

print("\n" + sep)

print("\n3. Топ-10 записей по средней продолжительности одного звонка:")
top10 = df.sort_values('avg_call_duration', ascending=False).head(10)
print(top10[['State', 'Area code',
             'Total day minutes', 'Total day calls',
             'Total eve minutes', 'Total eve calls',
             'Total night minutes', 'Total night calls',
             'avg_call_duration', 'Churn']].to_string())

print("\n" + sep)

print("\n4. Средняя продолжительность одного звонка по категориям Churn:")
grouped4 = df.groupby('Churn')['avg_call_duration'].mean()
print(grouped4.to_string())
diff4 = grouped4[True] - grouped4[False]
relative_diff4 = diff4 / grouped4[False] * 100
print(f"Разница: {diff4:.4f} минут ({relative_diff4:.2f}%).")
if abs(relative_diff4) < 5:
    print("Вывод: разница незначительная.")
elif abs(relative_diff4) < 15:
    print("Вывод: разница небольшая, но заметная.")
else:
    print("Вывод: разница существенная.")

print("\n" + sep)

print("\n5. Среднее количество звонков в службу поддержки по Churn:")
grouped5 = df.groupby('Churn')['Customer service calls'].mean()
print(grouped5.to_string())
diff5 = grouped5[True] - grouped5[False]
relative_diff5 = diff5 / grouped5[False] * 100
print(f"Разница: {diff5:.4f} звонков ({relative_diff5:.2f}%).")
if abs(relative_diff5) < 5:
    print("Вывод: разница незначительная.")
elif abs(relative_diff5) < 15:
    print("Вывод: разница небольшая, но заметная.")
else:
    print("Вывод: разница существенная.")

print("\n" + sep)

print("\n6. Таблица сопряженности Customer service calls × Churn:" + "\n")
ct = pd.crosstab(df['Customer service calls'], df['Churn'])
print(ct.to_string())
overall_churn = (df['Churn'].astype(str).str.lower() == 'true').mean() * 100
print("\n" + f"Общий процент оттока: {overall_churn:.2f}%")
churn_percent = ct[True] / ct.sum(axis=1) * 100
print("\n" + "Процент оттока по количеству звонков:" + "\n")
print(churn_percent.round(2).to_string())
threshold = churn_percent[churn_percent > 40].index.min()
print("\n" + f"Отток становится существенно выше (>40%) начиная с {threshold} звонков.")

print("\n" + sep)

print("\n7. Таблица сопряженности International plan × Churn:")
ct_intl = pd.crosstab(df['International plan'], df['Churn'])
print(ct_intl.to_string())
intl_churn = ct_intl[True] / ct_intl.sum(axis=1) * 100
print("Процент оттока по International plan:")
print(intl_churn.round(2).to_string())
if intl_churn['Yes'] > intl_churn['No']:
    print(f"Отток среди использующих международный роуминг ({intl_churn['Yes']:.2f}%) существенно выше, чем среди не использующих ({intl_churn['No']:.2f}%).")
else:
    print(f"Отток среди использующих международный роуминг ({intl_churn['Yes']:.2f}%) ниже, чем среди не использующих ({intl_churn['No']:.2f}%).")

print("\n" + sep)

print("\n8. Прогнозируемый отток:")
df['Прогнозируемый отток'] = (df['International plan'] == 'Yes') | (df['Customer service calls'] >= threshold)
conf = pd.crosstab(df['Churn'], df['Прогнозируемый отток'])
print("Таблица сопряженности факт/прогноз:")
print(conf.to_string())
actual = df['Churn']
pred = df['Прогнозируемый отток']
TP = ((actual == True) & (pred == True)).sum()
TN = ((actual == False) & (pred == False)).sum()
FP = ((actual == False) & (pred == True)).sum()
FN = ((actual == True) & (pred == False)).sum()
total = len(df)
print(f"TP={TP}, TN={TN}, FP={FP}, FN={FN}, всего={total}")
print(f"Ложноположительные (ошибки первого рода): {FP/total*100:.2f}%")
print(f"Ложноотрицательные (ошибки второго рода): {FN/total*100:.2f}%")
print(f"FPR (доля FP среди активных): {FP/(FP+TN)*100:.2f}%")
print(f"FNR (доля FN среди потерянных): {FN/(FN+TP)*100:.2f}%")
