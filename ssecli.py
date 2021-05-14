from sseclient import SSEClient
from requests import get

res = get("http://localhost:5000/v1/trigger/countdown/15")
channel_id = res.json().get("channel_id")
messages = SSEClient(f'http://localhost:5000/channels?channel_id={channel_id}')
for msg in messages:
    print(msg)
