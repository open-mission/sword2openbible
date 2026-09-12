"""Testes para o mapeamento do cânon protestante."""

import pytest
from sword2openbible.canon import (
    normalize_book_name,
    get_book_info,
    is_apocrypha,
    get_book_mapping,
    PROTESTANT_CANON,
    APOCRYPHA_BOOKS,
)


class TestNormalizeBookName:
    """Testes para normalização de nomes de livros."""
    
    def test_normalize_standard_names(self):
        """Testa normalização de nomes padrão."""
        assert normalize_book_name("Genesis") == "Genesis"
        assert normalize_book_name("Revelation") == "Revelation"
        assert normalize_book_name("Matthew") == "Matthew"
    
    def test_normalize_roman_numerals(self):
        """Testa conversão de numerais romanos para arábicos."""
        # Samuel
        assert normalize_book_name("I Samuel") == "1 Samuel"
        assert normalize_book_name("II Samuel") == "2 Samuel"
        
        # Kings
        assert normalize_book_name("I Kings") == "1 Kings"
        assert normalize_book_name("II Kings") == "2 Kings"
        
        # Chronicles
        assert normalize_book_name("I Chronicles") == "1 Chronicles"
        assert normalize_book_name("II Chronicles") == "2 Chronicles"
        
        # Corinthians
        assert normalize_book_name("I Corinthians") == "1 Corinthians"
        assert normalize_book_name("II Corinthians") == "2 Corinthians"
        
        # Thessalonians
        assert normalize_book_name("I Thessalonians") == "1 Thessalonians"
        assert normalize_book_name("II Thessalonians") == "2 Thessalonians"
        
        # Timothy
        assert normalize_book_name("I Timothy") == "1 Timothy"
        assert normalize_book_name("II Timothy") == "2 Timothy"
        
        # Peter
        assert normalize_book_name("I Peter") == "1 Peter"
        assert normalize_book_name("II Peter") == "2 Peter"
        
        # John
        assert normalize_book_name("I John") == "1 John"
        assert normalize_book_name("II John") == "2 John"
        assert normalize_book_name("III John") == "3 John"
    
    def test_normalize_revelation_of_john(self):
        """Testa o caso especial 'Revelation of John' -> 'Revelation'."""
        assert normalize_book_name("Revelation of John") == "Revelation"
        assert normalize_book_name("Revelation") == "Revelation"
    
    def test_normalize_song_of_solomon(self):
        """Testa 'Song of Solomon' permanece inalterado."""
        assert normalize_book_name("Song of Solomon") == "Song of Solomon"
    
    def test_normalize_abbreviations(self):
        """Testa abreviações comuns."""
        assert normalize_book_name("Gen") == "Genesis"
        assert normalize_book_name("Ex") == "Exodus"
        assert normalize_book_name("Rev") == "Revelation"
        assert normalize_book_name("Matt") == "Matthew"
    
    def test_normalize_unknown_book(self):
        """Testa livro desconhecido retorna None."""
        assert normalize_book_name("Unknown Book") is None
        assert normalize_book_name("Fake Book") is None
    
    def test_normalize_with_whitespace(self):
        """Testa normalização com espaços extras."""
        assert normalize_book_name("  Genesis  ") == "Genesis"
        assert normalize_book_name("I Samuel ") == "1 Samuel"


class TestGetBookInfo:
    """Testes para obtenção de informações de livros."""
    
    def test_get_info_genesis(self):
        """Testa informações de Gênesis."""
        book_id, testament_id, standard_name = get_book_info("Genesis")
        assert book_id == 1
        assert testament_id == 1  # OT
        assert standard_name == "Genesis"
    
    def test_get_info_revelation(self):
        """Testa informações de Apocalipse."""
        book_id, testament_id, standard_name = get_book_info("Revelation of John")
        assert book_id == 66
        assert testament_id == 2  # NT
        assert standard_name == "Revelation"
    
    def test_get_info_roman_numeral(self):
        """Testa com numeral romano."""
        book_id, testament_id, standard_name = get_book_info("I Samuel")
        assert book_id == 9
        assert testament_id == 1
        assert standard_name == "1 Samuel"
    
    def test_get_info_unknown(self):
        """Testa livro desconhecido."""
        assert get_book_info("Unknown Book") is None
    
    def test_get_info_apocrypha_excluded(self):
        """Testa que apócrifos retornam None quando não incluídos."""
        assert get_book_info("Tobit", include_apocrypha=False) is None
        assert get_book_info("1 Maccabees", include_apocrypha=False) is None
    
    def test_get_info_apocrypha_included(self):
        """Testa que apócrifos retornam info quando incluídos."""
        book_id, testament_id, standard_name = get_book_info("Tobit", include_apocrypha=True)
        assert book_id == 67
        assert testament_id == 1
        assert standard_name == "Tobit"
        
        book_id, testament_id, standard_name = get_book_info("I Maccabees", include_apocrypha=True)
        assert book_id == 77
        assert testament_id == 1
        assert standard_name == "1 Maccabees"


