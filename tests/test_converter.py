"""Testes para o conversor SWORD."""

import pytest
import sqlite3
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch

from sword2openbible.converter import SwordConverter, ConversionError


class TestSwordConverter:
    """Testes para a classe SwordConverter."""
    
    @patch('sword2openbible.converter.SwordModules')
    def test_init_with_module_name(self, mock_modules_class):
        """Testa inicialização com nome de módulo especificado."""
        mock_modules = Mock()
        mock_modules_class.return_value = mock_modules
        
        converter = SwordConverter(
            sword_path=Path("/fake/path.zip"),
            module_name="KJVA"
        )
        
        assert converter.module_name == "KJVA"
        assert converter.include_apocrypha is False
        assert converter.keep_markup is False
        mock_modules.parse_modules.assert_called_once()
    
    @patch('sword2openbible.converter.SwordModules')
    def test_init_auto_detect_single_module(self, mock_modules_class):
        """Testa auto-detecção quando há apenas um módulo."""
        mock_modules = Mock()
        mock_modules.modules = {"KJVA": Mock()}
        mock_modules_class.return_value = mock_modules
        
        converter = SwordConverter(sword_path=Path("/fake/path.zip"))
        
        assert converter.module_name == "KJVA"
    
    @patch('sword2openbible.converter.SwordModules')
    def test_init_auto_detect_multiple_modules_fails(self, mock_modules_class):
        """Testa que auto-detecção falha com múltiplos módulos."""
        mock_modules = Mock()
        mock_modules.modules = {"KJVA": Mock(), "ESV": Mock()}
        mock_modules_class.return_value = mock_modules
        
        with pytest.raises(ConversionError, match="Múltiplos módulos"):
            SwordConverter(sword_path=Path("/fake/path.zip"))
    
    @patch('sword2openbible.converter.SwordModules')
    def test_init_auto_detect_no_modules_fails(self, mock_modules_class):
        """Testa que auto-detecção falha sem módulos."""
        mock_modules = Mock()
        mock_modules.modules = {}
        mock_modules_class.return_value = mock_modules
        
        with pytest.raises(ConversionError, match="Nenhum módulo"):
            SwordConverter(sword_path=Path("/fake/path.zip"))
    
    @patch('sword2openbible.converter.SwordModules')
    def test_list_available_modules(self, mock_modules_class):
        """Testa listagem de módulos disponíveis."""
        mock_modules = Mock()
        mock_modules.modules = {"KJVA": Mock(), "ESV": Mock(), "NIV": Mock()}
        mock_modules_class.return_value = mock_modules
        
        converter = SwordConverter(
            sword_path=Path("/fake/path.zip"),
            module_name="KJVA"
        )
        
        available = converter.list_available_modules()
        assert set(available) == {"KJVA", "ESV", "NIV"}


class TestSQLiteSchema:
    """Testes para o esquema SQLite gerado."""
    
    def test_create_schema(self, tmp_path):
        """Testa criação do esquema OpenBible."""
        db_path = tmp_path / "test.sqlite"
        conn = sqlite3.connect(str(db_path))
        
        # Usar o método diretamente
        with patch('sword2openbible.converter.SwordModules'):
            converter = SwordConverter(
                sword_path=Path("/fake"),
                module_name="TEST"
            )
            converter._create_schema(conn)
        
        cursor = conn.cursor()
        
        # Verificar tabela metadata
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='metadata'")
        assert cursor.fetchone() is not None
        
        cursor.execute("PRAGMA table_info(metadata)")
        columns = {row[1]: row[2] for row in cursor.fetchall()}
        assert columns == {"key": "TEXT", "value": "TEXT"}
        
        # Verificar tabela book
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='book'")
        assert cursor.fetchone() is not None
        
        cursor.execute("PRAGMA table_info(book)")
        columns = {row[1]: row[2] for row in cursor.fetchall()}
        assert "id" in columns
        assert "name" in columns
        assert "testament_reference_id" in columns
        
        # Verificar tabela verse
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='verse'")
        assert cursor.fetchone() is not None
        
        cursor.execute("PRAGMA table_info(verse)")
        columns = {row[1]: row[2] for row in cursor.fetchall()}
        assert "book_id" in columns
        assert "chapter" in columns
        assert "verse" in columns
        assert "text" in columns
        
        conn.close()
    
    def test_insert_metadata(self, tmp_path):
        """Testa inserção de metadados."""
        db_path = tmp_path / "test.sqlite"
        conn = sqlite3.connect(str(db_path))
        
        with patch('sword2openbible.converter.SwordModules'):
            converter = SwordConverter(
                sword_path=Path("/fake"),
                module_name="TEST"
            )
            converter._create_schema(conn)
            
            metadata = {
                "name": "Test Bible",
                "abbreviation": "TEST",
                "source": "Test Source",
                "license": "Public Domain"
            }
            converter._insert_metadata(conn, metadata)
        
        cursor = conn.cursor()
        cursor.execute("SELECT key, value FROM metadata ORDER BY key")
        rows = cursor.fetchall()
        
        assert len(rows) == 4
        assert dict(rows) == metadata
        
        conn.close()


