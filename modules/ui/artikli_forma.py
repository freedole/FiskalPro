from modules.core.utils import format_km, parsiraj_km
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QLineEdit, QComboBox, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from database.models import Session, Artikal, Kategorija

class ArtikalForma(QDialog):
    def __init__(self, artikal=None, parent=None):
        super().__init__(parent)
        self.artikal = artikal
        self.session = Session()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Novi artikal' if not self.artikal else 'Izmena artikla')
        self.setFixedSize(400, 300)
        
        layout = QVBoxLayout()
        
        # Naziv
        layout.addWidget(QLabel('Naziv artikla:'))
        self.naziv_input = QLineEdit()
        if self.artikal:
            self.naziv_input.setText(self.artikal.naziv)
        layout.addWidget(self.naziv_input)
        
        # Cena
        layout.addWidget(QLabel('Cijena:'))
        self.cena_input = QLineEdit()
        if self.artikal:
            self.cena_input.setText(str(self.artikal.cena))
        layout.addWidget(self.cena_input)
        
        # Barkod
        layout.addWidget(QLabel('Barkod:'))
        self.barkod_input = QLineEdit()
        if self.artikal:
            self.barkod_input.setText(self.artikal.barkod or '')
        layout.addWidget(self.barkod_input)
        
        # Količina
        layout.addWidget(QLabel('Početna količina:'))
        self.kolicina_input = QLineEdit()
        if self.artikal:
            self.kolicina_input.setText(str(self.artikal.kolicina_na_stanju))
        else:
            self.kolicina_input.setText('0')
        layout.addWidget(self.kolicina_input)
        
        # Kategorija
        layout.addWidget(QLabel('Kategorija:'))
        self.kategorija_combo = QComboBox()
        self.ucitaj_kategorije()
        layout.addWidget(self.kategorija_combo)
        
        # Dugmići
        button_layout = QHBoxLayout()
        
        self.snimi_btn = QPushButton('Snimi')
        self.snimi_btn.clicked.connect(self.snimi_artikal)
        
        self.odustani_btn = QPushButton('Odustani')
        self.odustani_btn.clicked.connect(self.reject)
        
        button_layout.addWidget(self.snimi_btn)
        button_layout.addWidget(self.odustani_btn)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
    
    def ucitaj_kategorije(self):
        kategorije = self.session.query(Kategorija).all()
        self.kategorija_combo.clear()
        
        for kategorija in kategorije:
            self.kategorija_combo.addItem(kategorija.naziv, kategorija.id)
        
        # Postavi selektovanu kategoriju ako editujemo
        if self.artikal and self.artikal.kategorija:
            index = self.kategorija_combo.findData(self.artikal.kategorija.id)
            if index >= 0:
                self.kategorija_combo.setCurrentIndex(index)
    
    def snimi_artikal(self):
        try:
            # Validacija
            naziv = self.naziv_input.text().strip()
            cena = parsiraj_km(self.cena_input.text().strip())
            barkod = self.barkod_input.text().strip() or None
            kolicina = int(self.kolicina_input.text().strip())
            kategorija_id = self.kategorija_combo.currentData()
            
            if not naziv:
                raise ValueError("Naziv artikla je obavezan")
            
            if cena <= 0:
                raise ValueError("Cena mora biti veća od 0")
            
            # Snimanje
            if self.artikal:
                # Edit mode
                self.artikal.naziv = naziv
                self.artikal.cena = cena
                self.artikal.barkod = barkod
                self.artikal.kolicina_na_stanju = kolicina
                self.artikal.kategorija_id = kategorija_id
            else:
                # New mode
                novi_artikal = Artikal(
                    naziv=naziv,
                    cena=cena,
                    barkod=barkod,
                    kolicina_na_stanju=kolicina,
                    kategorija_id=kategorija_id
                )
                self.session.add(novi_artikal)
            
            self.session.commit()
            self.accept()
            
        except ValueError as e:
            QMessageBox.warning(self, 'Greška', f"Neispravni podaci: {e}")
        except Exception as e:
            self.session.rollback()
            QMessageBox.critical(self, 'Greška', f"Došlo je do greške: {e}")
    
    def closeEvent(self, event):
        self.session.close()
        event.accept()
