const jsonFile = Bun.file("./emojiMap.json");

let data = await jsonFile.json();
data = JSON.stringify(data);

const file = `import type { EmojiMap } from "./types";

export const emojiMap: EmojiMap = ${data};`;

Bun.write("./emojiMap.ts", file);
