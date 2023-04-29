from sys import exit, argv, stderr
import argparse as ap
from socket import socket
from pickle import dump, load
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QPushButton
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout, QListWidget, QListWidgetItem, QMessageBox, QDialog
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from queryclass import QueryObject


def parsing():
    parsed = None
    try:
        parser = ap.ArgumentParser(description='Client for the semantic search application', allow_abbrev=False)
        parser.add_argument('host', help='the host on which the server is running')
        parser.add_argument('port', help='the port at which the server should listen', type=int)
        parsed = parser.parse_args()
    except Exception as ex:
        print(ex)
        exit(2)
    return parsed


def get_connection(query, host, port):
    try:
        with socket() as sock:
            sock.connect((host, port))
            out_flo = sock.makefile(mode='wb')
            dump(query, out_flo)
            out_flo.flush()
            in_flo = sock.makefile(mode='rb')
            response = load(in_flo)
            return response
    except Exception as ex:
        print("Got exception not connection")
        print(ex, file=stderr)


def create_labels():
    query_label = QLabel('Query: ')
    query_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    query_label.setAutoFillBackground(True)
    palette = query_label.palette()
    query_label.setPalette(palette)

    num_label = QLabel('Num Results: ')
    num_label.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    num_label.setAutoFillBackground(True)
    palette = num_label.palette()
    num_label.setPalette(palette)
    return query_label, num_label


def create_line_edits():
    query_line_edit = QLineEdit("")
    num_line_edit = QLineEdit("5")
    return query_line_edit, num_line_edit


def create_buttons():
    search = QPushButton("Search")
    return search


def create_control_frame(labels, line_edits, buttons):

    control_frame_layout = QGridLayout()
    control_frame_layout.setSpacing(10)
    control_frame_layout.setContentsMargins(0, 0, 0, 0)
    control_frame_layout.setRowStretch(0, 0)
    control_frame_layout.setColumnStretch(0, 0)
    control_frame_layout.addWidget(labels[0], 0, 0)
    control_frame_layout.addWidget(labels[1], 1, 0)
    control_frame_layout.addWidget(line_edits[0], 0, 1)
    control_frame_layout.addWidget(line_edits[1], 1, 1)
    control_frame_layout.addWidget(buttons, 0, 2)
    control_frame = QFrame()
    control_frame.setLayout(control_frame_layout)
    control_frame.setFixedHeight(120)
    return control_frame


def create_grant_display():
    grant_display = QListWidget()
    return grant_display


def create_central_frame(grant_display, control_frame):
    central_frame_layout = QGridLayout()
    central_frame_layout.setSpacing(10)
    central_frame_layout.addWidget(control_frame, 0, 0)
    central_frame_layout.addWidget(grant_display, 1, 0)
    central_frame = QFrame()
    central_frame.setLayout(central_frame_layout)
    return central_frame


def create_window(central_frame):
    window = QMainWindow()
    window.setWindowTitle('Semantic Search For Government Grants')
    window.setCentralWidget(central_frame)
    screen_size = QDesktopWidget().screenGeometry()
    window.resize(screen_size.width()//2, screen_size.height()//2)
    return window


def format_list_items(documents):
    items = []
    for i, grant in enumerate(documents["documents"]):
        grant_meta = grant.meta
        name = grant_meta["name"]
        # name = (name[:80] + '...') if len(name) > 83 else name
        url = grant_meta["url"]
        col1 = f'{grant_meta["grant_num"]: >14}'
        col2 = f' |-| {url: >67}'
        col3 = f' |-| {name: >}'
        item_str = col1 + col2 + col3
        items.append(item_str)
    return items


def display_results(grant_display, items):
    grant_display.clear()
    list_items = []
    # items = format_list_items(response)
    for item in items:
        new_item = QListWidgetItem()
        new_item.setText(item)
        new_item.setFont(QFont('Courier'))
        grant_display.addItem(new_item)
        list_items.append(new_item)

    grant_display.setCurrentRow(0)
    grant_display.repaint()


def search_slot_helper(line_edits, grant_display, host, port, window):
    query_txt = line_edits[0].text()
    print(query_txt)
    if len(query_txt) == 0:
        print("len 0")
        return
    try:
        num_resp = int(line_edits[1].text())
        if num_resp < 1:
            num_resp = 1
    except ValueError:
        num_resp = 5
    query = QueryObject(query=query_txt, num=num_resp)
    resp = get_connection(query, host, port)
    if resp[0]:
        if resp[1] is not None:
            display_results(grant_display, resp[1])
    else:
        msg_box = QMessageBox(window)
        msg_box.setWindowTitle("Server Error")
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setText(resp[1])
        print(resp[1], file=stderr)


def main():
    args = parsing()

    app = QApplication(argv)

    # Create and lay out widgets.
    labels = create_labels()
    line_edits = create_line_edits()
    buttons = create_buttons()
    control_frame = create_control_frame(labels, line_edits, buttons)
    grant_display = create_grant_display()
    central_frame = create_central_frame(grant_display, control_frame)
    window = create_window(central_frame)
    window.show()

    # Handle events for the LineEdit objects.
    def search_slot():
        search_slot_helper(line_edits, grant_display, args.host, args.port, window)

    buttons.clicked.connect(search_slot)

    exit(app.exec_())


if __name__ == '__main__':
    main()


