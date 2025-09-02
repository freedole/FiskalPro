def format_km(iznos, decimalna_mjesta=2):
    """
    Formatira iznos u KM sa decimalnim zarezom
    npr: 12.3456 -> "12,35 KM"
    """
    if iznos is None:
        return "0,00 KM"
    
    try:
        zaokruzeno = round(float(iznos), decimalna_mjesta)
        # Formatiraj sa tačkom kao hiljadarkom, pa zamijeni decimalnu tačku zarezom
        formatirano = f"{zaokruzeno:,.{decimalna_mjesta}f}"
        
        # Zamijeni posljednju tačku zarezom (decimalni separator)
        parts = formatirano.split('.')
        if len(parts) == 2:
            # Ako ima decimalni dio
            cijeli_dio = parts[0].replace(',', '.')  # hiljadarke sa tačkama
            return f"{cijeli_dio},{parts[1]} KM"
        else:
            # Ako nema decimalni dio
            return f"{formatirano.replace(',', '.')},00 KM"
            
    except (ValueError, TypeError):
        return "0,00 KM"

def parsiraj_km(km_string):
    """
    Parsira string sa KM u decimalni broj
    npr: "12,35 KM" -> 12.35
    """
    try:
        # Ukloni "KM" i višak spaceova
        broj_str = km_string.replace('KM', '').strip()
        # Zamijeni zarez tačkom i konvertuj u float
        return float(broj_str.replace(',', '.'))
    except (ValueError, AttributeError):
        return 0.0
