This is an application that is allows the user to semantically search for grants from the NIH.

The attached database is purely for testing purposes as it only contains around 375 files to reduce its size so that GitHub can store it.
If you would like to use the full set of grants, you must save the documents through either `basic_gui.py` or `simple_server.py`.

Before running, make sure that the required packages are installed by first making sure pip is upgraded with `pip install --upgrade pip`
and then using `pip install -r requirements.txt` to install all packages. Do not forget to upgrade pip, as it may cause issues if not.

To run the application with `simple_gui.py`, make sure the requirements from `requirements.txt` are installed and then use the command `python -m basic_gui`.

To run the application with a server-client relationship, first run the server with `python -m simple_server port --update --print` where port is the port the server is listening on,
`--update` is an optional flag that tells the program to save all documents if 1 and nothing if anything else,
and `--print` is another optional flag that tells the server if it should print the results it sends.
Then, to run the client, use `python -m simple_client host port`, where host and port are the server's IP and port.

An example of the server-client version is as follows:\
Run the server with: `python -m simple_server 11000 -u 0 -p 1`
This will start the server listening on port 11000, not update the documents, and will print out the results

Then run the client with: `python -m simple_client 127.0.0.1 11000`
This will start the client with a connection to 127.0.0.1:11000, the address of the server.
