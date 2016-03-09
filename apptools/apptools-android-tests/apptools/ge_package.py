#!/usr/bin/env python
import sys, os, os.path, shutil, time
import comm, traceback, glob

def genPackage():
    try:
        global result

        #genarate package and execute
        if os.path.exists(comm.ConstPath + "/../report/packRes.txt") and os.path.exists(comm.ConstPath + "/../report/packageInfo.txt"):
            os.remove(comm.ConstPath + "/../report/packRes.txt")
            os.remove(comm.ConstPath + "/../report/packageInfo.txt")
        if os.path.exists(comm.ConstPath + "/../apks") and len(os.listdir(comm.ConstPath + "/../apks")) != 0:
            if comm.ANDROID_MODE in os.listdir(comm.ConstPath + "/../apks"):
                shutil.rmtree(comm.ConstPath + "/../apks/" + comm.ANDROID_MODE)
        else:
            os.mkdir(comm.ConstPath + "/../apks")
        os.mkdir(comm.ConstPath + "/../apks/" + comm.ANDROID_MODE + "/" + comm.ARCH)

        print "Generate APK ---------------->Start"
        casePath = comm.ConstPath + "/../tcs/"
        for i in os.listdir(casePath):
            print "##########"
            print i
            print "##########"
            flag = i[-8:].strip()
            caseStart = time.strftime("%Y-%m-%d %H:%M:%S")
            manifestLog = open(comm.ConstPath + "/../report/packageInfo.txt", 'a+')
            manifestLog.write(i+ "\n")
            manifestLog.write("Build start time: " + caseStart + "\n")
            manifestPath = casePath + i + "/manifest.json"

            if os.path.exists(comm.ConstPath + "/../tools/crosswalk/"):
                apk_list = glob.glob(comm.ConstPath + "/tools/crosswalk/*.apk")
            else:
                apk_list = glob.glob(comm.ConstPath + "/../../tools/crosswalk/*.apk")
            for item in apk_list:
                os.remove(item)

            cmd ="python make_apk.py --package=org.xwalk.test --app-versionCode=123 --arch=" + ARCH + " --manifest="
            status, info = comm.getstatusoutput(cmd + manifestPath)
            if flag == "negative":
                if status == 0:
                    print "Generate APK ---------------->O.K"
                    result = "FAIL"
                    manifestLog.write(result + "\n") 
                else:
                    print "Generate APK ---------------->Error"
                    result = "PASS"
                    manifestLog.write(result + "\n")
            else:
                if status != 0:
                    print "Generate APK ---------------->Error"
                    result = "FAIL"
                    manifestLog.write(result + "\n" + info + "\n")
                else:
                    print "Generate APK ---------------->O.K"
                    if os.path.exists(comm.ConstPath + "/tools/crosswalk/"):
                        apkpath = comm.ConstPath + "/tools/crosswalk/*.apk"
                    else:
                        apkpath = comm.ConstPath + "/../../tools/crosswalk/*.apk"
                    targetDir = comm.ConstPath + "/apks/" + comm.ARCH + "/" + i
                    if not os.path.exists(targetDir):
                        os.mkdir(targetDir)
                    apk_list = glob.glob(apkpath)
                    try:
                        for item in apk_list:
                            name = item.rsplit(os.sep)[-1]
                            shutil.copyfile(item, targetDir + "/" + name)
                    except IOError, e:
                        traceback.print_exc()
                        sys.exit(1)
                    else:
                        result = "PASS"
                        manifestLog.write(result + "\n")
            caseEnd = time.strftime("%Y-%m-%d %H:%M:%S")
            manifestLog.write("Build end time: " + caseEnd + "\n\n")
            manifestLog.flush()
            manifestLog.close()
            print "Package Result :" + result
            fp = open(comm.ConstPath + "/report/packRes.txt", 'a+')
            tt = i + "\t" + flag + "\t" + result + "\n"
            fp.write(tt)
            fp.close()
    except Exception,e:
        print Exception,":",e
        print "Execute case ---------------->Error"
        sys.exit(1)

if __name__ == "__main__":
    genPackage()
