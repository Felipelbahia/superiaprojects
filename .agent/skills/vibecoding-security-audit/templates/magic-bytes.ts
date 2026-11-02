// Server-side upload checks: detect the real type from the first bytes, never trust the extension or the client MIME.
// Works in Node 22+/Deno/Edge runtimes (no dependencies). Test: node --test tests/

const SIGNATURES: Record<string, number[][]> = {
  'image/jpeg': [[0xff, 0xd8, 0xff]],
  'image/png': [[0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]],
  'image/gif': [[0x47, 0x49, 0x46, 0x38, 0x37, 0x61], [0x47, 0x49, 0x46, 0x38, 0x39, 0x61]],
  'application/pdf': [[0x25, 0x50, 0x44, 0x46, 0x2d]],
}

const EXTENSION: Record<string, string> = {
  'image/jpeg': 'jpg', 'image/png': 'png', 'image/gif': 'gif', 'image/webp': 'webp', 'application/pdf': 'pdf',
}

const ascii = (b: Uint8Array, from: number, to: number) => String.fromCharCode(...b.slice(from, to))

/** Returns the detected MIME type, or null when the bytes match no allowed type. */
export function sniff(bytes: Uint8Array): string | null {
  for (const [mime, sigs] of Object.entries(SIGNATURES)) {
    if (sigs.some((sig) => sig.every((byte, i) => bytes[i] === byte))) return mime
  }
  if (bytes.length >= 12 && ascii(bytes, 0, 4) === 'RIFF' && ascii(bytes, 8, 12) === 'WEBP') return 'image/webp'
  return null
}

export type UploadCheck = { ok: true; mime: string; storageName: string } | { ok: false; reason: string }

/** Validates size and real type, and returns a storage name that ignores the user's filename (no `../`, no overwrite). */
export function checkUpload(bytes: Uint8Array, allowed: string[], maxBytes = 5 * 1024 * 1024): UploadCheck {
  if (bytes.length === 0 || bytes.length > maxBytes) return { ok: false, reason: 'size' }
  const mime = sniff(bytes)
  if (!mime || !allowed.includes(mime)) return { ok: false, reason: 'type' }
  return { ok: true, mime, storageName: `${crypto.randomUUID()}.${EXTENSION[mime]}` }
}
