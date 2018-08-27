#!/usr/bin/python
import MySQLdb
from requests.auth import HTTPBasicAuth
import requests
import datetime
import operator
import xlsxwriter
import json
import StringIO


battery = 0
NO_OF_DAYS = 2
SITE_WITH_BATTERY_ID = (6, 166, 193, 192, 194, 210, 211, 212, 219, 220, 218, 217, 216, 215, 214, 213, 209, 208, 224,
                        226, 227, 228, 229, 230, 231, 232, 233, 234, 221, 222)
SITE_WITH_BATTERY_ID = (228,228)

FILE_DATA = []

def process_solar_data(data_obj, solar_capacity):
    end_data = data_obj[0].get("measurements", {}).get("Solar_EnergyCnt", 0)
    start_data = data_obj[len(data_obj)-1].get("measurements", {}).get("Solar_EnergyCnt", 0)
    return (((end_data/1000) - (start_data/1000)) / (solar_capacity * NO_OF_DAYS))


def process_meter_data(data_obj, battery_capacity):
    if "Battery_EnergyCntOut" in data_obj[0].get("measurements", {}) and "Battery_EnergyCntIn" in data_obj[0].get("measurements", {}):
        out_to_data = data_obj[0].get("measurements", {}).get("Battery_EnergyCntOut", 0)
        in_to_data = data_obj[0].get("measurements", {}).get("Battery_EnergyCntIn", 0)
        in_from_data = data_obj[len(data_obj)-1].get("measurements", {}).get("Battery_EnergyCntIn", 0)
        out_from_data = data_obj[len(data_obj)-1].get("measurements", {}).get("Battery_EnergyCntOut", 0)

        battery_utilization = ((out_to_data - out_from_data) / (float(battery_capacity) * NO_OF_DAYS)) * 100
        efficiency_denominator = in_to_data - in_from_data
        if efficiency_denominator:
            battery_efficiency = ((out_to_data - out_from_data) / (in_to_data - in_from_data)) * 100
        else:
            battery_efficiency = 0
        return battery_utilization, battery_efficiency
    else:
        print "###############################"
        print data_obj[0].get("measurements", {})
        print "###############################"
        return 0,0


