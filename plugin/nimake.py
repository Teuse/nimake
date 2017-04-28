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

    import subprocess
    print("### %s" % cmakeCmd)
    print("### %s" % buildPath)
    retCode = subprocess.check_call(cmakeCmd, cwd=buildPath, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if retCode:
        print("Error code: %i" % retCode)

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
    return os.path.isfile(cmakeFile)

#--------------------------------------------------------------------------
def __configureNoUnity(cmakePath, noUnityFlag, buildType=''):
    __copyYcmExtraConf(cmakePath)

    args = " -DCMAKE_EXPORT_COMPILE_COMMANDS=\"1\" -DCMAKE_OSX_ARCHITECTURES=\"x86_64\" -D" + noUnityFlag + "=\"OFF\""
    if buildType:
        args = args + " -DCMAKE_BUILD_TYPE=\"" + buildType + "\""

    buildPath = __buildPath(cmakePath, 'build_no_unity')
    print("NIMAKE: runCmake(%s, %s, ...)" % (cmakePath, buildPath))
    __runCmake("../maschine", buildPath, args)

#--------------------------------------------------------------------------
def __configureNinja(cmakePath, buildType=''):
    args = " -DCMAKE_EXPORT_COMPILE_COMMANDS=\"1\" -DCMAKE_OSX_ARCHITECTURES=\"x86_64\" -DMASCHINE_TESTS=\"True\""
    if buildType:
        args = args + " -DCMAKE_BUILD_TYPE=\"" + buildType + "\""

    buildPath = __buildPath(cmakePath, 'build_ninja_'+buildType)
    print("NIMAKE: runCmake(%s, %s, ...)" % (cmakePath, buildPath))
    __runCmake("../maschine", buildPath, args)


#--------------------------------------------------------------------------
#--- main functions
#--------------------------------------------------------------------------
def ycmMaschine(cmakePath):
    if __isCmakeFile(cmakePath):
        __configureNoUnity(cmakePath, 'MASCHINE_UNITY_BUILDS')

#--------------------------------------------------------------------------
def ninjaDebug(cmakePath):
    if __isCmakeFile(cmakePath):
        __configureNinja(cmakePath, 'Debug')

#--------------------------------------------------------------------------
def ninjaRelWithDebug(cmakePath):
    if __isCmakeFile(cmakePath):
        __configureNinja(cmakePath)

#--------------------------------------------------------------------------
def ninjaRelease(cmakePath):
    if __isCmakeFile(cmakePath):
        __configureNinja(cmakePath, 'Release')


