" Vim syntax file
" Maintainer:   Romain Soufflet <romain@soufflet.io>
" URL:          romain.soufflet.io
" Last Change:  2014 November 12
" Version:      0.1

if version < 700
  syntax clear
endif


syn region folderListItem start=/^.+\:/ end=/$/
hi folderListItem bg=green
