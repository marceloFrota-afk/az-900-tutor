import path from 'node:path';
import {cloudflareTest,readD1Migrations} from '@cloudflare/vitest-plugin';
import {defineConfig} from 'vitest/config';
export default defineConfig({
 plugins:[cloudflareTest(async()=>({
  wrangler:{configPath:'./wrangler.toml'},
  miniflare:{bindings:{PUBLIC_BASE_URL:'https://tutor.example.test',GOOGLE_CLIENT_ID:'test-client',GOOGLE_CLIENT_SECRET:'test-secret',TOKEN_SIGNING_SECRET:'test-signing-secret-at-least-32-bytes-long',TEST_MIGRATIONS:await readD1Migrations(path.resolve('migrations'))},d1Databases:{DB:'az900-tutor-progress-test'}},
 }))],
 test:{include:['test/**/*.test.ts'],maxWorkers:1}
});
