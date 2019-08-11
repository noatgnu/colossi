import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, "static")
Rscript = r"C:\Program Files\R\R-3.6.1\bin\Rscript.exe"
R_script_to_be_execute = os.path.join(APP_ROOT, "scater.R")