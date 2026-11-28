# Homework 7

- [Makeheap](makeheap/README.md) — два способа построения minheap и [доказательство O(n)](makeheap/proof.md).
- [K-th minheap](k_th/README.md) — поиск k-го по величине элемента.
- [Heapsort](heapsort/README.md) — сортировка кучей inplace.

Из корня репозитория:

```bash
python -m pytest -q homework_7
python -m homework_7.benchmark
```

Замеры: Python 3.13.5, Linux, AMD EPYC 9V74, медиана 5 запусков. Перед каждым замером создавалась копия одного и того же входного массива (копирование вне замера). Использовал merge_sort из homework_6 без изменений. Все 57 тестов прошли.
