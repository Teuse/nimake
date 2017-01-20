if !has('python') || exists("g:nimake_plugin_loaded")
	finish
endif

let g:nimake_plugin_loaded = 1 
let s:nimake_plugin_path   = escape(expand('<sfile>:p:h'), '\')


"--------------------------------------------------------------------------
"--- Mapping 
"--------------------------------------------------------------------------

silent exec "command! -nargs=+ Masycm call <SID>MakeMaschineYcm('<args>')"
silent exec "command! -nargs=+ Mas  call <SID>MakeMaschine('<args>')"

" nnoremap <silent> <leader>h :NImake<cr>


"--------------------------------------------------------------------------
"--- Global
"--------------------------------------------------------------------------

" defines path to the location, where the build-folders should be. Path is 
" relative to the root directory (root CMakeLists.txt)
if !exists('g:nimake_relative_path_to_build_folder')
    let g:nimake_relative_path_to_build_folder = ".."
endif


"--------------------------------------------------------------------------
"--- Functions 
"--------------------------------------------------------------------------

" Create/Update ninja build folder (64bit only)
function! s:MakeMaschine(rootPath)
    let cmakeRoot = fnamemodify(l:rootPath, ":p")
python << EOF

import vim, sys
path = vim.eval('s:nimake_plugin_path')
sys.path.append(path)

import nimake
rootPath = vim.eval('cmakeRoot')
nimake.ninjaDebug(rootPath)

EOF
endfunction
 

function! s:MakeMaschineYcm(rootPath)
    let cmakeRoot = fnamemodify(l:rootPath, ":p")
python << EOF

import vim, sys
path = vim.eval('s:nimake_plugin_path')
sys.path.append(path)

import nimake
rootPath = vim.eval('cmakeRoot')
nimake.ycmMaschine(rootPath)

EOF
endfunction
 
