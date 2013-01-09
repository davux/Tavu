DESTDIR = /
INSTALL = install
INSTALL_PROGRAM = $(INSTALL) -m 755
INSTALL_DATA = $(INSTALL) -m 644
INSTALL_DIR = $(INSTALL) -d
UNINSTALL_PROGRAM = rm
UNINSTALL_DATA = rm
UNINSTALL_DIR = rmdir -p --ignore-fail-on-non-empty
COMPILE_DATA = pycompile

binary_f = tavu-listen
conf_f   = tavurc
share_f  = dotfile.skel

dest_binary_d = $(DESTDIR)/usr/bin
dest_conf_d   = $(DESTDIR)/etc
dest_doc_d    = $(DESTDIR)/usr/share/doc/tavu
dest_share_d  = $(DESTDIR)/usr/share/tavu
dest_mod_d    = $(DESTDIR)/usr/share/tavu/python

all:

install: prog-install doc-install

prog-install:
	$(INSTALL_DIR) $(dest_binary_d) $(dest_conf_d) $(dest_share_d) $(dest_mod_d)
	$(INSTALL_PROGRAM) $(binary_f) 	$(dest_binary_d)
	$(INSTALL_DATA) $(conf_f)	$(dest_conf_d)
	$(INSTALL_DATA) $(share_f)	$(dest_share_d)
	$(INSTALL_DATA) python/*.py	$(dest_mod_d)
	$(COMPILE_DATA) $(dest_mod_d)/*.py

doc-install:
	$(INSTALL_DIR) $(dest_doc_d)
	$(INSTALL_DATA) doc/*		$(dest_doc_d)

uninstall:
	- $(UNINSTALL_PROGRAM) $(dest_binary_d)/$(binary_f)
	- $(UNINSTALL_DATA) $(dest_doc_d)/*
	- $(UNINSTALL_DATA) $(dest_mod_d)/*.pyc
	- $(UNINSTALL_DATA) $(dest_mod_d)/*.py
	- $(UNINSTALL_DIR) $(dest_mod_d)
	- $(UNINSTALL_DATA) $(dest_share_d)/$(share_f)
	- $(UNINSTALL_DIR) $(dest_binary_d) $(dest_conf_d) $(dest_doc_d) \
			   $(dest_share_d)

purge: uninstall
	- $(UNINSTALL_DATA) $(dest_conf_d)/$(conf_f)
