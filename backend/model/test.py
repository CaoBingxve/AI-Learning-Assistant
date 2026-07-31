import asyncio

async def test_async():
    await asyncio.sleep(1)
    return 'AI回复内容'

res=asyncio.run(test_async())
print(res)