import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableView, QVBoxLayout, 
                             QWidget, QMenuBar, QMenu, QAction, QStatusBar, QToolBar,
                             QMessageBox)
from PyQt5.QtCore import Qt
from database.models import Session, Artikal
from modules.ui.artikli_forma import ArtikalForma  # DODAJTE OVO

class MainWindow(QMainWindow):
    # ... (ostali kod ostaje isti)
    
    def dodaj_artikal(self):
        forma = ArtikalForma(parent=self)
        if forma.exec_():
            self.ucitaj_artikle()  # Osveži prikaz
            self.statusBar().showMessage('Artikal uspešno dodat!')
    
    def ucitaj_artikle(self):
        # Ažurirajte ovu metodu za bolji prikaz
        from PyQt5.QtGui import QStandardItemModel, QStandardItem
        
        artikli = self.session.query(Artikal).all()
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['ID', 'Naziv', 'Cena', 'Stanje', 'Barkod', 'Kategorija'])
        
        for artikal in artikli:
            row = [
                QStandardItem(str(artikal.id)),
                QStandardItem(artikal.naziv),
                QStandardItem(f"{artikal.cena:.2f} RSD"),
                QStandardItem(str(artikal.kolicina_na_stanju)),
                QStandardItem(artikal.barkod or ''),
                QStandardItem(artikal.kategorija.naziv if artikal.kategorija else '')
            ]
            model.appendRow(row)
        
        self.table.setModel(model)
        self.table.setColumnWidth(1, 250)
        self.table.setColumnWidth(2, 100)
