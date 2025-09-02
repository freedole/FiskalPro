from modules.core.racun_service import RacunService
from database.models import Session, Artikal

def test_kreiraj_racun():
    print("🧪 Testiranje kreiranja računa...")
    
    service = RacunService()
    session = Session()
    
    # Prvo proverimo koji artikli postoje u bazi
    artikli = session.query(Artikal).all()
    print("Dostupni artikli:")
    for a in artikli:
        print(f"  {a.id}: {a.naziv} - {a.cena} RSD (Stanje: {a.kolicina_na_stanju})")
    
    # Kreiraj testne stavke za račun
    stavke_data = [
        {'artikal_id': 1, 'kolicina': 2},  # 2 Coca-Cole
        {'artikal_id': 2, 'kolicina': 1},  # 1 Čokolada
    ]
    
    try:
        racun = service.kreiraj_racun(stavke_data)
        print(f"✅ Račun uspešno kreiran! Broj: {racun.broj_racuna}")
        print(f"✅ Ukupan iznos: {racun.ukupan_iznos} RSD")
        
        # Proveri stanje artikala nakon prodaje
        print("\n📊 Stanje artikala nakon prodaje:")
        for a in session.query(Artikal).all():
            print(f"  {a.naziv}: {a.kolicina_na_stanju} komada")
            
    except Exception as e:
        print(f"❌ Greška: {e}")

if __name__ == "__main__":
    test_kreiraj_racun()
