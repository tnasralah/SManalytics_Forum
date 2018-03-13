import sys
import pandas

#----------------------------------------------------------------------
def csv_usercol():
    colnames = ['user_id','user_name','user_gender','diabetes_type','account_owner','meds_tools','DOB']
    data = pandas.read_csv('D:\Tudiabetes_Python_Code\Data_file\users_final.csv', names=colnames)
    users = data.user_id.tolist()
    # print len(users)
    # print "============== \n"
    # print users
    print users
    return users
# -----------------------