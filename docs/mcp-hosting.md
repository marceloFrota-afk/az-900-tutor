# Hosted AZ-900 Tutor MCP

The hosted path adds automatic continuity across conversations and MCP clients. The original local toolkit remains supported and does not require an account or cloud service.

## What runs where

- A stateless Cloudflare Worker serves the official TypeScript MCP SDK over Streamable HTTP at `/mcp`.
- Google OpenID Connect authenticates the person. The Worker implements the MCP OAuth 2.1 authorization-server endpoints, PKCE S256, per-client consent, token refresh and revocation, Protected Resource Metadata, authorization-server metadata, Client ID Metadata Documents, and Dynamic Client Registration as a compatibility fallback.
- D1 stores an internal Google subject identifier, one profile per student, and append-only assessment events. No Google email is stored. Tutor prompts, curriculum and original questions are versioned with the Worker.
- The model belongs to the student's MCP client. The service does not call an LLM.

The durable contract remains state v1. The profile and evidence ledger can be exported and imported by `scripts/tutor.py`. `import_progress` merges events idempotently and accepts an explicit reviewed mapping plan for curriculum-version changes. It never silently maps changed objectives.

## Local development

Requirements: Node.js 22 or later, npm, Python 3.11+ for the existing toolkit tests, and a Cloudflare account only for deployment.

```sh
cd mcp-worker
npm ci
npm run typecheck
npm test
npm run dev
```

`npm test` runs the Worker inside Cloudflare's local `workerd` test runtime with an isolated local D1 database. It includes a real MCP TypeScript client, two separate authenticated test identities, reconnect/resume, duplicate concurrent writes, question-key withholding, and authorization checks. These are local integration tests; they do not verify Google credentials, production Cloudflare, or any named AI application.

## Deploy to Cloudflare

Run these commands **from `mcp-worker/`**, not the repository root. If you have not installed the Worker dependencies yet:

```sh
cd mcp-worker
npm ci
```

Deployment has two stages: first create the Worker to obtain its public URL, then configure Google OAuth and publish the final settings. **Do not share the endpoint with students after the first deploy.** Authentication is not configured yet.

### 1. Create D1 and deploy the Worker for the first time

1. Authenticate Wrangler: `npx wrangler login`.
2. Create the D1 database: `npx wrangler d1 create az900-tutor-progress`.
3. In `mcp-worker/wrangler.toml` (relative to the repository root), replace `REPLACE_WITH_D1_DATABASE_ID` with the returned `database_id`.
4. Apply migrations: `npm run migrate:remote`.
5. Create the Worker and obtain its public URL: `npm run deploy`. If Wrangler asks to configure a `workers.dev` subdomain, complete that step. Copy the **actual HTTPS URL reported by Wrangler**, typically `https://az-900-tutor-mcp.<account-subdomain>.workers.dev`.

**This first deploy is only a bootstrap.** `wrangler.toml` initially contains `PUBLIC_BASE_URL = "http://localhost:8787"` for local development. OAuth metadata will not refer to the public URL yet, and `/mcp` returns `503` until `TOKEN_SIGNING_SECRET` is configured. Do not try to connect an MCP client at this stage.

### 2. Configure the public URL and Google OAuth

