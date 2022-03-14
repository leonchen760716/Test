import sys
import os
import shutil, errno
import ctypes
import datetime

SvnPath = r'C:\"Program Files"\TortoiseSVN\bin\svn.exe'

def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print ('Get small version Utility')
        print ('Usage: Export 50 Source OutputFolder')
        sys.exit(-1)
    StartTime = datetime.datetime.now ()
    OutputFolder = sys.argv[1]
    TestBuild = False
    if OutputFolder.lower () != "test":
      if not os.path.exists (OutputFolder):
          os.makedirs (OutputFolder)
    else:
      TestBuild = True

    os.system (SvnPath + r" export http://svn.insydesw.com/H2O-Kernel/Rev.5.0/Trunk " + OutputFolder + " --force --quiet")
    if not TestBuild:
      print ("Copy " + OutputFolder + " folder to " + OutputFolder + "_org folder....")
      copyanything (OutputFolder, OutputFolder + "_org")
      print ("Copy completed!!")

    #
    # Copy necessary files to exported folder
    #
    shutil.copy(r"E:\SVN\MySvnModified\ProjectBuild.bat",   OutputFolder + r"\StrawberryMountainBoardPkg\ProjectBuild.bat")
    shutil.copy(r"E:\SVN\MySvnModified\ArmBuild.bat",       OutputFolder + r"\InsydeModulePkg\ArmBuild.bat")
    shutil.copy(r"E:\SVN\MySvnModified\callArmBuild.bat",   OutputFolder + r"\InsydeModulePkg\callArmBuild64.bat")
    shutil.copy(r"E:\SVN\MySvnModified\ArmBuild64.bat",     OutputFolder + r"\InsydeModulePkg\ArmBuild64.bat")
    shutil.copy(r"E:\SVN\MySvnModified\callArmBuild64.bat", OutputFolder + r"\InsydeModulePkg\callArmBuild.bat")
    shutil.copy(r"E:\SVN\MySvnModified\KernelBuild.bat",    OutputFolder + r"\KernelBuild.bat")
    shutil.copy(r"E:\SVN\MySvnModified\TotalBuild.bat",     OutputFolder + r"\TotalBuild.bat")
    shutil.copy(r"E:\SVN\MySvnModified\TAGC.BAT",           OutputFolder + r"\TAGC.BAT")
    shutil.copy(r"E:\SVN\MySvnModified\CTAGS.EXE",          OutputFolder + r"\CTAGS.EXE")

    if not TestBuild:
      #
      # Generate Ctag file
      #
      OrgPaht = os.getcwd ()
      os.chdir (OutputFolder)
      os.system ("TAGC.BAT")
      os.chdir (OrgPaht)
      #
      # popup message for user to inidicate process is completed
      #
      EndTime = datetime.datetime.now ()
      print ("Start Time is " + str (StartTime) + ".\nEnd Time is " + str (EndTime) + ".\nDuration is " + str (EndTime - StartTime))
      ctypes.windll.user32.MessageBoxW(0, "Get source code completed!!!", "Proccess title", 1)
    else:
      shutil.copy(r"E:\SVN\MySvnModified\51TestBuild.bat",  OutputFolder + r"\TestBuild.bat")
      EndTime = datetime.datetime.now ()
      print ("Start Time is " + str (StartTime) + ".\nEnd Time is " + str (EndTime) + ".\nDuration is " + str (EndTime - StartTime))
      OrgPaht = os.getcwd ()
      os.chdir (OutputFolder)
      os.system ("TestBuild.bat")
      os.chdir (OrgPaht)
      EndTime = datetime.datetime.now ()
      print ("Start Time is " + str (StartTime) + ".\nEnd Time is " + str (EndTime) + ".\nDuration is " + str (EndTime - StartTime))