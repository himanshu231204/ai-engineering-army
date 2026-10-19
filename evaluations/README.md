# Evaluation fixtures

This directory holds small, host-neutral examples used to discuss and later evaluate AIEA workflows. It is not an evaluation runner and does not contain a full benchmark dataset.

ArmyBench is a separate project. It should own benchmark application code, execution harnesses, scoring, datasets, and release process. Keep only sanitized, minimal fixtures here, and mirror or version them deliberately when ArmyBench consumes them.

The initial reference application stack is Next.js, FastAPI, and PostgreSQL. Fixtures should test engineering behavior such as diagnosis, safe delegation, integration discipline, and evidence quality across that stack without prescribing one agent vendor.
