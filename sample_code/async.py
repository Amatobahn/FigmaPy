import FigmaPy.figmapy_async as figmapy_async
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

start = time.time()
images = figmaPy.get_file_images(file_key=file_key, ids=node_ids)
print(time.time() - start)
print(images.images)

start = time.time()
figmaPy = figmapy_async.AioHttpFigmaPy(token=auth_key)
loop = asyncio.get_event_loop()
result = loop.run_until_complete(figmaPy.get_file_images(file_key=file_key, ids=node_ids))
print(time.time() - start)
print(result.images)

figmapy_async.client.close()
# TODO fix this error RuntimeWarning: coroutine 'ClientSession.close' was never awaited
#   figma_session_async.client.close()