import argparse
import redis
import rediscluster
from datetime import datetime
from .redis_utils import get_redis_keys, get_redis_cluster_keys

def main():
    parser = argparse.ArgumentParser(description='Analyze Redis Instance Key Statistics.')
    parser.add_argument('--host', required=True, help='Redis host')
    parser.add_argument('--port', required=True, help='Redis port')
    parser.add_argument('--password', default=None, help='Redis password')
    parser.add_argument('--cluster', action='store_true', help='Enable cluster mode')
    parser.add_argument('--batch_size', type=int, default=1000, help='Batch size for SCAN command')
    parser.add_argument('--replica_only', action='store_true', help='Execute only on replica instances')
    parser.add_argument('--pretty_format', action='store_true', help='Display output in a human-readable format')

    args = parser.parse_args()
    CONNECTION_TIMEOUT = 10

    if args.cluster:
        try:
            rc = rediscluster.RedisCluster(startup_nodes=[{"host": args.host, "port": int(args.port)}],
                                           skip_full_coverage_check=True,
                                           password=args.password,
                                           socket_timeout=CONNECTION_TIMEOUT)

            redis_info = rc.info()

            if list(redis_info.values())[0].get('cluster_enabled') != 1:
                print("Error: Specified Redis instance is not running in cluster mode but --cluster flag was provided.")
                return

            process_start_time = datetime.now()

            if get_redis_cluster_keys(rc, args.batch_size, args.replica_only, args.pretty_format) == -1:
                print(f"Aborted the operation on non-readonly redis at host: {args.host}")
                return

            rc.close()

            process_end_time = datetime.now()
            process_taken_time = str(process_end_time - process_start_time).split(".")[0]
            print(f'Process completed in {process_taken_time} (HH:MM:SS)')

        except rediscluster.exceptions.RedisClusterError as e:
            print(f"Error connecting to Redis cluster: {args.host}. Error message: {str(e)}")
            return
        except rediscluster.exceptions.RedisClusterException as e:
            if "ERROR sending 'cluster slots' command to redis server" in str(e):
                print("Error: Specified Redis instance is not running in cluster mode but --cluster flag was provided.")
                return
            else:
                print(f"Failed to connect to Redis cluster: {args.host}. Error message: {str(e)}")
                return
    else:
        try:
            r = redis.Redis(host=args.host, port=int(args.port),
                            password=args.password,
                            socket_timeout=CONNECTION_TIMEOUT)

            redis_info = r.info()

            if redis_info.get('cluster_enabled') != 0:
                print("Error: Specified Redis instance is running in cluster mode but --cluster flag was not provided.")
                return

            if redis_info.get('role') != 'slave' and args.replica_only:
                print(f"Aborted the operation on non-readonly redis at host: {args.host}")
                return

            process_start_time = datetime.now()

            for db in redis_info.keys():
                if db.startswith('db'):
                    db_num = int(db[2:])
                    get_redis_keys(r, args.batch_size, db_num, args.pretty_format)

            r.close()

            process_end_time = datetime.now()
            process_taken_time = str(process_end_time - process_start_time).split(".")[0]
            print(f'Process completed in {process_taken_time} (HH:MM:SS)')

        except redis.exceptions.TimeoutError as e:
            print(f"Timeout connecting to Redis: {args.host}. Error message: {str(e)}")
        except redis.exceptions.ConnectionError as e:
            print(f"Failed to connect to Redis: {args.host}. Error message: {str(e)}")


if __name__ == "__main__":
    main()