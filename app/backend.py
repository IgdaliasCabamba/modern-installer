import pathlib
import platformdirs
import os
import sys

class Backend:
    def __init__(self, frontend):
        self._ui = frontend

        self.install_dir = None
        self.desktop_shortcut = False
        self.open_after_install = False
        self.sucess_url = None
        self.terms = {}
        self.more = {}

    def set_install_folder(self, path):
        self.install_dir = path

    def add_term(self, name, term):
        self.terms[name] == term

    def set_terms_status(self, name, accepted):
        self.terms[name] == accepted

    def create_desktop_shortcut(self, checked):
        self.desktop_shortcut = checked

    def set_sucess_url(self, url):
        self.sucess_url = url
    
    def open_after_install(self, checked):
        self.open_after_install = checked 

    def install(self):
        print("OK")
