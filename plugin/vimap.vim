let s:IMAP_vim = '0.1'

" SECTION: Script init
"=====================

if exists("g:loaded_imap_vim")
    finish
endif
if !has('python')
    echoerr "IMAP-VIM: this plugin requires python support"
    finish
endif
if v:version < 700
    echoerr "IMAP-VIM: this plugin requires vim >= 7. DOWNLOAD IT! You'll thank me later!"
    finish
endif
let g:loaded_imap_vim = 1


" SECTION: Load python functions
"===============================

python << EOF
import vim
import sys
vimap_path = vim.eval("expand('<sfile>:h')")
sys.path.append(vimap_path)
import vimap
EOF

python vimap.status()
