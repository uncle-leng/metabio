from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.core.files import File
from django.http import StreamingHttpResponse
from django.contrib import messages
from .models import UploadFile, DownloadFile, OutputJSON, InputJSON
from .models import UploadFileForm
import os
import json
from .upload_helper import transfer_to_json, transfer_to_inputjson, generate_filtered_input, generate_filtered_output
from .new_conc import generate_output


# Create your views here.


def mainpage(request):
    return render(request, 'main_page.html')

def testpage(request):
    return render(request, 'test_page.html')

def upload(request):

    if request.method == 'POST':
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
                    json_pk = str(outputjsonfile.pk)
                    f.close()

                os.remove('./tmp_output.json')
                os.remove('./tmp_input.csv')
                os.remove('./tmp_output.xlsx')
                os.remove('./tmp_input_json.json')
            except:
                return render(request, 'main_page.html', {'form': form, 'typeError': True, 'graph': False})

            return render(request, 'main_page.html', {'form': form, 'typeError': False, 'download_pk': download_pk, 'input_json_pk': input_json_pk, 'graph': True})
        else:
            return render(request, 'main_page.html', {'form': form, 'typeError': True, 'graph': False})
    else:
        form = UploadFileForm()
    return render(request, 'main_page.html', {'form': form, 'typeError': False, 'graph': False})



def download(request):
    def file_iterator(f, chunk_size=512):
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break
    for each in messages.get_messages(request):
        pk = each

    output_file = DownloadFile.objects.get(pk=int(pk.message))
    download_file_name = output_file.download_file
    response = StreamingHttpResponse(file_iterator(download_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(download_file_name)
    return response


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
    uploadfile_id = InputJSON.objects.get(pk=int(input_json_pk)).upload_file_id
    uploadfile_path = UploadFile.objects.get(pk=uploadfile_id).upload_file.path
    filtered_json = generate_filtered_input(uploadfile_path, selected)
    generate_filtered_output(filtered_json, './result_csv.csv')
    generate_output('./result_csv.csv', './result_xlsx.xlsx')
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

def test_page(request):
    return render(request, 'test_page.html')



























