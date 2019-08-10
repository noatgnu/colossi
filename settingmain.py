import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, "assets")
Rscript = ""
R_script_to_be_execute = os.path.join(APP_ROOT, "rScript.R")