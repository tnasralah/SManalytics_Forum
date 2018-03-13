
import sys
from bs4 import BeautifulSoup
import pprint
import util_fetch_mongo as fm
import pandas
import nltk
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
import string
import csv
import re, itertools
import LDA as lda


#------------------------------------------------------------------
wordlist=["one","im","would","also","ive","lol"]
def clean(doc):
    lemma = WordNetLemmatizer()
    exclude = set(string.punctuation)
    stoplist= stopwords.words('english')
    stoplist= stoplist+wordlist

    stop = set(stoplist)
    # stop= stop.append
    # print type(stop)
    # print(stop)
    # exit(0)
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

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
def csv_usercol():
    colnames = ['user_id','user_name','user_gender','diabetes_type','account_owner','meds_tools','DOB']
    data = pandas.read_csv('C:\TuDiabetes_Code - Final\Data_file\users_final.csv', names=colnames)
    users = data.user_id.tolist()
    # print len(users)
    # print "============== \n"
    # print users
    # print users
    return users

# ----------------------------------------------------------------------
def csv_Another_type_of_diabetes(x):
    colnames = [x]
    data = pandas.read_csv("C:\TuDiabetes_Code - Final\DiabetesTypes\Another_type_of_diabetes.csv", names=colnames)
    users = data.Another_type_of_diabetes.tolist()
    return users
# ----------------------------------------------------------------------
def csv_Gestational_diabetes(x):
    colnames = [x]
    data = pandas.read_csv("C:\TuDiabetes_Code - Final\DiabetesTypes\Gestational_diabetes.csv", names=colnames)
    users = data.Gestational_diabetes.tolist()
    return users
# ----------------------------------------------------------------------
def csv_Idk_type_of_diabetes(x):
    colnames = [x]
    data = pandas.read_csv("C:\TuDiabetes_Code - Final\DiabetesTypes\Idk_type_of_diabetes.csv", names=colnames)
    users = data.Idk_type_of_diabetes.tolist()
    return users
# ----------------------------------------------------------------------
def csv_No_diabetes(x):
    colnames = [x]
    data = pandas.read_csv("C:\TuDiabetes_Code - Final\DiabetesTypes\No_diabetes.csv", names=colnames)
    users = data.No_diabetes.tolist()
    return users
# ----------------------------------------------------------------------
def csv_Pre_diabetes(x):
    colnames = [x]
    data = pandas.read_csv("C:\TuDiabetes_Code - Final\DiabetesTypes\Pre_diabetes.csv", names=colnames)
    users = data.Pre_diabetes.tolist()
    return users
# ----------------------------------------------------------------------
def csv_Type1(x):
    colnames = [x]
    data = pandas.read_csv("C:\TuDiabetes_Code - Final\DiabetesTypes\Type1.csv", names=colnames)
    users = data.Type1.tolist()
    return users
# ----------------------------------------------------------------------
def csv_Type2(x):
    colnames = [x]
    data = pandas.read_csv("C:\TuDiabetes_Code - Final\DiabetesTypes\Type2.csv", names=colnames)
    users = data.Type2.tolist()
    return users