def generate_xlsx(sol_data, utilization_data, efficieny_data, site_data):
    file_name = 'RankingSheet_' + str(datetime.datetime.now()).replace(':', '-')
    file_name = file_name.split('.')[0].replace(' ', '_') + '.xlsx'

    workbook = xlsxwriter.Workbook(file_name)
    cell_format = workbook.add_format()
    # header_format = workbook.add_format()
    # header_format.set_font_color('gray')
    cell_format.set_align('left')

    worksheet = workbook.add_worksheet('Parameter Wise Ranking')
    worksheet.set_column(0, 15, 25)

    bold = workbook.add_format({'bold': True, "bg_color": "gray"})

    worksheet.write('A1', 'Solar Generation Rank', bold)
    worksheet.write('B1', 'Battery Utilization Rank', bold)
    worksheet.write('C1', 'Battery Efficiency Rank', bold)

    row = 1
    col = 0

    try:
        for s_data, u_data, e_data in zip(sol_data, utilization_data, efficieny_data):
            worksheet.write(row, col, s_data.get("solar_generation_score") if s_data.get("solar_generation_score", 0) != 0 else 'NA', cell_format)
            worksheet.write(row, col + 1, u_data.get("battery_utilization") if u_data.get("battery_utilization", 0) != 0 else 'NA', cell_format)
            worksheet.write(row, col + 2, e_data.get("battery_efficiency") if e_data.get("battery_efficiency", 0) != 0 else 'NA', cell_format)
            row += 1
    except:
        print "File Saving Failed"

    total_rating_sheet = workbook.add_worksheet('Total Ranking')
    total_rating_sheet.set_column(0, 15, 25)

    total_rating_sheet.write('A1', 'Solar Gen Score', bold)
    total_rating_sheet.write('B1', 'Gen Rank', bold)
    total_rating_sheet.write('C1', 'Normalized Solar Gen Score', bold)
    total_rating_sheet.write('D1', 'Battery Utilization (in%)', bold)
    total_rating_sheet.write('E1', 'BU Rank', bold)
    total_rating_sheet.write('F1', 'Normalized Battery Utilization ', bold)
    total_rating_sheet.write('G1', 'Battery Efficiency (in%)', bold)
    total_rating_sheet.write('H1', 'BE Rank', bold)
    total_rating_sheet.write('I1', 'Normalized Battery Efficiency', bold)
    total_rating_sheet.write('J1', 'Weightage Solar Score', bold)
    total_rating_sheet.write('K1', 'Weightage BU', bold)
    total_rating_sheet.write('L1', 'Weightage BE', bold)
    total_rating_sheet.write('M1', 'Total Weightage', bold)
    total_rating_sheet.write('N1', 'Total Score', bold)
    total_rating_sheet.write('O1', 'Rank', bold)
    total_rating_sheet.write('P1', 'Site Name', bold)
    row = 1
    col = 0

    try:
        for data in site_data:
            total_rating_sheet.write(row, col + 1, data.get("solar_rank"), cell_format)
            total_rating_sheet.write(row, col + 2, data.get("normalized_solar_generation_score"), cell_format)
            total_rating_sheet.write(row, col + 5, data.get("normalized_battery_utilization"), cell_format)
            total_rating_sheet.write(row, col + 8, data.get("normalized_battery_efficiency"), cell_format)
            total_rating_sheet.write(row, col + 4, data.get("battery_utilization_rank"), cell_format)
            total_rating_sheet.write(row, col + 7, data.get("battery_efficiency_rank"), cell_format)
            total_rating_sheet.write(row, col, data.get("solar_generation_score") if data.get("solar_generation_score", 0) != 0 else 'NA', cell_format)
            total_rating_sheet.write(row, col + 3, data.get("battery_utilization") if data.get("battery_utilization", 0) != 0 else 'NA', cell_format)
            total_rating_sheet.write(row, col + 6, data.get("battery_efficiency") if data.get("battery_efficiency", 0) != 0 else 'NA', cell_format)
            total_rating_sheet.write(row, col + 9, '50%', cell_format)
            total_rating_sheet.write(row, col + 10, '30%', cell_format)
            total_rating_sheet.write(row, col + 11, '20%', cell_format)
            total_rating_sheet.write(row, col + 12, '100%', cell_format)
            total_rating_sheet.write(row, col + 13, data.get('total_score'), cell_format)
            total_rating_sheet.write(row, col + 14, row, cell_format)
            total_rating_sheet.write(row, col + 15, data.get('site_name'), cell_format)
            row += 1
    except:
        print "File Saving Failed 10-13"

    workbook.close()

    return file_name


def generate_data():

    data_available = False
    with open("C:/django/myproject/rank/ranking_data.json") as f:
        FILE_DATA = json.load(f)
        f.close()

    for data in FILE_DATA:
        if data.get("date") == datetime.date.today().strftime("%B %d, %Y") and data.get("no_of_days") == NO_OF_DAYS:
            data_available = True
            SITE_DATA = data.get("site_data")
            solar_generation_score_list = data.get("solar_generation_score_list")
            battery_utilization_list = data.get("battery_utilization_list")
            battery_efficiency_list = data.get("battery_efficiency_list")

    if not data_available:
        current_date = datetime.datetime.utcnow().isoformat()
        end_date = datetime.datetime.utcnow() - datetime.timedelta(days=NO_OF_DAYS)
        end_date = end_date.isoformat()

        # Open database connection
        db = MySQLdb.connect(host="localhost", user="root", passwd="root", db="micro_proddb")

        # prepare a cursor object using cursor() method
        cursor = db.cursor()

        get_operational_site = "SELECT * FROM micro_proddb.operationalsite where sitewhere_tenant IS NOT NULL AND ID IN " + str(SITE_WITH_BATTERY_ID) + ";"

        # try:
        cursor.execute(get_operational_site)
        operational_sites = cursor.fetchall()
        SITE_DATA = []

        for site in operational_sites:
           site_obj = {
           "site_name" : site[8],
           "micro_cluster" : site[21],
           "param" : site[23],
           "tenant_name" : site[30],
           "solar_capacity": site[1],
           "battery_capacity" : site[27],
           "solar_generation_score": 0,
           "battery_utilization": 0,
           "battery_efficiency": 0
           }

           grid_assigned = "SELECT GRID_LIST FROM micro_proddb.microcluster_grid_list Where MICROCLUSTER = " \
                           + str(site_obj.get("micro_cluster")) + ";"

           cursor.execute(grid_assigned)
           grid_record_list = cursor.fetchall()

           if len(grid_record_list):
               grid_ids = str([int(element) for tupl in grid_record_list for element in tupl])
               grid_ids = grid_ids.replace("[", "(")
               grid_ids = grid_ids.replace("]", ")")

               get_grid_sql = "SELECT * from micro_proddb.grids Where ID IN " + str(grid_ids) + ";"

               cursor.execute(get_grid_sql)
               grid_list = cursor.fetchall()

               for grid in grid_list:
                   grid_data = {
                       "assignment_id" : grid[1],
                       "grid_name": grid[3],
                       "parameter": grid[9],
                       "site_id": grid[8]
                   }

                   if grid[1] == "28bd9fd1-22e0-4603-bcaf-4a64b17d84be":
                       grid_data["assignment_id"] = "e7cd7630-4823-447f-9c9a-1ac9fe0d25b2"


