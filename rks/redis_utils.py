import redis
import time
from .display import analyze_redis_keys
from .analysis import update_topk_heap, update_statistics


def get_redis_keys(r, batch_size, db_num, use_pretty):

    r.execute_command('SELECT', db_num)

    min_heap = []
    heap_size = 20
    prefix_statistics_map = {}

    total_key_count = 0
    total_key_size = 0
    key_count_by_type = {}

    script = """
            local cursor = ARGV[1]
            local result = {}

            local scanResult = redis.call('SCAN', cursor, 'COUNT', BATCH_SIZE_PLACEHOLDER)
            cursor = scanResult[1]

            for i, key in ipairs(scanResult[2]) do
                local key_type = redis.call('TYPE', key)['ok']
                local memory = redis.call('MEMORY', 'USAGE', key)
                local ttl = redis.call('TTL', key)

                table.insert(result, {key, key_type, memory, ttl})
            end

            return {cursor, result}
        """

    script = script.replace("BATCH_SIZE_PLACEHOLDER", str(batch_size))

    cursor = b'0'
    while True:
        cursor, result = r.eval(script, 0, cursor)

        for item in result:
            key_type = item[1]
            memory = int(item[2])

            total_key_count += 1
            total_key_size += memory

            if key_type not in key_count_by_type:
                key_count_by_type[key_type] = 0
            key_count_by_type[key_type] += 1

            update_topk_heap(item, min_heap, heap_size)
            update_statistics(item, prefix_statistics_map)

        if cursor == b'0':
            break

        time.sleep(0.01)

    return analyze_redis_keys(min_heap, prefix_statistics_map, total_key_size, total_key_count, key_count_by_type, db_num, use_pretty)


def get_redis_cluster_keys(rc, batch_size, replica_only, use_pretty):
    slave_flag = False

    min_heap = []
    heap_size = 20
    prefix_statistics_map = {}

    total_key_count = 0
    total_key_size = 0
    key_count_by_type = {}

    nodes = rc.cluster_nodes()

    masters = []
    for node in nodes:
        if 'master' in node['flags']:
            master_dict = {'master': node['id'], 'slots': node['slots'], 'slaves': []}
            masters.append(master_dict.copy())

    for node in nodes:
        if 'slave' in node['flags']:
            slave_flag = True
            for master in masters:
                if master['master'] == node['master']:
                    master['slaves'].append(node['id'])

    if slave_flag is False and replica_only:
        return -1

    for master in masters:
        if slave_flag is False:
            node = next((node for node in nodes if node['id'] == master['master']), None)
        else:
            node = next((node for node in nodes if node['id'] == master['slaves'][0]), None)
        r = redis.Redis(host=node['host'], port=node['port'])
        r.execute_command('READONLY')

        script = """
                    local cursor = ARGV[1]
                    local result = {}

                    local scanResult = redis.call('SCAN', cursor, 'COUNT', BATCH_SIZE_PLACEHOLDER)
                    cursor = scanResult[1]

                    for i, key in ipairs(scanResult[2]) do
                        local key_type = redis.call('TYPE', key)['ok']
                        local memory = redis.call('MEMORY', 'USAGE', key)
                        local ttl = redis.call('TTL', key)

                        table.insert(result, {key, key_type, memory, ttl})
                    end

                    return {cursor, result}
                    """

        script = script.replace("BATCH_SIZE_PLACEHOLDER", str(batch_size))

        cursor = b'0'
        while True:
            cursor, result = r.eval(script, 0, cursor)

            for item in result:
                key_type = item[1]
                memory = int(item[2])

                total_key_count += 1
                total_key_size += memory

                if key_type not in key_count_by_type:
                    key_count_by_type[key_type] = 0
                key_count_by_type[key_type] += 1

                update_topk_heap(item, min_heap, heap_size)
                update_statistics(item, prefix_statistics_map)

            if cursor == b'0':
                break

            time.sleep(0.01)

        r.close()

    return analyze_redis_keys(min_heap, prefix_statistics_map, total_key_size, total_key_count, key_count_by_type, 0, use_pretty)