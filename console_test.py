from database.models import Session, Artikal, Kategorija
from modules.core.racun_service import RacunService
from modules.core.izvestaji_service import IzvestajiService
from modules.core.utils import format_km  # DODAJTE OVO

def console_menu():
    session = Session()
    racun_service = RacunService()
    izvestaji_service = IzvestajiService()
    
    while True:
        print("\n=== FISKALPRO CONSOLE MENU ===")
        print("1. Prikaži sve artikle")
        print("2. Dodaj novi artikal")
        print("3. Kreiraj račun")
        print("4. Prikaži sve račune")
        print("5. Povraćaj robe")
        print("6. Izveštaji")
        print("7. Izlaz")
        
        choice = input("Izbor: ")
        
        if choice == "1":
            artikli = session.query(Artikal).all()
            for a in artikli:
                print(f"{a.id}: {a.naziv} - {format_km(a.cena)} (Stanje: {a.kolicina_na_stanju})")
                
        elif choice == "2":
            print("\n--- Novi artikal ---")
            naziv = input("Naziv: ")
            cena = float(input("Cena: ").replace(',', '.'))  # Podrška za decimalni zarez
            kolicina = int(input("Početna količina: "))
            barkod = input("Barkod (opciono): ") or None
            
            kategorija = session.query(Kategorija).first()
            
            novi = Artikal(
                naziv=naziv,
                cena=cena,
                barkod=barkod,
                kolicina_na_stanju=kolicina,
                kategorija=kategorija
            )
            session.add(novi)
            session.commit()
            print("✅ Artikal dodat!")
            
        elif choice == "3":
            print("\n--- Kreiranje računa ---")
            artikli = session.query(Artikal).all()
            
            if not artikli:
                print("Nema artikala u bazi!")
                continue
                
            print("Dostupni artikli:")
            for a in artikli:
                print(f"{a.id}: {a.naziv} - {format_km(a.cena)} (Stanje: {a.kolicina_na_stanju})")
            
            stavke = []
            while True:
                try:
                    art_id = int(input("Unesi ID artikla (0 za kraj): "))
                    if art_id == 0:
                        break
                    kolicina = int(input("Količina: "))
                    
                    stavke.append({'artikal_id': art_id, 'kolicina': kolicina})
                    print("Stavka dodata!")
                    
                except ValueError:
                    print("Neispravan unos!")
            
            if stavke:
                try:
                    racun = racun_service.kreiraj_racun(stavke)
                    print(f"✅ Račun {racun.broj_racuna} kreiran! Iznos: {format_km(racun.ukupan_iznos)}")
                except Exception as e:
                    print(f"❌ Greška: {e}")
        
        elif choice == "4":
            print("\n--- Svi računi ---")
            racuni = racun_service.get_svi_racuni()
            
            if not racuni:
                print("Nema računa u bazi!")
                continue
                
            for r in racuni:
                print(f"\n📄 {r.broj_racuna} - {r.datum_vreme}")
                print(f"   Iznos: {format_km(r.ukupan_iznos)}, Način plaćanja: {r.nacin_placanja}")
                
                for s in r.stavke:
                    print(f"   - {s.artikal.naziv}: {s.kolicina} x {format_km(s.cena)} = {format_km(s.ukupno)}")
        
        # ... ostale opcije (5, 6, 7) sa format_km ...
        
        elif choice == "7":
            break

if __name__ == "__main__":
    console_menu()
