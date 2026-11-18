import re
from copy import copy
from dataclasses import dataclass
from functools import lru_cache
from io import BytesIO
from itertools import groupby
from pathlib import Path
from uuid import uuid4
from weakref import WeakKeyDictionary
from xml.sax.saxutils import escape

import uharfbuzz
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import ShapeData, TTFont
from reportlab.platypus import (
    Flowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

_FONT_FILES = (
    "NotoSans",
    "NotoSansDevanagari",
    "NotoSansBengali",
    "NotoSansGujarati",
    "NotoSansGurmukhi",
    "NotoSansKannada",
    "NotoSansMalayalam",
    "NotoSansOriya",
    "NotoSansTamil",
    "NotoSansTelugu",
    "HMSCJK",
    "HMSKorean",
)


@lru_cache(maxsize=len(_FONT_FILES))
def _font_template(family):
    """Cache immutable source faces; each receipt gets its own glyph mappings."""
    return TTFont(
        family, str(Path(__file__).with_name("fonts") / f"{family}-Regular.ttf")
    )


class _ReceiptFont(TTFont):
    # These fonts are drawn directly, without Paragraph's font-family substitution.
    _multiByte = 0

    def __init__(self, family, receipt_id):
        self.__dict__.update(_font_template(family).__dict__)
        self.fontName = f"HMS-{receipt_id}-{family}"
        self.face = copy(self.face)
        self.face.name += f"-{receipt_id}".encode("ascii")
        self.face.charToGlyph = self.face.charToGlyph.copy()
        self.face.charWidths = self.face.charWidths.copy()
        self.state = WeakKeyDictionary()
        self._codes = {}
        self._original_text = {}
        self._hb_font = uharfbuzz.Font(uharfbuzz.Face(self.face._ttf_data))

    def glyph_code(self, glyph, original):
        """Allocate a glyph AND its original cluster, including ligature text."""
        key = (glyph, original)
        if key not in self._codes:
            code = 0xF0000 + len(self._codes)
            self._codes[key] = code
            self._original_text[code] = original
            self.face.charToGlyph[code] = glyph
            self.face.charWidths[code] = self.face._pdfScale(
                self.face.hmetrics[glyph][0]
            )
        return self._codes[key]

    def addObjects(self, doc):
        """Give shaped glyphs correct ToUnicode maps, rather than private-use text.

        ReportLab handles font embedding/subsetting. Its default map assumes one
        Unicode character per glyph; Indic ligatures need whole source clusters.
        Only this receipt's font objects are modified, after normal subsetting.
        """
        state = self.state[doc]
        subsets = [list(subset) for subset in state.subsets]
        names = [
            self.getSubsetInternalName(index, doc)[1:] for index in range(len(subsets))
        ]
        super().addObjects(doc)
        for name, subset in zip(names, subsets, strict=True):
            pdf_font = doc.idToObject[name]
            cmap = doc.idToObject[pdf_font.ToUnicode.name]
            entries = []
            for index, code in enumerate(subset):
                original = self._original_text.get(code, chr(code))
                encoded = original.encode("utf-16-be").hex().upper()
                entries.append(f"<{index:02X}> <{encoded}>")
            cmap.content = (
                "/CIDInit /ProcSet findresource begin\n12 dict begin\nbegincmap\n"
                "/CIDSystemInfo << /Registry (Adobe) /Ordering (UCS) "
                "/Supplement 0 >> def\n"
                "/CMapName /HMSUnicode def\n/CMapType 2 def\n"
                f"1 begincodespacerange\n<00> <{len(subset) - 1:02X}>\n"
                "endcodespacerange\n"
                f"{len(entries)} beginbfchar\n"
                + "\n".join(entries)
                + "\nendbfchar\nendcmap\n"
                "CMapName currentdict /CMap defineresource pop\nend\nend"
            )


@dataclass
class _Cluster:
    font: _ReceiptFont
    glyphs: list
    width: float


class _ReceiptFonts:
    def __init__(self):
        self.receipt_id = uuid4().hex
        self.fonts = {}
        self.fallback_used = False

    def font(self, family):
        if family not in self.fonts:
            font = self.fonts[family] = _ReceiptFont(family, self.receipt_id)
            pdfmetrics.registerFont(font)
        return self.fonts[family]

    def family_for(self, character, previous):
        code = ord(character)
        if character in "\u200c\u200d" and previous:
            return previous
        if previous and _font_template(previous).face.charToGlyph.get(code):
            return previous
        return next(
            (
                family
                for family in _FONT_FILES
                if _font_template(family).face.charToGlyph.get(code)
            ),
            None,
        )

    def shape(self, text, size):
        runs = []
        previous = None
        for character in text:
            family = self.family_for(character, previous)
            if family is None:
                self.fallback_used = True
                family, character = "NotoSans", f"[U+{ord(character):04X}]"
            if runs and runs[-1][0] == family:
                runs[-1][1] += character
            else:
                runs.append([family, character])
            previous = family
        clusters = []
        for family, run in runs:
            font = self.font(family)
            buffer = uharfbuzz.Buffer()
            buffer.add_str(run)
            # Merge reordered marks into their source grapheme. This also keeps
            # wrapping from separating a vowel sign or part of a conjunct.
            buffer.cluster_level = uharfbuzz.BufferClusterLevel.MONOTONE_GRAPHEMES
            buffer.guess_segment_properties()
            uharfbuzz.shape(font._hb_font, buffer)
            infos, positions = buffer.glyph_infos, buffer.glyph_positions
            boundaries = sorted({info.cluster for info in infos} | {len(run)})
            ends = dict(zip(boundaries, boundaries[1:], strict=False))
            for _, group in groupby(
                zip(infos, positions, strict=True), key=lambda item: item[0].cluster
            ):
                group = list(group)
                glyphs = []
                width = 0
                for index, (info, position) in enumerate(group):
                    # A nonzero glyph is essential: a ToUnicode entry alone can
                    # make text extraction pass while the page displays tofu.
                    if info.codepoint == 0:
                        raise ValueError(
                            f"Missing shaped glyph in bundled {family} font"
                        )
                    original = (
                        run[info.cluster : ends[info.cluster]] if index == 0 else ""
                    )
                    code = font.glyph_code(info.codepoint, original)
                    scale = font.face._pdfScale
                    advance = scale(position.x_advance)
                    glyphs.append(
                        (
                            chr(code),
                            ShapeData(
                                info.cluster,
                                advance,
                                scale(position.y_advance),
                                scale(position.x_offset),
                                scale(position.y_offset),
                                font.face.charWidths[code],
                            ),
                        )
                    )
                    width += advance * size / 1000
                clusters.append(_Cluster(font, glyphs, width))
        return clusters

    def close(self):
        for font in self.fonts.values():
            font.unregister()


class _ReceiptText(Flowable):
    """Wrap and draw each font run with HarfBuzz positioning and source text."""

    def __init__(self, text, fonts, size=10, leading=16):
        super().__init__()
        self.fonts, self.size, self.leading = fonts, size, leading
        self._fixed_lines = None
        self.tokens = [
            (token, fonts.shape(token, size) if token != "\n" else [])
            for token in re.findall(r"\n|[^\S\n]+|\S+", str(text))
        ]

    def wrap(self, available_width, available_height):
        if self._fixed_lines is not None:
            self.lines = self._fixed_lines
            self.width = available_width
            self.height = len(self.lines) * self.leading
            return self.width, self.height
        self.lines = [[]]
        width = 0
        for token, clusters in self.tokens:
            if token == "\n":
                self.lines.append([])
                width = 0
                continue
            token_width = sum(cluster.width for cluster in clusters)
            if width and width + token_width > available_width:
                self.lines.append([])
                width = 0
                if token.isspace():
                    continue
            for cluster in clusters:
                if width and width + cluster.width > available_width:
                    self.lines.append([])
                    width = 0
                self.lines[-1].append(cluster)
                width += cluster.width
        self.width = available_width
        self.height = max(1, len(self.lines)) * self.leading
        return self.width, self.height

    def split(self, available_width, available_height):
        # The table already wrapped the cell at its inner width. Preserve that
        # layout: Table.splitInRow passes the full column width to split().
        if not hasattr(self, "lines"):
            self.wrap(available_width, available_height)
        count = int(available_height // self.leading)
        if count <= 0:
            return []
        if count >= len(self.lines):
            return [self]
        parts = []
        for lines in (self.lines[:count], self.lines[count:]):
            part = copy(self)
            part._fixed_lines = lines
            part.lines = lines
            part.height = len(lines) * self.leading
            parts.append(part)
        return parts

    def draw(self):
        for line_number, line in enumerate(self.lines):
            y = self.height - self.size - line_number * self.leading
            positioned = []
            x = 0
            for cluster in line:
                for character, position in cluster.glyphs:
                    positioned.append(
                        (
                            cluster.font,
                            character,
                            position,
                            x + position.x_offset * self.size / 1000,
                        )
                    )
                    x += position.x_advance * self.size / 1000
            if not positioned:
                continue
            text = self.canv.beginText(positioned[0][3], y)
            for index, (font, character, position, glyph_x) in enumerate(positioned):
                next_x = positioned[index + 1][3] if index + 1 < len(positioned) else x
                text.setFont(font.fontName, self.size)
                # Tc can position a single glyph, including an overlapping mark,
                # without turning a large mark offset into a word-space TJ
                # adjustment. The font still declares its true glyph width.
                text.setCharSpace(next_x - glyph_x - position.width * self.size / 1000)
                text.setRise(position.y_offset * self.size / 1000)
                text.textOut(character)
            text.setCharSpace(0)
            text.setRise(0)
            self.canv.drawText(text)


def _render_receipt(payment, fonts):
    buffer = BytesIO()
    document = SimpleDocTemplate(
        buffer, pagesize=A4, title=f"Receipt {payment.receipt_no}", author="HMS"
    )
    styles = getSampleStyleSheet()
    heading = (
        "Payment adjustment receipt" if payment.adjustment_of_id else "Payment receipt"
    )
    story = [
        Paragraph("Hostel Management System", styles["Title"]),
        Paragraph(heading, styles["Heading1"]),
        Spacer(1, 16),
    ]
    details = [
        ("Receipt number", payment.receipt_no),
        ("Student ID", payment.student.student_id),
        ("Student name", payment.student.name),
        ("Payment date", payment.date.strftime("%d-%m-%Y")),
        ("Amount (INR)", f"{payment.amount:.2f}"),
        ("Payment mode", payment.mode),
        ("Reference", payment.reference or "None"),
    ]
    if payment.adjustment_of_id:
        details.extend(
            [
                ("Adjusts receipt", payment.adjustment_of.receipt_no),
                ("Reason", payment.adjustment_reason),
            ]
        )
    table = Table(
        [
            [
                Paragraph(escape(label), styles["Normal"]),
                _ReceiptText(value, fonts),
            ]
            for label, value in details
        ],
        colWidths=[130, 330],
        hAlign="LEFT",
        splitInRow=1,
    )
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#edf1e9")),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("LINEBELOW", (0, 0), (-1, -1), 0.5, colors.HexColor("#e3e4dc")),
            ]
        )
    )
    story.extend(
        [
            table,
            Spacer(1, 20),
            Paragraph(
                "Generated by HMS. Corrections are recorded as separate entries.",
                styles["Normal"],
            ),
        ]
    )
    if fonts.fallback_used:
        story.append(
            Paragraph(
                "Characters outside the bundled fonts are shown as [U+XXXX] "
                "Unicode code points.",
                styles["Normal"],
            )
        )
    document.build(story)
    buffer.seek(0)
    return buffer


def receipt_pdf(payment):
    fonts = _ReceiptFonts()
    try:
        return _render_receipt(payment, fonts)
    finally:
        fonts.close()
