import { readFileSync, writeFileSync } from "node:fs";

const data = readFileSync("./parse/emojiMap.json", "utf8");

const file = `import type { EmojiMap } from "./types";

export const emojiMap: EmojiMap = ${data};`;

writeFileSync("./src/emojiMap.ts", file, "utf8");
