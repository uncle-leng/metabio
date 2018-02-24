

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.core.files import File
from django.http import StreamingHttpResponse
from django.contrib import messages
from numpy.polynomial import polynomial as poly
from .models import UploadFile, DownloadFile, OutputJSON, InputJSON
from .models import UploadFileForm
import os
import json
from .upload_helper import valid_file, transfer_to_json, transfer_to_inputjson, \
    generate_filtered_input, generate_filtered_output, cal_predict_points, cal_expression
from .new_conc import generate_output



# Create your views here.


def mainpage(request):
    return render(request, 'main_page.html')

def testpage(request):
    return render(request, 'result_page.html')


'''
def upload(request):

    if request.method == 'POST':
        if 'try' in request.POST:
            with open('./static/sample_input.csv') as csvfile:
                uploadfile = UploadFile()
                uploadfile.upload_file = File(csvfile)
                uploadfile.save()
            with open('./static/sample_input_json.json') as jsonfile:
                inputjsonfile = InputJSON()
                inputjsonfile.upload_file = uploadfile
                inputjsonfile.input_json = File(jsonfile)
                inputjsonfile.save()

                input_json_pk = inputjsonfile.pk
            csvfile.close()
            jsonfile.close()
            return render(request, 'main_page.html', {'typeError': False, 'graph': True, 'input_json_pk': input_json_pk, 'show_result': True, 'try': True})
        if 'download_pk' in request.POST:
            messages.add_message(request, messages.INFO, request.POST['download_pk'])
            return HttpResponseRedirect('/download/')
        if 'download_sample' in request.POST:
            return HttpResponseRedirect('/download_sample/')
        if 'show_graph' in request.POST:
            return HttpResponseRedirect('/show_graph/')
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            upload_file = form.cleaned_data['upload_form']
            uploadfile = UploadFile()
            uploadfile.upload_file = upload_file
            uploadfile.save()
            try:
                with open('./tmp_input.csv', 'wb') as f:
                    for eachline in upload_file:
                        f.write(eachline)
                    f.close()
                if not valid_file('./tmp_input.csv'):
                    return render(request, 'main_page.html',
                                  {'form': form, 'typeError': True, 'graph': False, 'show_result': False, 'try': False})
                generate_output('./tmp_input.csv', 'tmp_output.xlsx')
                transfer_to_inputjson('./tmp_input.csv', './tmp_input_json.json')
                with open('./tmp_input_json.json', 'rb') as f:
                    inputjsonfile = InputJSON()
                    inputjsonfile.upload_file = uploadfile
                    inputjsonfile.input_json = File(f)
                    inputjsonfile.save()
                    input_json_pk = inputjsonfile.pk
                    f.close()
                with open('./tmp_output.xlsx', 'rb') as f:
                    downloadfile = DownloadFile()
                    downloadfile.upload_file = uploadfile
                    downloadfile.download_file = File(f)
                    downloadfile.save()
                    download_pk = downloadfile.pk
                    f.close()

                outputjsonfile = OutputJSON()
                outputjsonfile.download_file = downloadfile
                transfer_to_json('./tmp_output.xlsx', './tmp_output.json')
                with open('./tmp_output.json', 'rb') as f:
                    outputjsonfile.JSON_file = File(f)
                    outputjsonfile.save()
                    f.close()
                os.remove('./tmp_output.json')
                os.remove('./tmp_input.csv')
                os.remove('./tmp_output.xlsx')
                os.remove('./tmp_input_json.json')
            except:
                return render(request, 'main_page.html', {'form': form, 'typeError': True, 'graph': False, 'show_result': False, 'try': False})

            return render(request, 'main_page.html', {'form': form, 'typeError': False, 'input_json_pk': input_json_pk, 'graph': True, 'show_result': True, 'try': False})
        else:
            return render(request, 'main_page.html', {'form': form, 'typeError': True, 'graph': False, 'show_result': False, 'try': False})
    else:
        form = UploadFileForm()
    return render(request, 'main_page.html', {'form': form, 'typeError': False, 'graph': False, 'show_result': False, 'try': False})
'''




