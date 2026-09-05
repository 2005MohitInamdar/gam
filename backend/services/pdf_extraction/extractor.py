"""
PDF Table Extractor
====================
Extracts fixed-schema tables from the complaint-report PDF using pdfplumber.

Tables extracted (always present, fixed columns):
  1. complaint_transactions  - main complainant transaction list   (Page 2, Table 1)
  2. pending_transactions    - transactions pending at banks       (Page 2, Table 2)
  3. amount_summary          - summary of amounts put on hold      (Page 3, Table 1)
  4. lien_transactions       - detailed lien/action table          (Pages 3-7, Table 2)
  5. hold_accounts           - per-account hold details            (Page 8)
  6. failed_transactions     - failed / zero-amount transactions   (Page 9, Table 1)
  7. no_action_references    - reference nos with no action taken  (Page 9, Table 2)
  8. complaint_meta          - complaint acceptance meta-data      (Page 9, Table 3)

Usage (standalone):
    python extractor.py <path_to_pdf> [output_directory]

    If output_directory is omitted, JSON files are written to a folder called
    `extracted_tables/` placed next to the PDF file.
"""

import json
import os
import re
import sys
from pathlib import Path

import pdfplumber


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _clean(value) -> str:
    """Collapse newlines / extra whitespace inside a cell value."""
    if value is None:
        return ""
    text = str(value)
    text = re.sub(r"[\r\n\t]+", " ", text)
    text = re.sub(r" {2,}", " ", text)
    return text.strip()


def _clean_header(header: list) -> list:
    """Return a list of cleaned header strings."""
    return [_clean(h) for h in header]


def _rows_to_dicts(header: list, rows: list) -> list:
    """
    Convert raw table rows to a list of dicts keyed by header names.
    Duplicate column names get a numeric suffix (_2, _3, ...).
    """
    seen = {}
    unique_header = []
    for col in header:
        if col in seen:
            seen[col] += 1
            unique_header.append(f"{col}_{seen[col]}")
        else:
            seen[col] = 1
            unique_header.append(col)

    records = []
    for row in rows:
        record = {}
        for col, val in zip(unique_header, row):
            record[col] = _clean(val)
        records.append(record)
    return records


def _save_json(data: dict, output_dir: Path, filename: str) -> Path:
    """Write *data* as pretty JSON to output_dir/filename; return the path."""
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / filename
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return out_path


def _extract_simple(raw_table: list, table_name: str) -> dict:
    """Generic extractor: first row = header, remaining rows = data."""
    if not raw_table:
        return {"table": table_name, "columns": [], "rows": []}
    header = _clean_header(raw_table[0])
    rows = _rows_to_dicts(header, raw_table[1:])
    return {"table": table_name, "columns": header, "rows": rows}


# ---------------------------------------------------------------------------
# Main extractor
# ---------------------------------------------------------------------------

def extract_tables(pdf_path, output_dir=None) -> dict:
    """
    Open *pdf_path*, extract all known tables, write one JSON file per table
    into *output_dir*, and return a mapping of {table_name: json_path}.

    Parameters
    ----------
    pdf_path   : str | Path  – path to the complaint PDF file
    output_dir : str | Path  – directory for JSON output.
                               Defaults to <pdf_dir>/extracted_tables/

    Returns
    -------
    dict  { table_name (str) : output_path (Path) }
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    if output_dir is None:
        output_dir = pdf_path.parent / "extracted_tables"
    output_dir = Path(output_dir)

    written = {}

    with pdfplumber.open(pdf_path) as pdf:
        pages = pdf.pages  # list, 0-indexed

        # ------------------------------------------------------------------ #
        # Page 2  (index 1) — complaint_transactions + pending_transactions   #
        # ------------------------------------------------------------------ #
        p2_tables = pages[1].extract_tables()

        if len(p2_tables) >= 1:
            payload = _extract_simple(p2_tables[0], "complaint_transactions")
            written["complaint_transactions"] = _save_json(
                payload, output_dir, "complaint_transactions.json"
            )

        if len(p2_tables) >= 2:
            payload = _extract_simple(p2_tables[1], "pending_transactions")
            written["pending_transactions"] = _save_json(
                payload, output_dir, "pending_transactions.json"
            )

        # ------------------------------------------------------------------ #
        # Page 3  (index 2) — amount_summary + start of lien_transactions     #
        # ------------------------------------------------------------------ #
        p3_tables = pages[2].extract_tables()

        if len(p3_tables) >= 1:
            payload = _extract_simple(p3_tables[0], "amount_summary")
            written["amount_summary"] = _save_json(
                payload, output_dir, "amount_summary.json"
            )

        # lien_transactions spans pages 3-7; header is on page 3
        lien_header = []
        lien_rows = []

        if len(p3_tables) >= 2:
            raw = p3_tables[1]
            lien_header = _clean_header(raw[0])
            lien_rows.extend(_rows_to_dicts(lien_header, raw[1:]))

        # Continuation pages 4-7 (indices 3-6)
        for page_idx in range(3, 7):
            cont_tables = pages[page_idx].extract_tables()
            if not cont_tables:
                continue
            raw = cont_tables[0]
            # Skip row if it's a repeated header
            first_row = _clean_header(raw[0])
            data_rows = raw[1:] if first_row == lien_header else raw
            lien_rows.extend(_rows_to_dicts(lien_header, data_rows))

        if lien_header:
            payload = {
                "table": "lien_transactions",
                "columns": lien_header,
                "rows": lien_rows,
            }
            written["lien_transactions"] = _save_json(
                payload, output_dir, "lien_transactions.json"
            )

        # ------------------------------------------------------------------ #
        # Page 8  (index 7) — hold_accounts                                   #
        # ------------------------------------------------------------------ #
        p8_tables = pages[7].extract_tables()
        if p8_tables:
            payload = _extract_simple(p8_tables[0], "hold_accounts")
            written["hold_accounts"] = _save_json(
                payload, output_dir, "hold_accounts.json"
            )

        # ------------------------------------------------------------------ #
        # Page 9  (index 8) — failed_transactions, no_action_references,      #
        #                      complaint_meta                                  #
        # ------------------------------------------------------------------ #
        p9_tables = pages[8].extract_tables()

        if len(p9_tables) >= 1:
            payload = _extract_simple(p9_tables[0], "failed_transactions")
            written["failed_transactions"] = _save_json(
                payload, output_dir, "failed_transactions.json"
            )

        if len(p9_tables) >= 2:
            payload = _extract_simple(p9_tables[1], "no_action_references")
            written["no_action_references"] = _save_json(
                payload, output_dir, "no_action_references.json"
            )

        if len(p9_tables) >= 3:
            raw = p9_tables[2]
            # Key-value layout — convert to a flat dict
            meta = {}
            for row in raw:
                if len(row) >= 2:
                    meta[_clean(row[0])] = _clean(row[1])
            payload = {"table": "complaint_meta", "data": meta}
            written["complaint_meta"] = _save_json(
                payload, output_dir, "complaint_meta.json"
            )

    return written


# ---------------------------------------------------------------------------
# CLI entry-point
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: python extractor.py <pdf_path> [output_directory]")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) >= 3 else None

    print(f"Extracting tables from: {pdf_path}")
    written = extract_tables(pdf_path, output_dir)

    print(f"\nExtracted {len(written)} table(s):")
    for name, path in written.items():
        print(f"  [{name}]  ->  {path}")


if __name__ == "__main__":
    main()
