from sanic_sse import Sse
from sanic_sse.pub_sub import _StopMessage
sse = Sse()


def close_channel(channel_id: str) -> None:
    sse._pubsub.publish(data=_StopMessage(), channel_id=channel_id)
