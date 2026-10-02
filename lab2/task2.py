import sys

def main():
    lines = sys.stdin.read().split('\n')

    participants = lines[0].split()
    n_purchases = int(lines[1])
    n_people = len(participants)

    spent = {name: 0 for name in participants}
    for i in range(n_purchases):
        payer, amount = lines[2 + i].split()
        spent[payer] += round(float(amount) * 100)

    total_spent = sum(spent.values())

    balance = {
        name: spent[name] * n_people - total_spent
        for name in participants
    }

    debtors = sorted(
        [[name, -bal] for name, bal in balance.items() if bal < 0],
        key=lambda pair: -pair[1]
    )
    creditors = sorted(
        [[name, bal] for name, bal in balance.items() if bal > 0],
        key=lambda pair: -pair[1]
    )

    transfers = []
    i = j = 0
    while i < len(debtors) and j < len(creditors):
        debtor_name, debt   = debtors[i]
        creditor_name, credit = creditors[j]

        amount = min(debt, credit)
        transfers.append((debtor_name, creditor_name, amount / n_people / 100))

        debtors[i][1] -= amount
        creditors[j][1] -= amount

        if debtors[i][1] == 0: i += 1
        if creditors[j][1] == 0: j += 1

    print(len(transfers))
    for from_name, to_name, amount in transfers:
        print(f"{from_name} {to_name} {amount:.2f}")


if __name__ == "__main__":
    main()
