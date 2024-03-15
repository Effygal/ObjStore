# IBM Object Store Trace Analysis Tool

## Description:
This tool, implemented in Python, is designed to parse IBM Object Store trace files, calculate the Cumulative Distribution Function (CDF) of PUT and GET inter-reference times to the same key, and generate CDF plots for analysis. Additionally, it computes the CDF of the first GET after PUT to the same key time distances. The resulting CSV files containing the statistics are saved under the "./data" directory.

Use "plot.ipynb" to plot the statistic files with bokeh.

## Features:
- Parses IBM Object Store trace files;
- Calculates CDF of PUT and GET inter-reference (to the same key) times;
- Computes CDF of the first GET after PUT (to the same key) time istances;
- Saves statistical results as CSV files under "./data".

## Usage:

1. Ensure you have Python 3 installed on your system.

2. Clone or download the repository containing the script.

3. Open a terminal or command prompt and navigate to the directory containing the script.

4. Run the script using the following command:

```
python3 statistics.py "IBMObjectStoreTraceXXXPartX"
```

Replace `"IBMObjectStoreTraceXXXPartX"` with the name of the trace file you want to analyze.

5. The script will process the specified trace file and generate CDF plots for analysis.

6. The resulting CSV files containing the statistics will be saved under the "./data" directory.

## Requirements:
- Python 3
- NumPy
- Bokeh

## Example:
To analyze a trace file named "IBMObjectStoreTrace001Part0", run the following command:
```
python3 statistics.py "IBMObjectStoreTrace001Part0"
```

To analyze trace files in batch, modify the "batch_run_statistics.sh", run command:
```
./batch_run_statistics.sh
```