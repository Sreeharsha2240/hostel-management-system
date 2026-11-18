"""Accepted names must survive both PDF display and copying."""

from concurrent.futures import ThreadPoolExecutor
from datetime import date
from decimal import Decimal
from hashlib import sha256
from io import BytesIO
from pathlib import Path
from types import SimpleNamespace

from django.test import SimpleTestCase
from pypdf import PdfReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFontFile

from .receipts import _FONT_FILES, _font_template, _ReceiptFonts, receipt_pdf

NAMES = (
    "Anita 测试",
    "Zoë Łukasz Ελληνικά Мария",
    "अनिता शर्मा",
    "কুন্তলা শর্মা",
    "અનિતા શર્મા",
    "ਅਨੀਤਾ ਸ਼ਰਮਾ",
    "ಅನಿತಾ ಶರ್ಮಾ",
    "അനിത ശർമ്മ",
    "ଅନିତା ଶର୍ମା",
    "அனிதா சர்மா",
    "అనిత శర్మ",
    "山田 太郎 김민수",
    "कुँवर क्षितिज",
    "Anita测试अनिता",
    "Jose\u0301 Muñoz",
)


class ReceiptUnicodeUnitTests(SimpleTestCase):
    def payment(self, name, **overrides):
        values = {
            "receipt_no": "R00000000001",
            "student": SimpleNamespace(student_id="S123", name=name),
            "date": date(2026, 11, 18),
            "amount": Decimal("125.50"),
            "mode": "UPI",
            "reference": "",
            "adjustment_of_id": None,
            "adjustment_reason": "",
        }
        return SimpleNamespace(**(values | overrides))

    def text(self, payment):
        return "\n".join(
            page.extract_text() for page in PdfReader(receipt_pdf(payment)).pages
        )

    def test_multilingual_names_are_preserved(self):
        for name in NAMES:
            with self.subTest(name=name):
                self.assertIn(name, self.text(self.payment(name)))

    def test_unsupported_characters_are_identified_without_silent_replacement(self):
        payment = self.payment("Anita 🦄 أح")
        text = self.text(payment)
        self.assertIn("Anita [U+1F984] [U+0623][U+062D]", text)
        self.assertIn(
            "Characters outside the bundled fonts are shown as [U+XXXX]", text
        )

    def test_reference_and_adjustment_reason_keep_unicode_and_literal_markup(self):
        payment = self.payment(
            "Anita",
            reference="पावती 测试 <b>&</b>",
            adjustment_of_id=1,
            adjustment_of=SimpleNamespace(receipt_no="R00000000000"),
            adjustment_reason="திருத்தம் <b>₹</b> & 测试",
        )
        text = self.text(payment)
        self.assertIn(payment.reference, text)
        self.assertIn(payment.adjustment_reason, text)

    def test_shaped_names_use_real_nonzero_embedded_glyphs(self):
        fonts = _ReceiptFonts()
        try:
            for name in NAMES:
                with self.subTest(name=name):
                    clusters = fonts.shape(name, 10)
                    self.assertFalse(fonts.fallback_used)
                    self.assertTrue(clusters)
                    for cluster in clusters:
                        for code, _ in cluster.glyphs:
                            self.assertNotEqual(
                                cluster.font.face.charToGlyph[ord(code)], 0
                            )
            # Ligatures and matras must be shaped, not drawn in codepoint order.
            conjunct = fonts.shape("क्षि", 10)
            self.assertLess(
                sum(len(cluster.glyphs) for cluster in conjunct), len("क्षि")
            )
        finally:
            fonts.close()
        document = PdfReader(receipt_pdf(self.payment("अनिता 测试")))
        embedded = [
            font.get_object()["/FontDescriptor"]["/FontFile2"].get_data()
            for font in document.pages[0]["/Resources"]["/Font"].values()
            if font.get_object().get("/Subtype") == "/TrueType"
        ]
        self.assertGreaterEqual(len(embedded), 2)
        for data in embedded:
            self.assertGreater(TTFontFile(BytesIO(data), charInfo=False).numGlyphs, 1)

    def test_concurrent_receipts_keep_independent_cluster_mappings(self):
        # Different ligatures must not replace one another's ToUnicode entries.
        names = NAMES * 2
        self.text(self.payment("Warmup"))
        registries = (
            pdfmetrics._fonts,
            pdfmetrics._typefaces,
            pdfmetrics._dynFaceNames,
        )
        before = [registry.copy() for registry in registries]
        with ThreadPoolExecutor(max_workers=4) as executor:
            texts = list(
                executor.map(lambda name: self.text(self.payment(name)), names)
            )
        for name, text in zip(names, texts, strict=True):
            self.assertIn(name, text)
            self.assertFalse(
                any(0xF0000 <= ord(character) <= 0xFFFFD for character in text)
            )
        for registry, snapshot in zip(registries, before, strict=True):
            self.assertEqual(registry, snapshot)
        for family in _FONT_FILES:
            template = _font_template(family)
            self.assertFalse(any(code >= 0xF0000 for code in template.face.charToGlyph))
            self.assertFalse(hasattr(template, "__hbUnis"))
            self.assertFalse(hasattr(template, "_codes"))

    def test_long_unspaced_names_wrap_without_losing_characters(self):
        name = "测试" * 30
        text = self.text(self.payment(name))
        value = text.split("Student name\n", 1)[1].split("\nPayment date", 1)[0]
        self.assertEqual(value.replace("\n", ""), name)

    def test_maximum_multiline_values_continue_across_pages(self):
        # These multiline values are accepted at the public form field maxima.
        name = "A" + "\n" * 58 + "B"
        reason = "A\n" * 99 + "BC"
        self.assertEqual(len(name), 60)
        self.assertEqual(len(reason), 200)
        cases = (
            (self.payment(name), "Student name", "Payment date", "AB"),
            (
                self.payment(
                    "Anita",
                    adjustment_of_id=1,
                    adjustment_of=SimpleNamespace(receipt_no="R00000000000"),
                    adjustment_reason=reason,
                ),
                "Reason",
                "Generated by HMS.",
                "A" * 99 + "BC",
            ),
        )
        self.text(self.payment("Warmup"))
        registries = (
            pdfmetrics._fonts,
            pdfmetrics._typefaces,
            pdfmetrics._dynFaceNames,
        )
        before = [registry.copy() for registry in registries]
        for payment, label, following_label, expected in cases:
            with self.subTest(field=label):
                document = PdfReader(receipt_pdf(payment))
                self.assertGreater(len(document.pages), 1)
                text = "\n".join(page.extract_text() for page in document.pages)
                value = text.split(label + "\n", 1)[1].split(following_label, 1)[0]
                self.assertEqual("".join(value.split()), expected)
                self.assertIn("Generated by HMS.", text)
                for registry, snapshot in zip(registries, before, strict=True):
                    self.assertEqual(registry, snapshot)

    def test_font_assets_match_the_pinned_manifest(self):
        directory = Path(__file__).with_name("fonts")
        for line in (directory / "font-manifest.tsv").read_text().splitlines()[1:]:
            filename, expected, _, _ = line.split("\t")
            with self.subTest(font=filename):
                self.assertEqual(
                    sha256((directory / filename).read_bytes()).hexdigest(), expected
                )
