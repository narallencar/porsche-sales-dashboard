#!/usr/bin/env python3
"""Valida CSV sanitizado e atualiza o JSON dentro do HTML autônomo.

Uso: python scripts/update_dashboard.py
Nenhuma dependência externa. NÃO sanitiza dados pessoais de uma base crua.
"""
from __future__ import annotations

import csv
from datetime import date
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / "data" / "porsche_sales_clean.csv"
HTML_PATH = ROOT / "index.html"
COLUMNS = (
    "sale_id", "sale_date", "porsche_model", "model_year", "sale_price_usd",
    "vehicle_mileage_mi", "payment_method", "city", "state", "delivery_status",
    "date_valid",
)
TEXT = {"porsche_model", "payment_method", "city", "state", "delivery_status"}


def validated_records(path: Path) -> list[dict]:
    if not path.is_file():
        raise ValueError(f"CSV não encontrado: {path}")
    records = []
    used_ids = set()
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != list(COLUMNS):
            raise ValueError("Esquema do CSV diferente das 11 colunas permitidas, na ordem esperada.")
        for line_number, item in enumerate(reader, start=2):
            try:
                if any(not item.get(k, "").strip() for k in TEXT):
                    raise ValueError("campo categórico vazio")
                row = {key: item[key].strip() for key in COLUMNS}
                row["sale_id"] = int(row["sale_id"])
                row["model_year"] = int(row["model_year"])
                row["sale_price_usd"] = float(row["sale_price_usd"])
                row["vehicle_mileage_mi"] = float(row["vehicle_mileage_mi"])
                if row["sale_id"] in used_ids:
                    raise ValueError("sale_id duplicado")
                used_ids.add(row["sale_id"])
                if not 1900 <= row["model_year"] <= 2100:
                    raise ValueError("ano de modelo fora do intervalo esperado")
                if not (0 < row["sale_price_usd"] < 1e12):
                    raise ValueError("preço inválido")
                if not (0 <= row["vehicle_mileage_mi"] < 1e9):
                    raise ValueError("quilometragem inválida")
                date_text = row["sale_date"]
                date_valid_text = row["date_valid"].lower()
                if date_valid_text not in {"true", "false"}:
                    raise ValueError("date_valid deve ser True ou False")
                row["date_valid"] = date_valid_text == "true"
                if date_text:
                    parsed = date.fromisoformat(date_text)
                    if parsed.isoformat() != date_text or not row["date_valid"]:
                        raise ValueError("data ISO e sinalizador de validade inconsistentes")
                    row["sale_date"] = date_text
                else:
                    if row["date_valid"]:
                        raise ValueError("data ausente não pode ter date_valid=True")
                    row["sale_date"] = None
                records.append(row)
            except (ValueError, TypeError, KeyError) as exc:
                raise ValueError(f"Linha {line_number}: {exc}") from exc
    if not records:
        raise ValueError("O CSV está vazio")
    return records


def main() -> None:
    rows = validated_records(CSV_PATH)
    original = HTML_PATH.read_text(encoding="utf-8")
    content = json.dumps(rows, ensure_ascii=False, separators=(",", ":"), allow_nan=False)
    # Evita que texto de CSV feche o elemento <script> antes da hora.
    content = content.replace("<", "\\u003c")
    pattern = r'(<script\s+type="application/json"\s+id="embedded-data">)(.*?)(</script>)'
    updated, substitutions = re.subn(pattern, lambda m: m.group(1) + content + m.group(3), original, count=1, flags=re.S)
    if substitutions != 1:
        raise ValueError("Não foi localizado o bloco único 'embedded-data' no index.html")
    HTML_PATH.write_text(updated, encoding="utf-8")
    eligible = [r for r in rows if r["delivery_status"] != "Cancelled"]
    print(f"HTML atualizado: {len(rows)} registros, {len(eligible)} elegíveis; preço total USD {sum(r['sale_price_usd'] for r in eligible):,.2f}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        print(f"ERRO: {error}", file=sys.stderr)
        sys.exit(1)
