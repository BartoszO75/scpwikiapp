import sys
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QSizePolicy, QLineEdit, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QIcon
from google_auth_oauthlib.flow import InstalledAppFlow

class SCPFoundationApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Ustawienia głównego okna
        self.setWindowTitle("SCP Foundation Wiki App")
        self.setGeometry(100, 100, 810, 600)

        # Ustawienia ikony programu
        self.setWindowIcon(QIcon('scp_logo.png'))

        # Przycisk "Pokaż Opowiadanie"
        self.show_story_button = QPushButton("Pokaż Opowiadanie", self)
        self.show_story_button.clicked.connect(self.load_story)

        # Pole tekstowe na numer SCP lub link
        self.scp_entry = QLineEdit(self)
        self.scp_entry.setPlaceholderText("Podaj numer SCP lub link (opcjonalne)")

        # Przycisk "Zaloguj"
        self.login_button = QPushButton("Zaloguj", self)
        self.login_button.clicked.connect(self.login_with_google)

        # Labelka z informacją o logowaniu
        self.login_status_label = QLabel("", self)
        self.login_status_label.setAlignment(Qt.AlignCenter)

        # Układ głównego okna
        layout = QVBoxLayout()
        layout.addWidget(self.show_story_button)
        layout.addWidget(self.scp_entry)
        layout.addWidget(self.login_button)
        layout.addWidget(self.login_status_label)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Początkowy URL
        self.current_url = "http://scp-pl.wikidot.com/"
        self.web_view = QWebEngineView(self)
        self.web_view.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.web_view.setStyleSheet("margin: 2px;")  # Dodaj marginesy

        # Układ do wyświetlania przeglądarki
        web_layout = QVBoxLayout()
        web_layout.addWidget(self.web_view)
        layout.addLayout(web_layout)
        self.web_view.setUrl(QUrl(self.current_url))

        # Zmienna do śledzenia stanu logowania
        self.logged_in = False

        # Tworzenie przepływu autoryzacji
        self.flow = InstalledAppFlow.from_client_secrets_file(
        "C:\\Users\\kosie\\Downloads\\client_secret_810927591405-u5281humn84bg2dn20j56u41a2d3v33g.apps.googleusercontent.com.json",
        ['https://www.googleapis.com/auth/plus.login'],
        redirect_uri="http://scp-pl.wikidot.com/search")  # To URI przekierowania musi być takie samo, jak w Konsoli Google Cloud


        # Poświadczenia
        self.credentials = None

    def load_story(self):
        if self.logged_in:
            scp_input = self.scp_entry.text().strip()
            if scp_input.startswith("http"):
                self.current_url = scp_input
            elif scp_input:
                self.current_url = f"http://scp-pl.wikidot.com/scp-{scp_input}"
            else:
                self.current_url = "http://scp-pl.wikidot.com/"

            self.web_view.setUrl(QUrl(self.current_url))
        else:
            QMessageBox.warning(self, "Brak autoryzacji", "Proszę się zalogować przed korzystaniem z aplikacji.")

    def login_with_google(self):
        # Uruchamianie przepływu autoryzacji
        creds = self.flow.run_local_server(port=0)
        # Ustawienie poświadczeń
        self.credentials = creds

        # Po autoryzacji zapisz stan zalogowanego użytkownika
        self.logged_in = True
        self.login_status_label.setText("Zalogowano pomyślnie przez Google.")
        self.login_status_label.setStyleSheet("color: green")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    scp_app = SCPFoundationApp()
    scp_app.show()
    sys.exit(app.exec_())
