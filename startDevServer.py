from computing_codes import app

import os

print("Starting server in {}".format(os.getcwd()))
app.run(host='0.0.0.0', debug=True)
