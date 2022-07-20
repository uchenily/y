class Queue(object):
    """实现queue.Queue的get, put接口, 并额外添加peek方法"""

    def __init__(self):
        self._elements = []

    def put(self, element):
        self._elements.append(element)

    def get(self):
        assert self._elements
        res = self._elements[0]
        del self._elements[0]
        return res

    def peek(self):
        assert self._elements
        return self._elements[0]

    def __len__(self):
        return len(self._elements)

    def __str__(self):
        res = ['Queue:']
        for idx, element in enumerate(self._elements):
            res.append('    %3d %s' % (idx, element))

        return '\n'.join(res)
