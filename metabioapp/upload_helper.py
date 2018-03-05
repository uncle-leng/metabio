from django.core.exceptions import ValidationError
import xlrd
import json
import csv
import os
import pandas as pd
from .new_conc import generate_output

def valid_file_type(value):
    if value.name.split('.')[-1] != 'csv':
        raise ValidationError('Invalid File Type: %(value)s', params={'value': value},)


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    return False

def valid_file(file_path):
    try:
        num_S = 0
        #num_R = 0
        all_data = pd.read_csv(file_path, header=None).as_matrix()
        head = all_data[0]
        if head[0].strip() != 'id' or head[1].strip() != 'Concentration' or head[2].strip() != 'Group' or head[3].strip() != 'IS':
            return False
        for i in range(1, len(all_data)):
            if is_number(all_data[i][0]) or not is_number(all_data[i][1]) or is_number(all_data[i][2]) or not is_number(all_data[i][3]):
                return False
            for j in range(4, len(all_data[0])):
                if not is_number(all_data[i][j]):
                    return False
            if all_data[i][2] == 'S':
                num_S += 1
            #if all_data[i][2] == 'R':
                #num_R += 1
        #if num_S != 0 and num_R != 0:
        if num_S != 0:
            return True
        else:
            return False
    except:
        return False


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
        heads = []
        for j in range(cur_col_num):
            head = cur_sheet.col_values(j)[1].strip()
            heads.append(head)
            sheet_data[head] = cur_sheet.col_values(j)[2:]
        sheet_data['heads'] = heads
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

def generate_filtered_input(input_path, selected, offset):
    res = []
    with open(input_path, 'r') as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
        categories = [x.strip() for x in rows[0][4:]]
        for i in range(int(offset)+1, len(rows)):
            for j in range(len(categories)):
                index = str(i-1-int(offset))+','+categories[j]
                if (index in selected) and (selected[index]):
                    for k in range(int(offset)+1, len(rows)):
                        if rows[k][0] == rows[i][0] and rows[k][1] == rows[i][1] and rows[k][j+4] == rows[i][j+4]:
                            rows[k][j+4] = 0
                    rows[i][j+4] = 0

        for k in range(len(rows)):
            res.append(rows[k])

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

def cal_predict_points(points, equation):
    res = []
    if len(equation) == 3:
        for each in points:
            res.append([each[0], equation[0] + each[0]*equation[1] + each[0]*each[0]*equation[2]])
        return res
    elif len(equation) == 2:
        for each in points:
            res.append([each[0], equation[0] + each[0]*equation[1]])
        return res

def cal_expression(equation):
    if len(equation) == 3:
        return 'y = ' + str(round(equation[2], 2)) + 'x^2 + ' + str(round(equation[1], 2)) + 'x + ' + str(round(equation[0], 2))
    elif len(equation) == 2:
        return 'y = ' + str(round(equation[1], 2)) + 'x + ' + str(round(equation[0], 2))








































