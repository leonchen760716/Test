import sys
import os
import colorama
from colorama import Fore, Back, Style
import datetime

SupportedExtension = ('.h', '.c', '.vfr', '.inf', '', '.env', '.dsc', '.dec', '.fdf', '.uni', '.efi', '.dxs', '.idf', '.ani' , '.png', '.gif', '.vfcf', '.g', '.cpp', '.asm', '.s', '.nasm', '.jwasm', '.lib', '.exe', '.bin', '.auth', '.hash', '.txt', '.var', '.asl', '.aml', '.act', '.md', '.pdf', '.inc', '.tga', '.ini', '.py', '.bdf', '.fif')
SkipFilesList = ('CTAGS.EXE')
CURRENT_YEAR = str (datetime.date.today ().year)

def IsSupportedExtention(FilePath):
    Ext = os.path.splitext(FilePath)[1].lower()
    return Ext in SupportedExtension
#    if Ext in SupportedExtension:
#        return True
#    return False

def IsSupportedFileName (FilePath):
    BaseName = os.path.basename (FilePath)
    return not BaseName in SkipFilesList
#    if BaseName in SkipFilesList:
#        return False
#    return True

def IsSupportedFiles (FilePath):
    return IsSupportedFileName (FilePath) and IsSupportedExtention (FilePath)

def IsSkipPath(Path):
    '''function to determine what path should skip to check'''
    if not '\\' in Path:
        return False;
    Sep = Path.partition ('\\')
    SkipPath = Sep [2]
    if SkipPath == 'Build' or SkipPath == 'Conf' or SkipPath == 'InsydeModulePkg\\H2ODebug':
        print ("The skip path is " + Path)
        print ("The file name is " + Sep [0])
        return True


def CreateFile (SrcFilePath, DestFilePath):
    if not IsSupportedFiles (SrcFilePath):
        return
    with open (SrcFilePath, 'rb') as SrcFile:
        SrcBuf = SrcFile.readlines()
    Result = os.path.split (DestFilePath)
    if not os.path.exists (Result[0]):
        os.makedirs (Result[0])
    with open (DestFilePath, 'wb') as DestFile:
        DestFile.writelines (SrcBuf)


def CreateFiles (SrcFilePath, DestFilePath):
    SrcList = os.listdir (SrcFilePath)
    for SrcElem in SrcList:
        if os.path.isdir (SrcFilePath + '\\' + SrcElem):
            if not IsSkipPath (SrcFilePath + '\\' + SrcElem):
                CreateFiles (SrcFilePath + '\\' + SrcElem, DestFilePath + '\\' + SrcElem)
        else:
            CreateFile (SrcFilePath + '\\' + SrcElem, DestFilePath + '\\' + SrcElem)

def CreateDifferentFile (OrgFilePath, NewFilePath, DestOrgFilePath, DestNewFilePath):
    if not IsSupportedFiles (OrgFilePath):
        return
    if os.path.getmtime (OrgFilePath) == os.path.getmtime (NewFilePath):
        return
    try:
        with open (OrgFilePath, 'rb') as OrgFile:
            OrgBuf = OrgFile.readlines()
        with open (NewFilePath, 'rb') as NewFile:
            NewBuf = NewFile.readlines()
        if str (OrgBuf) != str (NewBuf):
            Result = os.path.split (DestOrgFilePath)
            if not os.path.exists (Result[0]):
                os.makedirs (Result[0])
            with open (DestOrgFilePath, 'wb') as DestOrgFile:
                DestOrgFile.writelines (OrgBuf)
            Result = os.path.split (DestNewFilePath)
            if not os.path.exists (Result[0]):
                os.makedirs (Result[0])
            with open (DestNewFilePath, 'wb') as DestNewFile:
                DestNewFile.writelines (NewBuf)
    except UnicodeDecodeError as err:
        print ("Input file " + OrgFilePath + " cause UnicodeDecodeError" + str (err))
    except PermissionError as Per:
        print (str (Per))

def CreateDifferentFiles (OrgFolder, NewFolder, DestOrgFolder, DestNewFolder):
    OrgList = os.listdir (OrgFolder)
    NewList = os.listdir (NewFolder)
    #
    #create different files and origninal file exists but new file doesn't exist"""
    #
    for OrgElem in OrgList:
        if OrgElem in NewList:
            if os.path.isdir (OrgFolder + '\\' + OrgElem):
                if not IsSkipPath (OrgFolder + '\\' + OrgElem):
                    CreateDifferentFiles (OrgFolder + '\\' + OrgElem, NewFolder + '\\' + OrgElem, \
                                          DestOrgFolder + '\\' + OrgElem, DestNewFolder + '\\' + OrgElem)
            else:
                CreateDifferentFile (OrgFolder + '\\' + OrgElem, NewFolder + '\\' + OrgElem, \
                                     DestOrgFolder + '\\' + OrgElem, DestNewFolder + '\\' + OrgElem)
        else:
            if os.path.isdir (OrgFolder + '\\' + OrgElem):
                if not IsSkipPath (OrgFolder + '\\' + OrgElem):
                    CreateFiles (OrgFolder + '\\' + OrgElem, DestOrgFolder + '\\' + OrgElem)
            else:
               CreateFile (OrgFolder + '\\' + OrgElem, DestOrgFolder + '\\' + OrgElem)
    #
    #create new file exists but original file doesn't exist"""
    #
    for NewElem in NewList:
        if not NewElem in OrgList:
            if os.path.isdir (NewFolder + '\\' + NewElem):
                if not IsSkipPath (NewFolder + '\\' + NewElem):
                    CreateFiles (NewFolder + '\\' + NewElem, DestNewFolder + '\\' + NewElem)
            else:
                CreateFile (NewFolder + '\\' + NewElem, DestNewFolder + '\\' + NewElem)


