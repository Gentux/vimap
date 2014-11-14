" Vim syntax file
" Maintainer:   Romain Soufflet <romain@soufflet.io>
" URL:          romain.soufflet.io
" Last Change:  2014 November 12
" Version:      0.1

if version < 700
  syntax clear
endif


syn region folderList_DirectoryName start=/^▸/ end=/  /
syn region folderList_TotalCount start=/- / end=/ /
syn region folderList_UnreadCount start=/(/ end=/)$/

hi folderList_DirectoryName gui=bold
hi folderList_UnreadCount guifg=green
