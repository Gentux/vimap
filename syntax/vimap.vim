" Vim syntax file
" Maintainer:   Romain Soufflet <romain@soufflet.io>
" URL:          romain.soufflet.io
" Last Change:  2014 November 12
" Version:      0.1

if version < 700
  syntax clear
endif


" Syntax for Status page
syn region folderList_line start=/^▸/ end=/)$/
syn region folderList_DirectoryName containedin=folderList_line start=/^▸/ end=/  /
syn region folderList_TotalCount containedin=folderList_line start=/- / end=/ /
syn region folderList_UnreadCount containedin=folderList_line start=/(/ end=/)$/

hi folderList_DirectoryName gui=bold
hi folderList_UnreadCount guifg=green

" Syntax for List page
syn region list_UID containedin=listLine start=/^\s\+\d\+/ end=/ /
syn region list_FROM containedin=listLine start=/▾ / end=/\s\+:/
syn region listLine start=/^\s\+\d\+/ end=/$/

hi list_UID gui=bold guifg=red
hi list_FROM guifg=orange
