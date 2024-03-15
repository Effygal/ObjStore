"""
File: statistics.py
Author: Effy Wang
Date: 2024-03-12

Description:
- Parses an IBM Object Store trace file, calculates CDF of PUT & GET inter-reference times, and CDF of GET after PUT inter-reference times;

- Result CSV files are saved under ./data.

- If usable data entries are less than 5, no statistics will be saved.

Usage:
python3 statistics.py "IBMObjectStoreTrace000Part0"
"""

import sys
import os
import numpy as np
from collections import Counter
from collections import defaultdict


def parse_file(file_path):
    trace = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            timestamp = int(parts[0])
            request_type = parts[1]
            object_id = parts[2]
            trace.append([timestamp, request_type, object_id])
    return np.array(trace)

def iat(trace):
    '''
    trace: need to be filtered by request_type;
    numpy array of shape (n, 3).
    '''
    n = trace.shape[0]
    out = [-1] * n
    T = defaultdict(int)
    
    for i in range(n):
        t = int(trace[i, 0])
        key = trace[i, 2]
        if key in T:
            out[i] = t - T[key]
        else:
            out[i] = -1
        T[key] = t
    return out

def cdf(data):
    data_sorted = np.sort(data)
    data_cdf = np.cumsum(data_sorted) / sum(data_sorted)
    # plt.plot(data_sorted, data_cdf, label=title, drawstyle='steps-post')
    return data_sorted, data_cdf

def read_after_write_dist(trace):
    '''
    trace: numpy array of shape (n, 3).
    '''
    T = defaultdict(int)
    Flag = defaultdict(int)
    out = []
    for i in range(trace.shape[0]):
        t = int(trace[i, 0])
        key = trace[i, 2]
        req = trace[i, 1]
        # if last access to the same key is a PUT
        if req == 'REST.GET.OBJECT' and key in T and Flag[key] == 1:
            out.append(t - T[key])
            Flag[key] = 0
        elif req == 'REST.PUT.OBJECT':
            Flag[key] = 1
            T[key] = t
    return np.array(out)

def save_statistics(input_file):
    file_name = input_file.split("IBMObjectStoreTrace")[1]
    trace = parse_file(input_file)
    trace_read = trace[trace[:, 1] == 'REST.GET.OBJECT']
    trace_write = trace[trace[:, 1] == 'REST.PUT.OBJECT']
    trace_write_iat = iat(trace_write)
    trace_read_iat = iat(trace_read)
    trace_read_iat = np.array([x for x in trace_read_iat if x != -1])
    trace_write_iat = np.array([x for x in trace_write_iat if x != -1])
    raw = read_after_write_dist(trace)
    
    xr, yr = cdf(trace_read_iat)
    xw, yw = cdf(trace_write_iat)
    rawx, rawy = cdf(raw)
    
    data_dir = './data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    if len(trace_read_iat) > 5:
        np.savetxt(os.path.join(data_dir, file_name + '_read_iat_cdf.csv'), np.column_stack((xr, yr)), delimiter=',', comments='')
    if len(trace_write_iat) > 5:
        np.savetxt(os.path.join(data_dir, file_name + '_write_iat_cdf.csv'), np.column_stack((xw, yw)), delimiter=',', comments='')
    if len(raw) > 5:
        np.savetxt(os.path.join(data_dir, file_name + '_raw_cdf.csv'), np.column_stack((rawx, rawy)), delimiter=',', comments='')


if __name__ == '__main__':
    input_file = sys.argv[1]
    print("Processing file: ", input_file)
    save_statistics(input_file)
    print("File: ", input_file, " saved.")
    