#                   if grid_data.get("assignment_id") and site_obj.get("tenant_name") and (site_obj.get("site_name") == "Navapada" or site_obj.get("site_name") ==  "CG Hatt"):
                   if grid_data.get("assignment_id") and site_obj.get("tenant_name"):
                       url = "http://52.32.19.136:9080/sitewhere/api/assignments/" + grid_data.get("assignment_id") + \
                             "/measurements?page=1&pageSize=10000&startDate=" + end_date + "&endDate=" + current_date

                       headers = {"X-SiteWhere-Tenant": site_obj.get("tenant_name"), 'content-type': 'application/json'}
                       data = requests.get(url, auth=HTTPBasicAuth('admin', 'password'), headers=headers)

                       if grid[3] == "Solar" or grid[3] == "Solar1" or grid[3] == "Solar2" or grid[3] == "Solar3":
                           if len(data.json().get("results")):
                               score = process_solar_data(data.json().get("results"), site_obj.get("solar_capacity"))
                               site_obj["solar_generation_score"] = score
                               site_obj["normalized_solar_generation_score"] = score/6
                           else:
                               site_obj["solar_generation_score"] = 0
                               site_obj["normalized_solar_generation_score"] = 0

                       if grid[3] == "Battery":

                           if len(data.json().get("results")):
                               battery_utilization, battery_efficiency = process_meter_data(data.json().get("results"), site_obj.get("battery_capacity"))
                               site_obj["battery_efficiency"] = battery_efficiency
                               site_obj["battery_utilization"] = battery_utilization
                               site_obj["normalized_battery_efficiency"] = battery_efficiency/95
                               site_obj["normalized_battery_utilization"] = battery_utilization/90
                           else:
                               site_obj["battery_efficiency"] = 0
                               site_obj["battery_utilization"] = 0
                               site_obj["normalized_battery_efficiency"] = 0
                               site_obj["normalized_battery_utilization"] = 0

                       site_obj["grid_type"] = grid[3]

           else:
               pass
           SITE_DATA.append(site_obj)

        solar_generation_score_list = sorted(SITE_DATA, key=lambda x: float(operator.itemgetter("solar_generation_score")(x)), reverse=True)
        battery_utilization_list = sorted(SITE_DATA, key=lambda x: float(operator.itemgetter("battery_utilization")(x)), reverse=True)
        battery_efficiency_list = sorted(SITE_DATA, key=lambda x: float(operator.itemgetter("battery_efficiency")(x)), reverse=True)

        for data in SITE_DATA:
            data["solar_rank"] = solar_generation_score_list.index(data) + 1
            data["battery_utilization_rank"] = battery_utilization_list.index(data) + 1
            data["battery_efficiency_rank"] = battery_efficiency_list.index(data) + 1
            data["total_score"] = ((50 * data.get("normalized_solar_generation_score", 0)) + (30 * data.get("normalized_battery_utilization", 0)) + (20 * data.get("normalized_battery_efficiency", 0)))

        SITE_DATA = sorted(SITE_DATA, key=lambda x: float(operator.itemgetter("total_score")(x)), reverse=True)

        with open('C:/django/myproject/rank/ranking_data.json', 'w') as outfile:
            data = {
                "site_data" : SITE_DATA,
                "solar_generation_score_list" : solar_generation_score_list,
                "battery_utilization_list" : battery_utilization_list,
                "battery_efficiency_list" : battery_efficiency_list,
                "date": datetime.date.today().strftime("%B %d, %Y"),
                "no_of_days": NO_OF_DAYS
            }
            FILE_DATA.append(data)
            json.dump(FILE_DATA, outfile)

        db.close()

    file_name = generate_xlsx(solar_generation_score_list, battery_utilization_list, battery_efficiency_list, SITE_DATA)

    return file_name
