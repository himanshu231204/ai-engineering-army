# Design principles

- **Portable by default:** use the Agent Skills file format and plain Markdown; isolate host-specific metadata in adapters.
- **Progressive disclosure:** keep skill descriptions concise and load detailed guidance only when relevant.
- **Small contracts:** define specialist scope, inputs, outputs, and write permissions. Do not encode fictional biographies or excessive roleplay.
- **One writer:** parallelize analysis when safe; serialize edits to shared code.
- **Evidence-based:** tie completion claims to observed checks, diffs, or other artifacts.
- **Bounded autonomy:** state limits for delegation and repair; surface ambiguity and blocked checks.
- **Least privilege:** grant only the tools and access needed for the task.
- **User control:** explain material actions, preserve reviewable changes, and ask before external or irreversible operations.
- **Independent evolution:** keep optional services and benchmarks outside the portable skill core.
