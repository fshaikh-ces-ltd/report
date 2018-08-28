# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.


""""
######operational SIte Insert Query

Insert into micro_proddb.operationalsite (CAPACITY, DISTRICT, NAME, SITESTATUS, STATE, GRIDTYPE, TYPE, sitewhere_tenant, VILLAGE, COMMDATE, CURRTARRIF, INVERTERTYPE, SUPPORTED_ACTIVITY) values
(72, "Bijapur", "KSV Site", "Operational", "Karnataka", "HYBRID", "MICROGRID", "Kalkeri_Sangeet_Vidyalaya", "Kalakeri", "July-2018", 0, "Grid Tie", "House Hold");

#####Grid Insert Query

INSERT INTO micro_proddb.grids (SITE_ID, ASSIGNMENT_ID, DEVICE_HW_ID, GRID_NAME, parameters) 
values ("025b9701-bbcc-4a3b-bf6b-059bd830f2d1", "ba7081ec-6ce9-42e2-8fdf-7cb892813feb", "KSV_Battery", "Battery", "Battery_TotalCurr,Battery_SocErr,Battery_CurrentIn,Battery_AhCntOut,Battery_CurrentOut,Battery_EnergyCntOut,Battery_Temp,Battery_Soc,Battery_CharVtg,Battery_AhCntIn,Battery_Voltage,Battery_EnergyCntIn,Battery_Soh");


INSERT INTO micro_proddb.grids (SITE_ID, ASSIGNMENT_ID, DEVICE_HW_ID, GRID_NAME, parameters) 
values ("025b9701-bbcc-4a3b-bf6b-059bd830f2d1", "d03a2f8a-f8b7-43fd-9daf-bed786a47e09", "KSV_Solar", "Solar", "Solar_Voltage,Solar_Current,Solar_Pac,Solar_DCPower,Solar_Power");

######IOTCLUSTER INSERT QUERY

INsert into micro_proddb.iotcluster (CLUSTER_DESCRIPTION, SITE_ID, SITE_NAME) values ("KSV Site", "025b9701-bbcc-4a3b-bf6b-059bd830f2d1", "KSV Site");


######MICROCLUSTER INSERT QUERY

INSERT INTO micro_proddb.microcluster (SITECLUSTER) values (52);

######MICERO GRID LIST INSERT

INSERT INTO micro_proddb.microcluster_grid_list (MICROCLUSTER, GRID_LIST) values (53, 151);

###Selco Batter Cap = 72 Solr CAp = 14
"""