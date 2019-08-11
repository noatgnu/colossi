import re
import tempfile
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


@web.stream_request_body
class DataUploadHandler(BaseHandler):
    def prepare(self) -> Optional[Awaitable[None]]:
        self.temp_file = open('test.txt', 'wb')

    def data_received(self, chunk: bytes) -> Optional[Awaitable[None]]:
        self.temp_file.write(chunk)

    def post(self, *args, **kwargs):
        self.temp_file.close()
        job_id = uuid.uuid4().hex
        folder = os.path.join(settingmain.APP_STATIC, "temp", job_id)
        os.makedirs(folder)
        input_file = ""
        with open("test.txt", "rt") as temp_file:
            content = False
            filename = ""
            content_json = False
            setting = ""
            for line in temp_file:
                if line.startswith('Content-Disposition') and not filename:
                    content = True
                    fi = re.search('filename="(.+)"', line)
                    if fi:
                        print(fi)
                        filename = fi.group(1)
                elif line.startswith('Content-Type: application/octet-stream'):
                    print(filename)
                    input_file = open(os.path.join(folder, filename), 'wt')
                elif line.startswith('Content-Type: application/json'):
                    input_file.close()
                    content_json = True
                else:
                    if not line.startswith("------WebKitFormBoundary"):
                        if not content and content_json:
                            line = line.strip()
                            if line:
                                setting += line
                        elif content and input_file:
                            if line.strip():
                                input_file.write(line)
                    else:
                        if content:
                            content = False
        print(setting)
        setting = escape.json_decode(setting)

        result = {"userResult": [], "compareDataframe": []}
        out = os.path.join(folder, "out_" + filename)
        subprocess.run([settingmain.Rscript, '--vanilla', settingmain.R_script_to_be_execute, os.path.join(folder, filename), out], shell=True)
        result_data = pd.read_csv(out, sep=" ")
        compare_df = pd.read_csv(r"C:\Users\Toan\Documents\GitHub\colossi\bulk_output.csv")
        result["summaryStats"] = result_data.to_dict(orient="records")
        result["compareDataframe"] = compare_df.to_dict()
        self.write(result)
