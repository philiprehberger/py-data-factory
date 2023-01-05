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


# --- Relationship / foreign-key tests ---


def test_related_factory_copies_foreign_key():
    user_factory = Factory({"id": "uuid", "name": "name"})
    user = user_factory.build()

    post_factory = Factory({"title": "text"})
    post_factory.related(user_factory, field="user_id", source_field="id")
    post = post_factory.build()

    assert post["user_id"] == user["id"]


def test_related_factory_auto_builds_parent_when_no_record():
    parent = Factory({"id": "uuid", "name": "name"})
    child = Factory({"body": "text"})
    child.related(parent, field="author_id", source_field="id")
    record = child.build()
    assert "author_id" in record
    assert isinstance(record["author_id"], str)


def test_related_factory_chaining():
    user_factory = Factory({"id": "uuid"})
    post_factory = Factory({"id": "uuid", "content": "text"})
    post_factory.related(user_factory, field="user_id", source_field="id")
    result = post_factory.build()
    assert "user_id" in result
    assert "content" in result


# --- Statistical distribution tests ---


def test_field_normal_distribution():
    factory = Factory({"name": "name"})
    factory.field("age", distribution="normal", mean=30, std=10)
    record = factory.build()
    assert "age" in record
    assert isinstance(record["age"], float)


def test_field_uniform_distribution():
    factory = Factory({})
    factory.field("score", distribution="uniform", min=0, max=100)
    record = factory.build()
    assert 0 <= record["score"] <= 100


def test_field_exponential_distribution():
    factory = Factory({})
    factory.field("wait_time", distribution="exponential", scale=5.0)
    record = factory.build()
    assert record["wait_time"] >= 0


def test_field_returns_factory_for_chaining():
    factory = Factory({})
    result = factory.field("x", distribution="normal", mean=0, std=1)
    assert result is factory


def test_field_unknown_distribution_raises():
    factory = Factory({})
    factory.field("x", distribution="unknown_dist")
    try:
        factory.build()
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_normal_distribution_range():
    """Values from normal(mean=100, std=1) should cluster near 100."""
    fake.seed(0)
    factory = Factory({})
    factory.field("val", distribution="normal", mean=100, std=1)
    records = factory.batch(50)
    values = [r["val"] for r in records]
    avg = sum(values) / len(values)
    assert 95 < avg < 105


# --- Batch tests ---


def test_batch_generates_correct_count():
    factory = Factory({"id": "uuid"})
    results = factory.batch(5)
    assert len(results) == 5


def test_batch_with_shared_overrides():
    factory = Factory({"name": "name", "role": "text"})
    results = factory.batch(3, overrides={"role": "admin"})
    assert all(r["role"] == "admin" for r in results)


def test_batch_with_per_item_overrides():
    factory = Factory({"name": "name", "score": "integer"})
    overrides = [{"score": 10}, {"score": 20}, {"score": 30}]
    results = factory.batch(3, overrides=overrides)
    assert results[0]["score"] == 10
    assert results[1]["score"] == 20
    assert results[2]["score"] == 30


def test_batch_with_mismatched_overrides_raises():
    factory = Factory({"id": "uuid"})
    try:
        factory.batch(3, overrides=[{"id": "a"}, {"id": "b"}])
        assert False, "Should have raised ValueError"
    except ValueError:
        pass


def test_batch_no_overrides():
    factory = Factory({"id": "uuid", "active": "boolean"})
    results = factory.batch(4)
    assert len(results) == 4
    assert all("id" in r and "active" in r for r in results)


# --- Build with overrides ---


def test_build_with_keyword_overrides():
    factory = Factory({"name": "name", "email": "email"})
    record = factory.build(name="Custom Name")
    assert record["name"] == "Custom Name"
    assert "@" in record["email"]


# --- fake.normal / fake.exponential ---


def test_fake_normal():
    fake.seed(1)
    val = fake.normal(mean=50, std=5)
    assert isinstance(val, float)


def test_fake_exponential():
    fake.seed(1)
    val = fake.exponential(scale=2.0)
    assert isinstance(val, float)
    assert val >= 0
