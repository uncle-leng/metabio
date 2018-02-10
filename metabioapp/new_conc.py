import csv
import numpy
import statistics
import itertools
import xlsxwriter
import os
import traceback


def enforce_R(input_path):
    has_R = False
    with open(input_path, 'r') as f:
        reader = csv.reader(f)
        rows = [row for row in reader]
        num_metabolo = len(rows[0]) - 4
        for row in rows:
            if row[2] == 'R':
                has_R = True
        f.close()
    with open(input_path, 'a') as f:
        writer = csv.writer(f)
        if not has_R:
            row_to_write = ['force_R', '0', 'R', '0']
            for i in range(num_metabolo):
                row_to_write.append('0')
            writer.writerow([])
            writer.writerow(row_to_write)
        f.close()


def get_groups(filename):
    groups = {}
    with open(filename, 'r') as fp:
        reader = csv.reader(fp)
        next(reader)

        for line in reader:
            if len(line) == 0:
                continue
            if line[2] not in groups:
                groups.update({line[2]: 0})
    fp.close()
    return (groups)


def group_count(filename, groups):
    with open(filename, 'r') as fp:
        reader = csv.reader(fp)
        next(reader)

        for line in reader:
            if len(line) == 0:
                continue
            for sample in groups:
                if sample == line[2]:
                    groups[sample] = groups[sample] + 1
    fp.close()
    return (groups)


def is_normalise(filename):
    mat = []
    with open(filename, 'r') as fp:
        reader = csv.reader(fp)
        fline = next(reader)

        for line in reader:
            if len(line) != 0:
                mat.append(line[3:])

    arr = numpy.array(mat)
    intarr = arr.astype(numpy.int)

    isnorm = []
    #isnorm = intarr[:, 0] / intarr[:, 0].min()
    isnorm = intarr[:, 0] / intarr[:, 0].max()
    finalarr = numpy.array(isnorm)

    for i in range(1, len(intarr[0])):
        val = intarr[:, i] / isnorm
        finalarr = numpy.vstack((finalarr, val))
    tr_finalarr = finalarr.transpose()
    tr_finalarr_list = tr_finalarr.tolist()
    fp.close()

    with open(filename, 'r') as fp:
        reader = csv.reader(fp)
        fline = next(reader)
        fin_list = []
        fin_list.append(fline)
        i = 0
        for line in reader:
            if len(line) != 0:
                fin_list.append(line[:3] + tr_finalarr_list[i])
                i = i + 1
    fp.close()
    return (fin_list, tr_finalarr)




def is_normalise_negative(filename):
    mat = []
    with open(filename, 'r') as fp:
        reader = csv.reader(fp)
        fline = next(reader)

        for line in reader:
            if len(line) != 0:
                mat.append(line[3:])

    arr = numpy.array(mat)
    intarr = arr.astype(numpy.int)

    isnorm = []
    MIN = intarr[:, 0]
    #isnorm = intarr[:, 0] / intarr[:, 0].min()
    isnorm = intarr[:, 0] / intarr[:, 0].max()

    finalarr = numpy.array(isnorm)

    for i in range(1, len(intarr[0])):
        val = intarr[:, i]
        finalarr = numpy.vstack((finalarr, val))
    tr_finalarr = finalarr.transpose()
    tr_finalarr_list = tr_finalarr.tolist()
    fp.close()

    with open(filename, 'r') as fp:
        reader = csv.reader(fp)
        fline = next(reader)
        fin_list = []
        fin_list.append(fline)
        i = 0
        for line in reader:
            if len(line) != 0:
                fin_list.append(line[:3] + tr_finalarr_list[i])
                i = i + 1
    fp.close()
    return (fin_list, tr_finalarr)


def subtract_reg(metlist):
    size = len(metlist)  # calculates the number of samples!
    num_met = len(metlist[0]) - 3
    met_count = 3
    Sub_mat = [[None] * (size - 1)]
    iscol = []
    Sub_mat = numpy.array(Sub_mat)

    for j in range(0, num_met):  # cycling through metabolites
        j = j + met_count

        Reg_li = []
        Reg_avg = 0
        for i in range(1, size):  # cycling through the number of samples
            if metlist[i][2] == 'R':
                Reg_li.append(metlist[i][j])
            #else:                   # added by ruobing
                #Reg_li.append(0)    # added by ruobing
        Reg_avg = statistics.mean(Reg_li)

        Sub_li = []
        for i in range(1, size):  # cycling through the number of samples
            sub_val = 0
            if (metlist[i][j] != 0):
                sub_val = metlist[i][j] - Reg_avg
            Sub_li.append(sub_val)

        Sub_li_arr = numpy.array([Sub_li])
        Sub_mat = numpy.vstack((Sub_mat, Sub_li_arr))
        tr_Sub_mat = Sub_mat[1:].transpose()
        tr_Sub_mat_li = tr_Sub_mat.tolist()

    fin_sub_li = []
    fin_sub_li.append(metlist[0])

    for l in range(1, len(metlist)):
        temp = []
        init_li = []
        init_li = [metlist[l][0], metlist[l][1], metlist[l][2]]
        temp.append(init_li + tr_Sub_mat_li[l - 1])
        fin_sub_li.extend(temp)

    return (fin_sub_li)


