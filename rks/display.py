from prettytable import PrettyTable
from .analysis import format_memory_size

def analyze_redis_keys(min_heap, prefix_statistics_map, total_key_size, total_key_count, key_count_by_type, db_num, use_pretty):

    average_key_size = total_key_size / total_key_count if total_key_count != 0 else 0

    print("\n" + "-"*25 + f"\nAnalyzing DB {db_num}\n" + "-"*25 + "\n")

    table = PrettyTable()
    table.title = "Top 20 largest keys in Redis"
    table.field_names = ["Key", "Type", "Size", "Size Ratio", "TTL"]

    sorted_items = sorted(min_heap, key=lambda x: x[0], reverse=True)

    for value, item in sorted_items:
        key = item[0]
        key_type = item[1]
        memory = int(item[2])
        ttl = item[3]

        size_increase_percentage = (memory - average_key_size) / average_key_size * 100
        formatted_size_ratio = "{:.1f}% ↑".format(size_increase_percentage)

        if use_pretty:
            memory = format_memory_size(memory)

        table.add_row([key.decode('utf-8', errors='ignore'), key_type.decode('utf-8'), memory, formatted_size_ratio, ttl])

    print(table)

    table = PrettyTable()
    table.title = "Key Count by Type"
    table.field_names = ["Type", "Count"]

    for key_type, count in key_count_by_type.items():
        table.add_row([key_type.decode('utf-8', errors='ignore'), count])

    print(table)

    table = PrettyTable()
    table.title = "Detailed Prefix Statistics"
    table.field_names = ["Prefix Name", "Count", "Average Size", "Max TTL", "Types"]

    for prefix, item in prefix_statistics_map.items():

        prefix_average_size = round(item['total_size'] / item['count'], 2) if item['count'] != 0 else 0

        if use_pretty:
            prefix_average_size = format_memory_size(prefix_average_size)

        types = ""
        for key_type, type_count in item['type_count'].items():
            types += " - Type: {}, Count: {}\n".format(key_type.decode('utf-8'), type_count)
        table.add_row([prefix.decode('utf-8', errors='ignore'), item['count'], prefix_average_size, item['max_ttl'], types])

    print(table)