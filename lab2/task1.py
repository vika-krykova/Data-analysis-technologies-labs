import sys

def median(sorted_values):
    count = len(sorted_values)
    if count % 2 == 1:
        return sorted_values[count // 2]
    else:
        return (sorted_values[count // 2 - 1] + sorted_values[count // 2]) / 2


def main():
    data = sys.stdin.read().split()
    total_records = int(data[0])
    attendance = sorted(map(int, data[1:1 + total_records]))

    if total_records % 2 == 1:
        middle_index = total_records // 2
        lower_half = attendance[:middle_index]
        upper_half = attendance[middle_index + 1:]
    else:
        half = total_records // 2
        lower_half = attendance[:half]
        upper_half = attendance[half:]

    first_quartile  = median(lower_half)
    third_quartile  = median(upper_half)
    interquartile_range = third_quartile - first_quartile

    lower_bound = first_quartile - 1.5 * interquartile_range
    upper_bound = third_quartile + 1.5 * interquartile_range

    outliers_count = sum(
        1 for value in attendance
        if value < lower_bound or value > upper_bound
    )
    print(outliers_count)


if __name__ == "__main__":
    main()
