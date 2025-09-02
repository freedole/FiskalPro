import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableView, QVBoxLayout, 
                             QWidget, QMenuBar, QMenu, QAction, QStatusBar, QToolBar,
                             QMessageBox)
from PyQt5.QtCore import Qt
from database.models import Session, Artikal
from modules.ui.artikli_forma import ArtikalForma

print("🚀 main.py se pokreće...")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        print("🔄 MainWindow.__init__() pozvan")
        
        try:
            self.session = Session()
            print("✅ SQLAlchemy sesija kreirana")
            self.initUI()
            print("✅ initUI() završen")
        except Exception as e:
            print(f"❌ Greška u MainWindow.__init__(): {e}")
            import traceback
            traceback.print_exc()
            # Zatvori sesiju ako postoji
            if hasattr(self, 'session'):
                self.session.close()

    def initUI(self):
        print("🔄 initUI() pozvan")
        
        try:
            # Podešavanje prozora
            self.setWindowTitle('FiskalPro - POS Sistem')
            self.setGeometry(100, 100, 1000, 600)
            print("✅ Prozor podešen")
            
            # Kreiranje centralnog widgeta
            central_widget = QWidget()
            self.setCentralWidget(central_widget)
            print("✅ Centralni widget kreiran")
            
            # Layout
            layout = QVBoxLayout(central_widget)
            print("✅ Layout kreiran")
            
            # Kreiranje tabele
            self.table = QTableView()
            layout.addWidget(self.table)
            print("✅ Tabela kreirana i dodata u layout")
            
            # Učitaj podatke
            self.ucitaj_artikle()
            print("✅ Artikli učitani")
            
            # Kreiraj meni
            self.kreiraj_meni()
            print("✅ Meni kreiran")
            
            # Kreiraj toolbar
            self.kreiraj_toolbar()
            print("✅ Toolbar kreiran")
            
            # Kreiraj status bar
            self.statusBar().showMessage('Spremno')
            print("✅ Status bar kreiran")
            
        except Exception as e:
            print(f"❌ Greška u initUI(): {e}")
            import traceback
            traceback.print_exc()

    def kreiraj_meni(self):
        print("🔄 Kreiranje menija...")
        try:
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
            
            print("✅ Meni kreiran")
        except Exception as e:
            print(f"❌ Greška pri kreiranju menija: {e}")

    def kreiraj_toolbar(self):
        print("🔄 Kreiranje toolbara...")
        try:
            toolbar = QToolBar('Glavni toolbar')
            self.addToolBar(toolbar)
            
            novi_action = QAction('➕ Novi', self)
            novi_action.triggered.connect(self.dodaj_artikal)
            toolbar.addAction(novi_action)
            
            print("✅ Toolbar kreiran")
        except Exception as e:
            print(f"❌ Greška pri kreiranju toolbara: {e}")

    def ucitaj_artikle(self):
        print("🔄 Učitavam artikle...")
        try:
            # Učitaj artikle iz baze
            artikli = self.session.query(Artikal).all()
            print(f"✅ Pronađeno {len(artikli)} artikala")
            
            # Prikaži u tabeli
            from PyQt5.QtGui import QStandardItemModel, QStandardItem
            
            model = QStandardItemModel()
            model.setHorizontalHeaderLabels(['ID', 'Naziv', 'Cena', 'Stanje', 'Barkod', 'Kategorija'])
            
            for artikal in artikli:
                # Formatiraj cijenu sa zarezom umjesto tačke
                cena_str = f"{float(artikal.cena):.2f}".replace('.', ',')
                
                row = [
                    QStandardItem(str(artikal.id)),
                    QStandardItem(artikal.naziv),
                    QStandardItem(f"{cena_str} KM"),  # Ovdje koristimo format sa zarezom
                    QStandardItem(str(artikal.kolicina_na_stanju)),
                    QStandardItem(artikal.barkod or ''),
                    QStandardItem(artikal.kategorija.naziv if artikal.kategorija else '')
                ]
                model.appendRow(row)
            
            self.table.setModel(model)
            self.table.setColumnWidth(1, 250)
            self.table.setColumnWidth(2, 100)
            print("✅ Tabela popunjena sa podacima")
            
        except Exception as e:
            print(f"❌ Greška pri učitavanju artikala: {e}")
            import traceback
            traceback.print_exc()

    def dodaj_artikal(self):
        print("🔄 Otvaranje forme za artikal...")
        try:
            forma = ArtikalForma(parent=self)
            if forma.exec_():
                self.ucitaj_artikle()
                self.statusBar().showMessage('Artikal uspešno dodat!')
        except Exception as e:
            print(f"❌ Greška pri otvaranju forme: {e}")

    def closeEvent(self, event):
        print("🔄 Zatvaranje aplikacije...")
        try:
            if hasattr(self, 'session'):
                self.session.close()
            event.accept()
        except Exception as e:
            print(f"❌ Greška pri zatvaranju: {e}")
            event.accept()

def main():
    print("✅ main() funkcija pozvana")
    
    try:
        app = QApplication(sys.argv)
        print("✅ QApplication kreiran")
        
        window = MainWindow()
        print("✅ MainWindow kreiran")
        
        window.show()
        print("✅ window.show() pozvan - prozor bi trebao biti vidljiv")
        
        print("🔄 Ulazim u glavnu petlju...")
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"❌ Greška u main(): {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    print("🔍 __name__ == '__main__' - pokrećem glavni program")
    main()
