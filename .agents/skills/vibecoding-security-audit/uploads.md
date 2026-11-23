# File uploads

Only when users can upload files. Rule: the server decides what a file is by reading its bytes, and decides where it goes by generating the name itself.

## Checks, in order

| # | Check | How |
|---|---|---|
| 1 | Size cap before reading the body | Reject by `Content-Length` and again on the real byte count; also set it at the bucket (`file_size_limit`) |
| 2 | Real type by magic bytes | `templates/magic-bytes.ts` (`sniff`, `checkUpload`): JPEG, PNG, GIF, WebP, PDF. The extension and the client MIME are never trusted |
| 3 | Allow list of types per feature | Avatar = images only; documents = PDF only. Everything else is rejected |
| 4 | Storage name generated server-side | UUID plus an extension taken from the **detected** type; the user's filename is discarded (this also kills `../` path traversal and overwrites) |
| 5 | Private bucket by default | Public only for content meant for the whole internet; serve private files through short-lived signed URLs |
| 6 | Bucket limits | `allowed_mime_types` and `file_size_limit` set at the bucket |
| 7 | Safe serving | Separate domain or `Content-Disposition: attachment` for downloads; never serve user HTML, SVG or scripts from your own origin |
| 8 | Owner-scoped storage policies | The folder or owner column ties each object to its user (see `supabase-rls.md`) |
| 9 | Scan if files are shared between users | Malware scanning for documents other users will open |

## Use

```ts
import { checkUpload } from './magic-bytes.ts'

const result = checkUpload(bytes, ['image/jpeg', 'image/png', 'image/webp'], 5 * 1024 * 1024)
if (!result.ok) return json(400, result.reason)          // 'size' | 'type'
await storage.from('avatars').upload(`${userId}/${result.storageName}`, bytes, { contentType: result.mime })
```

Test the helper: `node --test tests/magic-bytes.test.ts` from this skill's folder.

## Audit

Run prompt 4 in `prompts.md`. Manual test: rename an `.exe` to `.jpg` and upload it (must be rejected); upload a file named `../../x.png` (must land under a generated name); upload one byte over the cap (must be rejected).
