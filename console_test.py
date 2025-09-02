from database.models import Session, Artikal, Kategorija
from modules.core.racun_service import RacunService
from modules.core.izvestaji_service import IzvestajiService

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
            print("\n--- Povraćaj robe ---")
            racuni = racun_service.get_svi_racuni()
            
            if not racuni:
                print("Nema računa u bazi!")
                continue
                
            print("Računi za povraćaj:")
            for r in racuni:
                print(f"{r.id}: {r.broj_racuna} - {r.datum_vreme} - {r.ukupan_iznos} RSD")
            
            try:
                racun_id = int(input("Unesi ID računa: "))
                racun = racun_service.get_racun_po_id(racun_id)
                
                if not racun:
                    print("Račun nije pronađen!")
                    continue
                
                print(f"\nStavke na računu {racun.broj_racuna}:")
                for s in racun.stavke:
                    print(f"{s.artikal_id}: {s.artikal.naziv} - {s.kolicina} kom")
                
                stavke_za_povracaj = []
                while True:
                    art_id = int(input("Unesi ID artikla za povraćaj (0 za kraj): "))
                    if art_id == 0:
                        break
                    kolicina = int(input("Količina za povraćaj: "))
                    stavke_za_povracaj.append({'artikal_id': art_id, 'kolicina': kolicina})
                
                if stavke_za_povracaj:
                    racun = racun_service.povrati_robru(racun_id, stavke_za_povracaj)
                    print(f"✅ Povraćaj uspešno izvršen! Novi iznos računa: {racun.ukupan_iznos} RSD")
                    
            except Exception as e:
                print(f"❌ Greška: {e}")
        
        elif choice == "6":
            print("\n--- Izveštaji ---")
            print("1. Dnevni promet")
            print("2. Stanje zaliha")
            print("3. Top artikli")
            
            sub_choice = input("Izbor izveštaja: ")
            
            if sub_choice == "1":
                promet = izvestaji_service.dnevni_promet()
                print(f"\n📊 Dnevni promet za {promet['datum']}:")
                print(f"   Broj računa: {promet['broj_racuna']}")
                print(f"   Ukupan promet: {promet['ukupan_promet']:.2f} RSD")
                
            elif sub_choice == "2":
                stanje = izvestaji_service.stanje_zaliha()
                print(f"\n📦 Stanje zaliha (ukupna vrednost: {stanje['ukupna_vrednost']:.2f} RSD):")
                for art in stanje['stanje_artikala']:
                    print(f"   {art['artikal']}: {art['kolicina']} kom × {art['cena']} = {art['vrednost']:.2f} RSD")
                    
            elif sub_choice == "3":
                top = izvestaji_service.top_artikli()
                print("\n🏆 Top artikli po prodaji:")
                for i, art in enumerate(top, 1):
                    print(f"   {i}. {art['artikal']}: {art['prodaja_kolicina']} kom ({art['prodaja_vrednost']:.2f} RSD)")
        
        elif choice == "7":
            break

if __name__ == "__main__":
    console_menu()
