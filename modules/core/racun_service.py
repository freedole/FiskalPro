# modules/core/racun_service.py
from database.models import Session, Racun, StavkaRacuna, Artikal
from datetime import datetime

class RacunService:
    def __init__(self):
        self.session = Session()
    
    def kreiraj_racun(self, stavke_data, nacin_placanja='gotovina'):
        """Kreira novi fiskalni račun"""
        try:
            # Generiši broj računa (npr. RAC-20250902-001)
            broj_racuna = f"RAC-{datetime.now().strftime('%Y%m%d')}-001"
            
            # Kreiraj račun
            racun = Racun(
                broj_racuna=broj_racuna,
                nacin_placanja=nacin_placanja,
                ukupan_iznos=0,
                placen_iznos=0
            )
            self.session.add(racun)
            
            # Dodaj stavke
            ukupan_iznos = 0
            for stavka_data in stavke_data:
                artikal = self.session.query(Artikal).get(stavka_data['artikal_id'])
                if artikal:
                    ukupno = artikal.cena * stavka_data['kolicina']
                    stavka = StavkaRacuna(
                        kolicina=stavka_data['kolicina'],
                        cena=artikal.cena,
                        ukupno=ukupno,
                        artikal=artikal,
                        racun=racun
                    )
                    self.session.add(stavka)
                    ukupan_iznos += ukupno
                    
                    # Ažuriraj stanje artikla
                    artikal.kolicina_na_stanju -= stavka_data['kolicina']
            
            # Ažuriraj ukupan iznos računa
            racun.ukupan_iznos = ukupan_iznos
            racun.placen_iznos = ukupan_iznos  # Za sada pretpostavljamo da se plaća ceo iznos
            
            self.session.commit()
            return racun
            
        except Exception as e:
            self.session.rollback()
            raise e
    
    def get_svi_racuni(self):
        """Vrati sve račune sa stavkama"""
        return self.session.query(Racun).all()
    
    def get_racun_po_id(self, racun_id):
        """Vrati račun po ID-u sa stavkama"""
        return self.session.query(Racun).get(racun_id)
