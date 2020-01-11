

import sys, os
sys.path.append(os.path.join(os.getcwd(), "app"))

import app

app.boot()
app.run()