# Receipt fonts

Receipts embed these fonts so their output does not depend on server fonts.
The font binaries and their copyright notices are distributed under the SIL
Open Font License 1.1. The adjacent `*-OFL.txt` files are copied from upstream.
The application code is not covered by the font license.

`font-manifest.tsv` records each distributed font's SHA-256, its exact upstream
source URL pinned to a Git commit, and the source file's SHA-256. The ten
`NotoSans*-Regular.ttf` files are unmodified upstream files from
`notofonts/noto-fonts` commit
`ffebf8c1ee449e544955a7e813c54f9b73848eac`. Their license source is:

<https://raw.githubusercontent.com/notofonts/noto-fonts/ffebf8c1ee449e544955a7e813c54f9b73848eac/LICENSE>

`HMSCJK-Regular.ttf` and `HMSKorean-Regular.ttf` are modified subsets of the
Noto Sans SC and Noto Sans KR variable TrueType fonts from `notofonts/noto-cjk`
commit `f8d157532fbfaeda587e826d4cd5b21a49186f7c`. Their license source is:

<https://raw.githubusercontent.com/notofonts/noto-cjk/f8d157532fbfaeda587e826d4cd5b21a49186f7c/Sans/LICENSE>

The modified families were renamed **HMS CJK** and **HMS Korean**. They use the
static regular weight (`wght=400`), retain upstream copyright/license records,
and remove unused character ranges and hinting. `HMS CJK` retains the SC font's
default Chinese glyph forms. Japanese characters remain readable but do not
switch to Japanese regional glyph forms automatically.

## Supported text and fallback

The included fonts cover Latin, Greek, Cyrillic, Devanagari, Bengali, Gujarati,
Gurmukhi, Kannada, Malayalam, Odia, Tamil and Telugu. Han coverage includes
U+3400–U+4DB5 and U+4E00–U+9FEF. The source fonts omit the later assignments
U+4DB6–U+4DBF and U+9FF0–U+9FFF, which use the explicit fallback below. CJK
coverage also includes kana, CJK punctuation, compatibility characters, all
11,172 Hangul syllables and the Jamo present in the Korean source.
Actual support is determined from the bundled fonts' character maps; a Unicode
range alone is not treated as proof of glyph coverage.

HarfBuzz shapes script runs before rendering. The PDF embeds real glyph
outlines and maps each shaped grapheme cluster back to its original Unicode
text for copying, including conjuncts and combining marks. Wrapping keeps
these clusters together. Each receipt owns its mutable font and mapping data.

This is a bounded font set. Emoji, Arabic, Hebrew, Thai, CJK extension-B and
later ideographs, and other unbundled characters print explicit `[U+XXXX]`
code points, with an explanatory note on the receipt. This representation is
lossless and avoids a silent blank or missing-glyph square. Full bidirectional
paragraph layout and every Unicode script are outside this renderer's scope.

## Rebuilding the modified fonts

The application does not need FontTools. To rebuild the two modified subsets,
install `fonttools==4.68.0` in a separate build environment and run:

```text
python scripts/part3/rebuild_receipt_fonts.py --cache-directory PATH_TO_BUILD_CACHE
```

The script downloads only the two pinned variable sources into that cache,
verifies their source checksums, instantiates and subsets them, renames the
families, and prints their output checksums. It preserves the source timestamp
to make the generated binaries reproducible. Compare the output with
`font-manifest.tsv`; the receipt tests also verify all distributed hashes.

Verification includes exact pypdf text extraction across these scripts,
nonzero shaped glyph IDs, embedded TrueType outlines, concurrent receipts,
literal markup and unspaced-name wrapping. Rasterized receipt samples were
also inspected to confirm that text extraction was not masking missing glyphs.
