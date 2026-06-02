from __future__ import annotations

import argparse
from pathlib import Path

from pdf_to_musicxml.converter import convert_pdf_to_musicxml, open_in_musescore


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pdf2xml",
        description="Convert a PDF score into MusicXML using Audiveris.",
    )
    parser.add_argument("input_pdf", type=Path, help="Path to the PDF score")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("out"),
        help="Directory for generated files",
    )
    parser.add_argument(
        "--audiveris-jar",
        type=Path,
        required=True,
        help="Path to the Audiveris .jar file",
    )
    parser.add_argument(
        "--java",
        default="java",
        help="Java executable to use when running Audiveris",
    )
    parser.add_argument(
        "--musescore",
        default=None,
        help="Optional MuseScore executable path for opening the result",
    )
    parser.add_argument(
        "--open",
        action="store_true",
        help="Open the exported MusicXML in MuseScore after conversion",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    input_pdf = args.input_pdf.resolve()
    output_dir = args.output_dir.resolve()
    jar_path = args.audiveris_jar.resolve()

    if not input_pdf.exists():
        parser.error(f"Input PDF does not exist: {input_pdf}")

    if input_pdf.suffix.lower() != ".pdf":
        parser.error("Input file must be a PDF")

    if not jar_path.exists():
        parser.error(f"Audiveris jar does not exist: {jar_path}")

    try:
        result = convert_pdf_to_musicxml(args.java, jar_path, input_pdf, output_dir)
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        return 1

    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="")

    print(f"Exported: {result.exported_file}")

    if args.open:
        open_code = open_in_musescore(args.musescore, result.exported_file)
        if open_code != 0:
            return open_code

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
