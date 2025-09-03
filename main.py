import sys
import os
from modules.ui.kategorije_forma import KategorijeForma
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTableView, QVBoxLayout, 
                             QWidget, QMenuBar, QMenu, QAction, QStatusBar, QToolBar,
                             QMessageBox, QLineEdit, QGridLayout, QGroupBox, QLabel,
                             QStackedWidget)
from PyQt5.QtCore import Qt
from database.models import Session, Artikal
from modules.ui.artikli_forma import ArtikalForma
from modules.core.izvestaji_service import IzvestajiService

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
            if hasattr(self, 'session'):
                self.session.close()

    def initUI(self):
        print("🔄 initUI() pozvan")
        
        try:
            self.setWindowTitle('FiskalPro - POS Sistem')
            self.setGeometry(100, 100, 1000, 600)
            print("✅ Prozor podešen")
            
            # KREIRAJTE STACKED WIDGET
            self.stacked_widget = QStackedWidget()
            self.setCentralWidget(self.stacked_widget)
            
            # Kreiraj widget za artikle
            self.artikli_widget = QWidget()
            self.artikli_layout = QVBoxLayout(self.artikli_widget)
            
            self.table = QTableView()
            self.artikli_layout.addWidget(self.table)
            print("✅ Tabela kreirana i dodata u layout")
            
            # Kreiraj widget za dashboard
            self.dashboard_widget = QWidget()
            self.dashboard_widget.setLayout(QGridLayout())
            
            # Dodaj oba widgeta u stacked widget
            self.stacked_widget.addWidget(self.artikli_widget)
            self.stacked_widget.addWidget(self.dashboard_widget)
            
            # Pokazi artikle kao podrazumevani
            self.stacked_widget.setCurrentIndex(0)
            
            self.ucitaj_artikle()
            print("✅ Artikli učitani")
            
            self.kreiraj_meni()
            print("✅ Meni kreiran")
            
            self.kreiraj_toolbar()
            print("✅ Toolbar kreiran")
            
            self.statusBar().showMessage('Spremno')
            print("✅ Status bar kreiran")
            
            self.table.doubleClicked.connect(self.izmeni_artikal)
            
            self.table.setContextMenuPolicy(Qt.ActionsContextMenu)
            delete_action = QAction('Obriši artikal', self)
            delete_action.triggered.connect(self.obrisi_artikal)
            self.table.addAction(delete_action)
            
        except Exception as e:
            print(f"❌ Greška u initUI(): {e}")
            import traceback
            traceback.print_exc()

    def izmeni_artikal(self, index):
        try:
            row = index.row()
            artikal_id = int(self.table.model().index(row, 0).data())
            artikal = self.session.query(Artikal).get(artikal_id)
            if artikal:
                forma = ArtikalForma(artikal=artikal, parent=self)
                if forma.exec_():
                    self.ucitaj_artikle()
                    self.statusBar().showMessage('Artikal uspešno izmenjen!')
        except Exception as e:
            print(f"❌ Greška pri editovanju artikla: {e}")

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
            
            kategorije_action = QAction('Upravljanje kategorijama', self)
            kategorije_action.triggered.connect(self.upravljaj_kategorijama)
            artikli_menu.addAction(kategorije_action)
            
            # Izveštaji meni
            izvestaji_menu = menubar.addMenu('&Izveštaji')
            dashboard_action = QAction('📊 Dashboard', self)
            dashboard_action.triggered.connect(self.prikazi_dashboard)
            izvestaji_menu.addAction(dashboard_action)
            
            artikli_view_action = QAction('📋 Prikaži artikle', self)
            artikli_view_action.triggered.connect(self.prikazi_artikle_view)
            izvestaji_menu.addAction(artikli_view_action)
            
            print("✅ Meni kreiran")
        except Exception as e:
            print(f"❌ Greška pri kreiranju menija: {e}")
   
    def upravljaj_kategorijama(self):
        """Prikaži formu za upravljanje kategorijama"""
        try:
            forma = KategorijeForma(parent=self)
            forma.exec_()
        except Exception as e:
            QMessageBox.critical(self, "Greška", f"Došlo je do greške: {e}")
    
    def kreiraj_toolbar(self):
        print("🔄 Kreiranje toolbara...")
        try:
            toolbar = QToolBar('Glavni toolbar')
            self.addToolBar(toolbar)
            
            # Dashboard dugme
            dashboard_action = QAction('📊 Dashboard', self)
            dashboard_action.triggered.connect(self.prikazi_dashboard)
            toolbar.addAction(dashboard_action)
            
            # Novi artikal dugme
            novi_action = QAction('➕ Novi artikal', self)
            novi_action.triggered.connect(self.dodaj_artikal)
            toolbar.addAction(novi_action)
            
            # Search
            self.search_input = QLineEdit()
            self.search_input.setPlaceholderText("🔍 Pretraži artikle...")
            self.search_input.textChanged.connect(self.pretrazi_artikle)
            toolbar.addWidget(self.search_input)
            
            print("✅ Toolbar kreiran")
        except Exception as e:
            print(f"❌ Greška pri kreiranju toolbara: {e}")

    def pretrazi_artikle(self, tekst):
        try:
            if not tekst.strip():
                self.ucitaj_artikle()
                return
                
            artikli = self.session.query(Artikal).filter(
                (Artikal.naziv.ilike(f"%{tekst}%")) | 
                (Artikal.barkod.ilike(f"%{tekst}%"))
            ).all()
            
            self.prikazi_artikle(artikli)
            
        except Exception as e:
            print(f"❌ Greška pri pretrazi: {e}")

    def prikazi_artikle(self, artikli):
        from PyQt5.QtGui import QStandardItemModel, QStandardItem
        
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(['ID', 'Naziv', 'Cena', 'Stanje', 'Barkod', 'Kategorija'])
        
        for artikal in artikli:
            cena_str = f"{float(artikal.cena):.2f}".replace('.', ',')
            row = [
                QStandardItem(str(artikal.id)),
                QStandardItem(artikal.naziv),
                QStandardItem(f"{cena_str} KM"),
                QStandardItem(str(artikal.kolicina_na_stanju)),
                QStandardItem(artikal.barkod or ''),
                QStandardItem(artikal.kategorija.naziv if artikal.kategorija else '')
            ]
            model.appendRow(row)
        
        self.table.setModel(model)
        self.table.setColumnWidth(1, 250)
        self.table.setColumnWidth(2, 100)

    def prikazi_artikle_view(self):
        """Vraća prikaz artikala"""
        self.stacked_widget.setCurrentIndex(0)
        self.ucitaj_artikle()

    def ucitaj_artikle(self):
        print("🔄 Učitavam artikle...")
        try:
            artikli = self.session.query(Artikal).all()
            print(f"✅ Pronađeno {len(artikli)} artikala")
            self.prikazi_artikle(artikli)
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

    def obrisi_artikal(self):
        try:
            selected = self.table.currentIndex()
            if selected.isValid():
                row = selected.row()
                artikal_id = int(self.table.model().index(row, 0).data())
                
                reply = QMessageBox.question(self, 'Potvrda', 
                                          'Da li ste sigurni da želite obrisati ovaj artikal?',
                                          QMessageBox.Yes | QMessageBox.No)
                
                if reply == QMessageBox.Yes:
                    artikal = self.session.query(Artikal).get(artikal_id)
                    if artikal:
                        self.session.delete(artikal)
                        self.session.commit()
                        self.ucitaj_artikle()
                        self.statusBar().showMessage('Artikal uspešno obrisan!')
                        
        except Exception as e:
            self.session.rollback()
            print(f"❌ Greška pri brisanju artikala: {e}")

    def prikazi_dashboard(self):
        """Prikaži dashboard sa statistikama"""
        try:
            print("🔄 Prikazujem dashboard...")
            
            # Kreiraj potpuno novi widget za dashboard svaki put
            dashboard_widget = QWidget()
            grid = QGridLayout(dashboard_widget)
            
            izvestaji = IzvestajiService()
            
            # Današnji promet
            promet = izvestaji.dnevni_promet()
            group_promet = QGroupBox("📊 Današnji Promet")
            layout_promet = QVBoxLayout()
            layout_promet.addWidget(QLabel(f"🔄 Broj računa: {promet['broj_racuna']}"))
            layout_promet.addWidget(QLabel(f"💰 Ukupno: {self.format_km(promet['ukupan_promet'])}"))
            group_promet.setLayout(layout_promet)
            
            # Stanje zaliha
            stanje = izvestaji.stanje_zaliha()
            group_zalihe = QGroupBox("📦 Stanje Zaliha")
            layout_zalihe = QVBoxLayout()
            layout_zalihe.addWidget(QLabel(f"🏷️ Ukupna vrijednost: {self.format_km(stanje['ukupna_vrednost'])}"))
            layout_zalihe.addWidget(QLabel(f"📦 Broj artikala: {len(stanje['stanje_artikala'])}"))
            group_zalihe.setLayout(layout_zalihe)
            
            grid.addWidget(group_promet, 0, 0)
            grid.addWidget(group_zalihe, 0, 1)
            
            # Zameni postojeći dashboard widget novim
            self.stacked_widget.removeWidget(self.dashboard_widget)
            self.dashboard_widget = dashboard_widget
            self.stacked_widget.addWidget(self.dashboard_widget)
            self.stacked_widget.setCurrentIndex(1)
            
            self.statusBar().showMessage('Dashboard učitan')
            print("✅ Dashboard prikazan")
            
        except Exception as e:
            print(f"❌ Greška pri prikazu dashboarda: {e}")
            import traceback
            traceback.print_exc()

    def format_km(self, iznos):
        """Pomoćna funkcija za formatiranje KM"""
        try:
            return f"{float(iznos):.2f}".replace('.', ',') + " KM"
        except:
            return "0,00 KM"

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