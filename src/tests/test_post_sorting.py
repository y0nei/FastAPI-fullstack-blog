import pytest
from src.utils.helpers.postsorting import sortPosts
from src.schemas.sorting import SortChoices, OrderChoices

example_list = [
    {"id": 4, "date": ["21-03-2017"]},
    {"id": 2, "date": ["02-02-2023"]},
    {"id": 1, "date": ["27-12-2001"]},
    {"id": 3, "date": ["08-09-1990"]},
    {"id": 5, "date": ["10-02-2008"]}
]

def test_sort_by_id():
    """Checks post sorting by id key"""
    ascending = sortPosts(example_list, SortChoices.id)
    descending = sortPosts(example_list, SortChoices.id, OrderChoices.descending)
    assert ascending == [
        {"id": 1, "date": ["27-12-2001"]},
        {"id": 2, "date": ["02-02-2023"]},
        {"id": 3, "date": ["08-09-1990"]},
        {"id": 4, "date": ["21-03-2017"]},
        {"id": 5, "date": ["10-02-2008"]}
    ]
    assert descending == ascending[::-1]

def test_sort_by_date():
    """Checks post sorting by date key"""
    ascending = sortPosts(example_list, SortChoices.date)
    descending = sortPosts(example_list, SortChoices.date, OrderChoices.descending)
    assert ascending == [
        {"id": 3, "date": ["08-09-1990"]},
        {"id": 1, "date": ["27-12-2001"]},
        {"id": 5, "date": ["10-02-2008"]},
        {"id": 4, "date": ["21-03-2017"]},
        {"id": 2, "date": ["02-02-2023"]}
    ]
    assert descending == ascending[::-1]

def test_sort_invalid_key():
    """Checks if post sorting throws an error on invalid sort key"""
    with pytest.raises(ValueError):
        assert sortPosts(example_list, "foo")

def test_sort_key_is_None():
    """Checks if post sorting defaults to the id key when no key is specified"""
    result = sortPosts(example_list)
    assert result == sortPosts(example_list, SortChoices.id)