def upload(request):
    if request.method == 'POST':
        if 'try' in request.POST:
            with open('./static/sample_input.csv') as csvfile:
                uploadfile = UploadFile()
                uploadfile.upload_file = File(csvfile)
                uploadfile.save()
            with open('./static/sample_input_json.json') as jsonfile:
                inputjsonfile = InputJSON()
                inputjsonfile.upload_file = uploadfile
                inputjsonfile.input_json = File(jsonfile)
                inputjsonfile.save()
                input_json_pk = inputjsonfile.pk
            csvfile.close()
            jsonfile.close()
            return render(request, 'main_page.html', {'home': False,
                                                      'upload': False,
                                                      'visualization': True,
                                                      'typeError': False,
                                                      'input_json_pk': input_json_pk,
                                                      'try': True})
        if 'upload_your_own_file' in request.POST:
            return render(request, 'main_page.html', {'home': False,
                                                      'upload': True,
                                                      'visualization': False})
        if 'download_pk' in request.POST:
            messages.add_message(request, messages.INFO, request.POST['download_pk'])
            return HttpResponseRedirect('/download/')
        if 'download_sample' in request.POST:
            return HttpResponseRedirect('/download_sample/')
        if 'show_graph' in request.POST:
            return HttpResponseRedirect('/show_graph/')
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            upload_file = form.cleaned_data['upload_form']
            uploadfile = UploadFile()
            uploadfile.upload_file = upload_file
            uploadfile.save()
            try:
                with open('./tmp_input.csv', 'wb') as f:
                    for eachline in upload_file:
                        f.write(eachline)
                    f.close()
                if not valid_file('./tmp_input.csv'):
                    return render(request, 'main_page.html', {'form': form,
                                                              'typeError': True,
                                                              'home': False,
                                                              'upload': True,
                                                              'visualization': False})
                generate_output('./tmp_input.csv', 'tmp_output.xlsx', False)
                transfer_to_inputjson('./tmp_input.csv', './tmp_input_json.json')
                with open('./tmp_input_json.json', 'rb') as f:
                    inputjsonfile = InputJSON()
                    inputjsonfile.upload_file = uploadfile
                    inputjsonfile.input_json = File(f)
                    inputjsonfile.save()
                    input_json_pk = inputjsonfile.pk
                    f.close()
                with open('./tmp_output.xlsx', 'rb') as f:
                    downloadfile = DownloadFile()
                    downloadfile.upload_file = uploadfile
                    downloadfile.download_file = File(f)
                    downloadfile.save()
                    f.close()

                outputjsonfile = OutputJSON()
                outputjsonfile.download_file = downloadfile
                transfer_to_json('./tmp_output.xlsx', './tmp_output.json')
                with open('./tmp_output.json', 'rb') as f:
                    outputjsonfile.JSON_file = File(f)
                    outputjsonfile.save()
                    f.close()
                os.remove('./tmp_output.json')
                os.remove('./tmp_input.csv')
                os.remove('./tmp_output.xlsx')
                os.remove('./tmp_input_json.json')
            except:
                return render(request, 'main_page.html', {'form': form,
                                                          'typeError': True,
                                                          'home': False,
                                                          'upload': True,
                                                          'visualization': False})

            return render(request, 'main_page.html', {'form': form,
                                                      'typeError': False,
                                                      'input_json_pk': input_json_pk,
                                                      'home': False,
                                                      'upload': False,
                                                      'visualization': True,
                                                      'try': False})
        else:
            return render(request, 'main_page.html', {'form': form,
                                                      'typeError': True,
                                                      'home': False,
                                                      'upload': True,
                                                      'visualization': False})
    else:
        form = UploadFileForm()
    return render(request, 'main_page.html', {'form': form,
                                              'home': True,
                                              'upload': False,
                                              'visualization': False,
                                              'typeError': False})

