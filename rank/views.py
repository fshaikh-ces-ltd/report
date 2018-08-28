# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import os
import StringIO

from django.http import HttpResponse

from rank.utils import generate_data
from test_ces.settings import BASE_DIR


def rank(request):
    if request.method == "GET":
        file_name = generate_data(True)
        excel = open(os.path.join(BASE_DIR, 'report_data', file_name), "rb")
        output = StringIO.StringIO(excel.read())
        out_content = output.getvalue()
        output.close()
        response = HttpResponse(out_content,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=' + file_name
        return response


def rank_data(request):
    if request.method == "GET":
        solar_generation_score_list, battery_utilization_list, battery_efficiency_list, SITE_DATA = generate_data(False)
        data = {
            "solar_generation_score_list": solar_generation_score_list,
            "battery_utilization_score_list": battery_utilization_list,
            "battery_efficiency_score_list": battery_efficiency_list,
            "site_score_data": SITE_DATA
        }
        return HttpResponse(json.dumps(data), content_type="application/json")
