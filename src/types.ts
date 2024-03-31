export type Status = "fully-qualified" | "minimally-qualified" | "unqualified";

export type EmojiMapItem = {
  hexCodePoints: string;
  status: Status;
  emoji: string;
  version: string;
  baseName: string;
  fullName: string;
  isBase: boolean;
  baseHex: string;
  modifiers: null | {
    "1F3FB": string;
    "1F3FC": string;
    "1F3FD": string;
    "1F3FE": string;
    "1F3FF": string;
  };
};

export type EmojiMap = Record<string, EmojiMapItem>;
