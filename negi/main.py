# -*- coding: utf-8 -*-

import aaargh
from app import Negi

app = aaargh.App(description="Jinja2+JSON powered static HTML build tool")

@app.cmd(help='Parse JSON and build HTML')
@app.cmd_arg('-d','--data_dir',default='./data',help='JSON data dirctory(default:./data')
@app.cmd_arg('-t','--tmpl_dir',default='./templates',help='Jinja2 template dirctory(default:./templates')
@app.cmd_arg('-o','--out_dir',default='./dist',help='Output dirctory(default:./dist')
@app.cmd_arg('-v','--verbose',nargs='?',const=True,default=False)
def build(data_dir,tmpl_dir,out_dir,verbose):

    builder = Negi(
        data_dir= data_dir,
        tmpl_dir = tmpl_dir,
        out_dir = out_dir,
        verbose = verbose
    )
    builder.build()


def main():
    app.run()

if __name__ == '__main__':
    main()
