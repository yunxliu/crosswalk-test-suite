#!/usr/bin/env python
import sys, os, os.path, shutil, time
import glob
import thread, Queue
import comm, ge_package

import metacomm.combinatorics.all_pairs2
all_pairs = metacomm.combinatorics.all_pairs2.all_pairs2

totalNum = 0
result = ""

def genSelfcom(combIn, combOut):
    try:
        fp = open(combIn)
        comb = open(combOut, 'a+')
        comb.write(fp.read())
        fp.close()
        comb.close()
        print "Update selfcomb.txt ---------------->O.k"
        return
    except Exception,e:
        print Exception,"Update selfcomb.txt error:",e
        print "Update selfcomb.txt ---------------->Error"
        sys.exit(1)

def genmanifest(caseInput, flag):
    try:
        manifestLog = open(comm.ConstPath + "/../report/manifest_"+ flag + ".txt", 'a+')

        caseIn = open(caseInput)
        line = caseIn.readline().strip('\n\r')
        sectionList = line.split("\t")

        global totalNum 
        for line in caseIn:
            totalNum = totalNum + 1
            caseValue = ""
            print "##########"
            print "Case" + str(totalNum) + " :"
            print "Generate manifest.json ---------------->Start"
            items = line.strip('\n\r').split("\t")
            caseDir = comm.ConstPath + "/../tcs/manifest" + str(totalNum) + "-" + flag 
            if not os.path.exists(caseDir):
                os.mkdir(caseDir)
            fp = open(caseDir + "/manifest.json", 'w+')
            for i in range(len(items)):
                items[i] = items[i].replace("null","")
                if sectionList[i] not in ("icons", "icon", "background_color", "xwalk_android_permissions", "display"):
                    items[i] = items[i].replace("000", " ")
                    caseValue = caseValue + '"' + sectionList[i] + '" : "' + items[i] + '",\n'
                else:
                    items[i] = items[i].replace("comma", ",")
                    caseValue = caseValue + '"' + sectionList[i] + '" : ' + items[i] + ",\n"
            caseValue = "{\n" + caseValue[:-2] + "\n}"
            fp.write(caseValue)
            fp.close()
            print "Generate manifest.json ---------------->O.K"
            print caseValue
            manifestLog.write("manifest" + str(totalNum) + "\n--------------------------------\n" + caseValue + "\n--------------------------------\n")

            #copy source and config
            os.system("cp -rf " + comm.ConstPath + "/../resource/* " + caseDir)
        caseIn.close()
        manifestLog.close()
        print "Execute case ---------------->O.K"
    except Exception,e:
        print Exception,":",e
        print "Execute case ---------------->Error"
        sys.exit(1)

def lineCount(fp):
    fileTmp = open(fp)
    count = len(fileTmp.readlines())
    fileTmp.close()
    return count


def processTest(seedIn, flag):
    try:
        fileName = os.path.basename(seedIn)
        name = os.path.splitext(fileName)[0]
        print "Input Seed : " + fileName
        print "Excute " + flag + " cases ------------------------->Start"
        row = 0
        sectionList = []

        fp = open(seedIn)
        for line in fp:
            items = line.strip('\n\r').split(":")
            sectionName = items[0].split("-")[0]
            if sectionName not in sectionList:
                sectionList.append(sectionName)
            inputTxt = open(comm.ConstPath + "/../self/" + sectionName + "_input.txt", "a+")
            inputTxt.write(line)
            inputTxt.close()
        fp.close()

        for section in sectionList:
            caseline = ""
            counters = lineCount(comm.ConstPath + "/../self/" + section + "_input.txt")
            if counters >= 2:
                lists = [[] for m in range(counters)]
                inputTxt = open(comm.ConstPath + "/../self/" + section + "_input.txt", 'r+')
                for line in inputTxt:
                    items = line.strip('\n\r').split(":")
                    values = ":".join(items[1:]).split(",")
                    lists[row].extend(values)
                    row = row + 1
                pairs = all_pairs(lists)
                inputTxt.close()
                outTxt = open(comm.ConstPath + "/../self/" + section + "_output.txt", 'a+')
                for e, v in enumerate(pairs):
                    for c in range(len(v)):
                        caseline = caseline + v[c] + ","
                outTxt.write(section + ":" + caseline[:-1] + "\n")
                outTxt.close()
            else:
                shutil.copy(comm.ConstPath + "/../self/" + section + "_input.txt", comm.ConstPath + "/../self/" + section + "_output.txt")

        #1*********XX_output.txt -> selfcomb.txt
            genSelfcom(comm.ConstPath + "/../self/" + section + "_output.txt", comm.ConstPath + "/../allpairs/selfcomb.txt")

        #2*********selfcomb.txt -> caseXX.txt
        genCases(comm.ConstPath + "/../allpairs/selfcomb.txt", name, flag)

        #3*********output -> manifest.json
        genmanifest(comm.ConstPath + "/../allpairs/" + name + "_case.txt", flag)

        print "Excute " + flag + " cases ------------------------->O.K"
        print
    except Exception,e:
        print "Excute " + flag + " cases ------------------------->Error"
        print Exception,":",e
        sys.exit(1)


