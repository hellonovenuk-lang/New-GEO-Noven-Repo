/* Turn a JSON-serialisable value into lines of typed tokens, so a page can
 * display it as syntax-coloured code.
 *
 * The output matches `JSON.stringify(value, null, 2)` character for
 * character. That matters: the site claims the block it shows a reader is the
 * block in its own <head>, and that claim has to survive someone checking it.
 */

export type TokenKind =
  | 'indent'
  /** A schema.org keyword — @context, @type, @id. */
  | 'meta'
  | 'key'
  | 'str'
  | 'num'
  | 'bool'
  | 'null'
  | 'punct';

export type Token = { kind: TokenKind; text: string };

export type Line = {
  tokens: Token[];
  /**
   * Dotted path of the value this line opens — `name`, `founder.name`,
   * `knowsAbout[0]`. Empty on the lines that only close a brace or bracket, so
   * a caller marking a key never marks its closing line as well. This is what
   * lets a page single out particular facts without hand-counting line
   * numbers, which would silently point at the wrong fact the next time the
   * business data changes.
   */
  path: string;
};

const INDENT = '  ';

function keyTokens(key: string): Token[] {
  return [
    { kind: key.startsWith('@') ? 'meta' : 'key', text: JSON.stringify(key) },
    { kind: 'punct', text: ': ' },
  ];
}

function emit(
  value: unknown,
  depth: number,
  prefix: Token[],
  comma: boolean,
  out: Line[],
  path: string,
): void {
  const pad: Token = { kind: 'indent', text: INDENT.repeat(depth) };
  const tail: Token[] = comma ? [{ kind: 'punct', text: ',' }] : [];
  const open = (tokens: Token[]) => out.push({ tokens, path });
  const close = (tokens: Token[]) => out.push({ tokens, path: '' });

  if (value === null) {
    open([pad, ...prefix, { kind: 'null', text: 'null' }, ...tail]);
    return;
  }

  if (Array.isArray(value)) {
    if (value.length === 0) {
      open([pad, ...prefix, { kind: 'punct', text: '[]' }, ...tail]);
      return;
    }
    open([pad, ...prefix, { kind: 'punct', text: '[' }]);
    value.forEach((item, i) =>
      emit(item, depth + 1, [], i < value.length - 1, out, `${path}[${i}]`),
    );
    close([pad, { kind: 'punct', text: ']' }, ...tail]);
    return;
  }

  if (typeof value === 'object') {
    const entries = Object.entries(value as Record<string, unknown>).filter(
      ([, v]) => v !== undefined,
    );
    if (entries.length === 0) {
      open([pad, ...prefix, { kind: 'punct', text: '{}' }, ...tail]);
      return;
    }
    open([pad, ...prefix, { kind: 'punct', text: '{' }]);
    entries.forEach(([k, v], i) =>
      emit(v, depth + 1, keyTokens(k), i < entries.length - 1, out, path ? `${path}.${k}` : k),
    );
    close([pad, { kind: 'punct', text: '}' }, ...tail]);
    return;
  }

  const kind: TokenKind =
    typeof value === 'number' ? 'num' : typeof value === 'boolean' ? 'bool' : 'str';
  open([pad, ...prefix, { kind, text: JSON.stringify(value) }, ...tail]);
}

export function toLines(value: unknown): Line[] {
  const out: Line[] = [];
  emit(value, 0, [], false, out, '');
  return out;
}

/** The exact string the page head will carry, so the two can be compared. */
export function toSource(value: unknown): string {
  return JSON.stringify(value, null, 2);
}
