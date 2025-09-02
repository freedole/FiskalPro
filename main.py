import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableView, QVBoxLayout, 
                             QWidget, QMenuBar, QMenu, QAction, QStatusBar, QToolBar)
from PyQt5.QtCore import Qt
from database.models import Session, Artikal

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.session = Session()
        self.initUI()
        
    def initUI(self):
        # Podešavanje prozora
        self.setWindowTitle('FiskalPro - POS Sistem')
        self.setGeometry(100, 100, 1000, 600)
        
        # Kreiranje centralnog widgeta
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout
        layout = QVBoxLayout(central_widget)
        
        # Kreiranje tabele
        self.table = QTableView()
        layout.addWidget(self.table)
        
        # Učitaj podatke
        self.ucitaj_artikle()
        
        # Kreiraj meni
        self.kreiraj_meni()
        
        # Kreiraj toolbar
        self.kreiraj_toolbar()
        
        # Kreiraj status bar
        self.statusBar().showMessage('Spremno')
        
    def kreiraj_meni(self):
        menubar = self.menuBar()
        
        # Fajl meni
        file_menu = menubar.addMenu('&Fajl')
        
        exit_action = QAction('Izlaz', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Artikli meni
        artikli_menu = menubar.addMenu('&Artikli')
        
        novi_action = QAction('Novi artikal', self)
        novi_action.triggered.connect(self.dodaj_artikal)
        artikli_menu.addAction(novi_action)
        
    def kreiraj_toolbar(self):
        toolbar = QToolBar('Glavni toolbar')
        self.addToolBar(toolbar)
        
        novi_action = QAction('➕ Novi', self)
        novi_action.triggered.connect(self.dodaj_artikal)
        toolbar.addAction(novi_action)
        
    def ucitaj_artikle(self):
        # Učitaj artikle iz baze
        artikli = self.session.query(Artikal).all()
        
        # Prikaži u tabeli (za sada samo osnovni prikaz)
        from PyQt5.QtGui import QStandardItemModel, QStandardItem
        
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['ID', 'Naziv', 'Cena', 'Stanje', 'Barkod'])
        
        for artikal in artikli:
            row = [
                QStandardItem(str(artikal.id)),
                QStandardItem(artikal.naziv),
                QStandardItem(str(artikal.cena)),
                QStandardItem(str(artikal.kolicina_na_stanju)),
                QStandardItem(artikal.barkod or '')
            ]
            model.appendRow(row)
        
        self.table.setModel(model)
        self.table.setColumnWidth(1, 250)  # Širina za naziv
        
    def dodaj_artikal(self):
        self.statusBar().showMessage('Otvaranje forme za novi artikal...')
        # Ovo ćemo implementirati kasnije
        
    def closeEvent(self, event):
        self.session.close()
        event.accept()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
