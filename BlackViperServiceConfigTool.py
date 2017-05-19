######################################################################################
# Black Viper's Windows Service Configurations
#
######################################################################################
import os
from bs4 import BeautifulSoup
import urllib2

def WinXP_SP3_x86():
    url = "http://www.blackviper.com/service-configurations/black-vipers-windows-xp-x86-32-bit-service-pack-3-service-configurations"
    winver = "Windows XP SP3 x86"
    crawler(url)
    write_file(winver)

def WinXP_Pro_SP2_x64():
    url = "http://www.blackviper.com/service-configurations/black-vipers-windows-xp-pro-x64-64-bit-service-pack-2-service-configurations"
    winver = "Windows XP SP2 x64"
    crawler(url)
    write_file(winver)

def WinVista_SP2():
    url = "http://www.blackviper.com/service-configurations/black-vipers-windows-vista-service-pack-2-service-configurations"
    winver = "Windows Vista SP2"
    crawler(url)
    write_file(winver)

def Win7_SP1():
    url = "http://www.blackviper.com/service-configurations/black-vipers-windows-7-service-pack-1-service-configurations"
    winver = "Windows 7 SP1"
    crawler(url)
    write_file(winver)

def Win8():
    url = "http://www.blackviper.com/service-configurations/black-vipers-windows-8-service-configurations"
    winver = "Windows 8"
    crawler(url)
    write_file(winver)

def Win8_1():
    url = "http://www.blackviper.com/service-configurations/black-vipers-windows-8-1-service-configurations"
    winver = "Windows 8.1"
    crawler(url)
    write_file(winver)

def Win10():
    url = "http://www.blackviper.com/service-configurations/black-vipers-windows-10-service-configurations"
    winver = "Windows 10"
    crawler(url)
    write_file(winver)

def crawler(url):
    header = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(url,headers=header)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page, "lxml")

    ColumnName = ""
    ColumnNamebr = ""
    CellValue = ""
    CellValuebr = ""
    cell_tmp = ""
    col_tmp = ""

    table = soup.find("table", { "class" : "tablepress" })

    f = open('configuration', 'w')

    for row in table.findAll("tr"):
        #ColumnHeads
        col_name = row.findAll("th")
        for z in col_name:
            if len(z) == 1:
                if ColumnName=="":
                    ColumnName = str(z.find(text=True)).encode('utf-8').strip()
                else:
                    ColumnName = ColumnName + ";" + str(z.find(text=True)).encode('utf-8').strip()
            else:
                ColumnNamebr = z.findAll(text=True)
                for y in range(len(ColumnNamebr)):
                    col_list = ColumnNamebr[y].split(",")
                    for m in range(len(col_list)):
                        if col_tmp=="":
                            col_tmp = col_list[m].lstrip('\n').strip().encode('utf-8')
                        else:
                            col_tmp = col_tmp + " " + col_list[m].lstrip('\n').strip().encode('utf-8')
                if ColumnName == "":
                    ColumnName = col_tmp.strip()
                else:
                    ColumnName = ColumnName + ";" + col_tmp.strip()
                col_tmp = ""

        if len(col_name)>0:
            f.write(ColumnName.replace('"','') + "\n")

        #CellValues
        cells = row.findAll("td")
        for x in cells:
            if len(x) == 1:
                if CellValue=="":
                    CellValue = str(x.find(text=True).encode('utf-8')).strip()
                else:
                    CellValue = CellValue + ";" + str(x.find(text=True).encode('utf-8')).strip()
            else:
                CellValuebr = x.findAll(text=True)
                for x in range(len(CellValuebr)):
                    cell_list = CellValuebr[x].split(",")
                    for i in range(len(cell_list)):
                        if cell_tmp=="":
                            cell_tmp = cell_list[i].lstrip('\n').strip()
                        else:
                            cell_tmp = cell_tmp + " " + cell_list[i].lstrip('\n').strip()
                if CellValue == "":
                    CellValue = cell_tmp.strip()
                else:
                    CellValue = CellValue + ";" + cell_tmp.strip()
                cell_tmp = ""

        if len(col_name)==0:
            f.write(CellValue + "\n")
            CellValue = ""

    f.close()

def write_file(winver):
    filename = "configuration"
    with open(filename) as f:
      lis = [x.split(";") for x in f]
    lstAutomatic = []
    lstManual = []
    lstDisabled = []
    info = [line for line in zip(*lis)]

    print ""

    for line in info[2:]:
        tmpStr = line[0].replace('\n', ''.replace('"', '').strip())
        if winver == "Windows 7 SP1":
            if "Safe" in tmpStr: tmpStr = "Safe"        
        fileOutName = '%s - %s.txt' % (winver, tmpStr)
        if tmpStr == "Quick Notes": continue
        print(fileOutName)
        scriptOut = open(fileOutName, "w")
        
        for regEntry, mode in zip(info[1][1:], line[1:]):
            if mode.startswith("Manual"):
                lstManual.append(regEntry)
            if mode.startswith("Not Installed") or mode.startswith("Not installed") or mode.startswith("Not Available"):
                continue
            if mode.startswith("Automatic"):
                lstAutomatic.append(regEntry)
            if mode.startswith("Disabled"):
                lstDisabled.append(regEntry)
            if mode.startswith("Uninstalled"):
                continue
            if regEntry.startswith("?"):
                continue
            if regEntry.endswith("?"):
                continue
        scriptOut.write("Automatic:\n")
        for item in lstAutomatic:
            if item == lstAutomatic[len(lstAutomatic)-1]:
                scriptOut.write("%s" % item)
            else:
                scriptOut.write("%s " % item)
        scriptOut.write("\n")
        scriptOut.write("\nManual:\n")
        scriptOut.write("\n")
        for item in lstManual:
            if item == lstManual[len(lstManual)-1]:
                scriptOut.write("%s" % item)
            else:
                scriptOut.write("%s " % item)
        scriptOut.write("\n")
        scriptOut.write("\nDisabled:\n")
        scriptOut.write("\n")
        for item in lstDisabled:
            if item == lstDisabled[len(lstDisabled)-1]:
                scriptOut.write("%s" % item)
            else:
                scriptOut.write("%s " % item)
        scriptOut.close()
        del lstAutomatic[:]
        del lstManual[:]
        del lstDisabled[:]
    os.remove(filename)
    print ""

def handle_menu(menu):
    while True:
        for index, item in enumerate(menu, 1):
            print("{}  {}".format(index, item[0]))
        choice = int(raw_input("\nWhat should i do? ")) - 1
        if 0 <= choice < len(menu):
            menu[choice][1]()
        else:
            print("\nOnly number in range 1 - {} allowed".format(len(menu)))

print "##################################################"
print "#                                                #"
print "#  Black Viper's Windows Service Configurations  #"
print "#                                                #"
print "#                 v0.2 by rype                   #"
print "##################################################\n"

menu = [
    ["Windows XP SP3 x86", WinXP_SP3_x86],
    ["Windows XP Pro SP2 x64", WinXP_Pro_SP2_x64],
    ["Windows Vista SP2", WinVista_SP2],
    ["Windows 7 SP1", Win7_SP1],
    ["Windows 8", Win8],
    ["Windows 8.1", Win8_1],
    ["Windows 10", Win10],
    ["Exit Tool", quit]
]

handle_menu(menu)
