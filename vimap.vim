let s:IMAP_vim = '0.1'

" SECTION: Script init stuff {{{1
"============================================================
if exists("loaded_imap_vim")
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
"let loaded_imap_vim = 1


python << EOF
import vim
import sys
vimap_path = vim.eval("expand('<sfile>:h')")
sys.path.append(vimap_path)
import vimap
EOF

noremap  <Plug>(Vimap-status)           :python vimap.status()<CR>
noremap  <Plug>(Vimap-list)             :python vimap.list('INBOX')<CR>
noremap  <Plug>(Vimap-search)           :python vimap.search()<CR>
noremap  <Plug>(Vimap-changeMailbox)    :python change_mailbox()<CR>


map <F5> :python vimap.status()<CR>