# ----------------------------------------------------------------------
### export discussions to csv file  C:\TuDiabetes_Code - Final\DiabetesTypes\Another_type_of_diabetes.csv
def discussions(db, COLL_DISCUSSION, COLL_SAVE_STATUS):

    # user_final_list = csv_usercol()

    # Another_type_of_diabetes= csv_Another_type_of_diabetes('Another_type_of_diabetes')
    # Gestational_diabetes=csv_Gestational_diabetes('Gestational_diabetes')
    # Idk_type_of_diabetes=csv_Idk_type_of_diabetes('Idk_type_of_diabetes')
    # No_diabetes=csv_No_diabetes('No_diabetes')
    # Pre_diabetes=csv_Pre_diabetes('Pre_diabetes')
    # Type1= csv_Type1('Type1')
    # Type2= csv_Type2('Type2')

    cursor = db[COLL_DISCUSSION].find()
    coll_status = db[COLL_SAVE_STATUS]

    Tech_Cat_ID=['28','29','30','31','33','43','53','54']
    Cat_ID = ['1','3','5','6','7','8','9','10','11','12','13','14','15','16','17','20','21','22','23','24','25','27','28','29','30','31','32','33','34','35','36','37','38','39','40','41','42','43','44','45']

    c_dic= {-1:"", 1:"General", 3:'TuDiabetes Website',  5:'Type 1 and LADA / none',  6:'New to Type 1 Diabetes',  7:'Parents of Children with Type 1 Diabetes',  8:'Teens and Young Adults',  9:'Type 2',  10:'New to Type 2 diabetes',  11:'Teens and Young Adults',  12:'Diabetes and Pregnancy',  13: 'gestational diabetes',  14:'Trying to Get Pregnant',  15:'Managing Pregnancy with Diabetes',  16:'Community',  17:'Share Your Stories',  18:'Fun and Games',  19:'Arts and Poetry',  52:'Giveaways',  20:'Treatment',  22:'Oral Medications and non-insulin injectables',  23:'Insulin',  24:'Research/Cure',  25:'Food / none',  26:'Recipes',  27:'Nutrition',  28:'Diabetes Technology / none',  29:'Insulin Pumps',  30:'Glucose Monitoring',  31:'Diabetes Apps',  53:'DIY Closed Loop Systems',  54:'Commercial Closed Loop Systems',  32:'Healthy Living',  33:'Physical Activity',  34:'Weight',  35:'Mental and Emotional Wellness',  36:'Diabetes Complications and other Conditions',  37:'Eyes',  38:'Kidneys',  39:'Feet',  40:'Digestion',  41:'Other Conditions',  42:'Diabetes Advocacy',  43:'Self Advocacy',  44:'Public Advocacy', 53:'DIY Closed Loop Systems', 54:'Commercial Closed Loop Systems'}

    header_disucssion = "like_count,highest_post_number,discuss_id,user_id,category_id,category_name,title,last_posted_at,participant_count,views,reply_count,links,sum_of_clicks,replies"
    header_replies = ",post_number,quote_count,updated_at,moderator,reads,reply_count,id,avg_time,cooked,topic_id,username,user_created_at,user_id,incoming_link_count,reply_to_post_number"
    header = header_disucssion + header_replies

    # f = open("discussions.csv", "a")
    if(coll_status.find({"collection":"discussion_export"}).count() == 0):
        # f.write(header)
        data = [header.split(",")]
        csv_writer(data, "discussions.csv")

    cnt = 0
    for d in cursor:

        like_count = -1
        highest_post_number = -1
        discuss_id = -1
        user_id = -1
        category_id=-1
        category_name=-1
        title = ""
        last_posted_at = -1
        participant_count = -1
        views = -1
        reply_count = -1
        links = -1
        sum_of_clicks = -1
        replies = -1

        try:
            d['like_count']
        except KeyError:
            continue
        else:
            like_count = d['like_count']

        try:
            d['highest_post_number']
        except KeyError:
            continue
        else:
            highest_post_number = d['highest_post_number']

        try:
            d['id']
        except KeyError:
            continue
        else:
            discuss_id = d['id']



        try:
            d['user_id']
        except KeyError:
            continue
        else:
            user_id = d['user_id']

        try:
            d['category_id']
        except KeyError:
            continue
        else:
            # print "category_id : " + str(category_id) + "----- Discussion_ID :  "+ str(discuss_id)
            category_id = d['category_id']
            # print "category_id : " + str(category_id) + "----- Discussion_ID :  "+ str(discuss_id)
            category_name = c_dic[category_id]

        try:
            d['title']
        except KeyError:
            continue
        else:
            title = d['title'].replace(",", "").encode('ascii', 'ignore')

        try:
            d['last_posted_at']
        except KeyError:
            continue
        else:
            last_posted_at = d['last_posted_at']

        try:
            d['participant_count']
        except KeyError:
            continue
        else:
            participant_count = d['participant_count']

        try:
            d['views']
        except KeyError:
            continue
        else:
            views = d['views']

        try:
            d['reply_count']
        except KeyError:
            continue
        else:
            reply_count = d['reply_count']

        try:
            d["details"]["links"]
        except KeyError:
            continue
        else:
            l_dict = d["details"]["links"]
            links = len(l_dict)
            for l in l_dict:
                sum_of_clicks = sum_of_clicks + l["clicks"]

        try:
            d["post_stream"]["posts"]
        except KeyError:
            continue
        else:
            replies = len(d["post_stream"]["posts"]) - 1

        line_discuss = [like_count,highest_post_number,discuss_id,user_id,category_id,category_name,title,last_posted_at,participant_count,views,reply_count,links,sum_of_clicks,replies]
        line_discuss_str = [str(i) for i in line_discuss]
        line_discuss_str = ",".join(line_discuss_str)

        # print line_discuss
        # print line_discuss_str
        # pprint.pprint( d["post_stream"]["posts"])

        for p in d["post_stream"]["posts"]:

            post_number = -1
            quote_count = -1
            updated_at = ""
            moderator = ""
            reads = -1
            reply_count = -1
            id = -1
            avg_time = -1
            cooked = ""
            topic_id = -1
            username = ""
            user_created_at = ""
            user_id = -1
            incoming_link_count = -1
            reply_to_post_number = -1

            post_number = p["post_number"]
            quote_count = p["quote_count"]
            updated_at = p["updated_at"]
            moderator = p["moderator"]
            reads = p["reads"]
            reply_count = p["reply_count"]
            id = p["id"]
            avg_time = p["avg_time"]
            cooked = p["cooked"].replace(",", "").encode('ascii', 'ignore')
            topic_id = p["topic_id"]
            username = p["username"]
            user_created_at = p["created_at"]
            user_id = p["user_id"]
            incoming_link_count = p["incoming_link_count"]
            reply_to_post_number = p["reply_to_post_number"]



            # print cooked
            # cooked = re.search('<p>(.*)</p>', cooked).group(1)
            #
            if fm.check_if_saved(db, COLL_SAVE_STATUS, "discussion_export", id):
                print "Reply ID : " + str(id) + " already exported"
            elif str(category_id) in Tech_Cat_ID:
                soup  = BeautifulSoup(cooked)
                cooked_parsed = ""

                try:
                    soup.blockquote.text
                except AttributeError:
                    # print "blockquote skipped"
                    blockquote_parsed = ""
                    # continue
                else:
                    blockquote_parsed = soup.blockquote.text
                # blockquote_parsed = soup.blockquote.text

                try:
                    soup.findAll("p")
                except AttributeError:
                    print "p tag skipped"
                    print soup
                    continue
                else:
                    for p in soup.findAll("p"):
                        cooked_parsed = cooked_parsed + ''.join(p.findAll(text=True))

                Doc = cooked_parsed

                # blockquote_parsed = re.sub(r'[^a-zA-Z0-9-@\s]+', '', blockquote_parsed).lower().strip().replace("\n", " ")
                # cooked_parsed = re.sub(r'[^a-zA-Z0-9\s]+', '', cooked_parsed).lower().strip().replace("\n", " ")
                # # remove the blockquote section from cooked
                # cooked_parsed = re.sub(blockquote_parsed, "", cooked_parsed)

                # Doc= cooked_parsed
                # cooked_parsed=clean(cooked_parsed)
                cooked_parsed = cooked_parsed.lower().strip().replace("\n", " ").replace("."," ").replace("-",' ')
                # Remove punctuation
                cooked_parsed = result = re.sub(r"http\S+", "", cooked_parsed)
                cooked_parsed = result = re.sub(r"@\S+", "", cooked_parsed)
                #
                # cooked_parsed = re.sub(r'[^\w\s]', '', cooked_parsed).replace("  "," ")
                # # # Remove HTML tags:
                # # cooked_parsed = re.sub('<[^<]+?>', '', cooked_parsed)
                # # # Remove URLs:
                #
                # # Standardize words (remove multiple letters):
                # cooked_parsed = ''.join(''.join(s)[:2] for _, s in itertools.groupby(cooked_parsed))
                # cooked_parsed = lda.clean(cooked_parsed)
                # Call Clean Function
                # cooked_parsed=clean(cooked_parsed)




                # --------- Carete the Text data files
                print user_id
                print Doc
                print cooked_parsed+"\n==========================================================\n"
                # print type(user_id), "  ", type(user_final_list[0])
                # if str(user_id) in user_final_list:
                #     with open("C:/TuDiabetes_Code - Final/"+"Text/"+str(user_id)+".txt", "a") as f:
                #         f.write(cooked_parsed+"\n\n\n")
                #         f.close()
                # =========================================================================================
                # if str(user_id) in Another_type_of_diabetes:
                #     with open("C:/TuDiabetes_Code - Final/Types_Text/Another_type_of_diabetes.txt", "a") as f:
                #         f.write(cooked_parsed)
                #         f.close()
                # elif str(user_id) in Gestational_diabetes:
                #        with open("C:/TuDiabetes_Code - Final/Types_Text/Gestational_diabetes.txt", "a") as f:
                #             f.write(cooked_parsed)
                #             f.close()
                # elif str(user_id) in Idk_type_of_diabetes:
                #        with open("C:/TuDiabetes_Code - Final/Types_Text/Idk_type_of_diabetes.txt", "a") as f:
                #             f.write(cooked_parsed)
                #             f.close()
                # elif str(user_id) in No_diabetes:
                #        with open("C:/TuDiabetes_Code - Final/Types_Text/No_diabetes.txt", "a") as f:
                #             f.write(cooked_parsed)
                #             f.close()
                # elif str(user_id) in Pre_diabetes:
                #        with open("C:/TuDiabetes_Code - Final/Types_Text/Pre_diabetes.txt", "a") as f:
                #             f.write(cooked_parsed)
                #             f.close()
                # elif str(user_id) in Type1:
                #        with open("C:/TuDiabetes_Code - Final/Types_Text/Type1_Diabites.txt", "a") as f:
                #             f.write(cooked_parsed)
                #             f.close()
                # elif str(user_id) in Type2:
                #        with open("C:/TuDiabetes_Code - Final/Types_Text/Type2_Diabites.txt", "a") as f:
                #             f.write(cooked_parsed)
                #             f.close()
                # ===========================================================================================

                # if str(user_id) in Another_type_of_diabetes:
                #     with open("C:/TuDiabetes_Code - Final/Types_Text/Another_type_of_diabetes.txt", "a") as f:
                #         f.write(cooked_parsed)
                #         f.close()
                # elif str(user_id) in Gestational_diabetes:
                #        with open("C:/TuDiabetes_Code - Final/Types_Text/Gestational_diabetes.txt", "a") as f:
                #             f.write(cooked_parsed)
                #             f.close()
                # elif str(user_id) in Idk_type_of_diabetes:
                #        with open("C:/TuDiabetes_Code - Final/Types_Text/Idk_type_of_diabetes.txt", "a") as f:
                #             f.write(cooked_parsed)
                #             f.close()
                # elif str(user_id) in No_diabetes:
                #        with open("C:/TuDiabetes_Code - Final/Types_Text/No_diabetes.txt", "a") as f:
                #             f.write(cooked_parsed)
                #             f.close()
                # elif str(user_id) in Pre_diabetes:
                #        with open("C:/TuDiabetes_Code - Final/Types_Text/Pre_diabetes.txt", "a") as f:
                #             f.write(cooked_parsed)
                #             f.close()
                # elif str(user_id) in Type1:
                #        with open("C:/TuDiabetes_Code - Final/Types_Text/Type1_Diabites.txt", "a") as f:
                #             f.write(cooked_parsed)
                #             f.close()
                # elif str(user_id) in Type2:
                #        with open("C:/TuDiabetes_Code - Final/Types_Text/Type2_Diabites.txt", "a") as f:
                #             f.write(cooked_parsed)
                #             f.close()


                # if str(category_id) in Tech_Cat_ID:
                #        with open("C:/TuDiabetes_Code - Final/Types_Text/Diabetes_Technology.txt", "a") as f:
                #             f.write(cooked_parsed)
                #             f.close()

                # ===========================================================================================
                C_name= re.sub(r'[^\w\s]', '', str(category_name)).replace("  "," ").strip()
                print C_name
                if str(category_id) in Cat_ID:
                    with open("C:/TuDiabetes_Code - Final/Diabetes_Text/All.txt", "a") as f:
                        f.write(cooked_parsed)
                        f.close()
                    with open("C:/TuDiabetes_Code - Final/Diabetes_Text/"+C_name+".txt", "a") as f:
                        f.write(cooked_parsed)
                        f.close()
                        print "\n *****   " + str(category_id) + "   *****   "+ C_name + "   ******"

                # #===============================================================================================
                # C_name= re.sub(r'[^\w\s]', '', str(category_name)).replace("  "," ")
                # print C_name
                # if str(category_id)== "28":
                #     with open("C:/TuDiabetes_Code - Final/TechTypes_Text_New/Diabetes_Tech_General.txt", "a") as f:
                #         f.write(cooked_parsed)
                #         f.close()
                #         print "\n *****   " + str(category_id) + "   *****   "+ str(category_name)+ "   ******"
                # elif str(category_id)== "29":
                #     with open("C:/TuDiabetes_Code - Final/TechTypes_Text_New/Insulin_Pumps.txt", "a") as f:
                #         f.write(cooked_parsed)
                #         f.close()
                #         print "\n *****   " + str(category_id) + "   *****"
                # elif str(category_id)== "30":
                #     with open("C:/TuDiabetes_Code - Final/TechTypes_Text_New/Glucose_Monitoring.txt", "a") as f:
                #         f.write(cooked_parsed)
                #         f.close()
                #         print "\n *****   " + str(category_id) + "   *****"
                # elif str(category_id)== "31":
                #     with open("C:/TuDiabetes_Code - Final/TechTypes_Text_New/Diabetes_Apps.txt", "a") as f:
                #         f.write(cooked_parsed)
                #         f.close()
                #         print "\n *****   " + str(category_id) + "   *****"
                # elif str(category_id)== "33":
                #     with open("C:/TuDiabetes_Code - Final/TechTypes_Text_New/Physical_Activity.txt", "a") as f:
                #         f.write(cooked_parsed)
                #         f.close()
                #         print "\n *****   " + str(category_id) + "   *****"
                # elif str(category_id)== "43":
                #     with open("C:/TuDiabetes_Code - Final/TechTypes_Text_New/Self_Advocacy.txt", "a") as f:
                #         f.write(cooked_parsed)
                #         f.close()
                #         print "\n *****   " + str(category_id) + "   *****"
                # # ===========================================================================================
                # # print ">"*20
                # print "cooked " + str(len(cooked))
                # print cooked
                # print "-"*20
                # print "blockquote parsed " + str(len(blockquote_parsed))
                # print blockquote_parsed
                # print "-"*20
                # print "cooked parsed "+ str(len(cooked_parsed))
                # print cooked_parsed
                # print ">"*20

                # cooked_parsed = ""

                line_post = [post_number, quote_count, updated_at, moderator, reads, reply_count, id, avg_time, cooked_parsed, topic_id, username, user_created_at, user_id, incoming_link_count, reply_to_post_number]

                # print line_discuss
                # print len(line_post)

                line_post = [str(i) for i in line_post]
                line_post = ",".join(line_post).replace("\n", "")

                final_line = line_discuss_str+","+line_post+"\n"

                final_line  = final_line.encode('ascii', 'ignore')
                # print final_line
                data = [final_line.split(",")]
                csv_writer(data, "discussions.csv")
                # f.write(final_line)
                coll_status.insert_one({"collection":"discussion_export", "id":id})
                # cnt += 1
                # print "Count: ", cnt, " Reply ID: ", id
                print "Reply ID : " + str(id) + " Exported To CSV File" + "----- Discussion_ID :  "+ str(discuss_id)

