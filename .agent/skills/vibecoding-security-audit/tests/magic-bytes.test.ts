import test from 'node:test'
import assert from 'node:assert/strict'
import { sniff, checkUpload } from '../templates/magic-bytes.ts'

const bytes = (...n: number[]) => new Uint8Array(n)
const webp = new Uint8Array([0x52, 0x49, 0x46, 0x46, 0, 0, 0, 0, 0x57, 0x45, 0x42, 0x50, 0x56, 0x50])

test('recognizes jpeg, png, gif, webp and pdf', () => {
  assert.equal(sniff(bytes(0xff, 0xd8, 0xff, 0xe0)), 'image/jpeg')
  assert.equal(sniff(bytes(0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0)), 'image/png')
  assert.equal(sniff(bytes(0x47, 0x49, 0x46, 0x38, 0x39, 0x61, 1)), 'image/gif')
  assert.equal(sniff(webp), 'image/webp')
  assert.equal(sniff(bytes(0x25, 0x50, 0x44, 0x46, 0x2d, 0x31)), 'application/pdf')
})

test('an executable renamed to .jpg is rejected (the name is never read)', () => {
  const exe = bytes(0x4d, 0x5a, 0x90, 0x00) // "MZ" header of a Windows executable
  const r = checkUpload(exe, ['image/jpeg'])
  assert.deepEqual(r, { ok: false, reason: 'type' })
})

test('script content is rejected', () => {
  const html = new TextEncoder().encode('<script>alert(1)</script>')
  assert.equal(checkUpload(html, ['image/png']).ok, false)
})

test('allowed type but not in the allow list is rejected', () => {
  assert.deepEqual(checkUpload(bytes(0x25, 0x50, 0x44, 0x46, 0x2d), ['image/png']), { ok: false, reason: 'type' })
})

test('size limits apply (empty and oversized)', () => {
  assert.deepEqual(checkUpload(new Uint8Array(0), ['image/png']), { ok: false, reason: 'size' })
  const big = new Uint8Array(10); big.set([0xff, 0xd8, 0xff])
  assert.deepEqual(checkUpload(big, ['image/jpeg'], 5), { ok: false, reason: 'size' })
})

test('storage name is a uuid plus a safe extension, never the user filename', () => {
  const r = checkUpload(bytes(0xff, 0xd8, 0xff, 0xe0), ['image/jpeg'])
  assert.equal(r.ok, true)
  if (r.ok) {
    assert.match(r.storageName, /^[0-9a-f-]{36}\.jpg$/)
    assert.ok(!r.storageName.includes('..') && !r.storageName.includes('/'))
  }
})
