from django.core.exceptions import ValidationError
import xlrd
import json
import csv
import os
from .new_conc import generate_output

def valid_file_type(value):
    if value.name.split('.')[-1] != 'csv':
        raise ValidationError('Invalid File Type: %(value)s', params={'value': value},)

def strList_to_intList(strList):
    res = []
    for each in strList:
        res.append(float(each))
    return res

def transfer_to_json(input_path, output_path):
    book = xlrd.open_workbook(input_path)
    result = {}
    sh_num = len(book.sheet_names())
    for i in range(sh_num):
        cur_sheet = book.sheet_by_index(i)
        cur_col_num = cur_sheet.ncols
        sheet_data = {}
        for j in range(cur_col_num):
            head = cur_sheet.col_values(j)[1].strip()
            sheet_data[head] = cur_sheet.col_values(j)[2:]
        result[str(i)] = sheet_data

    with open(output_path, 'w') as f:
        json.dump(result, f)
        f.close()


def transfer_to_inputjson(input_path, output_path):
    result = {}

    with open(input_path, 'r') as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
        num_col = len(rows[0])
        f.close()
    for i in range(num_col):
        with open(input_path, 'r') as f:
            reader = csv.reader(f)
            cur_col = [row[i] for row in reader]
            head = cur_col[0].strip()
            try:
                result[head] = strList_to_intList(cur_col[1:])
            except ValueError:
                result[head] = cur_col[1:]
            f.close()

    with open(output_path, 'w') as f:
        json.dump(result, f)
        f.close()

def generate_filtered_input(input_path, selected):
    res = []

    with open(input_path, 'r') as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
        for i in range(len(rows)):
            #if (str(i-1) not in selected) or (not selected[str(i-1)]):
            if (str(i-1) in selected) and (selected[str(i-1)]):
                res.append(rows[i])
            else:
                continue
        f.close()
    return json.dumps(res)


def generate_filtered_output(input_file, output_path):
    try:
        outfile = open(output_path, 'w')
        writer = csv.writer(outfile)
        for row in json.loads(input_file):
            writer.writerow(row)
        outfile.close()
    except:
        if os.path.isfile(output_path):
            os.remove(output_path)







































