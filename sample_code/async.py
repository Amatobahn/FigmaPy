import FigmaPy
import asyncio
import time

file_key = 'REDACTED'
auth_key = 'REDACTED'

# TODO create a better sample, this actually results in the same times
#  and the async version sometimes crashes randomly with a no key find in dict error

figmaPy = FigmaPy.FigmaPy(token=auth_key)
file = figmaPy.get_file(file_key)
page1 = file.document.children[0]
nodes = page1.get_children_recursively()
node_ids = [node.id for node in nodes]


def sync_request(index):
    tic = time.time()
    images = figmaPy.get_file_images(file_key=file_key, ids=node_ids)
    toc = time.time()
    time_spent = toc - tic
    print(f"Sync time {index}: {time_spent}s")
    return time_spent


def sync_main(n):
    tic = time.time()
    for i in range(n):
        sync_request(i)
    toc = time.time()
    total_time = toc - tic
    print(f"Sync Total time taken : {total_time}s")


async def async_request(index):
    tic = time.time()
    figmaPy = FigmaPy.AioHttpFigmaPy(token=auth_key)
    result = await figmaPy.get_file_images(file_key=file_key, ids=node_ids)
    toc = time.time()
    time_spent = toc - tic
    print(f"Async time {index}: {time_spent}s")
    await figmaPy.client.close()
    return time_spent


async def async_main(n):
    tic = time.time()
    tasks = await asyncio.gather(*[async_request(i) for i in range(n)])
    toc = time.time()
    total_time = toc - tic
    print(f"Async Total time taken : {total_time}s")


# Uncomment for Windows
# asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
sync_main(5)
asyncio.run(async_main(5))

# Sync time 0: 2.156123638153076s
# Sync time 1: 1.790233850479126s
# Sync time 2: 0.8593003749847412s
# Sync time 3: 0.8280830383300781s
# Sync time 4: 3.3903250694274902s
# Sync Total time taken : 9.024065971374512s
# Async time 2: 1.1118452548980713s
# Async time 0: 1.252396821975708s
# Async time 1: 1.3930182456970215s
# Async time 3: 2.2680156230926514s
# Async time 4: 3.1117067337036133s
# Async Total time taken : 3.142949104309082s
