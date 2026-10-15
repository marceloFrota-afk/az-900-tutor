Dá para aproveitar bem esses 90 minutos. **Não consigo dizer se você vai passar sem ver seu desempenho** — e acertar só identidade e governança não garante aprovação. Vamos usar o tempo para corrigir essas lacunas e conferir o restante.

Governança e gerenciamento representam **30–35% da prova**; identidade também faz parte do conteúdo. A prova abrange ainda conceitos de nuvem e arquitetura/serviços. [Guia oficial AZ-900](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/az-900).

**Seu plano de 90 minutos**

| Tempo | O que fazer |
|---|---|
| 0–10 min | Responda às seis questões abaixo antes de ler a revisão. Marque as respostas em que chutou. |
| 10–30 min | Revise identidade e explique os conceitos em voz alta, sem consultar. |
| 30–55 min | Revise governança e refaça as questões que errou. |
| 55–75 min | Faça questões da avaliação prática oficial, incluindo outros assuntos da prova. |
| 75–90 min | Revise os erros e os acertos por chute. Para cada um, explique por que a alternativa correta serve e a sua não. |

**Diagnóstico — responda antes de continuar**

1. Qual serviço estabelece a identidade de quem está entrando? **A)** Azure Policy **B)** Microsoft Entra ID **C)** Resource locks.
2. Uma pessoa precisa visualizar a configuração dos recursos, sem alterá-los. Qual mecanismo concede esse acesso? **A)** Azure RBAC **B)** Azure Policy **C)** Management groups.
3. A empresa quer restringir a criação de recursos a regiões aprovadas. Use **A)** Resource locks **B)** Azure Policy **C)** Reader.
4. Para proteger um recurso contra exclusão pelo plano de controle, use **A)** Resource lock **B)** Autenticação **C)** Resource group.
5. Qual hierarquia está correta? **A)** Subscription → management group → recurso **B)** Management group → subscription → resource group → recurso.
6. O papel Reader sobre um recurso de armazenamento garante acesso ao conteúdo armazenado? **A)** Sim **B)** Não.

**Revisão de identidade — “quem é?” e “o que pode fazer?”**

- **Microsoft Entra ID / autenticação:** estabelece a identidade de quem entra.
- **Azure RBAC / autorização:** define quais ações uma identidade pode realizar nos recursos e em qual escopo.
- Os escopos incluem management group, subscription, resource group e recurso. Uma atribuição em um escopo superior pode ser herdada pelos inferiores.
- **Reader:** permite visualizar configurações. Isso, por si só, não concede acesso aos dados armazenados.

Exemplo: entrar com sua conta responde “quem é você?”. Poder alterar uma máquina virtual depende das permissões atribuídas. [RBAC na documentação oficial](https://learn.microsoft.com/en-us/azure/role-based-access-control/overview).

**Revisão de governança — organize, estabeleça regras e proteja**

- **Management groups** organizam subscriptions; **subscriptions** contêm resource groups; **resource groups** contêm recursos.
- **Azure Policy:** avalia e aplica regras aos recursos. Pense em “quais regiões são permitidas?”.
- **Resource locks:** protegem alterações no plano de controle. Um bloqueio contra exclusão do recurso não protege, por si só, a exclusão dos dados dentro dele.
- Para escolher: **permissão de uma pessoa → RBAC; regra para recursos → Policy; proteção contra exclusão do recurso → lock.** [Policy](https://learn.microsoft.com/en-us/azure/governance/policy/overview), [locks](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/lock-resources).

**Gabarito:** 1B, 2A, 3B, 4A, 5B, 6B.

Use a [avaliação prática oficial gratuita](https://learn.microsoft.com/en-us/credentials/certifications/practice-assessments-for-microsoft-certifications) no bloco de questões. Acertar essas seis com justificativas mostra progresso nesses conceitos; não é uma previsão de aprovação nem uma revisão completa do programa.

Me envie suas seis respostas e quais foram chutes. Assim ajustamos a revisão ao que você realmente precisa hoje.