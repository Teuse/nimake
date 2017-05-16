import vim
import os
import sys

#--------------------------------------------------------------------------
#--- Helper functions
#--------------------------------------------------------------------------
def __createDir(path):
    if not os.path.exists(path):
        os.makedirs(path)

#--------------------------------------------------------------------------
def __buildPath(cmakePath, folderName):
    relBuildPath = vim.eval('g:nimake_relative_path_to_build_folder')
    buildPath = os.path.join(cmakePath, relBuildPath)
    return os.path.join(buildPath, folderName)

#--------------------------------------------------------------------------
def __runCmake(cmakePath, buildPath, args):
    __createDir(buildPath)
    cmakeCmd = "cmake -G\"Ninja\" " + cmakePath + " " + args
    buildPath = os.path.abspath(buildPath)

    import subprocess
    print("NIMAKE: %s" % cmakeCmd)
    retCode = subprocess.check_call(cmakeCmd, cwd=buildPath, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if retCode:
        print("NIMKKE: cmake failed! Error code: %i" % retCode)
    else:
        print("NIMAKE: successful")

#--------------------------------------------------------------------------
def __copyYcmExtraConf(cmakePath):
    nimakeRoot = vim.eval('s:nimake_plugin_path')
    ycmSrc     = os.path.join(nimakeRoot, 'ycm_extra_conf.py')
    ycmDest    = os.path.join(cmakePath, '.ycm_extra_conf.py')

    if not os.path.isfile(ycmDest):
        from shutil import copyfile
        copyfile(ycmSrc, ycmDest)

#--------------------------------------------------------------------------
def __isCmakeFile(cmakePath):
    cmakeFile = os.path.join(cmakePath, 'CMakeLists.txt')
    if not os.path.isfile(cmakeFile):
        print("NIMAKE: Could't find CMakeLists.txt file at path: %s" % cmakePath)
        return False

    parentCmakePath = os.path.dirname(cmakePath)
    parentCmakeFile = os.path.join(parentCmakePath, 'CMakeLists.txt')
    if os.path.isfile(parentCmakeFile):
        print("NIMAKE: There is a CMakeLists.txt file in the parent directory... your relativ path is wrong! ParentPath= %s" % parentCmakeFile)
        return False

    return True

#--------------------------------------------------------------------------
def __configureNoUnity(cmakePath, noUnityFlag, buildType=''):
    args = " -DCMAKE_EXPORT_COMPILE_COMMANDS=\"1\" -DCMAKE_OSX_ARCHITECTURES=\"x86_64\" -D" + noUnityFlag + "=\"OFF\""
    if buildType:
        args = args + " -DCMAKE_BUILD_TYPE=\"" + buildType + "\""

    buildPath = __buildPath(cmakePath, 'build_no_unity')
    __runCmake("../maschine", buildPath, args)
    __copyYcmExtraConf(cmakePath)

#--------------------------------------------------------------------------
def __configureNinja(cmakePath, buildType=''):
    args = " -DCMAKE_EXPORT_COMPILE_COMMANDS=\"1\" -DCMAKE_OSX_ARCHITECTURES=\"x86_64\" -DMASCHINE_TESTS=\"True\""
    if buildType:
        args = args + " -DCMAKE_BUILD_TYPE=\"" + buildType + "\""

    buildPath = __buildPath(cmakePath, 'build_ninja_'+buildType)
    __runCmake("../maschine", buildPath, args)


#--------------------------------------------------------------------------
#--- main functions
#--------------------------------------------------------------------------
def ycmMaschine(cmakePath):
    cmakePath = os.path.abspath(cmakePath)
    if __isCmakeFile(cmakePath):
        __configureNoUnity(cmakePath, 'MASCHINE_UNITY_BUILDS')

#--------------------------------------------------------------------------
def ninjaDebug(cmakePath):
    cmakePath = os.path.abspath(cmakePath)
    if __isCmakeFile(cmakePath):
        __configureNinja(cmakePath, 'Debug')

#--------------------------------------------------------------------------
def ninjaRelWithDebug(cmakePath):
    cmakePath = os.path.abspath(cmakePath)
    if __isCmakeFile(cmakePath):
        __configureNinja(cmakePath)

#--------------------------------------------------------------------------
def ninjaRelease(cmakePath):
    cmakePath = os.path.abspath(cmakePath)
    if __isCmakeFile(cmakePath):
        __configureNinja(cmakePath, 'Release')


