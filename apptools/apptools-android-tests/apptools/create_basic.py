#!/usr/bin/env python
#
# Copyright (c) 2015 Intel Corporation.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of works must retain the original copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the original copyright
#   notice, this list of conditions and the following disclaimer in the
#   documentation and/or other materials provided with the distribution.
# * Neither the name of Intel Corporation nor the names of its contributors
#   may be used to endorse or promote products derived from this work without
#   specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY INTEL CORPORATION "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL INTEL CORPORATION BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY
# OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors:
#         Hongjuan, Wang<hongjuanx.wang@intel.com>
#         Yun, Liu<yunx.liu@intel.com>

import unittest
import os
import comm
import zipfile
import shutil


class TestCrosswalkApptoolsFunctions(unittest.TestCase):

    def test_create_crosswalkdir(self):
        comm.setUp()
        os.chdir(comm.XwalkPath)
        crosswalkdir = zipfile.ZipFile(comm.crosswalkzip,'r')
        for file in crosswalkdir.namelist():
            crosswalkdir.extract(file, r'.')
        crosswalkdir.close()
        comm.clear("org.xwalk.test")
        cmd = comm.HOST_PREFIX + comm.PackTools + \
            "crosswalk-app create org.xwalk.test" + comm.MODE + " --android-crosswalk=" + comm.crosswalkzip[:comm.crosswalkzip.index(".zip")] + "/ "
        return_code = os.system(cmd)
        self.assertEquals(return_code, 0)
        comm.clear("org.xwalk.test")
        shutil.rmtree(comm.crosswalkzip[:comm.crosswalkzip.index(".zip")])

    def test_dir_exist(self):
        comm.setUp()
        os.chdir(comm.XwalkPath)
        comm.clear("org.xwalk.test")
        os.mkdir("org.xwalk.test")
        cmd = comm.HOST_PREFIX + comm.PackTools + \
            "crosswalk-app create org.xwalk.test" + comm.MODE + " --android-crosswalk=" + \
            comm.crosswalkzip
        return_code = os.system(cmd)
        self.assertNotEquals(return_code, 0)
        comm.clear("org.xwalk.test")

    def test_main_activity(self):
        comm.setUp()
        comm.create(self)
        os.chdir('org.xwalk.test/prj/android')
        fp = open(os.getcwd() + '/AndroidManifest.xml')
        lines = fp.readlines()
        for i in range(len(lines)):
            line = lines[i].strip(' ').strip('\n\t')
            findLine = "<activity"
            if i <= len(lines):
                if findLine in line:
                    print "Find"
                    start = line.index("name")
                    self.assertIn('TestActivity', line[start:])
                    break
                else:
                    print "Continue find"
            else:
                self.assertIn(findLine, line)
        fp.close()
        comm.clear("org.xwalk.test")

if __name__ == '__main__':
    unittest.main()     
