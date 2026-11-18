"""Rebuild the two modified OFL fonts; fonttools==4.68.0 is a build-only tool."""

import argparse
import csv
from hashlib import sha256
from pathlib import Path
from urllib.request import urlopen

from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont


def rebuild(directory, cache_directory):
    with (directory / "font-manifest.tsv").open(newline="") as manifest:
        records = list(csv.DictReader(manifest, delimiter="\t"))
    for record in records:
        filename = record["file"]
        if not filename.startswith("HMS"):
            continue
        source_url = record["source_url"]
        cache_path = cache_directory / source_url.rsplit("/", 1)[1]
        if not cache_path.exists():
            with urlopen(source_url, timeout=60) as response:
                cache_path.write_bytes(response.read())
        if sha256(cache_path.read_bytes()).hexdigest() != record["source_sha256"]:
            raise ValueError(f"Source checksum mismatch: {cache_path.name}")
        font = TTFont(cache_path, recalcTimestamp=False)
        font = instantiateVariableFont(font, {"wght": 400}, inplace=True)
        options = subset.Options()
        options.name_IDs = ["*"]
        options.name_legacy = True
        options.name_languages = ["*"]
        options.layout_features = ["*"]
        options.hinting = False
        if filename == "HMSCJK-Regular.ttf":
            ranges = (
                (0x20, 0x7F),
                (0x2E80, 0xA000),
                (0xAC00, 0xD7B0),
                (0xF900, 0xFB00),
                (0xFE10, 0xFE20),
                (0xFE30, 0xFE50),
                (0xFF00, 0xFFF0),
            )
            family = "HMS CJK"
        else:
            ranges = ((0x1100, 0x1200), (0x3130, 0x3190), (0xAC00, 0xD7B0))
            family = "HMS Korean"
        subsetter = subset.Subsetter(options=options)
        subsetter.populate(
            unicodes={code for start, end in ranges for code in range(start, end)}
        )
        subsetter.subset(font)
        names = {
            1: family,
            2: "Regular",
            3: f"{family} Regular",
            4: f"{family} Regular",
            6: filename.removesuffix(".ttf"),
            16: family,
            17: "Regular",
        }
        for name in font["name"].names:
            if name.nameID in names:
                name.string = names[name.nameID].encode(name.getEncoding())
        output = directory / filename
        font.save(output)
        print(f"{filename}\t{sha256(output.read_bytes()).hexdigest()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache-directory", type=Path, required=True)
    args = parser.parse_args()
    args.cache_directory.mkdir(parents=True, exist_ok=True)
    rebuild(
        Path(__file__).resolve().parents[2] / "payments/fonts", args.cache_directory
    )
