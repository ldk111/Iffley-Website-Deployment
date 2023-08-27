import sys
sys.path.append('C:\\Users\\luke\\OneDrive\\Documents\\Iffley Backup\\iffley_v1\\Iffley-Website-Deployment')

from ast import literal_eval
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iffley_v1.settings')
if __name__ == "__main__":
    django.setup()

import pandas as pd
#from django.db import transaction
from django.core.files import File
from iffley_app.models import *
import psycopg2

from iffley_v1.settings import DATABASES

conn=psycopg2.connect(database = DATABASES["default"]["NAME"],
                      user = DATABASES["default"]["USER"],
                      password = DATABASES["default"]["PASSWORD"],
                      host = DATABASES["default"]["HOST"],
                      port = DATABASES["default"]["PORT"],)

cursor = conn.cursor()

#path depends on visual studios open folder location
df_holds = pd.read_csv("scripts\df_holds.csv")
df_routes = pd.read_csv("scripts\df_routes.csv",converters={"holds": literal_eval, 
                                                                      "start_holds": literal_eval}, encoding = "latin1") 
                                                                      #"all": literal_eval,
                                                                      #"tall": literal_eval,
                                                                      #"tech": literal_eval,
                                                                      #"flex": literal_eval,
                                                                      #"strong": literal_eval,
                                                                      #"dyno": literal_eval,
                                                                      #"finger": literal_eval,
                                                                      #"infamous": literal_eval,
                                                                      #"ambulance": literal_eval}, encoding="latin1")
df_bgrades = pd.read_csv("scripts\df_bgrade.csv")
df_techgrades = pd.read_csv("scripts\df_techgrade.csv")
df_furlonggrades = pd.read_csv("scripts\df_furlonggrade.csv")
df_sections = pd.read_csv("scripts\df_sections.csv")


def create_holds_from_dataframe(df):
    for _, row in df.iterrows():
        my_hold = Hold(name=row['index'], pixels_x1=row['pixel_x1'], pixels_x2=row['pixel_x2'], pixels_y1=row['pixel_y1'], pixels_y2=row['pixel_y2'])
        my_hold.save()


def create_tech_grades(df):
    for _, row in df.iterrows():
        grade = TechGrade(grade = row['grade'])
        grade.save()

def create_b_grades(df):
    for _, row in df.iterrows():
        grade = BGrade(grade = row['grade'])
        grade.save()


def create_furlong_grades(df):
    for _, row in df.iterrows():
        grade = FurlongGrade(grade = row['grade'])
        grade.save()


def create_sections(df):
    for _, row in df.iterrows():
        section = Section(short_name = row["short_name"], long_name = row["long_name"])
        section.save()


def create_routes_from_dataframe(df):
    for _, row in df.iterrows():

        try:
            tech_grade = TechGrade.objects.get(grade = row["tech_grade"])
        except TechGrade.DoesNotExist:
            tech_grade = None
            print("No tech grade.")
        
        try:
            b_grade = BGrade.objects.get(grade = row["b_grade"])
        except BGrade.DoesNotExist:
            b_grade = None
            print("No B grade.")
        
        try:       
            furlong_grade = FurlongGrade.objects.get(grade = row["furlong_grade"])
        except FurlongGrade.DoesNotExist:
            furlong_grade = None
            print("No furlong grade.")

        try:       
            section = Section.objects.get(short_name = row["section"])
        except Section.DoesNotExist:
            section = None
            print("No furlong grade.")

        my_route = Route(name=row['index'], 
                         tech_grade=tech_grade,
                         b_grade=b_grade,
                         furlong_grade=furlong_grade,
                         section=section,
                         other_grade=row["other_grade"], 
                         holds_str=row["holds_str"], 
                         stand_start=row["stand_start"],
                         description=row["description"],
                         stars=row["stars"],
                         tag_all=row["all"],
                         tag_tall=row["tall"],
                         tag_tech=row["tech"],
                         tag_flex=row["flex"],
                         tag_strong=row["strong"],
                         tag_dyno=row["dyno"],
                         tag_finger=row["finger"],
                         tag_infamous=row["infamous"],
                         tag_ambulance=row["ambulance"])

        holds = []
        for hold in row['holds']:
            try:
                hold = Hold.objects.get(name = hold)
                holds.append(hold)
            except Hold.DoesNotExist:
                print("Hold: ", hold, "does not exist.")
            
        print(holds)

        start_holds = []
        for hold in row['start_holds']:
            try:
                hold = Hold.objects.get(name = hold)
                start_holds.append(hold)
            except Hold.DoesNotExist:
                print("Start hold: ", hold, "does not exist.")
        
        
        
        image_file_name = ''.join(e for e in row['index'].lower() if e.isalnum()) + '.png'
        #path needs to match reading dataframe path
        image_file_path = 'C:\\Users\\luke\\OneDrive\\Documents\\Iffley App\\route_images' + "\\" + image_file_name

        if os.path.exists(image_file_path):
                print("Adding: ", image_file_name)
                # Create a Django File object directly from the file path
                django_file = File(open(image_file_path, 'rb'))
                # Assign the Django File object to the image field of MyModel
                my_route.image.save(image_file_name, django_file)
        else:
            print(image_file_name, "not found.")

        my_route.save()

        my_route.start_holds.set(start_holds)
        my_route.holds.set(holds)
        
        
        # Add any additional fields based on your DataFrame columns
        # Example: my_model.field_name = row['column_name']
        # Save the model after setting all the fields
        
create_holds_from_dataframe(df_holds)
create_tech_grades(df_techgrades)
create_b_grades(df_bgrades)
create_furlong_grades(df_furlonggrades)
create_sections(df_sections)
create_routes_from_dataframe(df_routes)