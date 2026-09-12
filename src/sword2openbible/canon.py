"""Mapeamento do cânon protestante para o esquema OpenBible."""

# Mapeamento completo dos 66 livros do cânon protestante
# Estrutura: nome_padrao -> (id, testamento_id, aliases)
PROTESTANT_CANON = {
    # Antigo Testamento (testament_reference_id = 1)
    "Genesis": (1, 1, ["Genesis", "Gen"]),
    "Exodus": (2, 1, ["Exodus", "Exod", "Ex"]),
    "Leviticus": (3, 1, ["Leviticus", "Lev", "Lv"]),
    "Numbers": (4, 1, ["Numbers", "Num", "Nm"]),
    "Deuteronomy": (5, 1, ["Deuteronomy", "Deut", "Dt"]),
    "Joshua": (6, 1, ["Joshua", "Josh", "Jos"]),
    "Judges": (7, 1, ["Judges", "Judg", "Jdg"]),
    "Ruth": (8, 1, ["Ruth", "Rth"]),
    "1 Samuel": (9, 1, ["1 Samuel", "I Samuel", "1Sam", "1 Sam"]),
    "2 Samuel": (10, 1, ["2 Samuel", "II Samuel", "2Sam", "2 Sam"]),
    "1 Kings": (11, 1, ["1 Kings", "I Kings", "1Kgs", "1 Kgs"]),
    "2 Kings": (12, 1, ["2 Kings", "II Kings", "2Kgs", "2 Kgs"]),
    "1 Chronicles": (13, 1, ["1 Chronicles", "I Chronicles", "1Chr", "1 Chr"]),
    "2 Chronicles": (14, 1, ["2 Chronicles", "II Chronicles", "2Chr", "2 Chr"]),
    "Ezra": (15, 1, ["Ezra", "Ezr"]),
    "Nehemiah": (16, 1, ["Nehemiah", "Neh"]),
    "Esther": (17, 1, ["Esther", "Est"]),
    "Job": (18, 1, ["Job"]),
    "Psalms": (19, 1, ["Psalms", "Psalm", "Ps", "Psa"]),
    "Proverbs": (20, 1, ["Proverbs", "Prov", "Prv"]),
    "Ecclesiastes": (21, 1, ["Ecclesiastes", "Eccl", "Ecc"]),
    "Song of Solomon": (22, 1, ["Song of Solomon", "Song of Songs", "Song", "SOS", "Cant"]),
    "Isaiah": (23, 1, ["Isaiah", "Isa"]),
    "Jeremiah": (24, 1, ["Jeremiah", "Jer"]),
    "Lamentations": (25, 1, ["Lamentations", "Lam"]),
    "Ezekiel": (26, 1, ["Ezekiel", "Ezek", "Ezk"]),
    "Daniel": (27, 1, ["Daniel", "Dan"]),
    "Hosea": (28, 1, ["Hosea", "Hos"]),
    "Joel": (29, 1, ["Joel"]),
    "Amos": (30, 1, ["Amos"]),
    "Obadiah": (31, 1, ["Obadiah", "Obad", "Ob"]),
    "Jonah": (32, 1, ["Jonah", "Jon"]),
    "Micah": (33, 1, ["Micah", "Mic"]),
    "Nahum": (34, 1, ["Nahum", "Nah"]),
    "Habakkuk": (35, 1, ["Habakkuk", "Hab"]),
    "Zephaniah": (36, 1, ["Zephaniah", "Zeph", "Zep"]),
    "Haggai": (37, 1, ["Haggai", "Hag"]),
    "Zechariah": (38, 1, ["Zechariah", "Zech", "Zec"]),
    "Malachi": (39, 1, ["Malachi", "Mal"]),
    
    # Novo Testamento (testament_reference_id = 2)
    "Matthew": (40, 2, ["Matthew", "Matt", "Mt"]),
    "Mark": (41, 2, ["Mark", "Mrk", "Mk"]),
    "Luke": (42, 2, ["Luke", "Luk", "Lk"]),
    "John": (43, 2, ["John", "Joh", "Jn"]),
    "Acts": (44, 2, ["Acts", "Act"]),
    "Romans": (45, 2, ["Romans", "Rom"]),
    "1 Corinthians": (46, 2, ["1 Corinthians", "I Corinthians", "1Cor", "1 Cor"]),
    "2 Corinthians": (47, 2, ["2 Corinthians", "II Corinthians", "2Cor", "2 Cor"]),
    "Galatians": (48, 2, ["Galatians", "Gal"]),
    "Ephesians": (49, 2, ["Ephesians", "Eph"]),
    "Philippians": (50, 2, ["Philippians", "Phil"]),
    "Colossians": (51, 2, ["Colossians", "Col"]),
    "1 Thessalonians": (52, 2, ["1 Thessalonians", "I Thessalonians", "1Thess", "1 Thess", "1 Thes"]),
    "2 Thessalonians": (53, 2, ["2 Thessalonians", "II Thessalonians", "2Thess", "2 Thess", "2 Thes"]),
    "1 Timothy": (54, 2, ["1 Timothy", "I Timothy", "1Tim", "1 Tim"]),
    "2 Timothy": (55, 2, ["2 Timothy", "II Timothy", "2Tim", "2 Tim"]),
    "Titus": (56, 2, ["Titus", "Tit"]),
    "Philemon": (57, 2, ["Philemon", "Phlm", "Phm"]),
    "Hebrews": (58, 2, ["Hebrews", "Heb"]),
    "James": (59, 2, ["James", "Jas"]),
    "1 Peter": (60, 2, ["1 Peter", "I Peter", "1Pet", "1 Pet", "1 Pe"]),
    "2 Peter": (61, 2, ["2 Peter", "II Peter", "2Pet", "2 Pet", "2 Pe"]),
    "1 John": (62, 2, ["1 John", "I John", "1Joh", "1 Joh", "1 Jn"]),
    "2 John": (63, 2, ["2 John", "II John", "2Joh", "2 Joh", "2 Jn"]),
    "3 John": (64, 2, ["3 John", "III John", "3Joh", "3 Joh", "3 Jn"]),
    "Jude": (65, 2, ["Jude", "Jud"]),
    "Revelation": (66, 2, ["Revelation", "Revelation of John", "Rev", "Rv"]),
}

