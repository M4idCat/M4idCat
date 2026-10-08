import fs from 'node:fs';
import { stripTypeScriptTypes } from 'node:module';
const source = fs.readFileSync(new URL('./terminal.ts', import.meta.url), 'utf8');
const terminal = await import('data:text/javascript;base64,' + Buffer.from(stripTypeScriptTypes(source)).toString('base64'));
const frame = terminal.default();
fs.writeFileSync(new URL('./frames.json', import.meta.url), JSON.stringify(Array.from({length: Math.ceil(terminal.duration * 10)}, (_, i) => frame(i / 10))));