def stats(metlist, groups, workbook, text):
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, text)
    worksheet.write(1, 0, "")
    out_count = 1
    for group in groups:
        out_count = out_count + 1
        op_text = "In group " + group
        worksheet.write(out_count, 0, op_text)
        out_count = out_count + 1
        size = len(metlist)
        num_met = len(metlist[0]) - 3
        sum = 0
        met_count = 3
        for j in range(0, num_met):  # cycling through metabolites
            j = j + met_count
            sum = 0
            li = []
            for i in range(1, size):  # cycling through the number of samples in each group
                if group == metlist[i][2]:
                    sum = sum + metlist[i][j]
                    li.append(metlist[i][j])
            try:
                #                op_text = "CV of" + metlist[0][j] + ": " + str(statistics.stdev(li)/statistics.mean(li)*100)
                if len(li) == 1:
                    li.append(0.0)
                worksheet.write(out_count, 0, metlist[0][j])
                worksheet.write(out_count, 1, statistics.stdev(li) / statistics.mean(li) * 100)
                # print("CV of", metlist[0][j], ": ", statistics.stdev(li)/statistics.mean(li)*100)
            except ZeroDivisionError:
                worksheet.write(out_count, 0, metlist[0][j])
                worksheet.write(out_count, 1, "NA")
                # print("\n Warning: sum = 0 causing a ZeroDivisionError. Therefore skipping calculating stats for this metabolite.")
                # print(li)
                # rint("\n")
            out_count = out_count + 1


def linreg(metlist):
    size = len(metlist)
    num_met = len(metlist[0]) - 3
    sum = 0
    met_count = 3
    conc_li = []

    for j in range(0, num_met):  # cycling through metabolites
        j = j + met_count
        sum = 0
        spike_li = []
        auc_li = []
        li = []
        for i in range(1, size):  # cycling through the number of samples in each group
            if metlist[i][2] == 'S':
                if metlist[i][j] != 0:
                    spike_li.append(metlist[i][1])
                    auc_li.append(metlist[i][j])
        spike_li = list(map(float, spike_li))
        fit = numpy.polyfit(spike_li, auc_li, 1)
        # print("For ", metlist[0][j], " m = ",fit[0]," c = ",fit[1])
        conc_li.append((metlist[0][j], fit[0], fit[1]))
    return (conc_li)


def conc_cal(metlist, conc_li):
    size = len(metlist)  # calculates the number of samples!
    num_met = len(metlist[0]) - 3
    met_count = 3
    Sub_mat = [[None] * (size - 1)]
    iscol = []
    Sub_mat = numpy.array(Sub_mat)

    for j in range(0, num_met):  # cycling through metabolites

        j = j + met_count

        Sub_li = []
        for i in range(1, size):  # cycling through the number of samples
            for k in conc_li:
                m = 0
                c = 0
                x = 0
                y = 0
                if k[0] == metlist[0][j]:
                    m = k[1]
                    c = k[2]
                    break

            y = metlist[i][j]

            if (metlist[i][j] != 0):
                x = (y - c) / m
            Sub_li.append(x)

        Sub_li_arr = numpy.array([Sub_li])
        Sub_mat = numpy.vstack((Sub_mat, Sub_li_arr))
        tr_Sub_mat = Sub_mat[1:].transpose()
        tr_Sub_mat_li = tr_Sub_mat.tolist()

    fin_sub_li = []
    fin_sub_li.append(metlist[0])

    for l in range(1, len(metlist)):
        temp = []
        init_li = []
        init_li = [metlist[l][0], metlist[l][1], metlist[l][2]]
        temp.append(init_li + tr_Sub_mat_li[l - 1])
        fin_sub_li.extend(temp)

    return (fin_sub_li)


def write_rawdata(workbook, filename):
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, 'Raw Data')
    with open(filename, 'r') as fp:
        reader = csv.reader(fp)
        x = 1
        y = 0
        for line in reader:
            for j in range(0, len(line)):
                if (x == 1):
                    worksheet.write(x, y, line[j])
                else:
                    if (y == 0 or y == 2):
                        worksheet.write(x, y, line[j])
                    else:
                        worksheet.write_number(x, y, float(line[j]))
                y = y + 1
            x = x + 1
            y = 0


def write_data(workbook, reader, text):
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, text)
    x = 1
    y = 0
    for line in reader:
        # print(line)
        for j in range(0, len(line)):
            if (x == 1):
                worksheet.write(x, y, line[j])
            else:
                if (y == 0 or y == 2):
                    worksheet.write(x, y, line[j])
                else:
                    worksheet.write_number(x, y, float(line[j]))
            y = y + 1
        x = x + 1
        y = 0


def generate_output(input_path, output_path, is_nor):
    try:
        workbook = xlsxwriter.Workbook(output_path)
        enforce_R(input_path)
        write_rawdata(workbook, input_path)
        groups = get_groups(input_path)
        groups = group_count(input_path, groups)
        if is_nor:
            isnorm = is_normalise(input_path)
        else:
            isnorm = is_normalise_negative(input_path)
        write_data(workbook, isnorm[0], "IS Normalised Data")
        stats(isnorm[0], groups, workbook, "CVs after Internal Standard Normalisation")
        reg_sub_li = subtract_reg(isnorm[0])
        write_data(workbook, reg_sub_li, "IS Normalised, Reagent Blank Subtracted Data")
        stats(reg_sub_li, groups, workbook, "CVs after Internal standard Normalisation and Reagent Blank Subtraction")
        conc_li = linreg(reg_sub_li)
        fin_conc_val = conc_cal(reg_sub_li, conc_li)
        write_data(workbook, fin_conc_val, "IS Normalised, Reagent Blank Subtracted CONCENTRATION Data")
        stats(fin_conc_val, groups, workbook, "CVs of Concentrations after Internal standard Normalisation and Reagent Blank Subtraction")
        workbook.close()
    except Exception as e:
        traceback.print_exc()
        print(e)
        if os.path.isfile(input_path):
            os.remove(input_path)
        if os.path.isfile(output_path):
            os.remove(output_path)



































