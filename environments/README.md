# environments/

Each environment gets an id and a file `environments/<env_id>.md` listing: OS, Git version, JDK (tool), JDK (project), dependency versions, and for LLM arms model + version + settings + date + price.

Two axes (see architecture doc §3): `tool_env_id` (what the tool runs on) and `project_env_id` (what builds/tests the merged project). Never merge them into one field.

Seed ids (create the files as you pin them):
- `harness_2024` — whatever Schesch's committed results used (JDK 8/11/17 per project). Fill from harness `environment.yml`, `build.gradle`, and the paper; unverified until then.
- `published_<tool>` — the tool's own published environment (from its paper/README), one per tool.
- `modern_2026` — current JDK LTS + current Git + current model; pin exact versions on first use.

Pin Git explicitly: results depend on the Git version (ort/recursive).
Run everything in Docker or Linux; the harness uses `killall`, `sh`, and expects `JAVA8_HOME`, `JAVA11_HOME`, `JAVA17_HOME`.