6. Replace `PUBLIC_BASE_URL` under `[vars]` in `mcp-worker/wrangler.toml` with the HTTPS address from step 5, **without a trailing slash or `/mcp`**. For a custom domain, first configure its routing and HTTPS in Cloudflare, and use that actual public origin instead.
7. In the [Google Cloud Console](https://console.cloud.google.com/auth/clients), create an OAuth 2.0 client of type **Web application**. Add `<PUBLIC_BASE_URL>/oauth/google/callback` as an authorized redirect URI, using the **actual URL**, not the literal placeholder. Configure the consent screen for the intended audience. The Worker requests only the Google identity scope `openid`.

### 3. Set secrets and finish deployment

8. Store the Google credentials and signing secret in Cloudflare, never in Git:

   ```sh
   npx wrangler secret put GOOGLE_CLIENT_ID
   npx wrangler secret put GOOGLE_CLIENT_SECRET
   npx wrangler secret put TOKEN_SIGNING_SECRET
   ```

   Google issues `GOOGLE_CLIENT_ID` and `GOOGLE_CLIENT_SECRET`. Generate a cryptographically random `TOKEN_SIGNING_SECRET` with at least 32 bytes, for example `openssl rand -base64 48`. Each `wrangler secret put` publishes a new Worker version, but does **not** replace the next step.

9. Deploy again: `npm run deploy`. This publishes the corrected `PUBLIC_BASE_URL` from `wrangler.toml` alongside the previously stored secrets.

### 4. Verify before sharing

10. Check `<PUBLIC_BASE_URL>/.well-known/oauth-authorization-server` and `<PUBLIC_BASE_URL>/.well-known/oauth-protected-resource`. Confirm they identify the public origin. An unauthenticated `POST <PUBLIC_BASE_URL>/mcp` must return `401` with a `resource_metadata` challenge. Finally, complete Google sign-in and a real MCP client write/read test.

Use HTTPS for the public URL. If you later change the Worker hostname or domain, update **both** `PUBLIC_BASE_URL` and the Google authorized redirect URI, then redeploy and retest. The local `http://localhost:8787` value must not remain in the final deployment.

## Connect a client

Add the deployed MCP server URL, `<PUBLIC_BASE_URL>/mcp`, using the client's remote MCP / Streamable HTTP connection flow and authorize with the Google account used for study. Clients differ in their support for OAuth, remote MCP, tool writes, and approval prompts. The repository does not claim universal client compatibility. Record tested client name, version, plan, date, and whether it completed OAuth and called `record_assessment` before advertising it as tested.

On first connection call `get_profile`; set exam deadline, available minutes, language and experience with `update_profile`. On later conversations call `get_profile`, `get_progress`, and `get_study_plan`. The same Google subject retrieves the same D1 learner record in another compatible client.

## Data and privacy

Assessment text may include a student's answer and misconceptions. Obtain the student's authorization before storing it in this hosted service. The server records only a stable provider subject, profile and assessment ledger; it does not persist conversation transcripts, model prompts, or email. D1 data remains until the student calls `delete_progress` or the operator deletes the database. Expired authorization transactions, used/expired codes, expired/revoked refresh tokens, and inactive client registrations older than 90 days are pruned daily. Expired tokens are rejected. Use `revoke` / the client's disconnect flow to revoke refresh credentials. An already-issued access token can remain usable for up to 15 minutes. Deleting progress leaves the Google identity so the student can reconnect; it deletes their profile and evidence.

Do not log request bodies, access tokens, question responses, or tool output. Cloudflare infrastructure and authorized account administrators remain part of the service trust boundary. Keep the deployment account and D1 access restricted; protect exports as personal data. The checksum detects accidental changes and does not authenticate learning claims.

A model may fail to invoke `record_assessment`, may send an inaccurate score, or may claim it saved something without checking the tool result. The MCP instructions require writing actual valid evidence and verifying tool success. The user can inspect `get_progress` or export at any time. Open-response assessments remain judgments by the model and are not independently verified by the Worker. If a client cannot reliably write tools, use the local toolkit and its explicit state export/import workflow.

## Operations and rollback

- Keep migrations additive and backward-compatible. Apply them with `npm run migrate:remote` before deploying code that depends on them.
- Review CI before deployment. `npm run typecheck`, `npm test`, `python scripts/validate.py`, and the Python unittest suite are separate checks.
- Roll back Worker code with `npx wrangler rollback [VERSION_ID]`. A Worker rollback does not reverse D1 migrations or restore deleted data. Preserve a tested older Worker version and use a forward D1 migration to repair data/schema issues.
- Delete a student's progress only through their authenticated tool call or a verified operator request. Never use real student records for acceptance tests.
- Rotate `TOKEN_SIGNING_SECRET` with a planned reauthorization because rotation invalidates existing access tokens. Rotate Google credentials in Google Cloud Console and Wrangler.

## Cost estimate

The Worker has no paid model calls. Current Cloudflare pricing lists Workers Free at 100,000 requests/day and D1 Free at 5 million rows read/day, 100,000 rows written/day, and 5 GB total storage. Workers Paid starts at US$5/month and includes 10 million Worker requests/month; D1 Paid includes the first 25 billion rows read/month, 50 million written/month and 5 GB storage before metered overage. A small tutor deployment should fit free limits at low usage; request volume, indexes, history length and concurrent OAuth registrations determine actual consumption. Google identity sign-in is subject to Google's current account and consent policies. Verify current prices before production budgeting: [Cloudflare Workers pricing](https://developers.cloudflare.com/workers/platform/pricing/).

The service stores event history in D1 and makes no Vectorize, Durable Objects, KV, RAG or model-provider calls.
