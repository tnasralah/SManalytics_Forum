import itertools
import xlsxwriter as xlsxwriter


def Excelfile(li,i):
    workbook = xlsxwriter.Workbook('Words.xlsx')
    worksheet1 = workbook.add_worksheet()
    worksheet1.write(i,0, li)
    # i= i+1
    workbook.close()

def readwords(mfile):
    byte_stream = itertools.groupby(
      itertools.takewhile(lambda c: bool(c),
          itertools.imap(mfile.read,
              itertools.repeat(1))), str.isspace)

    return ("".join(group) for pred, group in byte_stream if not pred)

def main():
    w=[]
    i =0
    # with open("C:\TuDiabetes_Code\TechTypes_Text\Mix.txt", 'r') as file:
    #     for word in readwords(f):
    #         w.append(str(word))
    #         Excelfile(str(word),i)
    #         i=i+1
    #         # print(word)
    # print(w)
    file = open("C:\TuDiabetes_Code\TechTypes_Text\Mix.txt", "r+")
    wordcount = {}
    for word in file.read().split():
        if word not in wordcount:
            wordcount[word] = 1
        else:
            wordcount[word] += 1

    for k, v in wordcount.items():
        print k, v
    file.close();
    # Excelfile(w)
if __name__ == '__main__':
    main()