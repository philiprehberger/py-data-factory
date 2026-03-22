from __future__ import annotations

from philiprehberger_data_factory import fake, Factory


def test_fake_name_returns_string():
    result = fake.name()
    assert isinstance(result, str)
    assert len(result) > 0


def test_fake_email_contains_at():
    result = fake.email()
    assert "@" in result


def test_factory_build_returns_dict_with_correct_keys():
    schema = {"full_name": "name", "addr": "email", "active": "boolean"}
    factory = Factory(schema)
    record = factory.build()
    assert isinstance(record, dict)
    assert set(record.keys()) == {"full_name", "addr", "active"}


def test_factory_build_batch_returns_correct_count():
    schema = {"id": "uuid", "score": "integer"}
    factory = Factory(schema)
    batch = factory.build_batch(10)
    assert len(batch) == 10
    assert all(isinstance(r, dict) for r in batch)


def test_seed_produces_reproducible_output():
    fake.seed(42)
    first = fake.name()
    fake.seed(42)
    second = fake.name()
    assert first == second
