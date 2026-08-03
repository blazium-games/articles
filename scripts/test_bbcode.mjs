import assert from 'assert';
import { markdownToBbcode } from './lib/articles.js';

const identity = (h) => h;

{
  const out = markdownToBbcode('# Hello World\n\nUse `Steam.initialize(app_id)`.\n', identity);
  assert.ok(out.includes('[font_size=22]Hello World[/font_size]'), out);
  assert.ok(!out.includes('font[i]size'), out);
  assert.ok(out.includes('[code]Steam.initialize(app_id)[/code]'), out);
  assert.ok(!out.includes('app[i]id'), out);
}

{
  const out = markdownToBbcode(
    '## Key Features\n\n- **Init**: `authenticate_with_server` works\n\nSee _italic_ and __bold__ words.\n',
    identity,
  );
  assert.ok(out.includes('[font_size=20]Key Features[/font_size]'), out);
  assert.ok(out.includes('[code]authenticate_with_server[/code]'), out);
  assert.ok(out.includes('[i]italic[/i]'), out);
  assert.ok(out.includes('[b]bold[/b]'), out);
}

{
  const out = markdownToBbcode('![cover](assets/steam_code.jpg)\n', (h) => `https://cdn.blazium.app/articles/x/${h}`);
  assert.ok(out.includes('[img]https://cdn.blazium.app/articles/x/assets/steam_code.jpg[/img]'), out);
  assert.ok(!out.includes('steam[i]code'), out);
}

console.log('test_bbcode: ok');
