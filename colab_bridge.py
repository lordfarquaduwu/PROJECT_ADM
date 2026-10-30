import asyncio
import json
from datetime import timedelta

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    params = StdioServerParameters(
        command="C:/ADM_Project/.tools/uv/bin/uvx.exe",
        args=["--python", "C:/ADM_Project/.tools/python/cpython-3.13.17-windows-x86_64-none/python.exe", "git+https://github.com/googlecolab/colab-mcp"],
    )
    async with stdio_client(params) as streams:
        async with ClientSession(*streams, read_timeout_seconds=timedelta(seconds=60)) as session:
            await session.initialize()
            print((await session.list_tools()).model_dump_json(), flush=True)
            while True:
                try:
                    line = await asyncio.to_thread(input)
                except EOFError:
                    break
                if not line.strip():
                    continue
                request = json.loads(line)
                if request.get("action") == "exit":
                    break
                try:
                    if request.get("action") == "list":
                        result = await session.list_tools()
                    else:
                        result = await session.call_tool(request["name"], request.get("arguments", {}))
                    print(result.model_dump_json(), flush=True)
                except Exception as error:
                    print(json.dumps({"error": str(error)}), flush=True)


asyncio.run(main())
