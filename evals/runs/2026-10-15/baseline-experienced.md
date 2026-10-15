Você já tem a base de infraestrutura. Em dez dias, com **7h30 no total**, eu concentraria o estudo em traduzir sua experiência para o modelo do Azure e reconhecer as diferenças que aparecem no AZ-900.

O escopo atual distribui a prova entre conceitos de nuvem (25–30%), arquitetura e serviços (35–40%) e gerenciamento e governança (30–35%). Isso pede atenção a governança, mesmo para quem já domina redes e containers. [Guia oficial do AZ-900](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/az-900)

**O que muda primeiro**

- **Organização:** recursos ficam em grupos de recursos; grupos de recursos ficam em assinaturas; grupos de gerenciamento organizam assinaturas. Essa hierarquia ajuda a entender onde aplicar acesso e governança.
- **Identidade e autorização:** Microsoft Entra autentica; Azure RBAC autoriza ações sobre recursos em determinado escopo. Poder visualizar a configuração com Reader não significa poder ler os dados armazenados.
- **Governança:** Azure Policy avalia ou impõe regras sobre recursos. Locks protegem alterações no plano de controle; não impedem, por si só, a exclusão dos dados de uma aplicação.
- **Operação:** numa VM, você continua responsável pelo sistema operacional convidado e pela aplicação. Em PaaS gerenciado, o provedor administra o sistema operacional da plataforma. Identidades, decisões de acesso e dados continuam exigindo responsabilidade do cliente.
- **Disponibilidade:** zonas isolam instalações dentro de uma região. Confira o suporte de cada serviço e região; pares de regiões e suporte a zonas não são universais.

Essas distinções estão documentadas nas referências de [RBAC](https://learn.microsoft.com/en-us/azure/role-based-access-control/overview), [Policy](https://learn.microsoft.com/en-us/azure/governance/policy/overview), [locks](https://learn.microsoft.com/en-us/azure/azure-resource-manager/management/lock-resources), [responsabilidade compartilhada](https://learn.microsoft.com/en-us/azure/security/fundamentals/shared-responsibility) e [regiões](https://learn.microsoft.com/en-us/azure/reliability/regions-overview).

**Seu plano de dez dias**

Use cada sessão assim: **5 minutos de revisão sem consulta, 20 de estudo, 15 de questões ou cenários e 5 para registrar erros**. Para cada erro, anote a distinção que faltou entender.

| Dia | Foco |
|---|---|
| 1 | Faça uma avaliação inicial e identifique lacunas no guia oficial. Revise responsabilidade compartilhada. |
| 2 | Conceitos de nuvem: passe rapidamente pelo que já conhece e concentre-se nos objetivos em que errou. |
| 3 | Hierarquia do Azure: recursos, grupos de recursos, assinaturas e grupos de gerenciamento. |
| 4 | Entra e RBAC: autenticação, autorização, escopos e acesso a dados. |
| 5 | Compute: compare VMs, App Service, containers e Functions pelos requisitos operacionais. |
| 6 | Redes e armazenamento: percorra os objetivos do guia, traduzindo os conceitos para sua experiência. |
| 7 | Regiões, zonas e disponibilidade: revise as premissas que dependem do serviço escolhido. |
| 8 | Governança: Policy, locks e demais objetivos de gerenciamento do guia. |
| 9 | Custos e ferramentas de gerenciamento indicados no guia; resolva questões desses temas. |
| 10 | Faça uma avaliação prática e use o tempo restante para corrigir as maiores lacunas. |

Use a [avaliação prática oficial](https://learn.microsoft.com/en-us/credentials/certifications/practice-assessments-for-microsoft-certifications) como diagnóstico. O objetivo é explicar por que as alternativas erradas falham, além de reconhecer a correta.

Para começar, responda a dois cenários, em uma ou duas frases cada:

1. Você precisa hospedar uma API web. Só essa informação permite escolher entre VM, App Service e containers? Que requisito pediria primeiro?
2. Uma pessoa tem Reader sobre um recurso de armazenamento. Isso basta para ler os dados? Qual distinção explica sua resposta?

Suas respostas ajudam a decidir quanto tempo dedicar a serviços e a permissões.
