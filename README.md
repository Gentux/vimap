V*imap*
=======


## Description ##

A VIM plugins to read your mail with an IMAP account.

* Get imap account status (New mails, mail counting… etc…)
* Get list of mails in INBOX (or any other directory)
* Search through mail
* Read mail
* Flag mail (Read, Unread, Delete, etc…) (NotImplementedYet)
* Copy, Move and Delete mail (NotImplementedYet)

All these action are done remotely via IMAP protocole, so you don't have to
worry with synchronization.


## Quickstart ##

This plugins rely on another library called *imap-cli*, you can install it with:

```
pip install imap-cli
```

Then, configure *imap-cli* creating a configuration file in `~/.config/imap-cli` containing :

    hostname = imap.example.org
    username = username
    password = secret
    ssl = True

Finaly, copy *vimap.vim* and *vimap.py* in your *VIM* plugin directory.


## Usage ##


## Contributing ##

All contributions are welcome.

You can [open new issues](https://github.com/Gentux/imap-cli/issues/new) for questions, bugs or new feature.


## Roadmap ##

The actual version of *Vimap* is *None*. (this version is actually a proof of concept)


### v0.1 ### (Work in progress)

* Status (list directory and new mail per directory)
* List (list content of a directory
* Read (display content of specified email)
* Mapping to get this working

### v0.2 ###

* Map search functionnalities
* Improve interface and mapping if needed

### v0.3 ###

* Flag
* Copy and Move
* Full Documentation (in vim)


## Creator ##

### Romain Soufflet ###

* [Twitter](http://twitter.com/Romain_Soufflet)
* [Github](http://github.com/Gentux)
* [http://romain.soufflet.io](http://romain.soufflet.io)


## Legal notices ##

Released under the [MIT License](http://www.opensource.org/licenses/mit-license.php).
