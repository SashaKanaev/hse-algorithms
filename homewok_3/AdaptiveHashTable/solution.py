class AdaptiveHashTable:
    MAX_LOAD_FACTOR = 0.75
    MAX_CHAIN_LENGTH = 4

    def __init__(self, capacity=8):
        if capacity <= 0:
            raise ValueError("Capacity must be greater than zero")

        self.capacity = capacity
        self.size = 0
        self.table = [[] for _ in range(capacity)]

    def _get_index(self, key):
        return hash(key) % self.capacity

    def insert(self, key, value):
        index = self._get_index(key)
        bucket = self.table[index]

        # Если ключ уже существует, просто обновляем значение
        for item in bucket:
            if item[0] == key:
                item[1] = value
                return

        # Иначе добавляем новую пару [key, value]
        bucket.append([key, value])
        self.size += 1

        load_factor = self.size / self.capacity

        # Увеличиваем таблицу либо при высокой заполненности,
        # либо при слишком длинной цепочке коллизий
        if (
            load_factor > self.MAX_LOAD_FACTOR
            or len(bucket) > self.MAX_CHAIN_LENGTH
        ):
            self._resize()

    def get(self, key):
        index = self._get_index(key)
        bucket = self.table[index]

        for i in range(len(bucket)):
            if bucket[i][0] == key:
                value = bucket[i][1]

                # Transpose heuristic:
                # найденный элемент двигается на одну позицию ближе к началу
                if i > 0:
                    bucket[i - 1], bucket[i] = bucket[i], bucket[i - 1]

                return value

        raise KeyError(key)

    def remove(self, key):
        index = self._get_index(key)
        bucket = self.table[index]

        for i in range(len(bucket)):
            if bucket[i][0] == key:
                value = bucket[i][1]

                bucket.pop(i)
                self.size -= 1

                return value

        raise KeyError(key)

    def _resize(self):
        old_table = self.table

        self.capacity *= 2
        self.table = [[] for _ in range(self.capacity)]

        # size не меняется, потому что новых элементов не появляется.
        # Мы только перераспределяем существующие элементы.
        for bucket in old_table:
            for item in bucket:
                key = item[0]
                value = item[1]

                index = self._get_index(key)
                self.table[index].append([key, value])

    def __len__(self):
        return self.size
