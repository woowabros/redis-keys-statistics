# Redis Keys Statistics

## Overview
`redis-keys-statistics` is a Python tool, designed for analyzing and reporting key usage statistics in Redis databases with exceptional speed and efficiency. By leveraging Lua scripting to reduce network I/O, it dramatically outperforms other open-source tools — tasks that typically take hours are completed in just minutes.

## Features
- **High Performance**: Utilizes Lua scripting to minimize network I/O, delivering results significantly faster than traditional methods. Where some tools might take hours, `redis-keys-statistics` can complete the same task in a fraction of the time.
- **Efficient Key Scanning**: Uses the Redis `SCAN` command for batch scanning of keys, further optimizing performance.
- **Memory Usage Statistics**: Reports memory usage for keys in various units (B, KB, MB, GB).
- **Top N Largest Keys**: Quickly identifies the largest keys for memory optimization.
- **Key Count by Type**: Provides a breakdown of keys by type for better data structure insights.
- **Prefix-Based Analysis**: Analyzes keys based on prefixes to understand namespace usage.
- **Cluster Support**: Compatible with Redis clusters, including replica-only analysis.
- **Readable Output**: Formatted and easy-to-read statistical tables using `prettytable`.

## Installation
```bash
pip install rks
```

## Usage
Execute the script with the necessary Redis connection parameters:
```bash
rks --host <REDIS_HOST> --port <REDIS_PORT> [--password <REDIS_PASSWORD>]
```
For detailed usage options:
```bash
rks --help
```

## Command Line Interface
```
usage: rks [-h] --host HOST --port PORT [--password PASSWORD] [--cluster] [--batch_size BATCH_SIZE] [--replica_only] [--pretty_format]

Analyze Redis Instance Key Statistics.

optional arguments:
  -h, --help            show this help message and exit
  --host HOST           Redis host
  --port PORT           Redis port
  --password PASSWORD   Redis password
  --ssl                 Enable SSL connection
  --cluster             Enable cluster mode
  --batch_size BATCH_SIZE
                        Batch size for SCAN command
  --replica_only        Execute only on replica instances
  --pretty_format       Display output in a human-readable format
```

## Example Output
Here is an example of what the output from `redis-keys-statistics` might look like:

### Top 20 Largest Keys in Redis
```
+-------------------+------+---------+------------+-------+
| Key               | Type | Size    | Size Ratio |  TTL  |
+-------------------+------+---------+------------+-------+
| user_sessions:123 | hash | 1.2 MB  | 150% ↑     |  360  |
| cache:page:001    | zset | 900 KB  | 120% ↑     |  -1   |
| config:app        | hash | 800 KB  | 100% ↑     | 86400 |
| queue:jobs        | list | 600 KB  | 80% ↑      |  -1   |
| temp:data:456     | set  | 500 KB  | 60% ↑      | 1800  |
| ...               | ...  | ...     | ...        |  ...  |
+-------------------+------+---------+------------+-------+

```

### Key Count by Type
```
+--------+-------+
|  Type  | Count |
+--------+-------+
| hash   | 250   |
| zset   | 150   |
| list   | 100   |
| set    | 75    |
| string | 200   |
+--------+-------+

```

### Detailed Prefix Statistics
```
+-------------+-------+--------------+---------+-----------------+
| Prefix Name | Count | Average Size | Max TTL | Types           |
+-------------+-------+--------------+---------+-----------------+
| user        | 100   | 200 KB       | 3600    | - Type: hash    |
|             |       |              |         |   Count: 50     |
|             |       |              |         | - Type: string  |
|             |       |              |         |   Count: 50     |
| cache       | 80    | 150 KB       | -1      | - Type: zset    |
|             |       |              |         |   Count: 80     |
| config      | 20    | 100 KB       | 86400   | - Type: hash    |
|             |       |              |         |   Count: 20     |
| temp        | 150   | 50 KB        | 1800    | - Type: set     |
|             |       |              |         |   Count: 100    |
|             |       |              |         | - Type: list    |
|             |       |              |         |   Count: 50     |
+-------------+-------+--------------+---------+-----------------+

```

## Requirements
- Python 3.x
- Redis server or cluster

## Contributing
Contributions are welcome. 

## Acknowledgements
Special thanks to all contributors and users of the `redis-keys-statistics` tool.

## License
This tool is licensed under the MIT License. See the [LICENSE](https://github.com/woowabros/redis-keys-statistics/blob/main/LICENSE.md) file for details.
