import queue

q = queue.Queue()
for i in range(20):
    q.put(i)

for i in range(20):
    if q.empty()==False:
        print(q.get_nowait())

print(q.get_nowait())
