import threading
import time


class TestThread(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self,name=name)

    def run(self):
        print(f'线程{self.name}正在进行!')
        n = 0
        while True:
            n += 1
            print(f'线程{self.name}>>>{n}')
            time.sleep(1)
        print(f'线程{self.name}结束运行')


t1 = TestThread('thread-1')
t2 = TestThread('thread-2')
t1.start()
t2.start()
