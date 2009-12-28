INSTALL = install
INSTALL_PROGRAM = $(INSTALL)
INSTALL_DATA = $(INSTALL) -m 644
INSTALL_DIR = $(INSTALL) -d
UNINSTALL_PROGRAM = rm
UNINSTALL_DATA = rm
UNINSTALL_DIR = rmdir -p --ignore-fail-on-non-empty
COMPILE_DATA = py_compilefiles

src_binary_d = bin
src_conf_d   = conf
src_doc_d    = doc
src_share_d  = share
src_mod_d    = python

binary_f = kjabnotify_listener
conf_f   = kjabnotifyrc
doc_f    = *
share_f  = dotfile.skel
mod_f    = *.py*

dest_binary_d = /usr/bin
dest_conf_d   = /etc/kde3
dest_doc_d    = /usr/share/doc/kjabnotify
dest_share_d  = /usr/share/kjabnotify
dest_mod_d    = /usr/share/kjabnotify/python

install:
	$(INSTALL_DIR) $(dest_binary_d) $(dest_conf_d)  $(dest_doc_d)    \
	               $(dest_share_d) $(dest_mod_d)
	$(INSTALL_PROGRAM) $(src_binary_d)/$(binary_f) 	$(dest_binary_d)
	$(INSTALL_DATA) $(src_conf_d)/$(conf_f)		$(dest_conf_d)
	$(INSTALL_DATA) $(src_doc_d)/$(doc_f)		$(dest_doc_d)
	$(INSTALL_DATA) $(src_share_d)/$(share_f)	$(dest_share_d)
	$(INSTALL_DATA) $(src_mod_d)/$(mod_f)		$(dest_mod_d)
	$(COMPILE_DATA) $(dest_mod_d)/$(mod_f)

uninstall:
	- $(UNINSTALL_PROGRAM) $(dest_binary_d)/$(binary_f)
	- $(UNINSTALL_DATA) $(dest_doc_d)/$(doc_f)
	- $(UNINSTALL_DATA) $(dest_mod_d)/$(mod_f)
	- $(UNINSTALL_DIR) $(dest_mod_d)
	- $(UNINSTALL_DATA) $(dest_share_d)/$(share_f)
	- $(UNINSTALL_DIR) $(dest_binary_d) $(dest_conf_d) $(dest_doc_d) \
			   $(dest_share_d)

purge: uninstall
	- $(UNINSTALL_DATA) $(dest_conf_d)/$(conf_f)
