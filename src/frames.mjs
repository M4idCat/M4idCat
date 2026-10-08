import fs from "node:fs";
import { stripTypeScriptTypes } from "node:module";
import path from "node:path";
const here = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, "$1"));
async function piece(name) {
  const text = fs.readFileSync(path.join(here, name + ".ts"), "utf8");
  return import("data:text/javascript;base64," + Buffer.from(stripTypeScriptTypes(text)).toString("base64"));
}
const big = (await piece("big-text")).default({text:"Y4NG"});
const terminalModule = await piece("terminal");
const term = terminalModule.default();
const frames = [];
for (let i=0;i<Math.ceil(terminalModule.duration*12);i++) {
  const t=i/12;
  frames.push({light:big(t,{paper:true}), dark:big(t,{paper:false}), terminal:term(t)});
}
fs.writeFileSync(path.join(here,"frames.json"), JSON.stringify(frames));

