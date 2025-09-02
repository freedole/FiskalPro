from database.models import Session, Racun, Artikal
from datetime import datetime, timedelta
from sqlalchemy import func

class IzvestajiService:
    def __init__(self):
        self.session = Session()
    
    def dnevni_promet(self, datum=None):
        """Izveštaj o dnevnom prometu"""
        if not datum:
            datum = datetime.now().date()
        
        start_date = datetime.combine(datum, datetime.min.time())
        end_date = start_date + timedelta(days=1)
        
        result = self.session.query(
            func.count(Racun.id).label('broj_racuna'),
            func.sum(Racun.ukupan_iznos).label('ukupan_promet')
        ).filter(
            Racun.datum_vreme >= start_date,
            Racun.datum_vreme < end_date
        ).first()
        
        return {
            'datum': datum,
            'broj_racuna': result.broj_racuna or 0,
            'ukupan_promet': result.ukupan_promet or 0.0
        }
    
    def stanje_zaliha(self):
        """Izveštaj o stanju zaliha"""
        artikli = self.session.query(Artikal).all()
        
        ukupna_vrednost = 0
        stanje = []
        
        for artikal in artikli:
            vrednost = artikal.cena * artikal.kolicina_na_stanju
            ukupna_vrednost += vrednost
            
            stanje.append({
                'artikal': artikal.naziv,
                'kolicina': artikal.kolicina_na_stanju,
                'cena': artikal.cena,
                'vrednost': vrednost
            })
        
        return {
            'stanje_artikala': stanje,
            'ukupna_vrednost': ukupna_vrednost
        }
    
    def top_artikli(self, limit=10):
        """Najprodavaniji artikli"""
        result = self.session.query(
            Artikal.naziv,
            func.sum(StavkaRacuna.kolicina).label('ukupna_prodaja'),
            func.sum(StavkaRacuna.ukupno).label('ukupna_vrednost')
        ).join(StavkaRacuna.artikal
        ).group_by(Artikal.id
        ).order_by(func.sum(StavkaRacuna.ukupno).desc()
        ).limit(limit).all()
        
        return [
            {
                'artikal': naziv,
                'prodaja_kolicina': ukupna_prodaja,
                'prodaja_vrednost': ukupna_vrednost
            }
            for naziv, ukupna_prodaja, ukupna_vrednost in result
        ]
