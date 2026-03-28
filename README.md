# philiprehberger-data-factory

[![Tests](https://github.com/philiprehberger/py-data-factory/actions/workflows/publish.yml/badge.svg)](https://github.com/philiprehberger/py-data-factory/actions/workflows/publish.yml)
[![PyPI version](https://img.shields.io/pypi/v/philiprehberger-data-factory.svg)](https://pypi.org/project/philiprehberger-data-factory/)
[![GitHub release](https://img.shields.io/github/v/release/philiprehberger/py-data-factory)](https://github.com/philiprehberger/py-data-factory/releases)
[![Last updated](https://img.shields.io/github/last-commit/philiprehberger/py-data-factory)](https://github.com/philiprehberger/py-data-factory/commits/main)
[![License](https://img.shields.io/github/license/philiprehberger/py-data-factory)](LICENSE)
[![Bug Reports](https://img.shields.io/github/issues/philiprehberger/py-data-factory/bug)](https://github.com/philiprehberger/py-data-factory/issues?q=is%3Aissue+is%3Aopen+label%3Abug)
[![Feature Requests](https://img.shields.io/github/issues/philiprehberger/py-data-factory/enhancement)](https://github.com/philiprehberger/py-data-factory/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement)
[![Sponsor](https://img.shields.io/badge/sponsor-GitHub%20Sponsors-ec6cb9)](https://github.com/sponsors/philiprehberger)

Lightweight test data generation with realistic fake values.

## Installation

```bash
pip install philiprehberger-data-factory
```

## Usage

### Generate fake values

```python
from philiprehberger_data_factory import fake

fake.name()      # "Alice Johnson"
fake.email()     # "bob.smith@example.com"
fake.integer()   # 472
fake.boolean()   # True
fake.text()      # "alpha bravo charlie delta echo"
fake.date()      # "2023-07-14"
fake.uuid()      # "a3b2c1d4-..."
fake.phone()     # "+1-555-123-4567"
fake.address()   # "742 Oak Street, Springfield"
```

### Factory

Define a schema and generate records in bulk:

```python
from philiprehberger_data_factory import Factory

user_factory = Factory({
    "name": "name",
    "email": "email",
    "age": "integer",
    "bio": "text",
    "joined": "date",
    "id": "uuid",
    "phone": "phone",
    "address": "address",
})

user = user_factory.build()
# {'name': 'Grace Wilson', 'email': 'henry.moore@mail.com', ...}

users = user_factory.build_batch(100)
# [{'name': ..., 'email': ..., ...}, ...]
```

### Weighted choices

```python
from philiprehberger_data_factory import fake

tier = fake.weighted_choice({"gold": 0.1, "silver": 0.3, "bronze": 0.6})
```

### Custom providers

Pass a callable instead of a provider string:

```python
from philiprehberger_data_factory import fake, Factory

factory = Factory({
    "name": "name",
    "role": lambda: fake.choice(["admin", "editor", "viewer"]),
})
```

### Reproducible output

```python
from philiprehberger_data_factory import fake

fake.seed(42)
fake.name()  # always the same name for seed 42
```

## API

| Method / Function | Description |
|---|---|
| `fake.name()` | Random full name |
| `fake.email()` | Random email address |
| `fake.integer(min, max)` | Random integer (default 0-1000) |
| `fake.decimal(min, max, precision)` | Random float (default 0-1000, 2 decimals) |
| `fake.boolean()` | Random `True` or `False` |
| `fake.choice(items)` | Random element from a list |
| `fake.text(words)` | Random words (default 5) |
| `fake.date(start, end)` | Random ISO date string |
| `fake.uuid()` | Random UUID4 string |
| `fake.phone()` | Random phone number in `+1-XXX-XXX-XXXX` format |
| `fake.address()` | Random street address with city |
| `fake.weighted_choice(options)` | Weighted random selection from a dict of options to weights |
| `fake.seed(n)` | Set random seed for reproducibility |
| `Factory(schema)` | Create a factory from a schema dict |
| `factory.build()` | Generate one record |
| `factory.build_batch(n)` | Generate *n* records |

## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## Support

If you find this package useful, consider starring the repository.

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Philip%20Rehberger-blue?logo=linkedin)](https://www.linkedin.com/in/philiprehberger/)
[![More Packages](https://img.shields.io/badge/More%20Packages-philiprehberger-orange)](https://github.com/philiprehberger?tab=repositories)

## License

[MIT](LICENSE)
