import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";

// OpenCode 2 consumes the default export's id and setup fields. Keeping this
// adapter in plain JavaScript avoids a package install or SDK dependency.
export default {
  id: "aiea",
  async setup(ctx) {
    if (typeof ctx.skill?.transform !== "function") {
      throw new Error("AIEA's plugin adapter requires OpenCode 2 skill transforms; use the portable skills ZIP on older hosts.");
    }
    const index = JSON.parse(await readFile(new URL("./skills-index.json", import.meta.url), "utf8"));
    const skills = await Promise.all(index.map(async ({ name, description }) => {
      if (!/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(name)) {
        throw new Error(`Invalid packaged AIEA skill name: ${name}`);
      }
      const path = fileURLToPath(new URL(`./skills/${name}/SKILL.md`, import.meta.url));
      const source = await readFile(path, "utf8");
      return {
        id: `aiea:${name}`,
        name,
        description,
        autoinvoke: true,
        path,
        content: source.replace(/^\uFEFF?---\r?\n[\s\S]*?\r?\n---[^\S\r\n]*\r?\n/, ""),
      };
    }));
    await ctx.skill.transform((editor) => {
      for (const skill of skills) {
        if (editor.get(skill.id) || editor.list().some((existing) => existing.name === skill.name)) {
          throw new Error(`AIEA skill already registered: ${skill.name}. Choose the plugin or project-skill installation, not both.`);
        }
      }
      for (const skill of skills) editor.add(skill);
    });
  },
};