class TestBookNameNormalization:
    """Testes integrados de normalização de nomes de livros."""
    
    def test_normalize_i_samuel_to_1_samuel(self):
        """Testa caso crítico: 'I Samuel' -> id 9, '1 Samuel'."""
        from sword2openbible.canon import get_book_info
        
        book_id, testament_id, standard_name = get_book_info("I Samuel")
        
        assert book_id == 9
        assert testament_id == 1
        assert standard_name == "1 Samuel"
    
    def test_normalize_revelation_of_john(self):
        """Testa caso crítico: 'Revelation of John' -> id 66, 'Revelation'."""
        from sword2openbible.canon import get_book_info
        
        book_id, testament_id, standard_name = get_book_info("Revelation of John")
        
        assert book_id == 66
        assert testament_id == 2
        assert standard_name == "Revelation"


class TestApocryphaHandling:
    """Testes para manipulação de livros apócrifos."""
    
    @patch('sword2openbible.converter.SwordModules')
    def test_apocrypha_skipped_by_default(self, mock_modules_class):
        """Testa que apócrifos são omitidos por padrão."""
        mock_modules = Mock()
        mock_modules.modules = {"TEST": Mock()}
        mock_modules_class.return_value = mock_modules
        
        converter = SwordConverter(
            sword_path=Path("/fake"),
            module_name="TEST",
            include_apocrypha=False
        )
        
        from sword2openbible.canon import is_apocrypha
        
        # Tobit deve ser identificado como apócrifo
        assert is_apocrypha("Tobit")
        
        # E não deve ter mapeamento quando apócrifos não são incluídos
        from sword2openbible.canon import get_book_info
        assert get_book_info("Tobit", include_apocrypha=False) is None
    
    @patch('sword2openbible.converter.SwordModules')
    def test_apocrypha_included_when_requested(self, mock_modules_class):
        """Testa que apócrifos são incluídos quando solicitado."""
        mock_modules = Mock()
        mock_modules.modules = {"TEST": Mock()}
        mock_modules_class.return_value = mock_modules
        
        converter = SwordConverter(
            sword_path=Path("/fake"),
            module_name="TEST",
            include_apocrypha=True
        )
        
        from sword2openbible.canon import get_book_info
        
        # Tobit deve ter mapeamento quando incluído
        book_info = get_book_info("Tobit", include_apocrypha=True)
        assert book_info is not None
        assert book_info[0] == 67  # ID >= 67 para apócrifos


class TestConversionStats:
    """Testes para estatísticas de conversão."""
    
    @patch('sword2openbible.converter.SwordModules')
    def test_stats_initialization(self, mock_modules_class):
        """Testa que estatísticas são inicializadas corretamente."""
        mock_modules = Mock()
        mock_modules.modules = {"TEST": Mock()}
        mock_modules_class.return_value = mock_modules
        
        converter = SwordConverter(
            sword_path=Path("/fake"),
            module_name="TEST"
        )
        
        assert converter.stats["books_processed"] == 0
        assert converter.stats["verses_processed"] == 0
        assert converter.stats["books_skipped"] == 0
        assert converter.stats["apocrypha_skipped"] == 0
        assert converter.stats["unmapped_books"] == []
