Parse the [Unicode emoji-test.txt ](https://unicode.org/Public/emoji/15.1/emoji-test.txt) file into a useful Typescript module. Use it for grouping emojis by skin tone, as one example.

- Parsing is done with Python - `parse.py` (it's way faster than Node/Bun/Deno)
- The output schema from `parse.py` is defined by `typescript-library-types.ts` which writes to `schema.json`
- The Typescript library is buiit with `npm run build-library` (requires Bun)
