import os
from sys import exit, argv
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, QPushButton, QTableView, QTableWidget, QTableWidgetItem
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout, QListWidget, QListWidgetItem, QMessageBox, QDialog
from PyQt5.QtGui import QFont
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
    # grant_display = QListWidget()
    grant_display = QTableWidget()
    grant_display.setColumnCount(3)
    grant_display.setHorizontalHeaderLabels(["Grant Number", "Link", "Title"])
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
    # grant_display.clear()
    # list_items = []
    # items = format_list_items(response)
    # for item in items:
    #     new_item = QListWidgetItem()
    #     new_item.setText(item)
    #     new_item.setFont(QFont('Courier'))
    #     grant_display.addItem(new_item)
    #     list_items.append(new_item)
    #
    # grant_display.setCurrentRow(0)
    # grant_display.repaint()


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

    # Handle events for the LineEdit objects.
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
        names = os.listdir(r"funding_opportunities")
        print(f"Found {len(names)} files.")
        msg_box = QMessageBox(window)
        msg_box.setWindowTitle("Saving Documents")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText("This will take a while. Thank you for your patience. \n Click OK to continue.")
        msg_box.exec_()
        search.store_documents(names)
        msg_box.setWindowTitle("Documents Saved")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setText("All documents have been saved. \n Click OK to continue.")
        msg_box.exec_()

    buttons[0].clicked.connect(search_slot)
    buttons[1].clicked.connect(save_slot)

    exit(app.exec_())


if __name__ == '__main__':
    main()


