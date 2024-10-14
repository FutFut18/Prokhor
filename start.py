import asyncio

async def run_script(script_name):
    process = None
    try:
        process = await asyncio.create_subprocess_exec("python", script_name)
    except:
        process = await asyncio.create_subprocess_exec("python3", script_name)
    return process

async def main():
    processes = await asyncio.gather(
        run_script("main.py"),
        run_script("discordbot.py")
    )
    for process in processes:
        await process.wait()
    for process in processes:
        process.terminate()
asyncio.run(main())
