import asyncio
import websockets
import subprocess


async def time(websocket, path):
    args = await websocket.recv()
    args = args.split(" ")
    with subprocess.Popen(["./ytdl", args[0], args[1]],
                          stdout=subprocess.PIPE,
                          bufsize=1,
                          universal_newlines=True) as process:
                          for line in process.stdout:
                            line = line.rstrip()
                            print(f"line = {line}")
                            await websocket.send(line)

start_server = websockets.serve(time, "127.0.0.1", 5678)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
