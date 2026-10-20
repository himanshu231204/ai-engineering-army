"""Validate, list, and package AIEA's portable Agent Skills."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / ".agents" / "skills"
VERSION_FILE = ROOT / "VERSION"
BUMP_CONFIG = ".version-bump.json"
PLUGIN_NAME = "ai-engineering-army"
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
FIELD_PATTERN = re.compile(r"^([a-z][a-z0-9_-]*):(?:[ \t]*(.*))?$")
VERSION_PATTERN = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?$")
HOST_PATHS = {
    "claude-code": ".claude/skills",
    "claude-code-plugin": "skills",
    "codex": ".agents/skills",
    "codex-plugin": "skills",
    "opencode": ".agents/skills",
    "opencode-plugin": "skills",
}
PLUGIN_HOSTS = {"claude-code-plugin", "codex-plugin", "opencode-plugin"}
REQUIRED_DOCS = (
    "README.md",
    "AGENTS.md",
    "LICENSE",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    BUMP_CONFIG,
    ".github/workflows/validate.yml",
    ".github/workflows/release.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/ISSUE_TEMPLATE/bug_report.md",
    ".github/ISSUE_TEMPLATE/evidence_report.md",
    ".github/ISSUE_TEMPLATE/feature_request.md",
    ".github/ISSUE_TEMPLATE/new_host.md",
    "docs/vision.md",
    "docs/architecture.md",
    "docs/design-principles.md",
    "docs/version-1.md",
    "docs/host-compatibility.md",
    "docs/cli.md",
    "docs/claude-code-plugin.md",
    "docs/workflow-validation.md",
    "docs/verification-status.md",
    "docs/release.md",
    "docs/release-notes.md",
    "docs/getting-started.md",
    "docs/security.md",
    "docs/skill-catalog.md",
    "docs/specialist-contracts.md",
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


def load_registry(root: Path) -> tuple[dict[str, str], list[str]]:
    groups: dict[str, str] = {}
    errors: list[str] = []
    try:
        document = json.loads((root / "skill-registry.json").read_text(encoding="utf-8-sig"))
        entries = document.get("skills") if isinstance(document, dict) else None
        if not isinstance(entries, list) or not entries:
            return {}, ["skill-registry.json must define a non-empty skills array"]
    except (OSError, ValueError) as error:
        return {}, [f"skill-registry.json: {error}"]
    for entry in entries:
        if not isinstance(entry, dict):
            errors.append("skill-registry.json entries must contain a name and group")
            continue
        name, group = entry.get("name"), entry.get("group")
        if not isinstance(name, str) or not NAME_PATTERN.fullmatch(name):
            errors.append("skill-registry.json contains an invalid name")
        elif group not in ("core", "specialists"):
            errors.append(f"skill-registry.json: {name} must use core or specialists")
        elif name in groups:
            errors.append(f"skill-registry.json: duplicate name {name}")
        else:
            groups[name] = group
    return groups, errors


def load_skills(root: Path = ROOT) -> tuple[list[Skill], list[str]]:
    skills_root = root / ".agents" / "skills"
    if not skills_root.is_dir():
        return [], [".agents/skills directory does not exist"]

    skill_files = sorted(skills_root.rglob("SKILL.md"))
    if not skill_files:
        return [], ["no SKILL.md files found under .agents/skills"]

    skills: list[Skill] = []
    groups, errors = load_registry(root)
    names: dict[str, Path] = {}
    for skill_file in skill_files:
        relative = skill_file.relative_to(root).as_posix()
        skill_dir = skill_file.parent
        if skill_dir.parent != skills_root:
            errors.append(f"{relative}: skills must be direct children of .agents/skills")
            continue
        if skill_dir.is_symlink() or skill_file.is_symlink() or any(child.is_symlink() for child in skill_dir.rglob("*")):
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
            group = groups.get(name, "")
            if not group:
                errors.append(f"{relative}: name is missing from skill-registry.json")
            skills.append(Skill(name=name, description=description, path=skill_dir, group=group))
    for name in sorted(groups.keys() - names.keys()):
        errors.append(f"skill-registry.json: no canonical skill found for {name}")
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
        if plugin.get("name") != PLUGIN_NAME:
            errors.append(f"plugin name must be {PLUGIN_NAME}")
        if plugin.get("version") != version:
            errors.append("plugin version must match VERSION")
        author = plugin.get("author")
        if not isinstance(author, dict) or not author.get("name") or not plugin.get("description"):
            errors.append("plugin must have an author name and description")
        if not plugin.get("displayName"):
            errors.append("plugin must have a displayName for the directory listing")
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
                or entries[0].get("name") != PLUGIN_NAME
                or entries[0].get("source") != "./"):
            errors.append(f"marketplace must list {PLUGIN_NAME} from ./")
        elif any(key in entries[0] for key in ("version", "skills", "strict")):
            errors.append("plugin.json owns the version and skill paths; do not override them in the marketplace")
        renames = marketplace.get("renames")
        if renames is not None:
            if not isinstance(renames, dict) or not all(
                    isinstance(old, str) and isinstance(new, (str, type(None)))
                    for old, new in renames.items()):
                errors.append("marketplace renames must map a former name to a current name or null")
            elif PLUGIN_NAME not in renames.values():
                errors.append(f"marketplace renames must map the former name to {PLUGIN_NAME}")
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
    errors.extend(adapter_errors(root, version))
    errors.extend(version_errors(root))

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


def adapter_errors(root: Path, version: str) -> list[str]:
    errors: list[str] = []
    for relative, expected in (
        (".codex-plugin/plugin.json", {"name": PLUGIN_NAME, "version": version, "skills": "./.agents/skills/"}),
        ("adapters/opencode/plugin/package.json", {"name": "aiea-opencode-plugin", "version": version,
                                                 "type": "module", "exports": "./index.js"}),
    ):
        try:
            document = json.loads((root / relative).read_text(encoding="utf-8"))
            if not isinstance(document, dict) or any(document.get(key) != value for key, value in expected.items()):
                errors.append(f"{relative}: adapter metadata must match AIEA name, version, and layout")
        except (OSError, ValueError) as error:
            errors.append(f"{relative}: {error}")
    if not (root / "adapters/opencode/plugin/index.js").is_file():
        errors.append("OpenCode plugin entrypoint is missing")
    return errors


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


# --- version registry -------------------------------------------------------
#
# `.version-bump.json` declares every file that carries the repository version.
# The same registry drives validation, drift detection, and version bumps, so a
# new host adapter is registered once instead of in several code paths.

@dataclass(frozen=True)
class VersionEntry:
    path: str
    field: str


def bump_registry(root: Path = ROOT) -> tuple[list[VersionEntry], list[str], list[str], list[str]]:
    """Return the declared version entries, audit excludes, required mentions, and errors."""
    config_path = root / BUMP_CONFIG
    if not config_path.is_file():
        return [], [], [], []
    try:
        document = json.loads(config_path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError) as error:
        return [], [], [], [f"{BUMP_CONFIG}: {error}"]
    if not isinstance(document, dict):
        return [], [], [], [f"{BUMP_CONFIG} must contain an object"]
    errors: list[str] = []
    entries: list[VersionEntry] = []
    declared = document.get("files")
    if not isinstance(declared, list) or not declared:
        errors.append(f"{BUMP_CONFIG} must define a non-empty files array")
        declared = []
    for entry in declared:
        if (not isinstance(entry, dict) or not isinstance(entry.get("path"), str)
                or not isinstance(entry.get("field"), str) or not entry["path"]):
            errors.append(f"{BUMP_CONFIG} entries need a path and a field")
            continue
        entries.append(VersionEntry(path=entry["path"], field=entry["field"]))
    audit = document.get("audit")
    excludes = audit.get("exclude") if isinstance(audit, dict) else []
    if not isinstance(excludes, list) or not all(isinstance(item, str) for item in excludes):
        errors.append(f"{BUMP_CONFIG} audit.exclude must be an array of strings")
        excludes = []
    mentions = document.get("must_mention") or []
    if not isinstance(mentions, list) or not all(isinstance(item, str) for item in mentions):
        errors.append(f"{BUMP_CONFIG} must_mention must be an array of strings")
        mentions = []
    return entries, excludes, mentions, errors


def _read_declared_version(root: Path, entry: VersionEntry) -> str:
    path = root / entry.path
    if entry.field == "text":
        return path.read_text(encoding="utf-8-sig").strip()
    if path.suffix.lower() in (".yaml", ".yml"):
        for line in path.read_text(encoding="utf-8-sig").splitlines():
            match = FIELD_PATTERN.match(line)
            if match and match.group(1) == entry.field:
                return _yaml_scalar(match.group(2) or "")
        raise KeyError(entry.field)
    document = json.loads(path.read_text(encoding="utf-8-sig"))
    value = document
    for part in entry.field.split("."):
        value = value[int(part)] if isinstance(value, list) and part.isdigit() else value[part]
    if not isinstance(value, str):
        raise TypeError(f"{entry.field} is not a string")
    return value


def _write_declared_version(root: Path, entry: VersionEntry, version: str) -> None:
    path = root / entry.path
    if entry.field == "text":
        path.write_text(f"{version}\n", encoding="utf-8")
        return
    if path.suffix.lower() in (".yaml", ".yml"):
        lines = path.read_text(encoding="utf-8-sig").splitlines()
        for index, line in enumerate(lines):
            match = FIELD_PATTERN.match(line)
            if match and match.group(1) == entry.field:
                lines[index] = f"{entry.field}: {version}"
                path.write_text("\n".join(lines) + "\n", encoding="utf-8")
                return
        raise KeyError(entry.field)
    original = path.read_text(encoding="utf-8-sig")
    document = json.loads(original)
    parts = entry.field.split(".")
    target = document
    for part in parts[:-1]:
        target = target[int(part)] if isinstance(target, list) and part.isdigit() else target[part]
    last = parts[-1]
    indexed = isinstance(target, list) and last.isdigit()
    previous = target[int(last)] if indexed else target.get(last)
    if not isinstance(previous, str):
        raise TypeError(f"{entry.field} is not a string")
    # Replace the value in place when it is unambiguous, so the rest of the
    # manifest keeps its original formatting.
    pattern = re.compile(r'("' + re.escape(last) + r'"\s*:\s*)"(' + re.escape(previous) + r')"')
    if len(pattern.findall(original)) == 1:
        path.write_text(pattern.sub(lambda match: match.group(1) + '"' + version + '"', original, count=1),
                        encoding="utf-8")
        return
    if indexed:
        target[int(last)] = version
    else:
        target[last] = version
    trailing = "\n" if original.endswith("\n") else ""
    path.write_text(json.dumps(document, indent=2) + trailing, encoding="utf-8")


def declared_versions(root: Path = ROOT) -> tuple[list[tuple[VersionEntry, str]], list[str]]:
    """Return every declared file's current version, plus any read errors."""
    entries, _, _, errors = bump_registry(root)
    rows: list[tuple[VersionEntry, str]] = []
    for entry in entries:
        try:
            rows.append((entry, _read_declared_version(root, entry)))
        except (OSError, KeyError, IndexError, TypeError, ValueError) as error:
            errors.append(f"{entry.path} ({entry.field}): {error}")
    return rows, errors


