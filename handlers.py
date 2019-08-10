import uuid
import os
import sqlite3
import asyncio
import settingmain
import subprocess
from typing import Optional, Awaitable
import pandas as pd
from tornado import web, ioloop, escape


conn = sqlite3.connect("./colossi.db")
c = conn.cursor()

try:
    print("Initialize job table")
    c.execute("""CREATE TABLE job (id integer primary key autoincrement, job_id text)""")
except sqlite3.OperationalError:
    print("job table already initiated")


class BaseHandler(web.RequestHandler):
    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        pass

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, PUT')

    def options(self):
        self.set_status(204)
        self.finish()


class HomeHandler(BaseHandler):
    @asyncio.coroutine
    def get(self):
        self.write("success")


class DataUploadHandler(BaseHandler):
    @asyncio.coroutine
    def post(self, *args, **kwargs):
        job_id = uuid.uuid4().hex
        folder = os.path.join(settingmain.APP_STATIC, "temp", job_id)
        os.makedirs(folder)
        result = {"user_result": [], "compare_dataframe": []}
        i = self.request.files["files"][0]
        print(i)
        f = os.path.join(folder, i["filename"])
        out = os.path.join(folder, "out_" + i["filename"])
        with open(f, 'wb') as input_file:
            input_file.write(i["body"])
        out = f
        # subprocess.call([settingmain.Rscript, '--vanilla', settingmain.R_script_to_be_execute, f, out], shell=True)
        result_data = pd.read_csv(out, sep="\t")
        result["user_result"] = result_data.to_json(orient='records')
        self.write(result)
