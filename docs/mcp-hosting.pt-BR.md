# Hospedar e conectar o MCP remoto

O MCP hospedado mantém o progresso entre conversas e clientes compatíveis. O toolkit local continua disponível sem conta ou serviço remoto. O modelo de IA roda no cliente MCP do estudante; o Worker não chama um provedor de modelos.

## O que o serviço armazena

O Google OpenID Connect autentica a pessoa. O Worker implementa OAuth 2.1 para clientes MCP, com PKCE S256, consentimento por cliente, atualização e revogação de tokens. O D1 guarda um identificador interno do Google, o perfil de estudo e um histórico append-only de avaliações. Não guarda e-mail, prompts ou transcrições.

As evidências são enviadas pelo modelo tutor após uma resposta real do estudante. O servidor valida o formato e grava o evento; não verifica se a nota ou a avaliação em texto livre está correta. Confira o resultado da ferramenta e consulte `get_progress` quando houver dúvida.

## Desenvolvimento local

Requisitos: Node.js 22+, npm e Python 3.11+ para os testes existentes do toolkit. Uma conta Cloudflare só é necessária para publicar.

```sh
cd mcp-worker
npm ci
npm run typecheck
npm test
npm run dev
```

Os testes usam o runtime local `workerd`, um D1 isolado e um cliente MCP TypeScript. Cobrem duas identidades, retomada, gravações duplicadas concorrentes, ocultação de gabaritos e autorização. Eles não comprovam um fluxo real de consentimento Google, produção Cloudflare ou compatibilidade com aplicativos específicos.

## Preparar recursos e credenciais

1. Entre na conta Cloudflare que administrará o serviço: `npx wrangler login`.
2. Crie o banco D1: `npx wrangler d1 create az900-tutor-progress`.
3. Copie o `database_id` retornado para `mcp-worker/wrangler.toml`, substituindo `REPLACE_WITH_D1_DATABASE_ID`.
4. Atualize `PUBLIC_BASE_URL` com o endereço HTTPS final do Worker, por exemplo `https://az-900-tutor-mcp.<subdominio>.workers.dev`.
5. Aplique as migrações: `npm run migrate:remote`.
6. No Google Cloud Console, crie um cliente OAuth do tipo **Web application**. Adicione exatamente `<PUBLIC_BASE_URL>/oauth/google/callback` como URI de redirecionamento autorizado. Configure a tela de consentimento para o público pretendido. O escopo solicitado é somente `openid`.
7. Cadastre os segredos diretamente no Wrangler, sem colocá-los no Git:

   ```sh
   npx wrangler secret put GOOGLE_CLIENT_ID
   npx wrangler secret put GOOGLE_CLIENT_SECRET
   npx wrangler secret put TOKEN_SIGNING_SECRET
   ```

   Os dois primeiros valores vêm do Google. Gere o último com pelo menos 32 bytes aleatórios; por exemplo, `openssl rand -base64 48`.

8. Publique: `npm run deploy`.

Não use HTTP em produção. Os valores locais do `wrangler.toml` não são configuração OAuth de produção.

## Verificar antes de compartilhar

Consulte os metadados do servidor de recursos e do servidor de autorização definidos no código. Faça uma chamada a `POST /mcp) sem token e confirme que a resposta é `401` com o desafio `resource_metadata`. Em seguida, complete o consentimento Google e teste o fluxo inteiro com um cliente MCP real:

1. conectar e autorizar;
2. consultar `get_profile` e inicializar `update_profile`;
3. obter plano, aula e questão;
4. responder e gravar uma evidência real com `record_assessment`;
5. verificar em `get_progress` e exportar;
6. desconectar e reconectar para confirmar a continuidade;
7. solicitar exclusão e confirmar que perfil e evidências foram removidos.

Registre cliente, versão, sistema operacional, data e quais etapas passaram. Um teste local não deve ser descrito como teste de produção. O repositório não promete compatibilidade universal entre clientes.

## Conectar um cliente

Adicione a URL `<PUBLIC_BASE_URL>/mcp) pelo fluxo de conexão MCP remoto / Streamable HTTP do cliente e autorize com a conta Google usada nos estudos. Os nomes dos menus variam entre aplicativos. O cliente precisa suportar MCP remoto, OAuth e ferramentas de escrita.

Na primeira sessão, consulte `get_profile` e use `update_profile` para definir prazo, minutos disponíveis, idioma e experiência. Ao voltar, use `get_profile`, `get_progress` e `get_study_plan`. O mesmo sujeito Google recupera o mesmo registro em outro cliente compatível.

Se o cliente não gravar e confirmar ferramentas de forma confiável, use o toolkit local e o fluxo de exportação/importação.

## Privacidade e operações

Respostas e equívocos podem ser dados pessoais. Obtenha autorização antes de armazenar esse histórico no serviço. Os dados ficam no D1 até o estudante usar `delete_progress` ou o operador excluir o banco. A limpeza diária remove transações OAuth expiradas, códigos usados/expirados, tokens revogados/expirados e registros inativos de clientes com mais de 90 dias. Tokens de acesso já emitidos podem continuar válidos por até 15 minutos. Revogue as credenciais pelo fluxo de desconexão do cliente ou ferramenta de revogação.

Não registre corpos de requisição, tokens, respostas ou saídas de ferramentas em logs. A Cloudflare e administradores autorizados da conta fazem parte da fronteira de confiança. Restrinja acesso à conta e ao D1. Exports contêm dados de aprendizagem e devem ficar em local privado. A integridade detecta alterações acidentais; não autentica uma alegação de aprendizagem.

Mantenha migrações aditivas e compatíveis. Aplique `npm run migrate:remote` antes de publicar código que dependa de uma migração. Para voltar o Worker, use `npx wrangler rollback [VERSION_ID]`. Isso não desfaz migrações nem restaura dados apagados; corrija o esquema com uma migração posterior. Rotacionar `TOKEN_SIGNING_SECRET` exige reautorização porque invalida tokens existentes.

O serviço não usa Vectorize, Durable Objects, KV, RAG nem chamadas pagas a modelos. Confira os [preços atuais da Cloudflare Workers e D1](https://developers.cloudflare.com/workers/platform/pricing/) antes de estimar orçamento.

## Limites do caminho hospedado

O estudante precisa confiar no operador do serviço com as evidências enviadas. O modelo pode deixar de salvar, registrar uma avaliação incorreta ou afirmar que salvou sem conferir o retorno. As instruções pedem que ele confirme a gravação, mas cada cliente pode se comportar de forma diferente. Open answers continuam sendo julgamentos do modelo; o servidor não é um avaliador independente.

Para decisões de estudo, consulte o progresso salvo e use evidências reais. O tutor ajuda a organizar preparação, mas não garante aprovação na certificação.
