# PDF to MusicXML converter

This project is a small local web app and command-line wrapper around a music OCR engine, designed to turn an engraved PDF score into MusicXML that can be opened in MuseScore, Dorico, Sibelius, and similar notation software.

## What it does

- Takes a PDF score as input.
- Runs Audiveris to recognize the notation and export MusicXML.
- Optionally opens the exported file in MuseScore.

## Web app

The quickest front end is the Streamlit app in [app.py](app.py). It lets you upload a PDF, choose the output format, and download the generated MusicXML.
The PDF picker supports drag and drop, the output-format selector is searchable, and Audiveris can be auto-detected or uploaded once as a jar file.

## Important limitation

This is not a generic PDF text extractor. It works best on printed or engraved scores. If the PDF is just a scanned image, the OCR quality depends on scan quality.

## Setup

1. Install Python 3.10 or newer.
2. Install Java if it is not already on your system.
3. Download Audiveris and either set the `AUDIVERIS_JAR` environment variable, place the jar somewhere common, or upload the jar in the app.

## Usage

Web app:

```bash
streamlit run app.py
```

CLI:

```bash
python pdf2xml.py input.pdf --audiveris-jar C:\path\to\audiveris.jar --output-dir out
```

Or after installing the package locally:

```bash
pdf2xml input.pdf --audiveris-jar C:\path\to\audiveris.jar --output-dir out --open
```

## Output

The converter writes the exported MusicXML file into the output directory and prints its path. If MuseScore is installed and `--open` is used, the file is opened automatically.

## Next improvements

- Add batch conversion for folders of PDFs.
- Add a small GUI.
- Add post-processing for exported MusicXML.
