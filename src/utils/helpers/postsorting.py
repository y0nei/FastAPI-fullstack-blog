from datetime import datetime
from src.schemas.sorting import SortChoices, OrderChoices

def sortPosts(arr: list, key: str | None = None, order=OrderChoices.ascending) -> list:
    if key is None:
        key = SortChoices.id
    elif not isinstance(key, SortChoices):
        raise ValueError(f"Invalid sort key '{key}', expected one of {list(SortChoices)}")

    reverse = order == OrderChoices.descending
    if key == SortChoices.date:
        sorted_arr = sorted(arr, key=lambda x: datetime.strptime(x[key][0], "%d-%m-%Y"), reverse=reverse)
    else:
        sorted_arr = sorted(arr, key=lambda x: x[key], reverse=reverse)

    return sorted_arr
