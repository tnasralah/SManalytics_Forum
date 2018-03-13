
import sys
import re
from bs4 import BeautifulSoup
import pprint
import util_fetch_mongo as fm


import csv
#----------------------------------------------------------------------
def csv_writer(data, path):
    """
    Write data to a CSV file path
    """
    with open(path, 'ab') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)
    csv_file.close()
# ----------------------------------------------------------------------

Another_type_of_diabetes=["Another_type_of_diabetes"]
Gestational_diabetes=["Gestational_diabetes"]
Idk_type_of_diabetes=["Idk_type_of_diabetes"]
No_diabetes=["No_diabetes"]
Pre_diabetes=["Pre_diabetes"]
Type1=["Type1"]
Type2=["Type2"]

### export discussions to csv file
def users(db, COLL_USER_DES, COLL_SAVE_USTATUS):

    cursor = db[COLL_USER_DES].find()
    coll_status = db[COLL_SAVE_USTATUS]


    header_user = "user_id,user_name"
    header_user_fields = ",user_gender,diabetes_type,account_owner,meds_tools,DOB"
    header = header_user + header_user_fields

    if(coll_status.find({"collection":"user_export"}).count() == 0):

        data = [header.split(",")]
        csv_writer(data, "final_users.csv")

    cnt = 0
    for d in cursor:

        user_id = -1
        user_name = ""
        gender=""
        diabetes_type=""
        account_owner=""
        meds_tools=""
        DOB=""

        try:
            d['id']
        except KeyError:
            continue
        else:
            user_id = d['id']

        try:
            d['username']
        except KeyError:
            continue
        else:
            user_name = d['username'].replace(",", "").encode('ascii', 'ignore')

        # try:
        #     d["custom_fields"]["date_of_birth"]
        # except KeyError:
        #     continue
        # else:
        #     date_of_birth = d["custom_fields"]["date_of_birth"].replace(",", "").encode('ascii', 'ignore')

        try:
            d["user_fields"]["10"]
        except KeyError:
            continue
        else:
            if  d["user_fields"]["10"]==None:
                gender=""
            else:
                gender = d["user_fields"]["10"].encode('ascii', 'ignore')

        try:
            d["user_fields"]["3"]
        except KeyError:
            continue
        else:
            if type(d["user_fields"]["3"]) == type([]) :
                diabetes_type= d["user_fields"]["3"][0].replace(",", "").encode('ascii', 'ignore')
            else:
                if  d["user_fields"]["3"]==None:
                    diabetes_type=""
                else:
                    diabetes_type = d["user_fields"]["3"].replace(",", "").encode('ascii', 'ignore')

        try:
            d["user_fields"]["2"]
        except KeyError:
            continue
        else:
            if  d["user_fields"]["2"]==None:
                account_owner=""
            else:
                account_owner = d["user_fields"]["2"].replace(",", "").encode('ascii', 'ignore')

        try:
            d["user_fields"]["5"]
        except KeyError:
            continue
        else:
            if  d["user_fields"]["5"]==None:
                meds_tools=""
            else:
                meds_tools = d["user_fields"]["5"].replace(",", "").encode('ascii', 'ignore')

        try:
            d["user_fields"]["9"]
        except KeyError:
            continue
        else:
            if  d["user_fields"]["9"]==None:
                DOB=""
            else:
                DOB = d["user_fields"]["9"].replace(",", "").encode('ascii', 'ignore')


        line_user = [user_id,user_name,gender,diabetes_type,account_owner,meds_tools,DOB]
        line_user_str = [str(i) for i in line_user]
        line_user_str = ",".join(line_user_str)

        # #------------------------------------------
        if diabetes_type.strip()=="another type of diabetes" or diabetes_type.strip()=="Another type of diabetes":
            Another_type_of_diabetes.append(user_id)
        elif diabetes_type.strip()=="Gestational diabetes":
            Gestational_diabetes.append(user_id)
        elif diabetes_type.strip()=="I do not know what type of diabetes" or diabetes_type.strip()=="I don&#039;t know what type of diabetes":
            Idk_type_of_diabetes.append(user_id)
        elif diabetes_type.strip()=="No diabetes":
            No_diabetes.append(user_id)
        elif diabetes_type.strip()=="Pre-diabetes":
            Pre_diabetes.append(user_id)
        elif diabetes_type.strip()=="Type 1 or type 1.5 (LADA) diabetes" or diabetes_type.strip()=="Type 1 or Type 1.5 (LADA) diabetes" or diabetes_type.strip()=="Diabetes Tipo 1 o 1.5 (LADA)":
            Type1.append(user_id)
        elif diabetes_type.strip()=="Diabetes de Tipo 2" or diabetes_type.strip()=="Type 2 diabetes":
            Type2.append(user_id)
        #------------------------------------------

        # print line_user_str

        # print line_discuss_str
        # pprint.pprint( d["post_stream"]["posts"])

        if  diabetes_type!="":
            if fm.check_if_saved(db, COLL_SAVE_USTATUS, "user_export", user_id):
                print "Reply ID : " + str(user_id) + " already exported"

            # if fm.check_if_saved(db, COLL_SAVE_STATUS, "discussion_export", id):
            #     print "Reply ID : " + str(id) + " already exported"
            else:

                final_line = line_user_str+"\n"
                final_line  = final_line.encode('ascii', 'ignore')
                data = [final_line.split(",")]
                csv_writer(data, "final_users.csv")
                coll_status.insert_one({"collection":"user_export", "id":user_id})
                print "Reply ID : " + str(user_id) + " User Info Exported To CSV File"

    print len(Another_type_of_diabetes),len(Gestational_diabetes), len(Idk_type_of_diabetes),len(No_diabetes),len(Pre_diabetes),len(Type1),len(Type2)
    print " Number of Users Extracted --->  ", len(Another_type_of_diabetes)+len(Gestational_diabetes)+ len(Idk_type_of_diabetes)+len(No_diabetes)+len(Pre_diabetes)+len(Type1)+len(Type2)

    with open('Another_type_of_diabetes.csv','ab') as f:
        writer = csv.writer(f);
        writer.writerows(zip(Another_type_of_diabetes));

    with open('Gestational_diabetes.csv','ab') as f:
        writer = csv.writer(f);
        writer.writerows(zip(Gestational_diabetes));

    with open('Idk_type_of_diabetes.csv','ab') as f:
        writer = csv.writer(f);
        writer.writerows(zip(Idk_type_of_diabetes));

    with open('No_diabetes.csv','ab') as f:
        writer = csv.writer(f);
        writer.writerows(zip(No_diabetes));

    with open('Pre_diabetes.csv','ab') as f:
        writer = csv.writer(f);
        writer.writerows(zip(Pre_diabetes));

    with open('Type1.csv','ab') as f:
        writer = csv.writer(f);
        writer.writerows(zip(Type1));

    with open('Type2.csv','ab') as f:
        writer = csv.writer(f);
        writer.writerows(zip(Type2));

    # csv_writer(Another_type_of_diabetes, "Another_type_of_diabetes.csv")
    # csv_writer(Gestational_diabetes, "Gestational_diabetes.csv")
    # csv_writer(Idk_type_of_diabetes, "Idk_type_of_diabetes.csv")
    # csv_writer(No_diabetes, "No_diabetes.csv")
    # csv_writer(Pre_diabetes, "Pre_diabetes.csv")
    # csv_writer(Type1, "Type1.csv")
    # csv_writer(Type2, "Type2.csv")

    # print "Gestational_diabetes\n==================================="
    # pprint.pprint(Gestational_diabetes)
    # print "Another_type_of_diabetes\n==================================="
    # pprint.pprint(Another_type_of_diabetes)
    # print "Gestational_diabetes\n==================================="
    # pprint.pprint(Gestational_diabetes)
    # print "Idk_type_of_diabetes\n==================================="
    # pprint.pprint(Idk_type_of_diabetes)
    # print "No_diabetes\n==================================="
    # pprint.pprint(No_diabetes)
    # print "Pre_diabetes\n==================================="
    # pprint.pprint(Pre_diabetes)
    # print "Type1\n==================================="
    # pprint.pprint(Type1)
    # print "Type2\n==================================="
    # pprint.pprint(Type2)

