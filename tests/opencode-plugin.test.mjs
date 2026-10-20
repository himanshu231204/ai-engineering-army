import assert from "node:assert/strict";
import { test } from "node:test";
import { readFile, mkdtemp, cp, rm, rmdir } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { pathToFileURL } from "node:url";

const directory = process.env.AIEA_TEST_PLUGIN;
assert.ok(directory, "Run through the Python distribution suite to build the test package");
const plugin = (await import(pathToFileURL(join(directory, "index.js")).href)).default;

function context(existing = []) {
  const skills = [...existing];
  return {
    skills,
    skill: {
      async transform(callback) {
        callback({
          list: () => skills,
          get: (id) => skills.find((skill) => skill.id === id),
          add: (skill) => skills.push(skill),
        });
      },
    },
  };
}

test("registers all nine exact packaged bodies and absolute resource paths", async () => {
  const ctx = context();
  await plugin.setup(ctx);
  assert.equal(plugin.id, "aiea");
  assert.equal(ctx.skills.length, 9);
  for (const skill of ctx.skills) {
    const source = await readFile(skill.path, "utf8");
    assert.equal(skill.content, source.replace(/^\uFEFF?---\r?\n[\s\S]*?\r?\n---[^\S\r\n]*\r?\n/, ""));
    assert.equal(skill.id, `aiea:${skill.name}`);
    assert.equal(skill.autoinvoke, true);
    assert.ok(skill.description.length > 0);
  }
  const bootstrap = ctx.skills.find((skill) => skill.name === "aiea-bootstrap");
  assert.ok((await readFile(join(bootstrap.path, "../references/discovery.md"), "utf8")).includes("bounded-repair"));
});

test("refuses a skill-name conflict before registering any partial set", async () => {
  const existing = { id: "other", name: "security-review", content: "user-owned" };
  const ctx = context([existing]);
  await assert.rejects(plugin.setup(ctx), /already registered/);
  assert.deepEqual(ctx.skills, [existing]);
});

test("reports unsupported hosts explicitly", async () => {
  await assert.rejects(plugin.setup({}), /OpenCode 2/);
});

test("missing bundled skill fails before any registration", async () => {
  const temporary = await mkdtemp(join(tmpdir(), "aiea-missing-skill-"));
  try {
    await cp(join(directory, "index.js"), join(temporary, "index.mjs"));
    await cp(join(directory, "skills-index.json"), join(temporary, "skills-index.json"));
    const incomplete = (await import(pathToFileURL(join(temporary, "index.mjs")).href)).default;
    const ctx = context();
    await assert.rejects(incomplete.setup(ctx), /ENOENT/);
    assert.deepEqual(ctx.skills, []);
  } finally {
    await rm(join(temporary, "index.mjs"), { force: true });
    await rm(join(temporary, "skills-index.json"), { force: true });
    await rmdir(temporary);
  }
});
