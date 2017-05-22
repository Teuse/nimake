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
    relBuildPath = vim.eval('g:vimake_relative_path_to_build_folder')
    buildPath = os.path.join(cmakePath, relBuildPath)
    return os.path.join(buildPath, folderName)

#--------------------------------------------------------------------------
def __runCmake(cmakePath, buildPath, args):
    __createDir(buildPath)
    cmakeCmd = "cmake -G\"Ninja\" " + cmakePath + " " + args
    buildPath = os.path.abspath(buildPath)

    import subprocess
    print("VIMAKE: %s" % cmakeCmd)
    retCode = subprocess.check_call(cmakeCmd, cwd=buildPath, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if retCode:
        print("NIMKKE: cmake failed! Error code: %i" % retCode)
    else:
        print("VIMAKE: successful")

#--------------------------------------------------------------------------
def __copyYcmExtraConf(cmakePath):
    vimakeRoot = vim.eval('s:vimake_plugin_path')
    ycmSrc     = os.path.join(vimakeRoot, 'ycm_extra_conf.py')
    ycmDest    = os.path.join(cmakePath, '.ycm_extra_conf.py')

    if not os.path.isfile(ycmDest):
        from shutil import copyfile
        copyfile(ycmSrc, ycmDest)
        print("VIMAKE: .ycm_extra_conf.py copyed to path: %s" % ycmDest)

#--------------------------------------------------------------------------
def __isCmakeFile(cmakePath):
    cmakeFile = os.path.join(cmakePath, 'CMakeLists.txt')
    if not os.path.isfile(cmakeFile):
        print("VIMAKE: Could't find CMakeLists.txt file at path: %s" % cmakePath)
        return False

    parentCmakePath = os.path.dirname(cmakePath)
    parentCmakeFile = os.path.join(parentCmakePath, 'CMakeLists.txt')
    if os.path.isfile(parentCmakeFile):
        print("VIMAKE: There is a CMakeLists.txt file in the parent directory... your relativ path is wrong! ParentPath= %s" % parentCmakeFile)
        return False

    return True

#--------------------------------------------------------------------------
def __configureNinja(cmakePath, folderName, extraArgs=''):
    args = " -DCMAKE_EXPORT_COMPILE_COMMANDS=\"1\" -DCMAKE_OSX_ARCHITECTURES=\"x86_64\" "
    args = args + extraArgs

    buildPath = __buildPath(cmakePath, folderName)
    __runCmake("../maschine", buildPath, args)


#--------------------------------------------------------------------------
#--- main functions
#--------------------------------------------------------------------------
def copyYcmConfig(cmakePath):
    cmakePath = os.path.abspath(cmakePath)
    if __isCmakeFile(cmakePath):
        __copyYcmExtraConf(cmakePath)

#--------------------------------------------------------------------------
def makeMasYcm(cmakePath):
    cmakePath = os.path.abspath(cmakePath)
    if __isCmakeFile(cmakePath):
        __configureNinja(cmakePath, 'build_no_unity', '-DMASCHINE_UNITY_BUILDS=OFF')
        __copyYcmExtraConf(cmakePath)

#--------------------------------------------------------------------------
def makeNinja(cmakePath, isDebug=True):
    cmakePath = os.path.abspath(cmakePath)
    if __isCmakeFile(cmakePath):
        if isDebug:
            __configureNinja(cmakePath, 'build_ninja_debug', '-DCMAKE_BUILD_TYPE=Debug')
        else:
            __configureNinja(cmakePath, 'build_ninja_release', '-DCMAKE_BUILD_TYPE=Release')

