# PDF-SprayJS-Hunter 🛡️

**PDF-SprayJS-Hunter** is a specialized static analysis tool designed to identify malicious JavaScript embedded within PDF documents, with a specific focus on detecting **Heap-Spraying** attack patterns.

Using advanced heuristic analysis and regex-based pattern matching, it scans PDF objects, extracts hidden JS payloads (even if compressed), and scores them against known exploit delivery techniques.

---

## Features

- **Deep Extraction**: Scans all PDF objects for `/JS` and `/JavaScript` keys, resolving indirect references.
- **Auto-Decompression**: Automatically handles `FlateDecode` (zlib) streams to reveal hidden code.
- **Heap-Spray Detection**: Heuristically identifies:
    - **NOP Sleds**: Detects common shellcode "slides" like `%u9090`, `\x90`, and `%u0C0C`.
    - **Massive String Concatenation**: Identifies loops designed to exponentially grow memory-filling payloads.
    - **Memory Allocation Vectors**: Flags large array allocations used to "spray" the heap.
    - **Suspicious Functions**: Monitors for usage of `eval()`, `unescape()`, and `String.fromCharCode()`.
- **Beautiful CLI**: Uses the `rich` library for clean, colored, and tabular terminal output.
- **JS Dumping**: Optional flag to save the beautified, extracted JavaScript for manual inspection.

---

##  Tech Stack

- **Python 3.10+**
- **pypdf**: For robust PDF structure parsing.
- **jsbeautifier**: To make obfuscated/messy malware payloads readable.
- **rich**: For a premium terminal user interface.

---

##  Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ayuhzkishan/PDF-SprayJS-Hunter.git
   cd PDF-SprayJS-Hunter
   ```

2. **Install dependencies**:
   ```bash
   pip install pypdf rich jsbeautifier
   ```

---

##  Usage

Run the scanner against any suspicious PDF file:

```bash
python pdf_analyzer/main.py --file path/to/suspicious.pdf
```

### Options

| Flag | Description |
| --- | --- |
| `--file [PATH]` | **Required**. The path to the PDF document to scan. |
| `--dump-js` | Optional. Saves the extracted JavaScript into a `.js` file for further analysis. |

### Example Output

```text
Scanning: malicious_test.pdf...
Found 1240 bytes of JavaScript payloads.

[Findings Table]
Category                     Matches Found
NOP Sled                     12
Massive String Concatenation 4
Suspicious Functions         2

Verdict: HIGH CONFIDENCE Heap Spray Detected.
```

---

## How It Works

Attackers often use JavaScript inside PDFs to exploit vulnerabilities in PDF readers (like Adobe Reader or Foxit). They "spray" the heap with NOP sleds and shellcode to make memory addresses predictable.

This tool works by:
1. **Parsing**: Walking the PDF object tree to find Action dictionaries.
2. **Normalizing**: Decompressing and decoding the bytes into a UTF-8 string.
3. **Beautifying**: Formatting the JS to bypass trivial spacing obfuscation.
4. **Scoring**: Applying weighted regex patterns. Finding a NOP sled combined with a massive loop results in a **High Confidence** verdict.

---

##  Disclaimer

This tool is for **educational and security research purposes only**. It is designed to assist malware analysts and students in understanding PDF-based threats. Do not use this tool on systems you do not have explicit permission to test.

---

**Author:** [ayuhzkishan](https://github.com/ayuhzkishan)
