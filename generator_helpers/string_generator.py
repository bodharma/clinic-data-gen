import string
import bisect
import itertools

import random

# from random import Random, randint, sample, random
from typing import Generator, Iterable, Optional, Sequence, TypeVar
from collections import OrderedDict

T = TypeVar("T")


def bothify(text="## ??", letters=string.ascii_letters):
    """Generate a string with each placeholder in ``text`` replaced according
    to the following rules:

    - Number signs ('#') are replaced with a random digit (0 to 9).
    - Question marks ('?') are replaced with a random character from ``letters``.

    By default, ``letters`` contains all ASCII letters, uppercase and lowercase.

    Under the hood, this method uses :meth:`numerify() <faker.providers.BaseProvider.numerify>` and
    and :meth:`lexify() <faker.providers.BaseProvider.lexify>` to generate random values for number
    signs and question marks respectively.

    :sample: letters='ABCDE'
    :sample: text='Product Number: ????-########'
    :sample: text='Product Number: ????-########', letters='ABCDE'
    """
    return lexify(numerify(text), letters=letters)


import re

_re_hash = re.compile(r"#")
_re_perc = re.compile(r"%")
_re_excl = re.compile(r"!")
_re_at = re.compile(r"@")
_re_qm = re.compile(r"\?")
_re_cir = re.compile(r"\^")


def lexify(text="????", letters=string.ascii_letters.upper):
    """Generate a string with each question mark ('?') in ``text``
    replaced with a random character from ``letters``.

    By default, ``letters`` contains all ASCII letters, uppercase and lowercase.

    :sample: text='Random Identifier: ??????????'
    :sample: text='Random Identifier: ??????????', letters='ABCDE'
    """
    return _re_qm.sub(lambda x: random_element(letters), text)


def numerify(text="###"):
    """Generate a string with each placeholder in ``text`` replaced according
    to the following rules:

    - Number signs ('#') are replaced with a random digit (0 to 9).
    - Percent signs ('%') are replaced with a random non-zero digit (1 to 9).
    - Exclamation marks ('!') are replaced with a random digit or an empty string.
    - At symbols ('@') are replaced with a random non-zero digit or an empty string.

    Under the hood, this method uses :meth:`random_digit() <faker.providers.BaseProvider.random_digit>`,
    :meth:`random_digit_not_null() <faker.providers.BaseProvider.random_digit_not_null>`,
    :meth:`random_digit_or_empty() <faker.providers.BaseProvider.random_digit_or_empty>`,
    and :meth:`random_digit_not_null_or_empty() <faker.providers.BaseProvider.random_digit_not_null_or_empty>`
    to generate the random values.

    :sample: text='Intel Core i%-%%##K vs AMD Ryzen % %%##X'
    :sample: text='!!! !!@ !@! !@@ @!! @!@ @@! @@@'
    """
    text = _re_hash.sub(lambda x: str(random_digit()), text)
    text = _re_perc.sub(lambda x: str(random_digit_not_null()), text)
    text = _re_excl.sub(lambda x: str(random_digit_or_empty()), text)
    text = _re_at.sub(lambda x: str(random_digit_not_null_or_empty()), text)
    return text


def random_digit():
    """Generate a random digit (0 to 9).

    :sample:
    """
    return random.randint(0, 9)


def random_digit_not_null():
    """Generate a random non-zero digit (1 to 9).

    :sample:
    """
    return random.randint(1, 9)


def random_digit_or_empty():
    """Generate a random digit (0 to 9) or an empty string.

    This method will return an empty string 50% of the time,
    and each digit has a 1/20 chance of being generated.

    :sample size=10:
    """
    if random.randint(0, 1):
        return random.randint(0, 9)
    else:
        return ""


def random_digit_not_null_or_empty():
    """Generate a random non-zero digit (1 to 9) or an empty string.

    This method will return an empty string 50% of the time,
    and each digit has a 1/18 chance of being generated.

    :sample size=10:
    """
    if random.randint(0, 1):
        return random.randint(1, 9)
    else:
        return ""


def random_element(elements=("a", "b", "c")):
    """Generate a randomly sampled object from ``elements``.

    For information on the ``elements`` argument, please refer to
    :meth:`random_elements() <faker.providers.BaseProvider.random_elements>` which
    is used under the hood with the ``unique`` argument set to ``False`` and the
    ``length`` argument set to ``1``.

    :sample: elements=('a', 'b', 'c', 'd')
    :sample size=10: elements=OrderedDict([
                 ("a", 0.45),
                 ("b", 0.35),
                 ("c", 0.15),
                 ("d", 0.05),
             ])
    """

    return random_elements(elements, length=1)[0]


