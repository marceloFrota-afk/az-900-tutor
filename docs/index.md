# AZ-900 Tutor

A portable tutoring kit for Microsoft Azure Fundamentals. It combines a versioned curriculum, original practice, explicit evidence, and an optional remote MCP for progress across compatible clients.

**Independent project.** It is not affiliated with or endorsed by Microsoft, does not reproduce the exam, and cannot guarantee a passing result.

## Choose a path

=== "Study with the hosted MCP"

1. Ask the project maintainer for the deployed server endpoint.
2. Connect your MCP client to the remote Streamable HTTP endpoint and authorize with Google.
3. Read your profile and progress, then ask the tutor to begin a short diagnostic.
4. Confirm that each assessment was saved before ending the session.

See [hosted setup and privacy](mcp-hosting.md) or [configuração em português](mcp-hosting.pt-BR.md).

The hosted service must be deployed by an operator. The repository does not currently promise a public endpoint or universal client support.

=== "Use the local toolkit"

1. Download or clone the repository.
2. Follow the [English study guide](usage.md) or [guia em português](usage.pt-BR.md).
3. Keep progress as a private local JSON file and export it when switching environments.

The local path needs no hosted account. Python 3.11+ is only required for progress utilities.

## For developers

- [Architecture and diagrams](architecture.md)
- [Data contracts](data-contracts.md)
- [Hosted MCP deployment, security, and operations](mcp-hosting.md)
- [State migration](state-migration.md)
- [Validation results and limitations](validation.md)
- [Contributing](https://github.com/vmenezesdev/az-900-tutor/blob/trunk/CONTRIBUTING.md)

## Comece em português

O AZ-900 Tutor é um kit portátil para estudar Azure Fundamentals com um agente de IA. Você pode usar os arquivos localmente ou, quando houver um servidor implantado, conectar um cliente MCP remoto para guardar seu progresso entre conversas.

- [Guia de uso em português](usage.pt-BR.md)
- [Configuração do MCP hospedado e privacidade](mcp-hosting.pt-BR.md)
- [Repositório e código-fonte](https://github.com/vmenezesdev/az-900-tutor)

O modelo roda no seu cliente de IA. O servidor armazena perfil e evidências de aprendizagem; não grava a conversa nem corrige respostas abertas por conta própria. Consulte os limites e a [validação do projeto](validation.md).

## What this project does and does not claim

The local toolkit and remote MCP share the state-v1 contract. The Worker stores profile settings and assessment events supplied by the tutor. It does not call a model provider, verify open-answer judgments, or infer learning from chat history. See the [architecture decision](architecture.md) and [data contract](data-contracts.md).
