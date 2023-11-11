import heapq

def format_memory_size(size):
    if size < 1024:
        return f"{size: .2f} B"
    elif size < 1024 * 1024:
        return f"{size / 1024:.2f} KB"
    elif size < 1024 * 1024 * 1024:
        return f"{size / (1024 * 1024):.2f} MB"
    else:
        return f"{size / (1024 * 1024 * 1024):.2f} GB"


def update_topk_heap(item, min_heap, heap_size):
    heapq.heappush(min_heap, (item[2], item))
    if len(min_heap) > heap_size:
        heapq.heappop(min_heap)


def update_statistics(item, prefix_statistics_map):
    key = item[0]
    key_type = item[1]
    memory = int(item[2])
    ttl = item[3]

    if b':' in key:
        key_prefix = key.split(b':')[0]
        if key_prefix not in prefix_statistics_map:
            prefix_statistics_map[key_prefix] = {}
            prefix_statistics_map[key_prefix]['count'] = 0
            prefix_statistics_map[key_prefix]['total_size'] = 0
            prefix_statistics_map[key_prefix]['max_ttl'] = -1
            prefix_statistics_map[key_prefix]['type_count'] = {}
        prefix_statistics_map[key_prefix]['count'] += 1
        prefix_statistics_map[key_prefix]['total_size'] += memory
        prefix_statistics_map[key_prefix]['max_ttl'] = max(prefix_statistics_map[key_prefix]['max_ttl'], ttl)

        if key_type not in prefix_statistics_map[key_prefix]['type_count']:
            prefix_statistics_map[key_prefix]['type_count'][key_type] = 0
        prefix_statistics_map[key_prefix]['type_count'][key_type] += 1