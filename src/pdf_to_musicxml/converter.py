from __future__ import annotations

import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ConversionResult:
    exported_file: Path
    stdout: str
    stderr: str


PREFERRED_EXTENSIONS = {
    "Compressed MusicXML (.mxl)": (".mxl",),
    "MusicXML (.musicxml)": (".musicxml", ".xml"),
    "Any available MusicXML": (".mxl", ".musicxml", ".xml"),
}


def run_audiveris(java_exe: str, jar_path: Path, input_pdf: Path, output_dir: Path) -> subprocess.CompletedProcess[str]:
    command = [
        java_exe,
        "-jar",
        str(jar_path),
        "-batch",
        "-export",
        "-output",
        str(output_dir),
        str(input_pdf),
    ]
    return subprocess.run(command, check=False, text=True, capture_output=True)


def find_musicxml(output_dir: Path, input_pdf: Path, preferred_extensions: tuple[str, ...]) -> Path | None:
    candidates = []
    for extension in ("*.mxl", "*.musicxml", "*.xml"):
        candidates.extend(output_dir.rglob(extension))

    if not candidates:
        return None

    expected_stem = input_pdf.stem.lower()

    def sort_key(path: Path) -> tuple[int, int, str]:
        stem_match = 0 if path.stem.lower() == expected_stem else 1
        preference_rank = preferred_extensions.index(path.suffix.lower()) if path.suffix.lower() in preferred_extensions else len(preferred_extensions)
        return (stem_match, preference_rank, str(path).lower())

    return sorted(candidates, key=sort_key)[0]


def convert_pdf_to_musicxml(java_exe: str, jar_path: Path, input_pdf: Path, output_dir: Path, preferred_extensions: tuple[str, ...] = PREFERRED_EXTENSIONS["Any available MusicXML"]) -> ConversionResult:
    output_dir.mkdir(parents=True, exist_ok=True)

    result = run_audiveris(java_exe, jar_path, input_pdf, output_dir)

    if result.returncode != 0:
        message = result.stderr or result.stdout or "Audiveris conversion failed."
        raise RuntimeError(message.strip())

    exported_file = find_musicxml(output_dir, input_pdf, preferred_extensions)
    if exported_file is None:
        raise RuntimeError("Conversion finished, but no MusicXML file was found.")

    return ConversionResult(exported_file=exported_file, stdout=result.stdout, stderr=result.stderr)


def open_in_musescore(musescore_exe: str | None, exported_file: Path) -> int:
    executable = musescore_exe
    if not executable:
        executable = shutil.which("musescore") or shutil.which("MuseScore4") or shutil.which("MuseScore3")

    if not executable:
        print("MuseScore executable not found, skipping --open.", file=sys.stderr)
        return 0

    process = subprocess.Popen([executable, str(exported_file)])
    return process.wait()
