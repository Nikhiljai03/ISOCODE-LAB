# Initial Assumptions and Decisions

- Website allocations are maintained separately from physical inventory at category/date level.
- Missing allocation and rate rows fail closed.
- 15-minute holds are the default synthetic hold duration.
- Confirmed and active pending holds consume website allocation.
- All money values use PostgreSQL NUMERIC and Python Decimal.
- Gemini never receives commercial inventory, price, tax, or availability facts and output is treated as untrusted.
- Payment provider event identifiers are unique, providing payment confirmation idempotency.
- These assumptions do not assert actual resort policy or legal facts.
