"""
Data Processing Pipeline - CLI Template

DS 3500 - MP1

Usage:
    python pipeline.py --input data.csv --output clean.csv --config config/config.yaml
    python pipeline.py --input data.csv --output clean.csv --config config/config.yaml --verbose
"""

import argparse
import logging
import sys

from src import (
    create_cleaning_report,
    load_data,
    save_data,
    process_data,
    setup_logging,
    validate_dataframe,
    validate_input
)

logger = logging.getLogger(__name__)


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Data Processing Pipeline")

    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to the input file"
    )

    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Path to the output file"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )

    parser.add_argument(
        "--config",
        required=True,
        help="Path to the Yaml configuration file"
    )

    return parser.parse_args()



def main():
    """Main pipeline function."""
    args = parse_arguments()
    setup_logging(args.verbose)
    logger.debug(f"Arguments parsed: input={args.input}, output={args.output}")

    if not validate_input(args.input):
        sys.exit(1)
    if not validate_input(args.config):
        sys.exit(1)

    try:
        df = load_data(args.input)
        config = load_data(args.config)
    except ValueError as e:
        logger.error(f"Error loading data: {e}")
        sys.exit(1)

    required_columns = config["validation"]["required_columns"]
    numeric_columns = config["validation"]["numeric_columns"]
    try:
        rows_before = len(df)
        df = validate_dataframe(df, required_columns, numeric_columns)
        logger.info(f"Validation complete: {rows_before} rows -> {len(df)} rows.")
    except ValueError:
        sys.exit(1)

    df_original = df.copy()  # Keep a copy for reporting

    try:
        df = process_data(df, config)
    except ValueError:
        sys.exit(1)

    report = create_cleaning_report(df_original, df)
    logger.info(f"Processing complete: {report['rows_before']} rows -> {report['rows_after']} rows.")


    save_data(df, args.output)
    logger.info(f"Saved cleaned data to {args.output}")

    print("\nCleaning report:")
    print(report)

if __name__ == "__main__":

    main()