import os
from sys import exit, argv
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QPushButton, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QDesktopWidget, QAbstractItemView, QLabel, QLineEdit, QGridLayout, QMessageBox
from PyQt5.QtCore import Qt

from grant_search import GrantSearch


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
    save = QPushButton("Save Documents")
    return search, save


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
    control_frame_layout.addWidget(buttons[0], 0, 2)
    control_frame_layout.addWidget(buttons[1], 1, 2)
    control_frame = QFrame()
    control_frame.setLayout(control_frame_layout)
    control_frame.setFixedHeight(120)
    return control_frame


def create_grant_display():
    grant_display = QTableWidget()
    grant_display.setColumnCount(3)
    grant_display.setHorizontalHeaderLabels(["Grant Number", "Link", "Title"])
    grant_display.setColumnWidth(0, 100)
    grant_display.setColumnWidth(1, 400)
    grant_display.setColumnWidth(2, 1000)
    grant_display.setEditTriggers(QAbstractItemView.NoEditTriggers)
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
    window.resize((screen_size.width() * 2) // 3, (screen_size.height() * 2) // 3)
    return window


def format_list_items(documents):
    items = []
    for i, grant in enumerate(documents["documents"]):
        grant_meta = grant.meta
        name = grant_meta["name"]
        url = grant_meta["url"]
        col1 = f'{grant_meta["grant_num"]}'
        col2 = f'{url}'
        col3 = f'{name}'
        item_str = [col1, col2, col3]
        items.append(item_str)
    return items


def display_results(grant_display, response, num):
    grant_display.setRowCount(num)
    items = format_list_items(response)
    for i, item in enumerate(items):
        for j, data in enumerate(item):
            grant_display.setItem(i, j, QTableWidgetItem(data))
    grant_display.setCurrentCell(0, 0)


def main():
    search = GrantSearch()

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

    def search_slot():
        query_txt = line_edits[0].text()
        print(query_txt)
        if len(query_txt) == 0:
            print("len 0")
            return
        try:
            num_resp = int(line_edits[1].text())
            if num_resp < 1:
                num_resp = 1
        except:
            num_resp = 5
        resp = search.search(query=query_txt, num=num_resp)
        display_results(grant_display, resp, num_resp)

    def save_slot():
        msg_box = QMessageBox(window)
        msg_box.setWindowTitle("Saving Documents")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg_box.setText("This will take a while (2-3 hours). Thank you for your patience. \n Click Ok to continue"
                        + " or Cancel to cancel.")
        ok = msg_box.exec_()
        if ok == QMessageBox.Ok:
            save_docs()
        else:
            print("Canceled saving documents.")

    def save_docs():
        names = os.listdir(r"funding_opportunities")
        print(f"Found {len(names)} files.")
        search.store_documents(names)
        print("Documents saved.")
        msg_box = QMessageBox(window)
        msg_box.setWindowTitle("Documents Saved")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText("All documents have been saved. \n Click OK to continue.")
        msg_box.exec_()

    buttons[0].clicked.connect(search_slot)
    buttons[1].clicked.connect(save_slot)

    exit(app.exec_())


if __name__ == '__main__':
    main()


