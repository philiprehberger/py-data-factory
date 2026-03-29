"""Lightweight test data generation with realistic fake values."""

from __future__ import annotations

import random
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

    def normal(self, mean: float = 0.0, std: float = 1.0) -> float:
        """Return a random float from a normal (Gaussian) distribution."""
        return self._rng.gauss(mean, std)

    def exponential(self, scale: float = 1.0) -> float:
        """Return a random float from an exponential distribution.

        *scale* is the inverse of the rate parameter (1/lambda), i.e. the mean.
        """
        return self._rng.expovariate(1.0 / scale)


fake = _Fake()


class _Relation:
    """Describes a foreign-key relationship between two factories."""

    __slots__ = ("factory", "field", "source_field")

    def __init__(self, factory: Factory, field: str, source_field: str) -> None:
        self.factory = factory
        self.field = field
        self.source_field = source_field


class _DistributionProvider:
    """Wraps a statistical distribution as a field provider."""

    __slots__ = ("distribution", "params")

    def __init__(self, distribution: str, **params: float) -> None:
        self.distribution = distribution
        self.params = params

    def __call__(self) -> float:
        if self.distribution == "normal":
            mean = self.params.get("mean", 0.0)
            std = self.params.get("std", 1.0)
            return fake.normal(mean, std)
        elif self.distribution == "uniform":
            low = self.params.get("min", 0.0)
            high = self.params.get("max", 1.0)
            return fake.decimal(low, high, precision=6)
        elif self.distribution == "exponential":
            scale = self.params.get("scale", 1.0)
            return fake.exponential(scale)
        else:
            raise ValueError(f"Unknown distribution: {self.distribution!r}")


class Factory:
    """Build dictionaries of fake data from a schema definition.

    Parameters
    ----------
    schema:
        Mapping of field names to provider strings (``"name"``,
        ``"email"``, ``"integer"``, ``"boolean"``, ``"text"``,
        ``"date"``, ``"uuid"``, ``"decimal"``, ``"phone"``,
        ``"address"``) or callables that return a value.
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
        self._relations: list[_Relation] = []
        self._last_record: dict[str, Any] | None = None

    # ------------------------------------------------------------------
    # Configuration helpers
    # ------------------------------------------------------------------

    def field(
        self,
        name: str,
        distribution: str,
        **params: float,
    ) -> Factory:
        """Register a numeric field backed by a statistical distribution.

        Supported distributions: ``"normal"``, ``"uniform"``, ``"exponential"``.

        Parameters
        ----------
        name:
            The field name in the generated record.
        distribution:
            One of ``"normal"``, ``"uniform"``, ``"exponential"``.
        **params:
            Distribution parameters.  ``"normal"`` accepts *mean* and *std*;
            ``"uniform"`` accepts *min* and *max*; ``"exponential"`` accepts
            *scale*.

        Returns the factory instance for chaining.
        """
        provider = _DistributionProvider(distribution, **params)
        self._schema[name] = provider
        return self

    def related(
        self,
        other: Factory,
        field: str = "id",
        source_field: str = "id",
    ) -> Factory:
        """Link this factory to *other* via a foreign-key relationship.

        When a record is built, the value of *source_field* from the most
        recently built record of *other* is copied into *field* of this
        factory's record.  If *other* has not yet produced a record, one
        is generated automatically.

        Parameters
        ----------
        other:
            The parent factory whose records are referenced.
        field:
            The foreign-key field name in **this** factory's records.
        source_field:
            The field name in *other*'s records that provides the value.

        Returns the factory instance for chaining.
        """
        self._relations.append(_Relation(other, field, source_field))
        return self

    def batch(
        self,
        n: int,
        overrides: dict[str, Any] | list[dict[str, Any]] | None = None,
    ) -> list[dict[str, Any]]:
        """Generate *n* records with optional per-item or shared overrides.

        Parameters
        ----------
        n:
            Number of records to generate.
        overrides:
            If a ``dict``, the same overrides are applied to every record.
            If a ``list`` of dicts, each dict is applied to the corresponding
            record (the list length must equal *n*).  ``None`` means no
            overrides.
        """
        if isinstance(overrides, list):
            if len(overrides) != n:
                raise ValueError(
                    f"overrides list length ({len(overrides)}) must equal n ({n})"
                )
            return [self._build_with_overrides(overrides[i]) for i in range(n)]
        shared = overrides or {}
        return [self._build_with_overrides(shared) for _ in range(n)]

    # ------------------------------------------------------------------
    # Record building
    # ------------------------------------------------------------------

    def build(self, **overrides: Any) -> dict[str, Any]:
        """Generate a single record matching the schema.

        Any keyword arguments override the generated values for the
        corresponding fields.
        """
        return self._build_with_overrides(overrides)

    def build_batch(self, n: int) -> list[dict[str, Any]]:
        """Generate *n* records matching the schema."""
        return [self.build() for _ in range(n)]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _build_with_overrides(self, overrides: dict[str, Any]) -> dict[str, Any]:
        record: dict[str, Any] = {}
        for key, provider in self._schema.items():
            if key in overrides:
                record[key] = overrides[key]
            elif callable(provider):
                record[key] = provider()
            elif isinstance(provider, str) and provider in self._PROVIDERS:
                record[key] = getattr(fake, self._PROVIDERS[provider])()
            else:
                raise ValueError(f"Unknown provider: {provider!r}")

        # Apply foreign-key relations
        for rel in self._relations:
            parent = rel.factory._last_record
            if parent is None:
                parent = rel.factory.build()
            record[rel.field] = parent[rel.source_field]

        self._last_record = record
        return record
