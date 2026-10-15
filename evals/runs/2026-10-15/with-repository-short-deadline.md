**Dá para fazer uma revisão útil em 90 minutos. Ainda não tenho evidência para dizer se você vai passar.** Não conheço seu histórico nem avaliei suas respostas; identidade e governança são lacunas que você relatou, e os demais assuntos continuam não avaliados. Vamos priorizar essas lacunas e testar o que você consegue explicar sem consultar.

Vou usar a skill AZ-900 Tutor para conduzir uma revisão com perguntas curtas e ajustar o tempo conforme suas respostas.

O guia oficial vigente, conferido hoje, distribui o conteúdo entre conceitos de nuvem (25–30%), arquitetura e serviços (35–40%) e gerenciamento e governança (30–35%). Identidade integra o segundo domínio. Esses pesos são por domínio, não uma contagem exata de questões. [Guia da Microsoft](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/az-900).

| Minutos | Revisão e atividade |
|---|---|
| 0–5 | Diagnóstico curto, uma pergunta por vez, com justificativa. Serve para ajustar o plano, sem tentar medir a prova inteira. |
| 5–30 | Identidade: Entra ID × Domain Services; autenticação × autorização; SSO, MFA, passwordless; Conditional Access e RBAC. Explicação curta, exemplo e aplicação. |
| 30–50 | Governança: hierarquia dos recursos; Policy × RBAC × locks; propósito de Purview. Resolver cenários e corrigir confusões. |
| 50–60 | Recuperação de memória: explicar as distinções anteriores sem notas. Se houver dificuldade, usar este bloco para reparar a principal lacuna. |
| 60–75 | Prática mista: incluir responsabilidade compartilhada, computação, armazenamento e custos/monitoramento. Poucos cenários com justificativa para detectar outras lacunas. |
| 75–85 | Corrigir os erros mais importantes e tentar cenários diferentes, sem pistas. |
| 85–90 | Recordar os pontos fracos sem consultar e definir a última prioridade antes da prova. |

Não vamos tentar esgotar todos os objetivos nesse tempo. Se a base já estiver firme, transferimos minutos de explicação para prática. A [avaliação prática oficial](https://learn.microsoft.com/en-us/credentials/certifications/practice-assessments-for-microsoft-certifications) também pode complementar a revisão; seu resultado não garante aprovação.

Para começar, uma base de governança: **management groups organizam assinaturas; assinaturas contêm grupos de recursos; grupos de recursos contêm recursos**. Autorização e governança são necessidades gerais de nuvem; no Azure, RBAC define quem pode fazer quais ações em determinado escopo, enquanto Policy verifica regras sobre os recursos. Por exemplo, alguém pode ter permissão para implantar e ainda assim encontrar uma regra que proíba a região escolhida. [RBAC](https://learn.microsoft.com/en-us/azure/role-based-access-control/overview), [Azure Policy](https://learn.microsoft.com/en-us/azure/governance/policy/overview).

**Primeira pergunta, agora:** uma pessoa entra no portal com sua conta e MFA, mas recebe “acesso negado” ao tentar reiniciar uma máquina virtual. O login bem-sucedido deveria permitir essa ação? Explique o que falta verificar. Se não souber, diga até onde consegue raciocinar.

Sua explicação vai orientar o primeiro bloco. Uma resposta correta isolada não comprova preparo: ainda precisaremos observar aplicação em situações diferentes e recuperação sem ajuda. Como a prova é amanhã, também será limitada a evidência de retenção em dias diferentes. Meu julgamento atual é **evidência insuficiente, com revisão direcionada recomendada**; os 90 minutos podem reduzir lacunas, mas não permitem prometer aprovação.
