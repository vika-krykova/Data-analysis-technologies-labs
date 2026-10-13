import pandas as pd
import requests
from io import StringIO

url = "https://en.wikipedia.org/wiki/List_of_Formula_One_World_Drivers%27_Champions"
response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

tables = pd.read_html(StringIO(response.text), flavor='html5lib')

df = None
for t in tables:
    flat = [c[1] if isinstance(c, tuple) else c for c in t.columns]
    if 'Season' in flat and 'Driver' in flat and 'Wins' in flat:
        df = t.copy()
        break

if df is None:
    raise RuntimeError("Таблица с чемпионами не найдена")

df.columns = [c[1] if isinstance(c, tuple) else c for c in df.columns]
df.columns = [str(c).split('[')[0].strip() for c in df.columns]

for col in ['Driver', 'Chassis', 'Engine', 'Tyres', 'Clinched']:
    if col in df.columns:
        df[col] = df[col].astype(str).str.replace(r'\[\d+\]', '', regex=True).str.strip()

df = df.dropna(subset=['Season', 'Driver'])
df = df[df['Season'].astype(str).str.match(r'^\d{4}')]

df['Season'] = df['Season'].astype(str).str.extract(r'(\d{4})').astype(int)
df = df[(df['Season'] >= 1950) & (df['Season'] <= 2025)]
df = df.drop_duplicates(subset=['Season']).sort_values('Season').reset_index(drop=True)

numeric_cols = ['Age', 'Poles', 'Wins', 'Podiums', 'Fastest laps', 'Points',
                '% Points', 'Margin', '% Margin', '# of rounds remaining']
for col in numeric_cols:
    if col in df.columns:
        df[col] = (df[col].astype(str)
                   .str.replace(r'\[\d+\]', '', regex=True)
                   .str.replace('%', '', regex=False)
                   .str.replace(',', '.', regex=False)
                   .str.strip())
        df[col] = pd.to_numeric(df[col], errors='coerce')

print("После очистки:")
print(df.head())
print(f"\nРазмер: {df.shape}")
print(f"Столбцы: {list(df.columns)}")
print("\nТипы данных:")
print(df.dtypes)

sep = "-" * 30

print("\n" + sep)
print("\n4.1. Возраст чемпионов:")
print(f"Средний возраст: {df['Age'].mean():.1f} лет")
print(f"Минимальный возраст: {df['Age'].min()} лет")
print(f"Максимальный возраст: {df['Age'].max()} лет")

youngest = df.loc[df['Age'].idxmin(), ['Season', 'Driver', 'Age']]
oldest = df.loc[df['Age'].idxmax(), ['Season', 'Driver', 'Age']]
print(f"Самый молодой: {youngest['Driver']} ({youngest['Season']}, {youngest['Age']} лет)")
print(f"Самый возрастной: {oldest['Driver']} ({oldest['Season']}, {oldest['Age']} лет)")

print("\n" + sep)
print("\n4.2. Титулы по конструкторам шасси:")
chassis_counts = df['Chassis'].value_counts()
print(chassis_counts.head(10))
top_chassis = chassis_counts.idxmax()
print(f"\nБольше всего титулов у конструктора: {top_chassis} ({chassis_counts.max()} титулов)")

print("\n" + sep)
print("\n4.3. Гонщики с наибольшим числом титулов:")
driver_titles = df['Driver'].value_counts()
print(driver_titles.head(10))
max_titles = driver_titles.max()
best_drivers = driver_titles[driver_titles == max_titles].index.tolist()
print(f"\nБольше всего титулов ({max_titles}) у: {', '.join(best_drivers)}")

print("\n" + sep)
print("\n4.4. Чемпионы с менее 30% побед в сезоне:")
df['Total_races'] = df['Clinched'].astype(str).str.extract(r'of\s+(\d+)').astype(float)
df['Win_percent'] = df['Wins'] / df['Total_races'] * 100

low_win_champions = df[df['Win_percent'] < 30][['Season', 'Driver', 'Wins', 'Total_races', 'Win_percent']]
print(low_win_champions.sort_values('Win_percent').to_string())

print("\n" + sep)
print("\n4.5. Максимальный перерыв между чемпионствами:")

driver_years = df.groupby('Driver')['Season'].apply(list).to_dict()
multi_champions = {d: years for d, years in driver_years.items() if len(years) >= 2}

max_gap = 0
max_gap_driver = None
max_gap_pair = None

for driver, years in multi_champions.items():
    years_sorted = sorted(years)
    for i in range(len(years_sorted) - 1):
        gap = years_sorted[i+1] - years_sorted[i]
        if gap > max_gap:
            max_gap = gap
            max_gap_driver = driver
            max_gap_pair = (years_sorted[i], years_sorted[i+1])

print(f"Максимальный перерыв: {max_gap} лет")
print(f"Гонщик: {max_gap_driver}")
print(f"Между чемпионствами: {max_gap_pair[0]} и {max_gap_pair[1]}")
