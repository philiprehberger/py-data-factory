"""Lightweight test data generation with realistic fake values."""

from __future__ import annotations

import random
import string
import uuid as _uuid
from datetime import date, timedelta
from typing import Any, Callable

__all__ = ["fake", "Factory"]

_NAMES: list[str] = [
    "Alice Johnson",
    "Bob Smith",
    "Carol Williams",
    "David Brown",
    "Emma Davis",
    "Frank Miller",
    "Grace Wilson",
    "Henry Moore",
    "Iris Taylor",
    "Jack Anderson",
    "Karen Thomas",
    "Leo Jackson",
    "Mia White",
    "Noah Harris",
    "Olivia Martin",
    "Paul Garcia",
    "Quinn Martinez",
    "Rachel Robinson",
    "Sam Clark",
    "Tina Lewis",
]

_DOMAINS: list[str] = [
    "example.com",
    "mail.com",
    "test.org",
    "demo.net",
    "inbox.io",
]

_WORDS: list[str] = [
    "alpha", "bravo", "charlie", "delta", "echo",
    "foxtrot", "golf", "hotel", "india", "juliet",
    "kilo", "lima", "mike", "november", "oscar",
    "papa", "quebec", "romeo", "sierra", "tango",
    "uniform", "victor", "whiskey", "xray", "yankee",
    "zulu", "quick", "brown", "fox", "jumps",
]

_STREET_NAMES: list[str] = [
    "Oak", "Maple", "Cedar", "Elm", "Pine",
    "Washington", "Park", "Main", "Highland", "Sunset",
]

_STREET_TYPES: list[str] = [
    "Street", "Avenue", "Drive", "Lane", "Boulevard",
]

_CITY_NAMES: list[str] = [
    "Springfield", "Riverdale", "Madison", "Georgetown", "Fairview",
    "Clinton", "Arlington", "Burlington", "Manchester", "Ashland",
]


class _Fake:
    """Generator for realistic fake values."""

    def __init__(self) -> None:
        self._rng = random.Random()

    def seed(self, n: int) -> None:
        """Set the random seed for reproducible output."""
        self._rng.seed(n)

    def name(self) -> str:
        """Return a random full name."""
        return self._rng.choice(_NAMES)

    def email(self) -> str:
        """Return a random email address derived from a name."""
        full = self.name()
        first, last = full.lower().split()
        domain = self._rng.choice(_DOMAINS)
        return f"{first}.{last}@{domain}"

    def integer(self, min: int = 0, max: int = 1000) -> int:
        """Return a random integer within *min*..*max* inclusive."""
        return self._rng.randint(min, max)

    def decimal(self, min: float = 0, max: float = 1000, precision: int = 2) -> float:
        """Return a random float rounded to *precision* decimal places."""
        return round(self._rng.uniform(min, max), precision)

    def boolean(self) -> bool:
        """Return a random boolean."""
        return self._rng.choice([True, False])

    def choice(self, items: list[Any]) -> Any:
        """Return a random element from *items*."""
        return self._rng.choice(items)

    def text(self, words: int = 5) -> str:
        """Return a string of *words* random words."""
        return " ".join(self._rng.choice(_WORDS) for _ in range(words))

    def date(self, start: str = "2020-01-01", end: str = "2026-12-31") -> str:
        """Return a random ISO-format date between *start* and *end*."""
        start_date = date.fromisoformat(start)
        end_date = date.fromisoformat(end)
        delta_days = (end_date - start_date).days
        random_days = self._rng.randint(0, delta_days)
        return (start_date + timedelta(days=random_days)).isoformat()

    def uuid(self) -> str:
        """Return a random UUID4 string."""
        return str(_uuid.UUID(int=self._rng.getrandbits(128), version=4))

    def phone(self) -> str:
        """Return a random phone number in ``+1-XXX-XXX-XXXX`` format."""
        digits = [str(self._rng.randint(0, 9)) for _ in range(10)]
        return f"+1-{''.join(digits[:3])}-{''.join(digits[3:6])}-{''.join(digits[6:])}"

    def address(self) -> str:
        """Return a random street address like ``\"123 Oak Street, Springfield\"``."""
        number = self._rng.randint(1, 9999)
        street = self._rng.choice(_STREET_NAMES)
        street_type = self._rng.choice(_STREET_TYPES)
        city = self._rng.choice(_CITY_NAMES)
        return f"{number} {street} {street_type}, {city}"

    def weighted_choice(self, options: dict[str, float]) -> str:
        """Return a weighted random selection from *options*.

        Keys are the choices and values are their weights.

        Example::

            fake.weighted_choice({"gold": 0.1, "silver": 0.3, "bronze": 0.6})
        """
        keys = list(options.keys())
        weights = [options[k] for k in keys]
        return self._rng.choices(keys, weights=weights, k=1)[0]


fake = _Fake()


class Factory:
    """Build dictionaries of fake data from a schema definition.

    Parameters
    ----------
    schema:
        Mapping of field names to provider strings (``"name"``,
        ``"email"``, ``"integer"``, ``"boolean"``, ``"text"``,
        ``"date"``, ``"uuid"``, ``"decimal"``) or callables that
        return a value.
    """

    _PROVIDERS: dict[str, str] = {
        "name": "name",
        "email": "email",
        "integer": "integer",
        "boolean": "boolean",
        "text": "text",
        "date": "date",
        "uuid": "uuid",
        "decimal": "decimal",
        "phone": "phone",
        "address": "address",
    }

    def __init__(self, schema: dict[str, str | Callable[[], Any]]) -> None:
        self._schema = schema

    def build(self) -> dict[str, Any]:
        """Generate a single record matching the schema."""
        record: dict[str, Any] = {}
        for key, provider in self._schema.items():
            if callable(provider):
                record[key] = provider()
            elif isinstance(provider, str) and provider in self._PROVIDERS:
                record[key] = getattr(fake, self._PROVIDERS[provider])()
            else:
                raise ValueError(f"Unknown provider: {provider!r}")
        return record

    def build_batch(self, n: int) -> list[dict[str, Any]]:
        """Generate *n* records matching the schema."""
        return [self.build() for _ in range(n)]
