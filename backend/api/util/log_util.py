import re
import datetime
from typing import Dict, Union


async def parse_logs(**kwargs) -> Dict[int, Dict[str, Union[datetime.datetime, str]]]:
    """
    Parses log entries from 'file.log' and returns a List[Dict] representing each log entry.

    :returns: List[Dict], each dictionary contains the following keys:
        - 'timestamp' (datetime): The timestamp of the log entry.
        - 'level' (str): The formatted log level.
        - 'message' (str): The log message.
    :rtype: list[dict[str, Union[datetime.datetime, str]]]

    Example:
    ```
        Assuming 'file.log' contains log entries in the format '[timestamp: level] message':
        parse_logs()  # Returns [
            {
                'timestamp': datetime.datetime(2024, 4, 11, 11, 19, 27, 231000), 
                'level': 'ERROR/MainProcess', 
                'message': 'consumer: Cannot connect to amqp://guest:**@127.0.0.1:5672//'
            }
        ]
    ```
    """
    with open('dotaverse.log', 'r', encoding='utf-8') as file:
        logs = file.readlines()

    parsed_logs = {}
    index = 0
    limit, offset = int(kwargs.get('limit')), int(kwargs.get('offset'))

    for log in logs:
        match = re.match(r'\[(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}): (\S+)/(\S+)] (.*)', log)
        if match:
            timestamp_str, level_first_part, level_second_part, message = match.groups()
            level = f"{level_first_part}/{level_second_part}"
            created_at = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S,%f")
            log_entry = {
                'created_at': created_at,
                'level': level,
                'message': message.strip()
            }
            parsed_logs[index] = log_entry
            index += 1

    if offset > len(parsed_logs):
        return {}
    return dict(list(parsed_logs.items())[offset:limit])
