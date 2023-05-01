from typing import Optional


class QueryObject:
    def __init__(self, query: Optional[str] = None, num: Optional[int] = 5):
        self._query = query
        self._num = num

    def get_query(self):
        return self._query

    def get_num(self):
        return self._num