def version_errors(root: Path = ROOT) -> list[str]:
    """Report drift between the declared version files and stale required mentions."""
    entries, _, mentions, errors = bump_registry(root)
    if errors or not entries:
        return errors
    rows, read_errors = declared_versions(root)
    if read_errors:
        return read_errors
    values = {value for _, value in rows}
    if len(values) > 1:
        detail = ", ".join(f"{entry.path}={value}" for entry, value in rows)
        return [f"declared version files are not in sync: {detail}"]
    current = rows[0][1]
    for relative in mentions:
        path = root / relative
        if not path.is_file():
            errors.append(f"{relative}: a file that must name the current version is missing")
            continue
        if current not in path.read_text(encoding="utf-8-sig"):
            errors.append(f"{relative} does not mention the current version {current}")
    return errors


def _audit_excluded(relative: str, excludes: list[str]) -> bool:
    parts = relative.split("/")
    for pattern in excludes:
        if fnmatch.fnmatch(relative, pattern):
            return True
        if any(fnmatch.fnmatch(part, pattern) for part in parts[:-1]):
            return True
    return False


def audit_versions(root: Path = ROOT) -> list[str]:
    """Find undeclared files that still contain the current version string."""
    entries, excludes, _, errors = bump_registry(root)
    if errors:
        return errors
    rows, read_errors = declared_versions(root)
    if read_errors:
        return read_errors
    if not rows:
        return []
    values = [value for _, value in rows]
    current = max(set(values), key=values.count)
    declared = {entry.path for entry in entries}
    pattern = re.compile(r"(?<![0-9.])" + re.escape(current) + r"(?![0-9])")
    findings: list[str] = []
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        relative = path.relative_to(root).as_posix()
        if relative in declared or _audit_excluded(relative, excludes):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if pattern.search(text):
            findings.append(relative)
    return findings


