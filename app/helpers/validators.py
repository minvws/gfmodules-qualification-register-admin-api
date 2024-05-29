from typing import TypeVar, List

T = TypeVar("T")


def validated_sets_equal(list_1: List[T], list_2: List[T]) -> bool:
    return set(list_1) == set(list_2)


def validate_list_for_removal(data: List[T]) -> bool:
    """
    used to validate entities that should exist within root
    """
    return len(data) > 1
