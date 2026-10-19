# Contributing to AIEA

Start with [the contribution guide](docs/contributing.md), [v1 scope](docs/version-1.md), and [final architecture](docs/architecture.md).

Before opening a pull request, run:

```sh
python tools/aiea.py validate
```

Changes to skills, packages, host behavior, or public interfaces should update the relevant documentation and changelog. Do not add an orchestration engine, application, hosted service, or ArmyBench runner to this repository without an explicit scope decision.
