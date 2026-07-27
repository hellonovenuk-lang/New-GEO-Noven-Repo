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
export type Line = Token[];

const INDENT = '  ';

function keyTokens(key: string): Token[] {
  return [
    { kind: key.startsWith('@') ? 'meta' : 'key', text: JSON.stringify(key) },
    { kind: 'punct', text: ': ' },
  ];
}

function emit(value: unknown, depth: number, prefix: Token[], comma: boolean, out: Line[]): void {
  const pad: Token = { kind: 'indent', text: INDENT.repeat(depth) };
  const tail: Token[] = comma ? [{ kind: 'punct', text: ',' }] : [];

  if (value === null) {
    out.push([pad, ...prefix, { kind: 'null', text: 'null' }, ...tail]);
    return;
  }

  if (Array.isArray(value)) {
    if (value.length === 0) {
      out.push([pad, ...prefix, { kind: 'punct', text: '[]' }, ...tail]);
      return;
    }
    out.push([pad, ...prefix, { kind: 'punct', text: '[' }]);
    value.forEach((item, i) => emit(item, depth + 1, [], i < value.length - 1, out));
    out.push([pad, { kind: 'punct', text: ']' }, ...tail]);
    return;
  }

  if (typeof value === 'object') {
    const entries = Object.entries(value as Record<string, unknown>).filter(
      ([, v]) => v !== undefined,
    );
    if (entries.length === 0) {
      out.push([pad, ...prefix, { kind: 'punct', text: '{}' }, ...tail]);
      return;
    }
    out.push([pad, ...prefix, { kind: 'punct', text: '{' }]);
    entries.forEach(([k, v], i) =>
      emit(v, depth + 1, keyTokens(k), i < entries.length - 1, out),
    );
    out.push([pad, { kind: 'punct', text: '}' }, ...tail]);
    return;
  }

  const kind: TokenKind =
    typeof value === 'number' ? 'num' : typeof value === 'boolean' ? 'bool' : 'str';
  out.push([pad, ...prefix, { kind, text: JSON.stringify(value) }, ...tail]);
}

export function toLines(value: unknown): Line[] {
  const out: Line[] = [];
  emit(value, 0, [], false, out);
  return out;
}

/** The exact string the page head will carry, so the two can be compared. */
export function toSource(value: unknown): string {
  return JSON.stringify(value, null, 2);
}
