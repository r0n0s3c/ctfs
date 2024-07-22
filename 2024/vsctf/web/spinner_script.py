import asyncio
import websockets
import json
import math


async def recv_sock(websocket):
    response = await websocket.recv()
    data = json.loads(response)
    print(f"Received: {data}")

    if 'spins' in data:
        print(f"Spins: {data['spins']}")
    if 'message' in data:
        print(f"Message: {data['message']}")

async def send_circle_points(websocket, centerX, centerY, radius, num_points):
    
    for i in range(num_points):
        theta = 2 * math.pi * i / num_points
        x = centerX + radius * math.cos(theta)
        y = centerY + radius * math.sin(theta)
        point = {'x': x, 'y': y, 'centerX': centerX, 'centerY': centerY}
        message = json.dumps(point)
        await websocket.send(message)
        print(f"Sent: {message}: i {i}")
        if i != 0:
            await recv_sock(websocket)


async def send_touch_points(websocket):
    for i in range(10):
        await send_circle_points(websocket, 50, 50, 5, 4)
    


async def main():
    uri = "wss://spinner.vsc.tf/ws"  # Change to the actual server URI if different

    async with websockets.connect(uri) as websocket:
        await send_touch_points(websocket)

if __name__ == "__main__":
    asyncio.run(main())