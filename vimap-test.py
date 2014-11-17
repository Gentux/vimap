import imap_cli
from imap_cli import config
from imap_cli import search


connect_conf = config.new_context_from_file(section='imap')
display_conf = config.new_context_from_file(section='display')
imap_account = imap_cli.connect(**connect_conf)


display_conf['format_list'] = u'{uid:>5} : {from:<40} : {subject}'
for truc in search.fetch_mails_info(imap_account, limit=10):
    truc['from'] = truncate_string(truc['from'], 40)
    print display_conf['format_list'].format(**truc)
