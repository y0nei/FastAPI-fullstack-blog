from enum import Enum

class SortChoices(str, Enum):
    id = "id"
    date = "date"

class OrderChoices(str, Enum):
    ascending = "asc"
    descending = "desc"