# Livros apócrifos (para modo --include-apocrypha)
# IDs começam em 67+
APOCRYPHA_BOOKS = {
    "Tobit": (67, 1, ["Tobit", "Tob"]),
    "Judith": (68, 1, ["Judith", "Jdt"]),
    "Additions to Esther": (69, 1, ["Additions to Esther", "AddEsth"]),
    "Wisdom": (70, 1, ["Wisdom", "Wisdom of Solomon", "Wis"]),
    "Sirach": (71, 1, ["Sirach", "Ecclesiasticus", "Sir"]),
    "Baruch": (72, 1, ["Baruch", "Bar"]),
    "Letter of Jeremiah": (73, 1, ["Letter of Jeremiah", "LetJer", "EpJer"]),
    "Prayer of Azariah": (74, 1, ["Prayer of Azariah", "PrAzar", "Song of the Three Children", "Song of Three"]),
    "Susanna": (75, 1, ["Susanna", "Sus"]),
    "Bel and the Dragon": (76, 1, ["Bel and the Dragon", "Bel"]),
    "1 Maccabees": (77, 1, ["1 Maccabees", "I Maccabees", "1Macc", "1 Macc"]),
    "2 Maccabees": (78, 1, ["2 Maccabees", "II Maccabees", "2Macc", "2 Macc"]),
    "3 Maccabees": (79, 1, ["3 Maccabees", "III Maccabees", "3Macc", "3 Macc"]),
    "4 Maccabees": (80, 1, ["4 Maccabees", "IV Maccabees", "4Macc", "4 Macc"]),
    "1 Esdras": (81, 1, ["1 Esdras", "I Esdras", "1Esd"]),
    "2 Esdras": (82, 1, ["2 Esdras", "II Esdras", "2Esd"]),
    "Prayer of Manasseh": (83, 1, ["Prayer of Manasseh", "Prayer of Manasses", "PrMan"]),
}


def normalize_book_name(sword_name: str) -> str:
    """
    Normaliza o nome de um livro do SWORD para o nome padrão do cânon protestante.
    
    Args:
        sword_name: Nome do livro como retornado pelo SWORD (ex: "I Samuel", "Revelation of John")
    
    Returns:
        Nome normalizado ou None se não for encontrado
    """
    # Remove espaços extras e normaliza
    name = sword_name.strip()
    
    # Busca direta em todas as aliases
    for standard_name, (book_id, testament_id, aliases) in PROTESTANT_CANON.items():
        if name in aliases:
            return standard_name
    
    return None


def get_book_mapping(include_apocrypha: bool = False) -> dict:
    """
    Retorna o mapeamento completo de livros baseado na configuração.
    
    Args:
        include_apocrypha: Se True, inclui os livros apócrifos
    
    Returns:
        Dicionário com nome_padrao -> (id, testament_id, aliases)
    """
    mapping = dict(PROTESTANT_CANON)
    if include_apocrypha:
        mapping.update(APOCRYPHA_BOOKS)
    return mapping


def is_apocrypha(book_name: str) -> bool:
    """
    Verifica se um livro é apócrifo.
    
    Args:
        book_name: Nome do livro (SWORD ou normalizado)
    
    Returns:
        True se o livro for apócrifo
    """
    # Tenta normalizar primeiro
    normalized = normalize_book_name(book_name)
    if normalized:
        return normalized in APOCRYPHA_BOOKS
    
    # Verifica diretamente nos apócrifos
    for standard_name, (book_id, testament_id, aliases) in APOCRYPHA_BOOKS.items():
        if book_name in aliases or book_name == standard_name:
            return True
    
    return False


def get_book_info(book_name: str, include_apocrypha: bool = False) -> tuple:
    """
    Obtém as informações de um livro (ID, testament_id, nome padrão).
    
    Args:
        book_name: Nome do livro (SWORD ou normalizado)
        include_apocrypha: Se True, busca também nos apócrifos
    
    Returns:
        Tupla (book_id, testament_id, standard_name) ou None se não encontrado
    """
    mapping = get_book_mapping(include_apocrypha)
    
    # Tenta normalizar
    normalized = normalize_book_name(book_name)
    if normalized and normalized in mapping:
        book_id, testament_id, aliases = mapping[normalized]
        return (book_id, testament_id, normalized)
    
    # Se inclui apócrifos, busca neles também
    if include_apocrypha:
        for standard_name, (book_id, testament_id, aliases) in APOCRYPHA_BOOKS.items():
            if book_name in aliases or book_name == standard_name:
                return (book_id, testament_id, standard_name)
    
    return None
