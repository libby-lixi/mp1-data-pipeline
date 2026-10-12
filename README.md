# MP1 Data Pipeline

This pipeline takes a CSV file, cleans it, and saves the clean version. You run it from the command line with `pipeline.py`, giving it an input file, an output path, and a config file. First it loads the CSV and the config, then it validates the data by checking that the required columns exist and removing rows where `rating` isn't a number. Next it removes duplicate rows, rows with missing values, and outliers in `rating`, based on the settings in `config.yaml`. The cleaned data is saved to `output/clean.csv` and a cleaning report is printed. `pipeline.py` runs the steps in order, and the rest of the code is in `src/`: `data_loaders.py` reads files, `data_validator.py` validates the data, `data_processor.py` cleans it, `data_output.py` saves it, and `utils.py` handles logging and file checks. Settings are in `config/` and test files are in `fixtures/`.

## Example

```bash
python3 pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

Output:

```text
13:56:33 DEBUG    __main__ — Arguments parsed: input=fixtures/sample_data.csv, output=output/clean.csv
13:56:33 INFO     src.utils — Input file validated: fixtures/sample_data.csv
13:56:33 INFO     src.utils — Input file validated: config/config.yaml
13:56:33 INFO     src.data_loaders — Loaded CSV file: fixtures/sample_data.csv (100 rows)
13:56:33 INFO     src.data_loaders — Loaded YAML file: config/config.yaml
13:56:33 WARNING  src.data_validator — Invalid value in rating: 'not_available'
13:56:33 WARNING  src.data_validator — Invalid value in rating: 'error'
13:56:33 DEBUG    src.data_validator — Validation: 100 -> 98 rows
13:56:33 INFO     __main__ — Validation complete: 100 rows -> 98 rows.
13:56:33 DEBUG    src.data_processor — Removed duplicates: 2 rows
13:56:33 DEBUG    src.data_processor — handle_missing: 2 rows
13:56:33 DEBUG    src.data_processor — rating: method=iqr, threshold=1.5, lower=43.625, upper=106.625, removed=2
13:56:33 INFO     __main__ — Processing complete: 98 rows -> 92 rows.
13:56:33 DEBUG    src.data_output — Saved 92 rows to output/clean.csv
13:56:33 INFO     __main__ — Saved cleaned data to output/clean.csv

Cleaning report:
{'rows_before': 98, 'rows_after': 92, 'rows_removed': 6, 'columns_before': 5, 'columns_after': 5, 'columns_removed': 0}
```
