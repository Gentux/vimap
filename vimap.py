# -*- coding: utf-8 -*-


import vim

import imap_cli
from imap_cli import config
from imap_cli import fetch
from imap_cli import search


connect_conf = config.new_context_from_file(section='imap')
display_conf = {
    'format_list': u'{uid:>6} : {subject:<80} | FROM: {from}',
    'format_status': u' '.join([
        u'{directory:<20} :',
        u'{count:>5} Mails -',
        u'{unseen:>5} Unseen -',
        u'{recent:>5} Recent']),
    'format_thread': u'{uid:>6} : {subject:<80} | FROM: {from}',
    'limit': 10}
trash_conf = config.new_context_from_file(section='trash')

current_dir = 'INBOX'
imap_account = None


def ensure_connection():
    global imap_account
    try:
        imap_account.noop()
    except Exception as e:
        print e
        imap_account = imap_cli.connect(**connect_conf)


def status():
    reset_buffer('vimap-status')
    b = vim.current.buffer
    b[:] = None

    ensure_connection()
    for directory_status in sorted(imap_cli.status(imap_account),
                                   key=lambda obj: obj['directory']):
        b.append(display_conf['format_status'].format(**directory_status))


def list():
    '''List mail in specified folder.'''
    reset_buffer('vimap-list')
    b = vim.current.buffer
    b[:] = None

    ensure_connection()
    for mail_info in search.fetch_mails_info(current_dir,
                                             limit=display_conf['limit']):
        b.append(u'UID : {:<10} From : {:<40} Subject : {}'.format(
            mail_info['uid'],
            truncate_string(mail_info['from'], 33),
            truncate_string(mail_info['subject'], 50),
        ))


def change_mailbox(mailbox_name):
    '''Change selected IMAP folder.'''
    global current_dir
    ensure_connection()
    cd_result = imap_cli.change_dir(imap_account, directory=mailbox_name)
    if cd_result == -1:
        print 'VIMAP: IMAP Folder {} can\'t be found'.format(mailbox_name)
    current_dir = mailbox_name


def read(uid):
    '''Read mail by uid.'''
    ensure_connection()
    fetched_mail = fetch.read(imap_account, uid)
    if fetched_mail is None:
        print "VIMAP: Mail was not fetched, an error occured"

    reset_buffer('vimap-read')
    b = vim.current.buffer
    b[:] = None
    b.append(fetch.display(fetched_mail))


def imap_search(adress):
    ensure_connection()
    search_criterion = search.create_search_criterion(address=adress)
    mail_set = search.fetch_uids(
        imap_account, search_criterion=search_criterion)
    if len(mail_set) == 0:
        print 'VIMAP: No mail found'
        return 0

    reset_buffer('vimap-list')
    b = vim.current.buffer
    b[:] = None
    for mail_info in search.fetch_mails_info(imap_account, mail_set=mail_set):
        b.append(u'UID : {:<10} From : {:<40} Subject : {}'.format(
            mail_info['uid'],
            truncate_string(mail_info['from'], 33),
            truncate_string(mail_info['subject'], 50),
        ))


def truncate_string(string, length):
    minus_than_position = string.find('<')
    if minus_than_position > 0 and string.find('>') > minus_than_position:
        string = string[0:minus_than_position]
    return string if len(string) < length else u'{0}…'.format(string[0:length])


def reset_buffer(buffer_name):
    # close preview window, it was something other than 'vim-ipython'
    vim.command("pcl")
    vim.command("silent pedit +set\ ma {}".format(buffer_name))
    vim.command("wincmd P")  # switch to preview window
    # subchannel window quick quit key 'q'
    vim.command('nnoremap <buffer> q :q<CR>')
    vim.command('nnoremap <buffer> <CR> :python<space>vimap.read(1033)')
    vim.command("set bufhidden=hide buftype=nofile ft=python")
    vim.command("setlocal nobuflisted")  # don't come up in buffer lists
    vim.command("setlocal nonumber")  # no line numbers, we have in/out nums
    # no swap file (so no complaints cross-instance)
    vim.command("setlocal noswapfile")
