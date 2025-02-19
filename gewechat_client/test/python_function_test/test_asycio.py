import asyncio
import unittest
import time

async def my_coroutine():
    async def sleep():
        await asyncio.sleep(1)
    tasks = [my_coroutine() for _ in range(10)]
    await asyncio.gather(*tasks)



class TestAsyncioMainEntry(unittest.TestCase):
    def test_coroutine(self):
        print("now time is:", time.time())
        asyncio.run(my_coroutine())
        print("now time is:", time.time())
    
if __name__ == '__main__':
    unittest.main()