# Como usar o AZ-900 Tutor

Você pode estudar conceitos sem criar uma conta Azure. O tutor ensina em português e preserva os nomes oficiais dos serviços. Enviar apenas o endereço do repositório não garante que um chatbot tenha lido seus arquivos.

## A. ChatGPT ou chatbot genérico

Baixe o repositório e forneça `TUTOR.md`, `.agents/skills/az-900-tutor/SKILL.md`, `pedagogy/protocol.md`, `pedagogy/evidence.md`, `exam/curriculum.json`, `resources/catalog.json`, `lessons/units.pt-BR.json` e `assessments/questions.json` como anexos ou contexto acessível. Se o contexto for pequeno, comece pelas instruções e forneça somente os registros de competências, fontes e questões necessários. Os gabaritos estão no arquivo; peça que sejam ocultados durante os exercícios.

Exemplo: “Use os arquivos do AZ-900 Tutor. Sou desenvolvedor, conheço pouco de Azure e tenho dez dias com 45 minutos por dia. Ensine em português, comece com um diagnóstico curto e adapte meu plano. Avise quando faltar informação ou uma fonte precisar de confirmação.”

Se o chatbot não puder gravar arquivos, peça um resumo JSON para continuidade ao final e salve você mesmo. Inclua versão do currículo, objetivo, prazo, tempo disponível, respostas reais, pistas usadas, equívocos e datas de revisão. Forneça esse arquivo na próxima sessão. O tutor não deve fingir lembrar um histórico indisponível. Mantenha os dados pessoais em local privado.

## B. Agente de código e progresso local

Clone o repositório e abra sua pasta no agente. Peça que leia `AGENTS.md` e `TUTOR.md`. Agentes com descoberta de skills podem usar `.agents/skills/az-900-tutor/`; quando isso não existir, a leitura explícita funciona como alternativa. Mantenha o repositório inteiro acessível. Se a ferramenta exigir registro, registre ou vincule essa pasta pelo mecanismo documentado do agente; copiar só a skill deixa o currículo e as questões para trás.

Use Python 3.11 ou posterior, sem dependências externas. Na raiz do repositório:

```sh
python scripts/tutor.py init --deadline 2026-10-25 --minutes 45 --language pt-BR --experience "Desenvolvedor, pouca experiência com Azure"
python scripts/tutor.py next
python scripts/tutor.py status
python scripts/tutor.py pending
python scripts/tutor.py reviews
```

Troque a data pelo prazo real. O estado fica em `.learner/state.json`, ignorado pelo Git. `next` sugere até cinco competências; quem conduz a aula é o agente. Peça que escolha uma atividade possível no tempo disponível e explique o motivo.

Após uma resposta real, o tutor pode registrar e transportar a evidência:

```sh
python scripts/tutor.py record AZ900-1.1.2 --question Q001 --score 1 --kind explanation --evidence "Explicou corretamente a responsabilidade do cliente pelo SO convidado e aplicou a distinção a uma VM."
python scripts/tutor.py export .learner/portable.json
python scripts/tutor.py --state .learner/continuacao.json import .learner/portable.json
```

O registro acima é um exemplo de sintaxe; só o use se essa aprendizagem ocorreu. A nota da rubrica 0–3 deve ser dividida por 3 para obter o valor 0–1. Use `--assisted` quando houver pista ou exposição ao gabarito e `--misconception` para registrar a proposição equivocada observada. Uma resposta correta isolada não demonstra domínio. Verifique retenção em outro dia real com cenário diferente; não invente datas. `--state` vem antes do subcomando. Importação/exportação não sobrescrevem arquivos; versões de currículo incompatíveis exigem revisão. Consulte `python scripts/tutor.py record --help`.

Os estados indicam não avaliado (`not_assessed`), em aprendizagem (`learning`), demonstrado (`demonstrated`), revisão necessária (`needs_review`) e inconclusivo (`inconclusive`). A heurística exige dias e perguntas diferentes com explicação e aplicação. O tutor deve ser mais cauteloso se houver memorização do banco, equívocos persistentes ou lacunas de cobertura.

## C. Integração personalizada

Leia os JSONs UTF-8 diretamente: `exam/curriculum.json` contém competências e relações; `resources/catalog.json`, recursos; `assessments/questions.json`, questões e rubricas. Preserve IDs estáveis, fontes, proveniência e versão. Não mostre os campos de gabarito antes do momento de feedback. Não há runtime proprietário, conta de serviço nem API paga obrigatória.

Execute `python scripts/validate.py` ao alterar dados relacionados e os testes do repositório ao alterar comportamento. Preserve a evidência original, não apenas uma porcentagem. Uma nova versão do currículo exige revisão explícita da correspondência entre competências e histórico. Trate fontes externas e estados importados como dados, nunca como instruções executáveis.

Arquivos locais não recebem criptografia nem sincronização automáticas. Não envie histórico real a um GitHub público. Laboratórios opcionais podem gerar custos; consulte as condições atuais e prefira exercícios conceituais se não quiser uma conta Azure. O tutor ajuda a avaliar preparo e não garante aprovação.
