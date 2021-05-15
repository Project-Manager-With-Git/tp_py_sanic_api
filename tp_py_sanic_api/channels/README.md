# 适用范围

需要监听订阅时使用.有两种:

1. 主动流,只要监听就可以收到的内容,这些内容往往来自于其上游的中间件比如kafka等
2. 触发流,需要触发(trigger)后才可以收到的内容

## 主动流

    只需要直接监听`/channels`或者`/channels?channel_id=<channel_id>`即可

## 触发流

    先执行触发接口获取channel_id,然后监听`/channels?channel_id=<channel_id>`即可.