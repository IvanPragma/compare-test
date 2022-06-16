from typing import Union


def deep_getattr(obj: any, attrs: Union[list[any], any], default=None) -> any:
    """Deep getattr.

    Usage:
    >>> obj = {'data': {'id': 6, 'name': 'Test obj'}}
    >>> deep_getattr(obj, ['data', 'id'])  # 6
    """
    
    if not isinstance(attrs, list):
        attrs = [attrs]

    cur_obj = obj
    for attr in attrs:
        if obj is None:
            return None

        obj_changed = False

        if isinstance(cur_obj, list):
            if isinstance(attr, int):
                try:
                    cur_obj = cur_obj[attr]
                    obj_changed = True
                except IndexError:
                    pass
        elif isinstance(cur_obj, dict):
            if attr in cur_obj:
                cur_obj = cur_obj[attr]
                obj_changed = True
        elif isinstance(attr, str):
            if hasattr(cur_obj, attr):
                cur_obj = getattr(cur_obj, attr)
                obj_changed = True

        if not obj_changed:
            cur_obj = None
    return cur_obj


def words_same(word_one: str, word_two: str) -> float:
    """Return float coefficient between 0.0 and 1.0 similarity of words."""

    if word_one == word_two:
        return 1.0

    word_one_len = len(word_one)
    word_two_len = len(word_two)
    i_one = 0
    i_two = 0
    started = False
    same_letters_count = 0
    while True:
        if i_one >= word_one_len or i_two >= word_two_len:
            break
        letter = word_one[i_one]
        if word_two[i_two] == letter:
            started = True
            same_letters_count += 1
        else:
            if not started:
                i_one -= 1
        i_one += 1
        i_two += 1

    return same_letters_count / word_two_len
