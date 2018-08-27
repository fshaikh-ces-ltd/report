# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
import json

from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseRedirect
)
import StringIO
from rank.utils import generate_data
from test_ces.settings import BASE_DIR
import os


battery = 0
NO_OF_DAYS = 7
SITE_WITH_BATTERY_ID = (6, 166, 193, 192, 194, 210, 211, 212, 219, 220, 218, 217, 216, 215, 214, 213, 209, 208, 224,
                        226, 227, 228, 229, 230, 231, 232, 233, 234, 221, 222)

FILE_DATA = []


def quotation(request):
    if request.method == "GET":
        file_name = generate_data()
        excel = open(os.path.join(BASE_DIR, 'report_data', file_name), "rb")
        output = StringIO.StringIO(excel.read())
        out_content = output.getvalue()
        output.close()
        response = HttpResponse(out_content,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
        return response
