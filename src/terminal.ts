/*
 * terminal: a shell session in a rounded frame. Each command is typed a key at a
 * time, its output prints line by line and scrolls, and a clear starts over.
 */
import type { Frame, Meta } from "../types.ts";

export interface TerminalOptions {
  [key: string]: unknown;
  prompt: string;
  title: string;
}

export const meta = {
  name: "terminal",
  category: "ui",
  note: "a shell session: typed commands, output, scrolling, clear",
  cols: 62,
  rows: 11,
  fps: 20,
  options: { prompt: "y4ng ~ $", title: "~/research" },
} satisfies Meta<TerminalOptions>;

// Each command: what is typed, seconds before its output, then the output.
// A number in the output is a pause before the next line.
const SESSION: [string, number, (string | number)[] | null][] = [
  ["cat interests.txt", 0.15, ["binary exploitation", "LLM4Sec / AI", "kernel security", 2.5]],
  ["cat teams.txt", 0.12, ["BITs2Sys  / co-founder", "NeSE      / member", 2.5]],
  ["echo keep exploring", 0.12, ["keep exploring", 2.5]],
  ["clear", 0, null],
];

function mulberry32(a: number) {
  return () => {
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

interface Step {
  cmd: string;
  shown: number;
  keys: number[];
  lines: [number, string][];
  enter?: number;
}

export let duration = 0;
export default function terminal({ prompt = meta.options.prompt, title = meta.options.title }: Partial<TerminalOptions> = {}): Frame {
  const { cols, rows } = meta;
  const inner = cols - 4;
  const view = rows - 2;
  const rand = mulberry32(5);
  const head = prompt + " ";

  // Lay the session out in time once: when each prompt shows, each key lands,
  // and each output line prints. The loop ends the moment clear runs.
  const steps: Step[] = [];
  let at = 0;
  for (const [cmd, wait, out] of SESSION) {
    const s: Step = { cmd, shown: at, keys: [], lines: [] };
    at += 0.9 + rand() * 0.6;
    for (let i = 0; i < cmd.length; i++) {
      s.keys.push(at);
      at += 0.06 + rand() * 0.07 + (cmd[i] === " " ? rand() * 0.12 : 0) + (rand() < 0.04 ? 0.35 : 0);
    }
    s.enter = at + 0.12;
    at = s.enter + wait;
    for (const line of out || []) {
      if (typeof line === "number") at += line;
      else s.lines.push([(at += 0.035), line]);
    }
    at += 0.05;
    steps.push(s);
  }
  const period = steps[steps.length - 1].enter! + 0.1;
  duration = period;
  // Open on the interests; retain the upstream deterministic typing and cursor.
  const start = steps[0].enter! + 0.3;

  const cell = (s: string) => (s.length > inner ? s.slice(0, inner) : s.padEnd(inner));
  return (t) => {
    const now = (((t + start) % period) + period) % period;
    const lines: string[] = [];
    let cursor: [number, number] | null = null; // [line index, column]
    let ref = 0; // the moment the cursor last moved, for the blink
    for (const s of steps) {
      if (s.shown > now) break;
      const typed = s.keys.filter((k) => k <= now).length;
      lines.push(head + s.cmd.slice(0, typed));
      ref = typed ? s.keys[typed - 1] : s.shown;
      if (now < s.enter!) {
        cursor = [lines.length - 1, head.length + typed];
        break;
      }
      ref = s.enter!;
      for (const [k, line] of s.lines) {
        if (k > now) break;
        lines.push(line);
        ref = k;
      }
      // While the command runs the cursor waits at the start of the next line.
      cursor = [lines.length, 0];
    }
    const top = Math.max(0, lines.length + (cursor && cursor[0] === lines.length ? 1 : 0) - view);
    // Solid while keys land, blinking once the cursor has sat still.
    const blink = (now - ref) % 1 < 0.55;
    const body: string[] = [];
    for (let r = 0; r < view; r++) {
      const i = top + r;
      let s = cell(lines[i] ?? "");
      if (cursor && cursor[0] === i && blink && cursor[1] < inner) s = s.slice(0, cursor[1]) + "█" + s.slice(cursor[1] + 1);
      body.push("│ " + s + " │");
    }
    const name = title ? "─ " + title.slice(0, cols - 6) + " " : "";
    return ["╭" + (name + "─".repeat(cols)).slice(0, cols - 2) + "╮", ...body, "╰" + "─".repeat(cols - 2) + "╯"].join("\n");
  };
}

