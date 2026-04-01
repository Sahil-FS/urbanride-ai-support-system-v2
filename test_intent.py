import asyncio
import httpx

async def test():
    async with httpx.AsyncClient() as client:
        tests = [
            {'message': 'cancel my ride'},
            {'message': 'my driver is misbehaving'},
            {'message': 'I was charged twice'},
        ]
        print('\nTesting local intent model:\n')
        for test_input in tests:
            resp = await client.post('http://localhost:8000/api/v1/chat', json=test_input, timeout=10)
            data = resp.json()
            print(f"  '{test_input['message']}' -> {data['intent']} ({data['confidence']:.2%})")
        print()

asyncio.run(test())