def random_elements(
    elements=("a", "b", "c"), length=None, unique=False, use_weighting=None
):
    """Generate a list of randomly sampled objects from ``elements``.

    Set ``unique`` to ``False`` for random sampling with replacement, and set ``unique`` to
    ``True`` for random sampling without replacement.

    If ``length`` is set to ``None`` or is omitted, ``length`` will be set to a random
    integer from 1 to the size of ``elements``.

    The value of ``length`` cannot be greater than the number of objects
    in ``elements`` if ``unique`` is set to ``True``.

    The value of ``elements`` can be any sequence type (``list``, ``tuple``, ``set``,
    ``string``, etc) or an ``OrderedDict`` type. If it is the latter, the keys will be
    used as the objects for sampling, and the values will be used as weighted probabilities
    if ``unique`` is set to ``False``. For example:

    .. code-block:: python

        # Random sampling with replacement
        fake.random_elements(
            elements=OrderedDict([
                ("variable_1", 0.5),        # Generates "variable_1" 50% of the time
                ("variable_2", 0.2),        # Generates "variable_2" 20% of the time
                ("variable_3", 0.2),        # Generates "variable_3" 20% of the time
                ("variable_4": 0.1),        # Generates "variable_4" 10% of the time
            ]), unique=False
        )

        # Random sampling without replacement (defaults to uniform distribution)
        fake.random_elements(
            elements=OrderedDict([
                ("variable_1", 0.5),
                ("variable_2", 0.2),
                ("variable_3", 0.2),
                ("variable_4": 0.1),
            ]), unique=True
        )

    :sample: elements=('a', 'b', 'c', 'd'), unique=False
    :sample: elements=('a', 'b', 'c', 'd'), unique=True
    :sample: elements=('a', 'b', 'c', 'd'), length=10, unique=False
    :sample: elements=('a', 'b', 'c', 'd'), length=4, unique=True
    :sample: elements=OrderedDict([
                    ("a", 0.45),
                    ("b", 0.35),
                   ("c", 0.15),
                   ("d", 0.05),
               ]), length=20, unique=False
    :sample: elements=OrderedDict([
                   ("a", 0.45),
                   ("b", 0.35),
                   ("c", 0.15),
                   ("d", 0.05),
               ]), unique=True
    """
    use_weighting = use_weighting if use_weighting is not None else False

    if isinstance(elements, dict) and not isinstance(elements, OrderedDict):
        raise ValueError(
            "Use OrderedDict only to avoid dependency on PYTHONHASHSEED (See #363)."
        )

    fn = choices_distribution_unique if unique else choices_distribution

    if length is None:
        length = random.randint(1, len(elements))

    if unique and length > len(elements):
        raise ValueError(
            "Sample length cannot be longer than the number of unique elements to pick from."
        )

    if isinstance(elements, dict):
        if not hasattr(elements, "_key_cache"):
            elements._key_cache = tuple(elements.keys())

        choices = elements._key_cache
        probabilities = tuple(elements.values()) if use_weighting else None
    else:
        if unique:
            # shortcut
            return random.sample(elements, length)
        choices = elements
        probabilities = None

    return fn(tuple(choices), probabilities, random, length=length)


def choices_distribution_unique(
    a: Sequence[T],
    p: Sequence[float],
    random: Optional[random.Random] = None,
    length: int = 1,
) -> Sequence[T]:
    # As of Python 3.7, there isn't a way to sample unique elements that takes
    # weight into account.
    # if random is None:
    #     random = random

    assert len(a) == len(p)
    assert (
        len(a) >= length
    ), "You can't request more unique samples than elements in the dataset."

    choices = []
    items = list(a)
    probabilities = list(p)
    for i in range(length):
        cdf = tuple(cumsum(probabilities))
        normal = cdf[-1]
        cdf2 = [i / normal for i in cdf]
        uniform_sample = random_sample(random=random)
        idx = bisect.bisect_right(cdf2, uniform_sample)
        item = items[idx]
        choices.append(item)
        probabilities.pop(idx)
        items.pop(idx)
    return choices


def choices_distribution(
    a: Sequence[T],
    p: Sequence[float],
    random: Optional[random.Random] = None,
    length: int = 1,
) -> Sequence[T]:
    # if random is None:
    #     random = random.Random

    if p is not None:
        assert len(a) == len(p)

    if hasattr(random, "choices"):
        if length == 1 and p is None:
            return (random.choice(a),)
        else:
            return random.choices(a, weights=p, k=length)
    else:
        choices = []

        if p is None:
            p = itertools.repeat(1, len(a))

        cdf = list(cumsum(p))
        normal = cdf[-1]
        cdf2 = [i / normal for i in cdf]
        for _ in range(length):
            uniform_sample = random_sample(random=random)
            idx = bisect.bisect_right(cdf2, uniform_sample)
            item = a[idx]
            choices.append(item)
        return choices


def random_sample(random: Optional[random.Random] = None) -> float:
    # if random is None:
    #     random = Random()
    return random.uniform(0.0, 1.0)


def cumsum(it: Iterable[float]) -> Generator[float, None, None]:
    total: float = 0
    for x in it:
        total += x
        yield total


if __name__ == "__main__":
    print(bothify(text="#####-#####"))
