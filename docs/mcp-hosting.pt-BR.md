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

## Publicar na Cloudflare

Execute os comandos **dentro de `mcp-worker/`**, não na raiz do repositório. Se ainda não preparou as dependências do Worker:

```sh
cd mcp-worker
npm ci
```

A publicação tem duas etapas: primeiro criar o Worker e obter sua URL pública; depois configurar o Google OAuth e publicar a configuração definitiva. **Não compartilhe o endpoint com estudantes após o primeiro deploy.** A autenticação ainda não estará configurada.

### 1. Criar o D1 e fazer o primeiro deploy

1. Autentique o Wrangler: `npx wrangler login`.
2. Crie o banco D1: `npx wrangler d1 create az900-tutor-progress`.
3. Em `mcp-worker/wrangler.toml` (caminho relativo à raiz do repositório), substitua `REPLACE_WITH_D1_DATABASE_ID` pelo `database_id` retornado.
4. Aplique as migrações: `npm run migrate:remote`.
5. Crie o Worker e obtenha a URL pública: `npm run deploy`. Se o Wrangler solicitar a configuração de um subdomínio `workers.dev`, conclua essa etapa. Copie a **URL HTTPS efetivamente exibida pelo Wrangler**, normalmente `https://az-900-tutor-mcp.<subdominio-da-conta>.workers.dev`.

**Esse primeiro deploy serve apenas para inicializar o serviço.** O `wrangler.toml` começa com `PUBLIC_BASE_URL = "http://localhost:8787"`, usada no desenvolvimento local. Os metadados OAuth ainda não apontarão para a URL pública, e `/mcp` responderá `503` enquanto `TOKEN_SIGNING_SECRET` não estiver configurado. Ainda não tente conectar um cliente MCP.

### 2. Configurar a URL pública e o Google OAuth

6. Em `[vars]` de `mcp-worker/wrangler.toml`, substitua `PUBLIC_BASE_URL` pela URL HTTPS obtida no passo 5, **sem barra final e sem `/mcp`**. Se for usar domínio próprio, configure antes o roteamento e o HTTPS na Cloudflare e use essa origem pública.
7. No [Google Cloud Console](https://console.cloud.google.com/auth/clients), crie um cliente OAuth 2.0 do tipo **Web application**. Cadastre `<PUBLIC_BASE_URL>/oauth/google/callback` como URI de redirecionamento autorizado, substituindo o marcador pela **URL real**. Configure a tela de consentimento para o público pretendido. O Worker solicita somente o escopo de identidade Google `openid`.

### 3. Cadastrar os segredos e concluir a publicação

8. Cadastre as credenciais Google e o segredo de assinatura na Cloudflare, nunca no Git:

   ```sh
   npx wrangler secret put GOOGLE_CLIENT_ID
   npx wrangler secret put GOOGLE_CLIENT_SECRET
   npx wrangler secret put TOKEN_SIGNING_SECRET
   ```

   O Google fornece `GOOGLE_CLIENT_ID` e `GOOGLE_CLIENT_SECRET`. Gere `TOKEN_SIGNING_SECRET` com pelo menos 32 bytes aleatórios, por exemplo `openssl rand -base64 48`. Cada `wrangler secret put` publica uma nova versão do Worker, mas **não substitui** a etapa seguinte.

9. Publique novamente: `npm run deploy`. Assim o Worker usa o `PUBLIC_BASE_URL` corrigido no `wrangler.toml` e os segredos já cadastrados.

### 4. Validar antes de compartilhar

10. Acesse `<PUBLIC_BASE_URL>/.well-known/oauth-authorization-server` e `<PUBLIC_BASE_URL>/.well-known/oauth-protected-resource`. Confira se os metadados identificam a origem pública. Uma requisição `POST <PUBLIC_BASE_URL>/mcp` sem token deve retornar `401` com o desafio `resource_metadata`. Por fim, valide o login Google e a leitura/gravação em um cliente MCP real.

Use HTTPS na URL pública. Se mudar o domínio ou hostname do Worker, atualize **tanto** `PUBLIC_BASE_URL` quanto a URI autorizada no Google, publique novamente e repita o teste. O valor local `http://localhost:8787` não deve permanecer na configuração definitiva.

## Verificar antes de compartilhar

Consulte os metadados do servidor de recursos e do servidor de autorização definidos no código. Faça uma chamada a `POST /mcp` sem token e confirme que a resposta é `401` com o desafio `resource_metadata`. Em seguida, complete o consentimento Google e teste o fluxo inteiro com um cliente MCP real:

1. conectar e autorizar;
2. consultar `get_profile` e inicializar `update_profile`;
3. obter plano, aula e questão;
4. responder e gravar uma evidência real com `record_assessment`;
5. verificar em `get_progress` e exportar;
6. desconectar e reconectar para confirmar a continuidade;
7. solicitar exclusão e confirmar que perfil e evidências foram removidos.

Registre cliente, versão, sistema operacional, data e quais etapas passaram. Um teste local não deve ser descrito como teste de produção. O repositório não promete compatibilidade universal entre clientes.

## Conectar um cliente

Adicione a URL `<PUBLIC_BASE_URL>/mcp` pelo fluxo de conexão MCP remoto / Streamable HTTP do cliente e autorize com a conta Google usada nos estudos. Os nomes dos menus variam entre aplicativos. O cliente precisa suportar MCP remoto, OAuth e ferramentas de escrita.

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
