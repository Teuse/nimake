if !has('python') || exists("g:vimake_plugin_loaded")
	finish
endif

let g:vimake_plugin_loaded = 1 
let s:vimake_plugin_path   = escape(expand('<sfile>:p:h'), '\')


"--------------------------------------------------------------------------
"--- Mapping 
"--------------------------------------------------------------------------

silent exec "command! -nargs=1 VimakeCopyYcm call <SID>CopyYcm('<args>')"
silent exec "command! -nargs=1 VimakeMasYcm  call <SID>MasYcm('<args>')"
silent exec "command! -nargs=1 Vimake        call <SID>Make('<args>', 'debug')"

" nnoremap <silent> <leader>h :VImake<cr>


"--------------------------------------------------------------------------
"--- Global
"--------------------------------------------------------------------------

" defines path to the location, where the build-folders should be. Path is 
" relative to the root directory (root CMakeLists.txt)
if !exists('g:vimake_relative_path_to_build_folder')
    let g:vimake_relative_path_to_build_folder = ".."
endif


"--------------------------------------------------------------------------
"--- Functions 
"--------------------------------------------------------------------------

function! s:CopyYcm(rootPath)
    let cmakeRoot = fnamemodify(a:rootPath, ":p")
python << EOF
import vim, sys
path = vim.eval('s:vimake_plugin_path')
sys.path.append(path)

import vimake
rootPath = vim.eval('cmakeRoot')
vimake.copyYcmConfig(rootPath)
EOF
endfunction

"--------------------------------------------------------------------------
function! s:MasYcm(rootPath)
    let cmakeRoot = fnamemodify(a:rootPath, ":p")
python << EOF
import vim, sys
path = vim.eval('s:vimake_plugin_path')
sys.path.append(path)

import vimake
rootPath = vim.eval('cmakeRoot')
vimake.makeMasYcm(rootPath)
EOF
endfunction

"--------------------------------------------------------------------------
function! s:Make(rootPath, buildType)
    let cmakeRoot = fnamemodify(a:rootPath, ":p")
python << EOF
import vim, sys
path = vim.eval('s:vimake_plugin_path')
sys.path.append(path)

import vimake
rootPath  = vim.eval('cmakeRoot')
buildType = vim.eval('a:buildType')
isDebug = buildType.lower() != 'release'
vimake.makeNinja(rootPath, isDebug)
EOF
endfunction
 
 
