from itertools import islice


def batched(iterable, n):
    if n < 1:
        raise ValueError('n must be at least one')
    iterator = iter(iterable)
    while batch := tuple(islice(iterator, n)):
        yield batch


def elegant_batches(s: str, n: int) -> list[str]:
    """Разделяет текст по словам, а потом собирает обратно, но делит на несколько частей, если текст больше `n`"""
    if n < 1:
        raise ValueError('n must be at least one')
    words = s.split(' ')
    parts = [[]]
    part_size = 0
    for w in words:
        part_size += len(w) + 1
        if part_size > n:
            parts[-1] = ' '.join(parts[-1])
            parts.append([])
            part_size = 0
        parts[-1].append(w)
    if isinstance(parts[-1], list):
        parts[-1] = parts[-1] = ' '.join(parts[-1])
    return parts

