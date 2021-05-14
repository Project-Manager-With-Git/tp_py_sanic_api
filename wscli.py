import websocket
# wsapp = websocket.WebSocketApp("ws://localhost:5000/v1/ws/echo",
#                                on_open=lambda ws: ws.send("Hello"),
#                                on_message=lambda ws, message: print(f"get message {message}"))
# print("connect to ws://localhost:5000/v1/ws/echo")
# wsapp.run_forever()

ws = websocket.create_connection("ws://localhost:5000/v1/ws/echo")
ws.send("Hello")
message = ws.recv()
print(f"get message {message}")
ws.close()