def download_sample(request):
    def file_iterator(filename, chunk_size=512):
        with open(filename, 'r') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    sample_name = 'static/sample_input.csv'
    response = StreamingHttpResponse(file_iterator(sample_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(sample_name)
    return response

def show_graph(request):
    request = request
    input_json_pk = request.GET.get('input_json_pk', None)
    input_json_file = InputJSON.objects.get(pk=int(input_json_pk)).input_json
    return HttpResponse(input_json_file)

def show_result(request):
    selected = json.loads(request.POST['selected'])
    input_json_pk = request.POST['input_json_pk']
    offset = request.POST['offset']
    if request.POST['is_nor'] == 'true':
        is_nor = True
    else:
        is_nor = False
    uploadfile_id = InputJSON.objects.get(pk=int(input_json_pk)).upload_file_id
    uploadfile_path = UploadFile.objects.get(pk=uploadfile_id).upload_file.path
    filtered_json = generate_filtered_input(uploadfile_path, selected, offset)
    generate_filtered_output(filtered_json, './result_csv.csv')
    generate_output('./result_csv.csv', './result_xlsx.xlsx', is_nor)
    transfer_to_json('./result_xlsx.xlsx', './result_json.json')

    with open('./result_json.json', 'r') as f:
        response = json.load(f)
    f.close()
    if os.path.isfile('./result_csv.csv'):
        os.remove('./result_csv.csv')
    if os.path.isfile('./result_xlsx.xlsx'):
        os.remove('./result_xlsx.xlsx')
    if os.path.isfile('./result_json.json'):
        os.remove('./result_json.json')

    return HttpResponse(json.dumps(response))

def result_page(request):
    return render(request, 'result_page.html')

def download(request):
    def file_iterator(filename, chunk_size=512):
        with open(filename, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break
    selected = json.loads(request.POST['selected'])
    offset = json.loads(request.POST['offset'])
    input_json_pk = request.POST['input_json_pk']
    if request.POST['is_nor'] == 'true':
        is_nor = True
    else:
        is_nor = False
    uploadfile_id = InputJSON.objects.get(pk=int(input_json_pk)).upload_file_id
    uploadfile_path = UploadFile.objects.get(pk=uploadfile_id).upload_file.path
    filtered_json = generate_filtered_input(uploadfile_path, selected, offset)
    generate_filtered_output(filtered_json, './result_csv.csv')
    generate_output('./result_csv.csv', './result_xlsx.xlsx', is_nor)

    response = StreamingHttpResponse(file_iterator('./result_xlsx.xlsx'))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format('./result_xlsx.xlsx')

    '''
    if os.path.isfile('./result_csv.csv'):
        os.remove('./result_csv.csv')
    if os.path.isfile('./result_xlsx.xlsx'):
        os.remove('./result_xlsx.xlsx')
    '''
    return response

def show_try_graph(request):
    with open('./static/sample_input_json.json', 'r') as f:
        json_response = json.load(f)
    f.close()
    return HttpResponse(json.dumps(json_response))

def weighted_regression(request):
    if request.method == 'POST':
        equation = []
        weight = request.POST['weight']
        dataX = []
        dataY = []
        weights = []
        res = {}
        points = json.loads(request.POST['points'])
        for each_point in points:
            if weight == 'None':
                weights.append(1)
            if weight == '1/x':
                if each_point[0] == 0:
                    weights.append(0)
                else:
                    weights.append(1 / each_point[0])
            if weight == '1/x^2':
                if each_point[0] == 0:
                    weights.append(0)
                else:
                    weights.append(1 / (each_point[0] ** 2))
            if weight == '1/y':
                if each_point[1] == 0:
                    weights.append(0)
                else:
                    weights.append(1 / each_point[1])
            if weight == '1/y^2':
                if each_point[1] == 0:
                    weights.append(0)
                else:
                    weights.append(1 / (each_point[1] ** 2))
            dataX.append(each_point[0])
            dataY.append(each_point[1])
        if request.POST['regression_method'] == 'quadratic':
            equation, stats = poly.polyfit(x=dataX, y=dataY, deg=2, w=weights, full=True)
        if request.POST['regression_method'] == 'linear':
            equation, stats = poly.polyfit(x=dataX, y=dataY, deg=1, w=weights, full=True)
        res['points'] = points
        res['equation'] = equation.tolist()
        res['predicted_points'] = cal_predict_points(points, equation.tolist())
        res['expression'] = cal_expression(equation.tolist())
        return HttpResponse(json.dumps(res))




































