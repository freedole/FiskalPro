from database.models import Session, Artikal, Racun, StavkaRacuna

def migrate_to_km():
    session = Session()
    
    print("🔄 Migriram artikle...")
    artikli = session.query(Artikal).all()
    for art in artikli:
        if isinstance(art.cena, float):
            continue  # Već je float
        art.cena = float(art.cena)
    
    print("🔄 Migriram račune...")
    racuni = session.query(Racun).all()
    for racun in racuni:
        racun.ukupan_iznos = float(racun.ukupan_iznos)
        racun.placen_iznos = float(racun.placen_iznos)
    
    print("🔄 Migriram stavke računa...")
    stavke = session.query(StavkaRacuna).all()
    for stavka in stavke:
        stavka.cena = float(stavka.cena)
        stavka.ukupno = float(stavka.ukupno)
    
    session.commit()
    print("✅ Migracija na KM uspješno završena!")

if __name__ == "__main__":
    migrate_to_km()
