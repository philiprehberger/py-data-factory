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

### Bulk generation with overrides

Use `batch()` to generate multiple records with optional per-item or shared overrides:

```python
from philiprehberger_data_factory import Factory

factory = Factory({"name": "name", "role": "text"})

# Shared overrides applied to every record
admins = factory.batch(5, overrides={"role": "admin"})

# Per-item overrides
records = factory.batch(3, overrides=[
    {"role": "admin"},
    {"role": "editor"},
    {"role": "viewer"},
])
```

### Relationship / foreign-key support

Link factories so generated objects have consistent foreign-key references:

```python
from philiprehberger_data_factory import Factory

user_factory = Factory({"id": "uuid", "name": "name"})
user = user_factory.build()

post_factory = Factory({"title": "text", "body": "text"})
post_factory.related(user_factory, field="user_id", source_field="id")

post = post_factory.build()
# post["user_id"] matches user["id"]
```

### Statistical distribution profiles

Generate numeric fields following statistical distributions:

```python
from philiprehberger_data_factory import Factory

factory = Factory({"name": "name"})
factory.field("age", distribution="normal", mean=30, std=10)
factory.field("score", distribution="uniform", min=0, max=100)
factory.field("wait_time", distribution="exponential", scale=5.0)

record = factory.build()
# {'name': 'Alice Johnson', 'age': 28.4, 'score': 73.2, 'wait_time': 3.1}
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

| Function / Class | Description |
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
| `fake.normal(mean, std)` | Random float from a normal distribution |
| `fake.exponential(scale)` | Random float from an exponential distribution |
| `fake.seed(n)` | Set random seed for reproducibility |
| `Factory(schema)` | Create a factory from a schema dict |
| `factory.build(**overrides)` | Generate one record with optional field overrides |
| `factory.build_batch(n)` | Generate *n* records |
| `factory.batch(n, overrides)` | Generate *n* records with shared or per-item overrides |
| `factory.field(name, distribution, **params)` | Add a field with a statistical distribution (normal, uniform, exponential) |
| `factory.related(other, field, source_field)` | Link to another factory for foreign-key consistency |

## Development

```bash
pip install -e .
python -m pytest tests/ -v
```

## Support

If you find this package useful, consider giving it a star on GitHub — it helps motivate continued maintenance and development.

[![LinkedIn](https://img.shields.io/badge/Philip%20Rehberger-LinkedIn-0A66C2?logo=linkedin)](https://www.linkedin.com/in/philiprehberger)
[![More packages](https://img.shields.io/badge/more-open%20source%20packages-blue)](https://philiprehberger.com/open-source-packages)

## License

[MIT](LICENSE)
