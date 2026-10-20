"""Validate, list, and package AIEA's portable Agent Skills."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / ".agents" / "skills"
VERSION_FILE = ROOT / "VERSION"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FIELD_PATTERN = re.compile(r"^([a-z][a-z0-9_-]*):(?:[ \t]*(.*))?$")
VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
HOST_PATHS = {
    "claude-code": ".claude/skills",
    "claude-code-plugin": "skills",
    "codex": ".agents/skills",
    "opencode": ".agents/skills",
}
REQUIRED_DOCS = (
    "README.md",
    "AGENTS.md",
    "CLAUDE.md",
    "LICENSE",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    ".github/workflows/validate.yml",
    "docs/vision.md",
    "docs/architecture.md",
    "docs/design-principles.md",
    "docs/version-1.md",
    "docs/host-compatibility.md",
    "docs/cli.md",
    "docs/claude-code-plugin.md",
    "docs/release.md",
    "docs/security.md",
    "docs/contributing.md",
    "adapters/README.md",
    "adapters/claude-code/README.md",
    "adapters/codex/README.md",
    "adapters/opencode/README.md",
    "evaluations/README.md",
    "evaluations/fixtures/README.md",
)


@dataclass(frozen=True)
class Skill:
    name: str
    description: str
    path: Path
    group: str


def _yaml_scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            parsed = json.loads(value)
            return parsed if isinstance(parsed, str) else value[1:-1]
        except json.JSONDecodeError:
            return value[1:-1]
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    return value


def parse_frontmatter(path: Path) -> tuple[dict[str, str], list[str]]:
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, ["missing opening YAML frontmatter delimiter"]
    try:
        closing = next(i for i, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        return {}, ["missing closing YAML frontmatter delimiter"]

    fields: dict[str, str] = {}
    errors: list[str] = []
    current_field: str | None = None
    block_field: str | None = None
    block_style: str | None = None
    block_lines: list[str] = []

    def finish_block() -> None:
        nonlocal block_field, block_style, block_lines
        if block_field is not None:
            separator = " " if block_style and block_style.startswith(">") else "\n"
            fields[block_field] = separator.join(part for part in block_lines if part).strip()
        block_field = None
        block_style = None
        block_lines = []

    for line_number, line in enumerate(lines[1:closing], start=2):
        if block_field is not None:
            if not line.strip() or line[:1].isspace():
                block_lines.append(line.strip())
                continue
            finish_block()

        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line[:1].isspace():
            if current_field is None:
                errors.append(f"line {line_number}: indented content has no parent field")
            continue

        match = FIELD_PATTERN.fullmatch(line)
        if not match:
            errors.append(f"line {line_number}: malformed frontmatter field")
            current_field = None
            continue
        key, raw_value = match.groups()
        if key in fields or key == block_field:
            errors.append(f"line {line_number}: duplicate {key!r} field")
        current_field = key
        raw_value = raw_value or ""
        if raw_value in (">", ">-", ">+", "|", "|-", "|+"):
            block_field = key
            block_style = raw_value
            block_lines = []
        else:
            fields[key] = _yaml_scalar(raw_value)

    finish_block()
    for required in ("name", "description"):
        if not fields.get(required, "").strip():
            errors.append(f"frontmatter must define a non-empty {required}")
    name = fields.get("name", "")
    description = fields.get("description", "")
    if name and (not NAME_PATTERN.fullmatch(name) or len(name) > 64):
        errors.append("name must be lowercase alphanumeric with single hyphen separators and at most 64 characters")
    if description and len(description) > 1024:
        errors.append("description must be at most 1024 characters")
    return fields, errors


def load_skills(root: Path = ROOT) -> tuple[list[Skill], list[str]]:
    skills_root = root / ".agents" / "skills"
    if not skills_root.is_dir():
        return [], [".agents/skills directory does not exist"]

    skill_files = sorted(skills_root.rglob("SKILL.md"))
    if not skill_files:
        return [], ["no SKILL.md files found under .agents/skills"]

    skills: list[Skill] = []
    errors: list[str] = []
    names: dict[str, Path] = {}
    for skill_file in skill_files:
        relative = skill_file.relative_to(root).as_posix()
        skill_dir = skill_file.parent
        if skill_file.is_symlink() or any(child.is_symlink() for child in skill_dir.rglob("*")):
            errors.append(f"{relative}: symlinks are not allowed in packaged skill directories")
            continue
        fields, file_errors = parse_frontmatter(skill_file)
        errors.extend(f"{relative}: {error}" for error in file_errors)
        name = fields.get("name", "")
        description = fields.get("description", "")
        if name:
            if skill_dir.name != name:
                errors.append(f"{relative}: directory name must match frontmatter name {name!r}")
            if name in names:
                errors.append(f"{relative}: duplicate skill name also used by {names[name].relative_to(root).as_posix()}")
            names[name] = skill_file
            group = "specialists" if "specialists" in skill_dir.relative_to(skills_root).parts else "core"
            skills.append(Skill(name=name, description=description, path=skill_dir, group=group))
    return skills, errors


def plugin_errors(root: Path, skills: list[Skill], version: str) -> list[str]:
    """Check AIEA distribution invariants, not the entire Claude Code schema."""
    errors: list[str] = []
    documents: dict[str, dict] = {}
    for name in ("plugin", "marketplace"):
        path = root / ".claude-plugin" / f"{name}.json"
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(document, dict):
                raise ValueError("expected a JSON object")
            documents[name] = document
        except (OSError, ValueError) as error:
            errors.append(f".claude-plugin/{name}.json: {error}")
    plugin = documents.get("plugin")
    if plugin is not None:
        if plugin.get("name") != "aiea":
            errors.append("plugin name must be aiea")
        if plugin.get("version") != version:
            errors.append("plugin version must match VERSION")
        author = plugin.get("author")
        if not isinstance(author, dict) or not author.get("name") or not plugin.get("description"):
            errors.append("plugin must have an author name and description")
        expected = sorted("./" + skill.path.relative_to(root).as_posix() for skill in skills)
        paths = plugin.get("skills")
        if not isinstance(paths, list) or not all(isinstance(path, str) for path in paths):
            errors.append("plugin skills must be an array of paths")
        elif sorted(paths) != expected:
            errors.append("plugin skills must reference every canonical skill exactly once")
        # The default directory is additive even with custom skills paths.
        if (root / "skills").exists():
            errors.append("root skills/ would add non-canonical plugin skills")
    marketplace = documents.get("marketplace")
    if marketplace is not None:
        if marketplace.get("name") != "aiea-marketplace":
            errors.append("marketplace name must be aiea-marketplace")
        owner = marketplace.get("owner")
        if not isinstance(owner, dict) or not owner.get("name"):
            errors.append("marketplace must have an owner name")
        entries = marketplace.get("plugins")
        if (not isinstance(entries, list) or len(entries) != 1
                or not isinstance(entries[0], dict)
                or entries[0].get("name") != "aiea"
                or entries[0].get("source") != "./"):
            errors.append("marketplace must list aiea from ./")
        elif any(key in entries[0] for key in ("version", "skills", "strict")):
            errors.append("plugin.json owns the version and skill paths; do not override them in the marketplace")
    return errors


def repository_errors(root: Path = ROOT) -> tuple[list[Skill], list[str]]:
    skills, errors = load_skills(root)
    version_path = root / "VERSION"
    if not version_path.is_file():
        errors.append("VERSION file is missing")
        version = ""
    else:
        version = version_path.read_text(encoding="utf-8-sig").strip()
        if not VERSION_PATTERN.fullmatch(version):
            errors.append("VERSION must contain a semantic version such as 1.0.0")

    errors.extend(plugin_errors(root, skills, version))

    for required in REQUIRED_DOCS:
        if not (root / required).is_file():
            errors.append(f"required v1 document is missing: {required}")

    fixture_root = root / "evaluations" / "fixtures"
    if fixture_root.is_dir():
        for fixture in sorted(fixture_root.rglob("*.json")):
            try:
                json.loads(fixture.read_text(encoding="utf-8-sig"))
            except (OSError, json.JSONDecodeError) as error:
                errors.append(f"{fixture.relative_to(root).as_posix()}: invalid JSON ({error})")
    return skills, errors


def command_validate(_: argparse.Namespace) -> int:
    skills, errors = repository_errors()
    if errors:
        print("AIEA validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    version = VERSION_FILE.read_text(encoding="utf-8-sig").strip()
    print(f"AIEA {version}: validated {len(skills)} skills, plugin/marketplace metadata, required documents, and evaluation fixtures.")
    return 0


def command_list(args: argparse.Namespace) -> int:
    skills, errors = repository_errors()
    if errors:
        print("AIEA validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    selected = [skill for skill in skills if args.group == "all" or skill.group == args.group]
    for skill in selected:
        print(f"{skill.name} [{skill.group}] | {skill.description}")
    print(f"{len(selected)} skills")
    return 0


def _archive_entry(archive: zipfile.ZipFile, name: str, data: bytes) -> None:
    info = zipfile.ZipInfo(name, date_time=(2026, 1, 1, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    archive.writestr(info, data)


def command_package(args: argparse.Namespace) -> int:
    skills, errors = repository_errors()
    if errors:
        print("AIEA validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    if args.skill:
        by_name = {skill.name: skill for skill in skills}
        unknown = sorted(set(args.skill) - by_name.keys())
        if unknown:
            print(f"unknown skill name(s): {', '.join(unknown)}", file=sys.stderr)
            return 2
        selected = [by_name[name] for name in sorted(set(args.skill))]
    else:
        selected = skills

    version = VERSION_FILE.read_text(encoding="utf-8-sig").strip()
    install_path = HOST_PATHS[args.host]
    output_dir = Path(args.output).expanduser().resolve()
    try:
        output_dir.mkdir(parents=True, exist_ok=True)
    except OSError as error:
        print(f"could not create output directory: {error}", file=sys.stderr)
        return 1
    archive_path = output_dir / f"aiea-{version}-{args.host}.zip"
    payloads: list[tuple[str, bytes]] = []
    manifest_files: list[dict[str, object]] = []

    def add_payload(name: str, data: bytes) -> None:
        payloads.append((name, data))
        manifest_files.append({
            "path": name, "size": len(data), "sha256": hashlib.sha256(data).hexdigest(),
        })

    prefix = PurePosixPath(install_path)
    for skill in selected:
        for file_path in sorted(skill.path.rglob("*")):
            if not file_path.is_file():
                continue
            relative_inside_skill = file_path.relative_to(skill.path).as_posix()
            archive_name = (prefix / skill.name / PurePosixPath(relative_inside_skill)).as_posix()
            data = file_path.read_bytes()
            add_payload(archive_name, data)

    is_plugin = args.host == "claude-code-plugin"
    if is_plugin:
        plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        # The standalone bundle uses Claude Code's standard skills/ layout.
        plugin.pop("skills", None)
        add_payload(".claude-plugin/plugin.json", (json.dumps(plugin, indent=2) + "\n").encode("utf-8"))
        add_payload("LICENSE", (ROOT / "LICENSE").read_bytes())

    installation = (
        "Extract into a separate plugin directory, then run `claude --plugin-dir ./aiea-plugin` "
        "using the extracted directory's actual path. In Claude Code invoke `/aiea:aiea-bootstrap`.\n\n"
        if is_plugin else
        f"Extract this archive at the root of the target project. The skills will be placed under `{install_path}/`.\n\n"
    )
    install_readme = (
        f"# AIEA {version} package for {args.host}\n\n" + installation +
        "Review skill contents before enabling them in an agent host. This package contains instructions and resources; "
        "it does not install an agent, grant tools, or configure permissions.\n"
    ).encode("utf-8")
    add_payload("AIEA-INSTALL.md", install_readme)

    manifest = {
        "name": "ai-engineering-army",
        "version": version,
        "host": args.host,
        "format": "Claude Code plugin" if is_plugin else "Agent Skills",
        "install_path": install_path,
        "skills": [skill.name for skill in selected],
        "files": manifest_files,
    }
    payloads.extend([
        ("aiea-manifest.json", (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode("utf-8")),
    ])

    try:
        with archive_path.open("xb") as output_file:
            try:
                with zipfile.ZipFile(output_file, mode="w") as archive:
                    for name, data in sorted(payloads, key=lambda item: item[0]):
                        _archive_entry(archive, name, data)
            except Exception:
                archive_path.unlink(missing_ok=True)
                raise
    except FileExistsError:
        print(f"refusing to overwrite existing archive: {archive_path}", file=sys.stderr)
        return 2
    except OSError as error:
        print(f"could not write archive: {error}", file=sys.stderr)
        return 1

    print(f"Created {archive_path} with {len(selected)} skills for {args.host} at {install_path}/")
    return 0


def build_parser() -> argparse.ArgumentParser:
    version = VERSION_FILE.read_text(encoding="utf-8-sig").strip() if VERSION_FILE.is_file() else "unknown"
    parser = argparse.ArgumentParser(prog="aiea", description="Work with the AIEA portable skill library.")
    parser.add_argument("--version", action="version", version=f"AIEA {version}")
    commands = parser.add_subparsers(dest="command", required=True)

    validate = commands.add_parser("validate", help="validate skills, required docs, and evaluation fixture JSON")
    validate.set_defaults(handler=command_validate)

    list_command = commands.add_parser("list", help="list validated skills")
    list_command.add_argument("--group", choices=("all", "core", "specialists"), default="all")
    list_command.set_defaults(handler=command_list)

    package = commands.add_parser("package", help="create a host-layout ZIP archive")
    package.add_argument("--host", choices=tuple(HOST_PATHS), required=True)
    package.add_argument("--output", default="dist", help="output directory (default: dist)")
    package.add_argument("--skill", action="append", help="include one skill by exact name; repeat to select several")
    package.set_defaults(handler=command_package)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())


