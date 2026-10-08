/**
 * Original ASCII maid-cat mascot for M4idCat.
 * Frilled headpiece, ribbon bow, jeweled collar, apron, and curling tail.
 */
export const meta = { cols: 46, rows: 17, fps: 12 };
const ART = [
  "               .-~~~~~~~~~-.",
  "       /\\     /_/\\_/\\_/\\_/\\_\\     /\\",
  "      /  \\___/      ___      \\___/  \\",
  "     /          .--(   )--.          \\",
  "    |          /___/___\\___\\          |",
  "    |       o                 o      |",
  "    |            \\  ^  /            |",
  "----|      .      \\_w_/      .       |----",
  "     \\                             /",
  "      '._                       _.'",
  "         '-._________________.-'",
  "             >o<--<>-->o<",
  "           /  \\ \\______/ /  \\        __",
  "          |    \\________/    |     .'  )",
  "          |   /|        |\\   |____/  .'",
  "           \\ (_|________|_) /______.'",
  "            '-------------'",
];
export default function maidCat() {
  return (t: number) => {
    const lines = [...ART];
    const blink = t % 5.4 > 4.95 && t % 5.4 < 5.16;
    lines[5] = blink
      ? "    |       -                 -      |"
      : ART[5];
    const glint = t % 4.1 > 1.65 && t % 4.1 < 1.90;
    lines[11] = glint
      ? "             >o<--**-->o<"
      : ART[11];
    return lines.join("\n");
  };
}

