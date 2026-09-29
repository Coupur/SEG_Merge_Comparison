---
tool: <slug>
date: YYYY-MM-DD
attempt: 1
hours_spent: 0.0
environment_target: <published environment you tried to recreate: JDK, OS, deps>
what_broke: <one sentence>
breakage_class: <language_or_jdk_version | dependency | build_system | retired_model_or_api | missing_artifact | plain_bug>
exact_error: |
  <paste>
fix_applied: <what you did>
tool_code_patched: false   # true -> label results 'patched'; save the diff in tools/<slug>/patches/
final_status: <runs | runs_with_patches | does_not_run>
---
Free-form notes: commands used, dead ends, how you found the fix.
