#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os

def extract_values(content, pattern):
    match = re.search(pattern, content)
    return int(match.group(1)) if match else 0

def extract_time(content):
    match = re.search(r'Time Consumption:\s*([\d.]+)\s*S', content)
    return float(match.group(1)) if match else 0

def calculate_precision_recall(tp, tp_fp, tp_fn):
    precision = tp / tp_fp if tp_fp != 0 else 0
    recall = tp / tp_fn if tp_fn != 0 else 0
    return precision, recall


files = sorted([f for f in os.listdir() if os.path.isfile(f)])

total_precision_type = 0
total_recall_type = 0
total_precision_var = 0
total_recall_var = 0
total_time = 0
file_count = 0


for i in range(1, len(files)//2 + 1):
    gt_file = f'{i}_ground_truth.txt'
    out_file = f'{i}_output.txt'

    if os.path.exists(gt_file) and os.path.exists(out_file):
        with open(gt_file, 'r', encoding='utf-8') as f:
            ground_truth_content = f.read()

        with open(out_file, 'r', encoding='utf-8') as f:
            analysis_result_content = f.read()


        tp = extract_values(analysis_result_content, r'\*\*(\d+)\*\*')
        tp_fp = extract_values(analysis_result_content, r'##(\d+)##')
        tp_fn = extract_values(ground_truth_content, r'@@(\d+)@@')
        time = extract_time(analysis_result_content)


        precision_type, recall_type = calculate_precision_recall(tp, tp_fp, tp_fn)


        precision_var, recall_var = calculate_precision_recall(tp_fp, tp_fp, tp_fn)

        print(f'{i}_output.txt - Precision (Type): {precision_type:.2f}, Recall (Type): {recall_type:.2f}')
        print(f'{i}_output.txt - Precision (Var): {precision_var:.2f}, Recall (Var): {recall_var:.2f}')
        print(f'{i}_output.txt - Time: {time:.2f} S')

        total_precision_type += precision_type
        total_recall_type += recall_type
        total_precision_var += precision_var
        total_recall_var += recall_var
        total_time += time
        file_count += 1


avg_precision_type = total_precision_type / file_count if file_count != 0 else 0
avg_recall_type = total_recall_type / file_count if file_count != 0 else 0
avg_precision_var = total_precision_var / file_count if file_count != 0 else 0
avg_recall_var = total_recall_var / file_count if file_count != 0 else 0
avg_time = total_time / file_count if file_count != 0 else 0

print(f'\nAverage Precision (Type): {avg_precision_type:.2f}')
print(f'Average Recall (Type): {avg_recall_type:.2f}')
print(f'Average Precision (Var): {avg_precision_var:.2f}')
print(f'Average Recall (Var): {avg_recall_var:.2f}')
print(f'Average Time: {avg_time:.2f} S')

