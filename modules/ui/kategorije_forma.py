from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QPushButton, QMessageBox, QListWidget,
                             QInputDialog)
from database.models import Session, Kategorija

class KategorijeForma(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.session = Session()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Upravljanje kategorijama')
        self.setGeometry(200, 200, 400, 500)
        
        layout = QVBoxLayout()
        
        # Lista kategorija
        layout.addWidget(QLabel('Lista kategorija:'))
        self.lista_kategorija = QListWidget()
        self.ucitaj_kategorije()
        layout.addWidget(self.lista_kategorija)
        
        # Forma za dodavanje
        layout.addWidget(QLabel('Dodaj novu kategoriju:'))
        self.nova_kategorija_input = QLineEdit()
        layout.addWidget(self.nova_kategorija_input)
        
        # Dugmići
        button_layout = QHBoxLayout()
        
        self.dodaj_btn = QPushButton('Dodaj')
        self.dodaj_btn.clicked.connect(self.dodaj_kategoriju)
        
        self.izmeni_btn = QPushButton('Izmeni')
        self.izmeni_btn.clicked.connect(self.izmeni_kategoriju)
        
        self.obrisi_btn = QPushButton('Obriši')
        self.obrisi_btn.clicked.connect(self.obrisi_kategoriju)
        
        self.zatvori_btn = QPushButton('Zatvori')
        self.zatvori_btn.clicked.connect(self.accept)
        
        button_layout.addWidget(self.dodaj_btn)
        button_layout.addWidget(self.izmeni_btn)
        button_layout.addWidget(self.obrisi_btn)
        button_layout.addWidget(self.zatvori_btn)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def ucitaj_kategorije(self):
        self.lista_kategorija.clear()
        kategorije = self.session.query(Kategorija).all()
        for kat in kategorije:
            self.lista_kategorija.addItem(f"{kat.id}: {kat.naziv}")
    
    def dodaj_kategoriju(self):
        naziv = self.nova_kategorija_input.text().strip()
        if not naziv:
            QMessageBox.warning(self, 'Greška', 'Unesite naziv kategorije!')
            return
        
        try:
            nova_kategorija = Kategorija(naziv=naziv)
            self.session.add(nova_kategorija)
            self.session.commit()
            self.ucitaj_kategorije()
            self.nova_kategorija_input.clear()
            QMessageBox.information(self, 'Uspeh', 'Kategorija uspešno dodata!')
        except Exception as e:
            self.session.rollback()
            QMessageBox.critical(self, 'Greška', f'Došlo je do greške: {e}')
    
    def izmeni_kategoriju(self):
        selected = self.lista_kategorija.currentItem()
        if not selected:
            QMessageBox.warning(self, 'Greška', 'Odaberite kategoriju za izmenu!')
            return
        
        # Parsiraj ID iz teksta
        kat_id = int(selected.text().split(':')[0])
        kategorija = self.session.query(Kategorija).get(kat_id)
        
        novi_naziv, ok = QInputDialog.getText(self, 'Izmena kategorije', 
                                            'Novi naziv kategorije:',
                                            text=kategorija.naziv)
        if ok and novi_naziv.strip():
            try:
                kategorija.naziv = novi_naziv.strip()
                self.session.commit()
                self.ucitaj_kategorije()
                QMessageBox.information(self, 'Uspeh', 'Kategorija uspešno izmenjena!')
            except Exception as e:
                self.session.rollback()
                QMessageBox.critical(self, 'Greška', f'Došlo je do greške: {e}')
    
    def obrisi_kategoriju(self):
        selected = self.lista_kategorija.currentItem()
        if not selected:
            QMessageBox.warning(self, 'Greška', 'Odaberite kategoriju za brisanje!')
            return
        
        kat_id = int(selected.text().split(':')[0])
        kategorija = self.session.query(Kategorija).get(kat_id)
        
        reply = QMessageBox.question(self, 'Potvrda', 
                                   f'Da li ste sigurni da želite obrisati kategoriju "{kategorija.naziv}"?',
                                   QMessageBox.Yes | QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            try:
                self.session.delete(kategorija)
                self.session.commit()
                self.ucitaj_kategorije()
                QMessageBox.information(self, 'Uspeh', 'Kategorija uspešno obrisana!')
            except Exception as e:
                self.session.rollback()
                QMessageBox.critical(self, 'Greška', f'Došlo je do greške: {e}')