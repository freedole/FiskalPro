from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

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
    cena = Column(Float, nullable=False)
    barkod = Column(String(20), unique=True)
    kolicina_na_stanju = Column(Integer, default=0)
    kategorija_id = Column(Integer, ForeignKey('kategorije.id'))
    kategorija = relationship("Kategorija", back_populates="artikli")

    def __repr__(self):
        return f"<Artikal(naziv='{self.naziv}', cena={self.cena}, stanje={self.kolicina_na_stanju})>"

# Kreiramo sve tabele
Base.metadata.create_all(engine)

# Pravimo sesiju
Session = sessionmaker(bind=engine)
session = Session()

# DODAJEMO TESTNE PODATKE (nakon create_all i session)
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
