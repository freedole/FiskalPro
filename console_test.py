from database.models import Session, Artikal, Kategorija
from modules.core.racun_service import RacunService

def console_menu():
    session = Session()
    racun_service = RacunService()
    
    while True:
        print("\n=== FISKALPRO CONSOLE MENU ===")
        print("1. Prikaži sve artikle")
        print("2. Dodaj novi artikal")
        print("3. Kreiraj račun")
        print("4. Prikaži sve račune")
        print("5. Izlaz")
        
        choice = input("Izbor: ")
        
        if choice == "1":
            artikli = session.query(Artikal).all()
            for a in artikli:
                print(f"{a.id}: {a.naziv} - {a.cena} RSD (Stanje: {a.kolicina_na_stanju})")
                
        elif choice == "2":
            print("\n--- Novi artikal ---")
            naziv = input("Naziv: ")
            cena = float(input("Cena: "))
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
                print(f"{a.id}: {a.naziv} - {a.cena} RSD (Stanje: {a.kolicina_na_stanju})")
            
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
                    print(f"✅ Račun {racun.broj_racuna} kreiran! Iznos: {racun.ukupan_iznos} RSD")
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
                print(f"   Iznos: {r.ukupan_iznos} RSD, Način plaćanja: {r.nacin_placanja}")
                
                for s in r.stavke:
                    print(f"   - {s.artikal.naziv}: {s.kolicina} x {s.cena} = {s.ukupno} RSD")
        
        elif choice == "5":
            break

if __name__ == "__main__":
    console_menu()