def genCases(selfcomb, name, flag):
    try:
        print "Genarate " + flag + " case.txt file ---------------->Start"
        caseFile = open(comm.ConstPath + "/../allpairs/" + name + "_case.txt", 'w+')
        names = ""
        row = 0
        counters = lineCount(selfcomb)
        lists = [[] for m in range(counters)]
        fobj = open(selfcomb)
        for line in fobj:
            items = line.strip('\n\r').split(":")
            names = names + items[0] + "\t"
        caseFile.write(names.rstrip("\t") + "\n")

        fobj.seek(0)
        for line in fobj:
            items = line.strip('\n\r').split(":")
            values = items[1:]
            lists[row].extend(":".join(values).split(","))
            row = row + 1
        fobj.close()

        pairs = all_pairs(lists)
        for e, v in enumerate(pairs):
            case = ""
            for c in range(0,len(v)):
                case = case + v[c] +"\t"
            caseFile.write(case.rstrip("\t") + "\n")
        caseFile.close()
        print "Genarate " + flag + " case.txt file ---------------->O.k"
    except Exception,e:
        print "Generate " + flag + " case.txt file ---------------->Error"
        print Exception,":",e
        sys.exit(1)


def sourceInit():
    try:
        if os.path.exists(comm.ConstPath + "/../tcs") or os.path.exists(comm.ConstPath + "/../apks") or os.path.exists(comm.ConstPath + "/../report"):
            try:
                shutil.rmtree(comm.ConstPath + "/../tcs")
                shutil.rmtree(comm.ConstPath + "/../apks")
                shutil.rmtree(comm.ConstPath + "/../report")
            except Exception,e:
                os.system("rm -rf " + comm.ConstPath + "/../tcs/* &>/dev/null")
                os.system("rm -rf " + comm.ConstPath + "/../apks/* &>/dev/null")
                os.system("rm -rf " + comm.ConstPath + "/../report/* &>/dev/null")
            if os.path.exists(comm.ConstPath + "/tests.py"):
                os.remove(comm.ConstPath + "/tests.py")
            os.mkdir(comm.ConstPath + "/../tcs")
            os.mkdir(comm.ConstPath + "/../report")
            txt_list = glob.glob(comm.ConstPath + "/../allpairs/*.txt")
            for item in txt_list:
                os.remove(item)
        else:
            os.mkdir(comm.ConstPath + "/../tcs")
            os.mkdir(comm.ConstPath + "/../report")

        Start = time.strftime("%Y-%m-%d %H:%M:%S")
        print "Start time: " + Start
        for flag in ["positive", "negative"]:
            for seedIn in os.listdir(comm.ConstPath + "/../allpairs/" + flag + "/"):
                if os.path.exists(comm.ConstPath + "/../self"):
                    txt_list = glob.glob(comm.ConstPath + "/../self/*.txt")
                    for item in txt_list:
                        os.remove(item)
                else:
                    os.mkdir(comm.ConstPath + "/../self")
                
                if os.path.exists(comm.ConstPath + "/../allpairs/selfcomb.txt"):
                    try:
                        os.remove(comm.ConstPath + "/../allpairs/selfcomb.txt")
                    except Exception,e:
                        os.system("rm -rf " + comm.ConstPath + "/../allpairs/selfcomb.txt &>/dev/null")
                
                processTest(comm.ConstPath + "/../allpairs/" + flag + "/" + seedIn, flag)
        End = time.strftime("%Y-%m-%d %H:%M:%S")
        print "End time: " + End
    except Exception,e:
        print Exception,":",e
        sys.exit(1)

if __name__ == "__main__":
    sourceInit()
