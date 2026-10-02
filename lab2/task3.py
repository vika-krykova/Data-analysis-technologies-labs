import sys
import re
from decimal import Decimal, ROUND_HALF_UP


def parse_line(line):
    line = line.strip()
    if not line:
        return None

    date_match = re.match(r'^(\d{1,2})[./](\d{1,2})[./](\d{4})', line)
    if not date_match:
        return None

    day, month, year = (int(date_match.group(i)) for i in (1, 2, 3))
    if not (1 <= day <= 31 and 1 <= month <= 12):
        return None

    rest = line[date_match.end():]

    cost_match = re.search(r'(\d+[.,]\d{1,2})\s*$', rest)
    if not cost_match:
        cost_match = re.search(r'(\d+)\s*$', rest)
    if not cost_match:
        return None

    cost_str = cost_match.group(1)
    name_part = rest[:cost_match.start()]

    name_part = name_part.strip(' \t,;')
    if len(name_part) >= 2 and name_part[0] == '"' and name_part[-1] == '"':
        name_part = name_part[1:-1].strip()

    if not name_part:
        return None

    cost_str = cost_str.replace(',', '.')
    if not re.match(r'^\d+(?:\.\d{1,2})?$', cost_str):
        return None

    return (day, month, year, name_part, Decimal(cost_str))


def main():
    orders = []
    for line in sys.stdin.read().splitlines():
        parsed = parse_line(line)
        if parsed is not None:
            orders.append(parsed)

    if not orders:
        return

    pizza_counts = {}
    for _, _, _, name, _ in orders:
        pizza_counts[name] = pizza_counts.get(name, 0) + 1
    pizzas_sorted = sorted(pizza_counts.items(), key=lambda pair: -pair[1])

    daily_totals = {}
    for d, mo, y, _, cost in orders:
        key = (y, mo, d)
        daily_totals[key] = daily_totals.get(key, Decimal(0)) + cost
    dates_sorted = sorted(daily_totals.items())

    most_expensive = max(orders, key=lambda o: o[4])

    total = sum((o[4] for o in orders), Decimal(0))
    average = (total / len(orders)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    print("а)")
    for name, cnt in pizzas_sorted:
        print(f"{name} - {cnt}")

    print("б)")
    for (y, mo, d), s in dates_sorted:
        print(f"{d:02d}.{mo:02d}.{y} {s}")

    print("в)")
    d, mo, y, name, cost = most_expensive
    print(f"{d:02d}.{mo:02d}.{y} {name} {cost}")

    print("г)")
    print(average)


if __name__ == "__main__":
    main()
