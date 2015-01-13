# -*- coding: utf-8 -*-


"""VIMAP python functions"""


import vim

import six

import imap_cli
from imap_cli import config
from imap_cli import fetch
from imap_cli import search


connect_conf = config.new_context_from_file(section='imap')
current_dir = 'INBOX'
current_mail = None
display_conf = {
    'format_list': u'{uid:>5} ▾ {from:<36.35} : {subject}',
    'format_status': u'▸ {directory}  - {count} ({unseen})',
    'format_thread': u'{uid:>5} ▾ {from:<36.35} : {subject}',
    'limit': 20}
imap_account = None
trash_conf = config.new_context_from_file(section='trash')
uids = []

status_mappings = [
    ('o', ':python vimap.list_dir(vim.current.line.split()[1])<cr>'),
    ('q', ':q<CR>'),
]

list_mappings = [
    ('o', ':python vimap.read(vim.current.line.split()[0])<cr>'),
    ('/', ':python vimap.imap_search("")<left><left>'),
    ('q', ':python vimap.status()<cr>'),
]

read_mappings = [
    ('h', ':python vimap.headers()<cr>'),
    ('q', ':python vimap.list_dir()<cr>'),
]


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

    b[0] = u'Mailbox list:'

    for key, action in status_mappings:
        vim.command("nnoremap <silent> <buffer> {} {}".format(key, action))


def list_dir(directory=None):
    '''List mail in specified folder.'''
    reset_buffer('vimap-list')
    b = vim.current.buffer
    b[:] = None

    if directory is not None and current_dir != directory:
        ret = change_mailbox(directory)
        if ret is None:
            return None

    ensure_connection()
    threads = search.fetch_threads(imap_account, limit=display_conf['limit'])
    mail_tree = search.threads_to_mail_tree(threads)
    for output in search.display_mail_tree(
            imap_account, mail_tree,
            format_thread=display_conf['format_thread']):
        for line in output.split('\n'):
            b.append(line)

    b[0] = u'Mails from {}:'.format(current_dir)

    for key, action in list_mappings:
        vim.command("nnoremap <silent> <buffer> {} {}".format(key, action))
    vim.command("normal G")


def change_mailbox(mailbox_name):
    '''Change selected IMAP folder.'''
    global current_dir
    ensure_connection()
    cd_result = imap_cli.change_dir(imap_account, directory=mailbox_name)
    if cd_result == -1:
        print 'VIMAP: IMAP Folder {} can\'t be found'.format(mailbox_name)
        return None
    current_dir = mailbox_name
    return mailbox_name


def read(uid):
    '''Read mail by uid.'''
    ensure_connection()
    if isinstance(uid, six.string_types):
        uid = int(uid)
    fetched_mails = list(fetch.read(imap_account, uid))
    if fetched_mails is None:
        print "VIMAP: Mail was not fetched, an error occured"
        list_dir()

    global current_mail
    reset_buffer('vimap-read')
    b = vim.current.buffer
    b[:] = None
    for fetched_mail in fetched_mails:
        current_mail = fetched_mail
        for line in fetch.display(current_mail).split('\n'):
            b.append(line.replace('\r', ''))

    vim.command("set ft=mail")
    for key, action in read_mappings:
        vim.command("nnoremap <silent> <buffer> {} {}".format(key, action))
    vim.command("normal dd")


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
        b.append(display_conf['format_list'].format(
            **mail_info).replace('\n', ' '))

    b[0] = u'Mails from «{}»:'.format(adress)

    for key, action in list_mappings:
        vim.command("nnoremap <silent> <buffer> {} {}".format(key, action))


def headers():
    reset_buffer('vimap-read')
    b = vim.current.buffer
    b[:] = None

    for header_name, header_value in current_mail['headers'].items():
        lines = '{}: {}'.format(header_name, header_value).split('\n')
        for line in lines:
            b.append(line)

    b[0] = u'Mail headers:'
    vim.command("set ft=mail")
    for key, action in read_mappings:
        vim.command("nnoremap <silent> <buffer> {} {}".format(key, action))
    vim.command("normal dd")


def reset_buffer(buffer_name):
    # close preview window
    vim.command("pcl")
    vim.command("silent pedit +set\ ma {}".format(buffer_name))
    vim.command("wincmd P")  # switch to preview window
    vim.command("set bufhidden=hide buftype=nofile ft=vimap")
    vim.command("setlocal nobuflisted")  # don't come up in buffer lists
    vim.command("setlocal nonumber")  # no line numbers, we have in/out nums
    # no swap file (so no complaints cross-instance)
    vim.command("setlocal noswapfile")
