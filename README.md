This is an application that is allows the user to semantically search for grants from the NIH.

The attached database is purely for testing purposes as it only contains around 375 files to reduce its size so that GitHub can store it.
If you would like to use the full set of grants, you must save the documents through either `basic_gui.py` or `simple_server.py`.

Before running, make sure that the required packages are installed by first making sure pip is upgraded with `pip install --upgrade pip`
and then using `pip install -r requirements.txt` to install all packages. Do not forget to upgrade pip, as it may cause issues if not.

To run the application with `simple_gui.py`, make sure the requirements from `requirements.txt` are installed and then use the command `python -m basic_gui`.

To run the application with a server-client relationship, first run the server with `python -m simple_server port update` where port is the port the server is listening on,
and update is a flag that tells the program to save all documents if 1 and nothing if anything else. Then, to run the client,
use `python -m simple_client host port`, where host and port are the server's IP and port.