def command_version(args: argparse.Namespace) -> int:
    return run_version(ROOT, new_version=args.new_version, audit=args.audit)


def run_version(root: Path = ROOT, new_version: str | None = None, audit: bool = False) -> int:
    rows, errors = declared_versions(root)
    if errors:
        print("Version registry failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    if not rows:
        print(f"No version files are declared in {BUMP_CONFIG}.", file=sys.stderr)
        return 1
    print("Declared versions:")
    for entry, value in rows:
        print(f"  {entry.path} ({entry.field})  {value}")
    values = sorted({value for _, value in rows})
    drift = len(values) > 1
    print("")
    if drift:
        print("DRIFT DETECTED - declared versions are not in sync:", file=sys.stderr)
        for value in values:
            print(f"  {value}", file=sys.stderr)
    else:
        print(f"All declared files are in sync at {values[0]}")

    if new_version:
        return _bump_version(root, new_version)
    if drift:
        return 1
    if audit:
        findings = audit_versions(root)
        print("")
        if findings:
            print(f"Undeclared files containing {values[0]}:", file=sys.stderr)
            for finding in findings:
                print(f"  {finding}", file=sys.stderr)
            print("Declare them in "
                  f"{BUMP_CONFIG} or exclude them from the audit.", file=sys.stderr)
            return 1
        print(f"No undeclared files contain the version string {values[0]}. All clear.")
    return 0


def _bump_version(root: Path, new_version: str) -> int:
    if not VERSION_PATTERN.fullmatch(new_version):
        print(f"error: '{new_version}' does not look like a version (expected X.Y.Z)", file=sys.stderr)
        return 2
    entries, _, _, errors = bump_registry(root)
    if errors:
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    # Preflight every declared file before writing, so a failure leaves the
    # repository untouched instead of half-bumped.
    try:
        for entry in entries:
            _read_declared_version(root, entry)
    except (OSError, KeyError, IndexError, TypeError, ValueError) as error:
        print(f"error: cannot read a declared version file: {error}", file=sys.stderr)
        return 1
    print("")
    print(f"Bumping all declared files to {new_version}:")
    print("")
    for entry in entries:
        try:
            previous = _read_declared_version(root, entry)
            _write_declared_version(root, entry, new_version)
        except (OSError, KeyError, IndexError, TypeError, ValueError) as error:
            print(f"error: could not update {entry.path}: {error}", file=sys.stderr)
            return 1
        print(f"  {entry.path} ({entry.field})  {previous} -> {new_version}")
    print("")
    print("Done. Running audit to check for missed files.")
    print("")
    findings = audit_versions(root)
    if findings:
        print("Undeclared files still contain the version string:", file=sys.stderr)
        for finding in findings:
            print(f"  {finding}", file=sys.stderr)
        return 1
    print("No undeclared files contain the version string. All clear.")
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
    info.create_system = 3  # Fixed Unix metadata, including on Windows.
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

    is_plugin = args.host in PLUGIN_HOSTS
    if args.host == "claude-code-plugin":
        plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
        # The standalone bundle uses Claude Code's standard skills/ layout.
        plugin.pop("skills", None)
        add_payload(".claude-plugin/plugin.json", (json.dumps(plugin, indent=2) + "\n").encode("utf-8"))
    elif args.host == "codex-plugin":
        plugin = json.loads((ROOT / ".codex-plugin/plugin.json").read_text(encoding="utf-8"))
        plugin["skills"] = "./skills/"
        add_payload(".codex-plugin/plugin.json", (json.dumps(plugin, indent=2) + "\n").encode("utf-8"))
        marketplace = {
            "name": "aiea-marketplace", "interface": {"displayName": "AI Engineering Army"},
            "plugins": [{"name": PLUGIN_NAME, "source": {"source": "local", "path": "./"},
                         "policy": {"installation": "AVAILABLE", "authentication": "ON_USE"},
                         "category": "Productivity"}],
        }
        add_payload(".agents/plugins/marketplace.json", (json.dumps(marketplace, indent=2) + "\n").encode("utf-8"))
    elif args.host == "opencode-plugin":
        for name in ("package.json", "index.js"):
            add_payload(name, (ROOT / "adapters/opencode/plugin" / name).read_bytes())
        index = [{"name": skill.name, "description": skill.description} for skill in selected]
        add_payload("skills-index.json", (json.dumps(index, indent=2) + "\n").encode("utf-8"))

    add_payload("LICENSE" if is_plugin else "AIEA-LICENSE.txt", (ROOT / "LICENSE").read_bytes())

    plugin_installation = {
        "claude-code-plugin":
        "Extract into a separate plugin directory, then run `claude --plugin-dir ./aiea-plugin` "
        "using the extracted directory's actual path. In Claude Code invoke `/ai-engineering-army:aiea-bootstrap`.\n\n",
        "codex-plugin":
        "Extract into a separate directory, keeping hidden folders. Run `codex plugin marketplace add /path/to/extracted-plugin` "
        "then `codex plugin add ai-engineering-army@aiea-marketplace`. Start a new session and request `aiea-bootstrap`. "
        "These host commands update your plugin configuration.\n\n",
        "opencode-plugin":
        'Extract into a separate directory. In the target project, merge `"plugins": ["/absolute/path/to/extracted-plugin"]` '
        'into `opencode.json(c)`, preserving existing entries. Requires OpenCode 2; restart the host and request `aiea-bootstrap`. '
        'The adapter reads bundled skills and registers them; it adds no hooks, tools, or network calls.\n\n',
    }
    installation = plugin_installation.get(args.host,
        f"Extract this archive at the root of the target project. The skills will be placed under `{install_path}/`.\n\n"
    )
    install_readme = (
        f"# AIEA {version} package for {args.host}\n\n" + installation +
        "Review skill contents and adapter code before enabling them in an agent host. "
        "The package does not install an agent, grant tools, or configure permissions.\n\n"
        "Start a new host session, ask it to load `aiea-bootstrap`, and give it your task, "
        "acceptance checks, and a repair-attempt budget. Automatic activation is not guaranteed. "
        "If a skill is missing, report it rather than claiming it loaded.\n\n"
        "Developer guide: https://github.com/himanshu231204/ai-engineering-army/blob/main/docs/getting-started.md\n"
    ).encode("utf-8")
    add_payload("AIEA-INSTALL.md", install_readme)

    manifest = {
        "name": "ai-engineering-army",
        "version": version,
        "host": args.host,
        "format": {"claude-code-plugin": "Claude Code plugin", "codex-plugin": "Codex plugin",
                   "opencode-plugin": "OpenCode 2 plugin"}.get(args.host, "Agent Skills"),
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


def command_release(args: argparse.Namespace) -> int:
    """Stage all distributions and checksums locally; never publish."""
    if command_validate(args):
        return 1
    version = VERSION_FILE.read_text(encoding="utf-8-sig").strip()
    output_dir = Path(args.output or f"dist/release-{version}").expanduser().resolve()
    if output_dir.exists():
        print(f"refusing to overwrite existing release directory: {output_dir}", file=sys.stderr)
        return 2
    try:
        output_dir.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="aiea-release-", dir=output_dir.parent) as temporary:
            stage = Path(temporary) / "bundle"
            stage.mkdir()
            for host in HOST_PATHS:
                result = command_package(argparse.Namespace(host=host, output=str(stage), skill=None))
                if result:
                    return result
            (stage / "RELEASE-NOTES.md").write_bytes((ROOT / "docs/release-notes.md").read_bytes())
            checksums = "".join(
                f"{hashlib.sha256(path.read_bytes()).hexdigest()}  {path.name}\n"
                for path in sorted(stage.iterdir())
            )
            (stage / "SHA256SUMS").write_bytes(checksums.encode("utf-8"))
            # Exclusive creation preserves existing output, including an empty
            # directory. Copy files instead of relying on directory renames,
            # which some Windows sandboxes do not permit.
            output_dir.mkdir()
            for path in sorted(stage.iterdir()):
                with (output_dir / path.name).open("xb") as destination:
                    destination.write(path.read_bytes())
    except FileExistsError:
        print(f"refusing to overwrite existing release output: {output_dir}", file=sys.stderr)
        return 2
    except OSError as error:
        print(f"could not prepare release: {error}", file=sys.stderr)
        return 1
    print(f"Prepared {output_dir}. Review checks and release notes before publishing.")
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

    release = commands.add_parser("release", help="prepare all host ZIPs, release notes, and SHA256SUMS locally")
    release.add_argument("--output", help="new output directory (default: dist/release-<version>)")
    release.set_defaults(handler=command_release)

    version = commands.add_parser(
        "version",
        help="check, audit, or bump the version declared across the repository",
    )
    version.add_argument("new_version", nargs="?", help="new semantic version to write to every declared file")
    version.add_argument("--check", action="store_true", help="report declared versions and detect drift")
    version.add_argument("--audit", action="store_true", help="also scan the repository for undeclared version references")
    version.set_defaults(handler=command_version)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.handler(args)


if __name__ == "__main__":
    raise SystemExit(main())