def UpdateFileIbHeader (File):
     NeedUpdate = False
     CorrectIbHeader = False
     MyEncode = 'utf-16' if File.lower ().endswith (".uni") else None
     try:
       with open (File, 'r', encoding = MyEncode) as MyFile:
           Lines = MyFile.readlines ()
           Index = 0
           for Line in Lines:
              if Line.find ("Copyright (c)") != -1 and Line.find ("Insyde Software Corp") != -1:
                  CorrectIbHeader = True
                  #
                  # Get number of space after - to determine the location of year.
                  #
                  if (Line.find ('-') != -1 and Line.find (CURRENT_YEAR) == -1):
                      NeedUpdate = True
                      NumSpaceAfterDash = 0
                      for Char in Line[Line.find ("-")]:
                          if Char.isdigit ():
                              break
                          NumSpaceAfterDash += 1
                      if Line [Line.find ("-") + 1] == ' ':
                        Line = Line[:Line.find ("-") + NumSpaceAfterDash + 1] + CURRENT_YEAR + Line[Line.find ("-") + NumSpaceAfterDash + 5:]
                      else:
                        Line = Line[:Line.find ("-") + NumSpaceAfterDash] + CURRENT_YEAR + Line[Line.find ("-") + NumSpaceAfterDash + 4:]
                      Lines[Index] = Line
                  elif Line.find (CURRENT_YEAR) == -1:
                      #
                      # Find ',' in "Copyright (c) ####,....", so we can insert ' - CURRENT_YEAR' in this string.
                      #
                      NeedUpdate = True
                      Line = Line[:Line.find (",")] + " - " + CURRENT_YEAR + Line[Line.find (","):]
                      Lines[Index] = Line
                  break
              Index += 1
     except UnicodeDecodeError as err:
       #
       # We have support normal encoding and utf-16 encode.
       # If system triggers any other unicode decode exception, print error message here.
       #
       print (err)
     if NeedUpdate == True:
         print (Fore.BLUE + Style.BRIGHT + "Update", File, "IB header!!!")
         with open (File, 'w', encoding = MyEncode) as MyFile:
             MyFile.writelines (Lines)

     if CorrectIbHeader == False:
         print (Fore.RED + Style.BRIGHT + File, "doesn't have correct IB header!!!")

def UpdateFilesIbHeader (Folder):
    List = os.listdir (Folder)
    for Element in List:
        if os.path.isdir (Folder + '\\' + Element):
            UpdateFilesIbHeader (Folder + '\\' + Element)
        else:
            UpdateFileIbHeader (Folder + '\\' + Element)



if __name__ == '__main__':
    if len(sys.argv) != 4:
        print ('Get small version Utility')
        print ('Usage: GetSmallVersion OriginalFolder NewFolder DestinationFolder')
        print ('sys.argv is ' + str (len (sys.argv)) + ' !!')
        sys.exit(-1)
    OrgFolder = sys.argv[1]
    NewFolder = sys.argv[2]
    DestinationFolder = sys.argv[3]
    if not os.path.exists (OrgFolder) or not os.path.isdir (OrgFolder):
        print ("The " + str (OriginalFolder) + " folder doesn't exist")
        sys.exit (-1)
    if not os.path.exists (NewFolder) or not os.path.isdir (NewFolder):
        print ("The " + str (NewFolder) + " folder doesn't exist")
        sys.exit (-1)
    if not os.path.exists (DestinationFolder):
        os.makedirs (DestinationFolder)
    if not os.path.exists (DestinationFolder + '\\Org'):
        os.mkdir (DestinationFolder + '\\Org')
    if not os.path.exists (DestinationFolder + '\\Mod'):
        os.mkdir (DestinationFolder + '\\Mod')
    CreateDifferentFiles (OrgFolder, NewFolder, DestinationFolder + '\\Org', DestinationFolder + '\\Mod')
    #
    # Note: Usage for colorma package
    # 1.Before using coloram, must call colorama.init ()
    # 2.colorma isn't a standard python pacakge, need install this package by yourself
    #
    colorama.init ()
    UpdateFilesIbHeader (DestinationFolder + '\\Mod')




