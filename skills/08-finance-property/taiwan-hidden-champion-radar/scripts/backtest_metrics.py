#!/usr/bin/env python3
import argparse
import csv
import json


def safe_div(a, b):
    return a / b if b else None


def main():
    parser = argparse.ArgumentParser(description="Compute binary radar backtest metrics.")
    parser.add_argument("csv_file", help="CSV with score and actual columns")
    parser.add_argument("--threshold", type=float, default=65.0)
    parser.add_argument("--score-column", default="score")
    parser.add_argument("--actual-column", default="actual")
    args = parser.parse_args()

    counts = {"tp": 0, "fp": 0, "tn": 0, "fn": 0}
    with open(args.csv_file, newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            predicted = float(row[args.score_column]) >= args.threshold
            actual = str(row[args.actual_column]).strip().lower() in {"1", "true", "yes", "y"}
            key = "tp" if predicted and actual else "fp" if predicted else "fn" if actual else "tn"
            counts[key] += 1

    tp, fp, tn, fn = (counts[k] for k in ("tp", "fp", "tn", "fn"))
    precision = safe_div(tp, tp + fp)
    recall = safe_div(tp, tp + fn)
    specificity = safe_div(tn, tn + fp)
    metrics = {
        **counts,
        "n": tp + fp + tn + fn,
        "threshold": args.threshold,
        "precision": precision,
        "recall": recall,
        "specificity": specificity,
        "f1": safe_div(2 * precision * recall, precision + recall) if precision is not None and recall is not None else None,
        "balanced_accuracy": (recall + specificity) / 2 if recall is not None and specificity is not None else None,
    }
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

