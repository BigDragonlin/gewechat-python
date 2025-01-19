import unittest
import queue

class TestQueue(unittest.TestCase):
    def setUp(self):
        # 初始化队列对象
        self.q = queue.Queue()

    def test_enqueue(self):
        # 测试入队操作
        self.q.put(1)
        self.q.put(2)
        # 打印队列
        print(self.q.queue)
        self.assertEqual(self.q.qsize(), 2, "队列大小应为2")

    def test_dequeue(self):
        # 测试出队操作
        self.q.put(1)
        self.q.put(2)
        self.assertEqual(self.q.get(), 1, "出队的第一个元素应为1")
        self.assertEqual(self.q.qsize(), 1, "队列大小应为1")

    def test_empty_queue(self):
        # 测试空队列的情况
        self.assertTrue(self.q.empty(), "队列应为空")
        self.q.put(1)
        self.assertFalse(self.q.empty(), "队列不应为空")

    def test_full_queue(self):
        # 测试满队列的情况（默认队列大小无限制，这里设置一个限制）
        self.q = queue.Queue(maxsize=2)
        self.q.put(1)
        self.q.put(2)
        self.assertTrue(self.q.full(), "队列应已满")
        with self.assertRaises(queue.Full):
            self.q.put(3, block=False)

    def test_queue_size(self):
        # 测试队列大小
        self.assertEqual(self.q.qsize(), 0, "初始队列大小应为0")
        self.q.put(1)
        self.q.put(2)
        self.assertEqual(self.q.qsize(), 2, "队列大小应为2")

    def test_enqueue_json(self):
        # 测试入队操作
        self.q.put({"key": "value"})
        self.q.put({"key1": "value1"})
        self.q.put({"key2": "value2"})
        print(self.q.queue)
        #打印单个json
        print(self.q.get())
        print(self.q.queue)