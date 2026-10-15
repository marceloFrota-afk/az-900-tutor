# AZ-900 Tutor

[English](README.md) · [Como usar](docs/usage.pt-BR.md) · [Recursos](resources/README.md)

Um kit aberto que ajuda agentes de IA a ensinar Azure Fundamentals com currículo
verificável, diagnóstico, questões autorais, feedback e revisão. Você estuda na
ferramenta que escolher, sem implantar aplicação ou criar infraestrutura cloud.
O tutor pode ensinar em português mesmo quando consulta uma fonte em inglês.

## Comece agora

**ChatGPT ou chatbot:** baixe o ZIP do repositório, extraia e anexe `TUTOR.md`, `.agents/skills/az-900-tutor/SKILL.md`,
`pedagogy/protocol.md`, `pedagogy/evidence.md`, `exam/curriculum.json`,
`resources/catalog.json`, `lessons/units.pt-BR.json` e `assessments/questions.json`. Peça ao agente para
confirmar o que conseguiu ler. Apenas enviar a URL não garante acesso aos arquivos.
Se houver limite de contexto, envie o contrato e os dados do domínio em estudo.

Copie esta mensagem:

> Use o protocolo TUTOR.md. Sou desenvolvedor, tenho pouca experiência com Azure,
> dez dias e 45 minutos por dia. Ensine em português brasileiro. Comece com um
> diagnóstico curto, uma pergunta por vez. Use minhas justificativas para avaliar
> compreensão, cite fontes e termine com um registro portátil de progresso.

**Agente de código:** clone o projeto, abra a pasta e peça para ler `AGENTS.md` e
usar `.agents/skills/az-900-tutor/SKILL.md`. A descoberta automática depende do
agente; a leitura explícita é a alternativa portátil. Mantenha o repositório inteiro
disponível. [Instruções completas](docs/usage.pt-BR.md).

**Integração própria:** os JSONs e protocolos podem ser consumidos diretamente.
Python 3.11+ é necessário apenas para os utilitários, sem instalar pacotes.

## Progresso local

Na pasta do repositório, substitua o prazo pelo seu:

```sh
python scripts/tutor.py init --deadline 2026-12-20 --minutes 45 --language pt-BR
python scripts/tutor.py next
python scripts/tutor.py pending
python scripts/tutor.py reviews
python scripts/tutor.py export .learner/portable.json
```

O agente avalia a resposta pela rubrica e usa `record` para registrar evidências;
o utilitário não corrige linguagem natural sozinho. A pasta `.learner/` não entra
no Git por padrão. Exporte com cuidado: o arquivo contém seu histórico pessoal.
Em outro ambiente, use `python scripts/tutor.py --state .learner/restored.json import .learner/portable.json`.
Se o chatbot não salvar arquivos, peça o estado em JSON, salve manualmente e
forneça esse estado na próxima sessão. Ele não deve inventar memória anterior.

## Escopo e confiança

Currículo baseado no [guia oficial](https://learn.microsoft.com/credentials/certifications/resources/study-guides/az-900?wt.mc_id=studentamb_475517)
vigente desde **20/07/2026**, verificado em **15/10/2026**. Todos os objetivos estão
mapeados, com 57 fichas didáticas essenciais e 65 questões autorais cobrindo as 57 competências. As fichas não substituem um curso completo. As fontes oficiais têm precedência sobre as comunitárias.

Acertar uma questão não comprova domínio. O protocolo pede explicação, aplicação
em outro contexto e evidências espaçadas. Os critérios são heurísticos, não uma
probabilidade de aprovação. Simulados autorais não reproduzem a prova real.

O monitor semanal/manual propõe revisão quando detecta mudanças e falha
explicitamente se não consegue interpretar a fonte. Nunca altera silenciosamente
o currículo. O agendamento só funciona após o merge na branch principal.

Links oficiais Microsoft Learn podem incluir o Contributor ID do mantenedor para atribuição no Microsoft Student Ambassadors. Isso não garante visitas qualificadas nem implica endosso da Microsoft. [Detalhes](resources/README.md#microsoft-student-ambassadors-attribution).

## Validar e contribuir

```sh
python scripts/validate.py
python -m unittest discover -s tests -v
```

Veja [CONTRIBUTING.md](CONTRIBUTING.md), [manutenção](docs/maintenance.md) e
[resultados e limitações](docs/validation.md). Não aceitamos exam dumps. Os itens
autorais ainda não têm calibração estatística nem revisão da Microsoft. O projeto
é independente; links externos mantêm seus direitos e licenças. Laboratórios podem
gerar cobrança no Azure; consulte as instruções e remova os recursos depois.

See / Veja [completion evidence](docs/completion-report.md), [teaching units](lessons/README.md) and [state migration](docs/state-migration.md).
