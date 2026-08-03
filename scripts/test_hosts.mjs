import assert from 'assert';
import { normalizeHosts, validateHosts } from './lib/articles.js';

assert.deepStrictEqual(normalizeHosts(undefined), []);
assert.deepStrictEqual(normalizeHosts(null), []);
assert.deepStrictEqual(normalizeHosts([]), []);

const hosts = normalizeHosts([
  { name: 'IndieDB', url: 'https://www.indiedb.com/engines/blazium-engine/news/steam-module' },
  { name: 'itch.io', url: 'https://blazium.itch.io/steam-module' },
  { name: 'Dup', url: 'https://www.indiedb.com/engines/blazium-engine/news/steam-module' },
]);
assert.strictEqual(hosts.length, 2);
assert.strictEqual(hosts[0].name, 'IndieDB');
assert.strictEqual(hosts[1].name, 'itch.io');

assert.strictEqual(validateHosts('nope'), 'hosts must be an array of { name, url } objects');
assert.ok(validateHosts([{ name: '', url: 'https://x.test' }]));
assert.ok(validateHosts([{ name: 'X', url: '/relative' }]));
assert.strictEqual(validateHosts([{ name: 'X', url: 'https://x.test' }]), null);

console.log('test_hosts: ok');