class TestIsApocrypha:
    """Testes para verificação de livros apócrifos."""
    
    def test_protestant_books_not_apocrypha(self):
        """Testa que livros protestantes não são apócrifos."""
        assert not is_apocrypha("Genesis")
        assert not is_apocrypha("Revelation")
        assert not is_apocrypha("I Samuel")
        assert not is_apocrypha("Matthew")
    
    def test_apocrypha_books(self):
        """Testa que livros apócrifos são reconhecidos."""
        assert is_apocrypha("Tobit")
        assert is_apocrypha("Judith")
        assert is_apocrypha("Wisdom")
        assert is_apocrypha("Sirach")
        assert is_apocrypha("Baruch")
        assert is_apocrypha("1 Maccabees")
        assert is_apocrypha("2 Maccabees")
        assert is_apocrypha("I Maccabees")
    
    def test_apocrypha_with_roman_numerals(self):
        """Testa apócrifos com numerais romanos."""
        assert is_apocrypha("I Maccabees")
        assert is_apocrypha("II Maccabees")
        assert is_apocrypha("III Maccabees")


class TestGetBookMapping:
    """Testes para obtenção do mapeamento completo."""
    
    def test_mapping_without_apocrypha(self):
        """Testa mapeamento sem apócrifos."""
        mapping = get_book_mapping(include_apocrypha=False)
        assert len(mapping) == 66
        assert "Genesis" in mapping
        assert "Revelation" in mapping
        assert "Tobit" not in mapping
    
    def test_mapping_with_apocrypha(self):
        """Testa mapeamento com apócrifos."""
        mapping = get_book_mapping(include_apocrypha=True)
        assert len(mapping) > 66
        assert "Genesis" in mapping
        assert "Revelation" in mapping
        assert "Tobit" in mapping
        assert "1 Maccabees" in mapping
    
    def test_protestant_canon_has_66_books(self):
        """Testa que o cânon protestante tem exatamente 66 livros."""
        assert len(PROTESTANT_CANON) == 66
    
    def test_testament_ids_correct(self):
        """Testa que os IDs de testamento estão corretos."""
        # OT: 1-39
        genesis_id, genesis_testament, _ = PROTESTANT_CANON["Genesis"]
        assert genesis_id == 1
        assert genesis_testament == 1
        
        malachi_id, malachi_testament, _ = PROTESTANT_CANON["Malachi"]
        assert malachi_id == 39
        assert malachi_testament == 1
        
        # NT: 40-66
        matthew_id, matthew_testament, _ = PROTESTANT_CANON["Matthew"]
        assert matthew_id == 40
        assert matthew_testament == 2
        
        revelation_id, revelation_testament, _ = PROTESTANT_CANON["Revelation"]
        assert revelation_id == 66
        assert revelation_testament == 2
    
    def test_no_duplicate_ids(self):
        """Testa que não há IDs duplicados."""
        all_books = get_book_mapping(include_apocrypha=True)
        ids = [book_id for book_id, _, _ in all_books.values()]
        assert len(ids) == len(set(ids)), "IDs duplicados encontrados"


class TestKJVASpecificCases:
    """Testes para casos específicos do KJVA mencionados na especificação."""
    
    def test_kjva_roman_numerals(self):
        """Testa que numerais romanos do KJVA são mapeados corretamente."""
        # KJVA usa I, II, III
        assert get_book_info("I Samuel")[2] == "1 Samuel"
        assert get_book_info("II Kings")[2] == "2 Kings"
        assert get_book_info("III John")[2] == "3 John"
    
    def test_kjva_revelation_of_john(self):
        """Testa o mapeamento específico de 'Revelation of John'."""
        book_id, testament_id, standard_name = get_book_info("Revelation of John")
        assert book_id == 66
        assert standard_name == "Revelation"
    
    def test_kjva_apocrypha_in_ot_list(self):
        """
        Testa que apócrifos (que KJVA mistura na lista 'ot') são
        corretamente identificados e podem ser filtrados.
        """
        # Tobit estaria na lista 'ot' do KJVA mas deve ser identificado como apócrifo
        assert is_apocrypha("Tobit")
        assert is_apocrypha("Judith")
        assert is_apocrypha("Wisdom")
        
        # E não deve ser incluído por padrão
        assert get_book_info("Tobit", include_apocrypha=False) is None
