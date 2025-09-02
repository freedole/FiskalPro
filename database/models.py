from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime, Numeric  # DODATO
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime  # DODATO

# Kreiramo bazu podataka
engine = create_engine('sqlite:///database.db', echo=True)
Base = declarative_base()

class Kategorija(Base):
    __tablename__ = 'kategorije'
    id = Column(Integer, primary_key=True)
    naziv = Column(String(50), unique=True, nullable=False)
    artikli = relationship("Artikal", back_populates="kategorija")

    def __repr__(self):
        return f"<Kategorija(naziv='{self.naziv}')>"

class Artikal(Base):
    __tablename__ = 'artikli'
    id = Column(Integer, primary_key=True)
    naziv = Column(String(100), nullable=False)
    cena = Column(Numeric(10, 4), nullable=False)  # PROMJENI: 10 cifara, 4 decimale
    barkod = Column(String(20), unique=True)
    kolicina_na_stanju = Column(Integer, default=0)
    kategorija_id = Column(Integer, ForeignKey('kategorije.id'))
    kategorija = relationship("Kategorija", back_populates="artikli")

    def __repr__(self):
        return f"<Artikal(naziv='{self.naziv}', cena={float(self.cena)}, stanje={self.kolicina_na_stanju})>"

class Racun(Base):
    __tablename__ = 'racuni'
    id = Column(Integer, primary_key=True)
    broj_racuna = Column(String(20), unique=True, nullable=False)
    datum_vreme = Column(DateTime, default=datetime.now)
    ukupan_iznos = Column(Numeric(10, 4), default=0.0)  # PROMJENI
    placen_iznos = Column(Numeric(10, 4), default=0.0)  # PROMJENI
    nacin_placanja = Column(String(20), default='gotovina')
    stavke = relationship("StavkaRacuna", back_populates="racun")

    def __repr__(self):
        return f"<Racun(broj={self.broj_racuna}, iznos={float(self.ukupan_iznos)})>"

class StavkaRacuna(Base):
    __tablename__ = 'stavke_racuna'
    id = Column(Integer, primary_key=True)
    kolicina = Column(Integer, nullable=False)
    cena = Column(Numeric(10, 4), nullable=False)  # PROMJENI
    ukupno = Column(Numeric(10, 4), nullable=False)  # PROMJENI
    racun_id = Column(Integer, ForeignKey('racuni.id'))
    artikal_id = Column(Integer, ForeignKey('artikli.id'))
    racun = relationship("Racun", back_populates="stavke")
    artikal = relationship("Artikal")

    def __repr__(self):
        return f"<Stavka(artikal={self.artikal.naziv}, kolicina={self.kolicina})>"

# Pravimo sesiju
Session = sessionmaker(bind=engine)

if __name__ == "__main__":
    # Kreiraj tabele i testne podatke SAMO kada se skripta pokreće direktno
    Base.metadata.create_all(engine)
    session = Session()

    try:
        # Proverimo da li već postoje kategorije da ne bismo duplirali
        if session.query(Kategorija).count() == 0:
            # Kreiramo kategorije
            k1 = Kategorija(naziv="Pića")
            k2 = Kategorija(naziv="Slatkiši")
            k3 = Kategorija(naziv="Mlečni proizvodi")
            
            session.add_all([k1, k2, k3])
            session.commit()
            
            # Kreiramo artikle
            a1 = Artikal(naziv="Coca-Cola 0.5L", cena=150.0, barkod="123456789", kolicina_na_stanju=50, kategorija=k1)
            a2 = Artikal(naziv="Čokolada 100g", cena=200.0, barkod="987654321", kolicina_na_stanju=30, kategorija=k2)
            a3 = Artikal(naziv="Mleko 1L", cena=100.0, barkod="555555555", kolicina_na_stanju=20, kategorija=k3)
            
            session.add_all([a1, a2, a3])
            session.commit()
            print("✓ Testni podaci uspešno dodati u bazu!")
        else:
            print("✓ Baza već sadrži podatke, preskačem dodavanje testnih.")

    except Exception as e:
        session.rollback()
        print(f"✗ Greška pri dodavanju testnih podataka: {e}")
