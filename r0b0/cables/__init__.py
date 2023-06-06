import importlib
import glob
from os.path import basename
from r0b0 import logging
from r0b0.config import MESSAGES_DIR, CABLES_DIR
# from r0b0.cables.msg_funcs import *
# print(f'abs: {abspath(".")}, rel: {relpath(".")}')

'''
This will import everything found
in python files in this r0b0.messages director

Usage:
from r0b0.messages import *
'''

for file in glob.glob(str(CABLES_DIR / '*.py')):
    if '__init__' in file: continue
    mod_name = basename(file).split('.')[0]
    logging.debug(mod_name)
    mod = importlib.import_module(f'r0b0.cables.{mod_name}')
    globals().update({mod_name:mod})
    globals().update({v:getattr(mod,v) for v in dir(mod) if '__' not in v})
