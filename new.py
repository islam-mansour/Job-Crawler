import xlrd, xlwt
import operator

workbook0 = xlrd.open_workbook('Programming Data_101.xlsx')
sheet0 = workbook0.sheet_by_name('Sheet1')

All = []
Languages = []
Frameworks = []
Libraries_APIs = []
Storage = []
Other = []

for i in range(2, 24):
    Languages.append(sheet0.cell(i,2).value)

for i in range(26, 70):
    Frameworks.append(sheet0.cell(i,2).value)

for i in range(72, 115):
    Libraries_APIs.append(sheet0.cell(i,2).value)

for i in range(118, 133):
    Storage.append(sheet0.cell(i,2).value)

for i in range(135, 234):
    Other.append(sheet0.cell(i,2).value)

All = Languages + Frameworks + Libraries_APIs + Storage + Other


def divide(desciption):
    test = [w for w in desciption.split()]
    words = []
    for x in test:
        x = x.split(',')
        for j in x:
            words.append(j)
    return words



workbook_read = xlrd.open_workbook('indeed.xlsx')
sheet_read = workbook_read.sheet_by_name('Worksheet')

statistics = {}

workbook_write = xlwt.Workbook()

for k in range(1, sheet_read.nrows, 100):
    
    name = 'sheet' + str(int(k/100))
    sheet_write = workbook_write.add_sheet(name)

    sheet_write.write(0,0, "job-title")
    sheet_write.write(0,1, "employer")
    sheet_write.write(0,2, "website")
    sheet_write.write(0,3, "email")
    sheet_write.write(0,4, "phone")
    sheet_write.write(0,5, "names")
    sheet_write.write(0,6, "job_description")

    sheet_write.write(0,sheet_read.ncols, "Languages")
    sheet_write.write(0,sheet_read.ncols+1, "Frameworks")
    sheet_write.write(0,sheet_read.ncols+2, "API/Libraries")
    sheet_write.write(0,sheet_read.ncols+3, "Storage")
    sheet_write.write(0,sheet_read.ncols+4, "Other")

    
    for i in range(k, k+100):
        
        for j in range(0, sheet_read.ncols):
            try:
                sheet_write.write(i-k+1, j, sheet_read.cell(i,j).value)
            except:
                sheet_write.write(i-k+1, j, '')

        description = ''
        try:
            description = sheet_read.cell(i,6).value
        except:
            description = ''

        words = set(divide(description))
        
        Languages_str = ""
        Frameworks_str = ""
        Libraries_APIs_str = ""
        Storage_str = ""
        Other_str = ""
        
        for word in words:

            if word in All and word not in statistics:
                statistics[word] = 0

            if word in All and word in statistics:
                statistics[word] += 1

            if word in Languages:
                Languages_str = Languages_str + "," + word
            if word in Frameworks:
                Frameworks_str = Frameworks_str + "," + word
            if word in Libraries_APIs:
                Libraries_APIs_str = Libraries_APIs_str + "," + word
            if word in Storage:
                Storage_str = Storage_str + "," +  word
            if word in Other:
                Other_str = Other_str + "," + word

        try:
            sheet_write.write(i-k+1,sheet_read.ncols, Languages_str)
            sheet_write.write(i-k+1,sheet_read.ncols+1, Frameworks_str)
            sheet_write.write(i-k+1,sheet_read.ncols+2, Libraries_APIs_str)
            sheet_write.write(i-k+1,sheet_read.ncols+3, Storage_str)
            sheet_write.write(i-k+1,sheet_read.ncols+4, Other_str)
        except:
            print('ouch')

        

sheet_write = workbook_write.add_sheet("statistics")
statistics = sorted(statistics.items(), key=operator.itemgetter(1))
statistics.reverse()

sheet_write.write(0,1, "Technologies Statistics")

sheet_write.write(3,1, "Technology")
sheet_write.write(3,2, "Count")

for i in range(5, len(statistics)):
    sheet_write.write(i,1, statistics[i-5][0])
    sheet_write.write(i,2, statistics[i-5][1])


workbook_write.save('indeed-new.xlsx')


    
    