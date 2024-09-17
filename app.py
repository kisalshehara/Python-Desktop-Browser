import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QTabWidget, QHBoxLayout, QFormLayout, QAction, QMenu, QMenuBar, QFileDialog, QInputDialog, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Pro Browser')
        self.setGeometry(100, 100, 1200, 800)

        # Create a QVBoxLayout for the main layout
        layout = QVBoxLayout()

        # Create a QTabWidget for handling multiple tabs
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_widget.tabCloseRequested.connect(self.close_tab)

        # Create a QPushButton for the New Tab button
        self.new_tab_button = QPushButton()
        self.new_tab_button.setIcon(QIcon("path/to/add_tab_icon.png"))  # Update with path to your icon
        self.new_tab_button.setIconSize(QSize(20, 20))
        self.new_tab_button.setStyleSheet("border-radius: 10px;")
        self.new_tab_button.clicked.connect(self.add_new_tab)

        # Create a QLineEdit for the URL bar
        self.url_bar = QLineEdit()
        self.url_bar.setPlaceholderText("Enter URL")
        self.url_bar.setStyleSheet("border-radius: 10px; padding: 5px;")
        self.url_bar.returnPressed.connect(self.load_url)

        # Create a QPushButton for the Go button with a search icon
        self.go_button = QPushButton()
        self.go_button.setIcon(QIcon("media/search_icon.png"))  # Update with path to your icon
        self.go_button.setIconSize(QSize(20, 20))
        self.go_button.setStyleSheet("border-radius: 10px;")
        self.go_button.clicked.connect(self.load_url)

        # Create navigation buttons
        self.back_button = QPushButton("Back")
        self.back_button.setStyleSheet("border-radius: 10px; background-color: #f0f0f0; padding: 5px;")
        self.back_button.clicked.connect(self.go_back)

        self.forward_button = QPushButton("Forward")
        self.forward_button.setStyleSheet("border-radius: 10px; background-color: #f0f0f0; padding: 5px;")
        self.forward_button.clicked.connect(self.go_forward)

        self.reload_button = QPushButton("Reload")
        self.reload_button.setStyleSheet("border-radius: 10px; background-color: #f0f0f0; padding: 5px;")
        self.reload_button.clicked.connect(self.reload_page)

        # Create a layout for navigation buttons
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.back_button)
        nav_layout.addWidget(self.forward_button)
        nav_layout.addWidget(self.reload_button)

        # Create a layout for URL bar and Go button
        url_layout = QHBoxLayout()
        url_layout.addWidget(self.url_bar)
        url_layout.addWidget(self.go_button)

        # Create a layout for tab bar and New Tab button
        tab_layout = QHBoxLayout()
        tab_layout.addWidget(self.tab_widget)
        tab_layout.addWidget(self.new_tab_button)

        # Add URL bar, Go button, navigation buttons, and tab bar to main layout
        layout.addLayout(url_layout)
        layout.addLayout(nav_layout)
        layout.addLayout(tab_layout)

        # Set layout to a QWidget and set it as central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Create menu bar for bookmarks
        self.menu_bar = self.menuBar()
        self.bookmark_menu = self.menu_bar.addMenu("Bookmarks")
        self.add_bookmark_action = QAction("Add Bookmark", self)
        self.add_bookmark_action.triggered.connect(self.add_bookmark)
        self.bookmark_menu.addAction(self.add_bookmark_action)
        
        self.bookmarks = []

        # Load default home page
        self.add_new_tab(QUrl("http://www.google.com"))

    def add_new_tab(self, url=None):
        # Create a new QWebEngineView for the tab
        browser = QWebEngineView()
        if url:
            browser.setUrl(url)
        else:
            browser.setUrl(QUrl("http://www.google.com"))

        # Add the new tab to the tab widget
        index = self.tab_widget.addTab(browser, "New Tab")
        self.tab_widget.setCurrentIndex(index)

        # Connect the current tab's URL change signal to the URL bar
        browser.urlChanged.connect(lambda q: self.url_bar.setText(q.toString()))
        browser.titleChanged.connect(lambda title: self.tab_widget.setTabText(self.tab_widget.currentIndex(), title))

    def load_url(self):
        # Load the URL in the current tab
        current_browser = self.tab_widget.currentWidget()
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        current_browser.setUrl(QUrl(url))

    def close_tab(self, index):
        # Close the tab at the given index
        if self.tab_widget.count() > 1:
            self.tab_widget.removeTab(index)

    def go_back(self):
        # Navigate back in the current tab
        current_browser = self.tab_widget.currentWidget()
        if current_browser.canGoBack():
            current_browser.back()

    def go_forward(self):
        # Navigate forward in the current tab
        current_browser = self.tab_widget.currentWidget()
        if current_browser.canGoForward():
            current_browser.forward()

    def reload_page(self):
        # Reload the current page
        current_browser = self.tab_widget.currentWidget()
        current_browser.reload()

    def add_bookmark(self):
        # Add a new bookmark
        current_browser = self.tab_widget.currentWidget()
        url = current_browser.url().toString()
        title = current_browser.title()
        self.bookmarks.append((title, url))
        
        # Update the bookmarks menu
        self.bookmark_menu.clear()
        self.bookmark_menu.addAction(self.add_bookmark_action)
        for title, url in self.bookmarks:
            action = QAction(title, self)
            action.setData(url)
            action.triggered.connect(self.open_bookmark)
            self.bookmark_menu.addAction(action)

    def open_bookmark(self):
        # Open a bookmarked URL
        action = self.sender()
        url = action.data()
        self.add_new_tab(QUrl(url))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())
