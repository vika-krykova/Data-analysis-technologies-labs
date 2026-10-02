import requests

mbox = requests.get('https://www.py4e.com/code3/mbox.txt').text
all_lines = mbox.split('\n')

email_counts = {}

for line in all_lines:
    if line.startswith('From '):
        parts = line.split()
        if len(parts) >= 2:
            email = parts[1]
            email_counts[email] = email_counts.get(email, 0) + 1

max_email = max(email_counts, key=email_counts.get)
max_count = email_counts[max_email]

print(f"Адрес: {max_email}")
print(f"Количество писем: {max_count}")
