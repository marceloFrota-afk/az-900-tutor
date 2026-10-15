Vou usar o roteiro da habilidade AZ-900 Tutor para concentrar seus **dez dias × 45 minutos em diferenças do Azure**. Sua experiência permite acelerar fundamentos de Linux, redes e IAM; vou checar como você os aplica ao Azure antes de decidir o que podemos abreviar. Não tenho histórico de tentativas suas.

O foco será construir um mapa de decisões: como o Azure organiza recursos, onde você concede acesso, o que continua sob sua responsabilidade e quando escolher cada serviço. Podemos trabalhar com cenários sem precisar de uma assinatura Azure.

Plano inicial, ajustável após o diagnóstico:

| Dias | Foco |
|---|---|
| 1–2 | Diagnóstico curto; responsabilidade compartilhada; hierarquia de recursos, assinaturas e regiões |
| 3–4 | Escolha entre VMs, App Service, containers e Functions; redes no Azure |
| 5–6 | Armazenamento; Microsoft Entra ID, Azure RBAC e segurança |
| 7–8 | Custos, Policy, locks, ferramentas de gestão e monitoramento |
| 9 | Cenários mistos e revisão das lacunas |
| 10 | Recuperação sem consulta, revisão final e Practice Assessment oficial |

Em cada sessão: **5 minutos de recuperação sem consulta, 20 de estudo focado, 15 de aplicação e 5 de feedback**. A partir do segundo dia, retomamos decisões anteriores com cenários diferentes para verificar retenção.

A distribuição considera o [guia oficial da AZ-900](https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/az-900): conceitos de nuvem, 25–30%; arquitetura e serviços, 35–40%; gestão e governança, 30–35%. São pesos por domínio, não contagens exatas de questões. Os dez dias são nosso orçamento inicial; a evidência das respostas vai orientar os ajustes.

Vamos começar com um diagnóstico de três cenários, **um por vez**, sem explicação prévia. Assim identificamos quais distinções realmente precisam de estudo.

**Cenário 1 — identidade e acesso**

Você entra no portal com uma identidade do Microsoft Entra ID e recebe a função **Reader** em um resource group que contém uma conta de armazenamento. Você consegue consultar a configuração da conta, mas a aplicação precisa ler os blobs armazenados nela.

Um colega afirma: “Como você já está autenticado e é Reader no grupo, também pode ler o conteúdo dos blobs”.

Você concorda? Explique a diferença entre autenticação e autorização nesse caso e qual acesso precisaria ser verificado para ler os dados. Se não souber o nome exato da função, descreva a permissão necessária. Termine indicando confiança baixa, média ou alta.
