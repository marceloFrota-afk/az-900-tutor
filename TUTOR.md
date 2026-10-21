# Start a tutoring session

Read [.agents/skills/az-900-tutor/SKILL.md](.agents/skills/az-900-tutor/SKILL.md). This is the shared behavioral contract for agents with or without native skill support. Its paths are relative to this repository root, not to the current shell directory.

The tutor uses the versioned curriculum for scope, curated resources for study, original assessments for evidence, and persisted state when available. With the authenticated hosted MCP connected, use `get_profile` and `get_progress` to resume without asking for an export. Without that connection, local files or an explicitly supplied export are the continuity path; reading this repository alone does not reveal prior sessions.

Example: “Quero estudar AZ-900. Sou desenvolvedor, conheço pouco de Azure, tenho dez dias e 45 minutos por dia. Comece com um diagnóstico curto e acompanhe meu progresso localmente.”

See [English usage](docs/usage.md) or [uso em português](docs/usage.pt-BR.md). No paid model, Azure account, or deployment is required for conceptual study. Optional labs may need an Azure subscription and incur charges; prefer the supplied no-account alternatives unless the learner chooses a lab.
