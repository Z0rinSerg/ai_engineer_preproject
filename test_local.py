import asyncio
from fastmcp import Client
from scripts.mcp_server import mcp

async def test_tool():
    # Используем встроенный клиент для прямого вызова
    async with Client(mcp) as client:
        result = await client.call_tool("hello", {"name": "Сергей"})
        print(result)

if __name__ == "__main__":
    asyncio.run(test_tool())