# Changelog

## 0.3.0 (2026-03-28)

- Add `Factory.related(other, field, source_field)` for foreign-key relationships between factories
- Add `Factory.field(name, distribution, **params)` for statistical distribution profiles (normal, uniform, exponential)
- Add `Factory.batch(n, overrides)` for bulk generation with optional per-item or shared overrides
- Add `Factory.build(**overrides)` keyword argument support for field overrides
- Add `fake.normal(mean, std)` for sampling from a normal distribution
- Add `fake.exponential(scale)` for sampling from an exponential distribution

## 0.2.0 (2026-03-27)

- Add `fake.phone()` for random phone number generation
- Add `fake.address()` for random street address generation
- Add `fake.weighted_choice()` for weighted random selection
- Register `"phone"` and `"address"` as Factory provider strings
- Add `.github/` issue templates, PR template, and Dependabot config
- Update README with full badge set and all standard sections

## 0.1.1 (2026-03-22)

- Add badges to README
- Rename Install section to Installation in README
- Add Development section to README
- Add Changelog URL to project URLs
- Add `#readme` anchor to Homepage URL
- Add pytest and mypy configuration

## 0.1.0 (2026-03-21)

- Initial release
- Fake value generators: name, email, integer, decimal, boolean, choice, text, date, uuid
- Seeded random for reproducible output
- Factory class for schema-based record generation with build and build_batch
