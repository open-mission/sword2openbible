"""Conversor de módulos SWORD para SQLite compatível com OpenBible."""

import sqlite3
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from pysword.modules import SwordModules

from .canon import get_book_info, is_apocrypha


class ConversionError(Exception):
    """Erro durante a conversão."""
    pass


class SwordConverter:
    """Conversor de módulos SWORD para SQLite OpenBible."""
    
    def __init__(
        self,
        sword_path: Path,
        module_name: Optional[str] = None,
        include_apocrypha: bool = False,
        keep_markup: bool = False
    ):
        """
        Inicializa o conversor.
        
        Args:
            sword_path: Caminho para o ZIP ou diretório do SWORD
            module_name: Nome do módulo (ex: "KJVA"). Se None, tenta detectar automaticamente
            include_apocrypha: Se True, inclui livros apócrifos (IDs 67+)
            keep_markup: Se True, mantém marcação OSIS (padrão: limpa com clean=True)
        """
        self.sword_path = Path(sword_path)
        self.module_name = module_name
        self.include_apocrypha = include_apocrypha
        self.keep_markup = keep_markup
        
        # Estatísticas
        self.stats = {
            "books_processed": 0,
            "verses_processed": 0,
            "books_skipped": 0,
            "apocrypha_skipped": 0,
            "unmapped_books": []
        }
        
        # Carregar módulos SWORD
        self.modules = SwordModules(str(sword_path))
        self.modules.parse_modules()
        
        # Detectar módulo se não especificado
        if not self.module_name:
            self.module_name = self._detect_module()
    
    def _detect_module(self) -> str:
        """
        Detecta automaticamente o módulo se houver apenas um disponível.
        
        Returns:
            Nome do módulo detectado
        
        Raises:
            ConversionError: Se não houver módulos ou houver múltiplos módulos
        """
        available = self.list_available_modules()
        if len(available) == 0:
            raise ConversionError(
                f"Nenhum módulo SWORD encontrado em {self.sword_path}"
            )
        if len(available) > 1:
            modules_list = ", ".join(available)
            raise ConversionError(
                f"Múltiplos módulos encontrados: {modules_list}. "
                f"Especifique o módulo com --module"
            )
        return available[0]
    
    def list_available_modules(self) -> List[str]:
        """
        Lista todos os módulos disponíveis no caminho SWORD.
        
        Returns:
            Lista de nomes de módulos
        """
        # Parse modules retorna um dicionário de módulos
        if hasattr(self.modules, 'modules'):
            return list(self.modules.modules.keys())
        return []
    
    def convert(
        self,
        output_path: Path,
        metadata: Optional[Dict[str, str]] = None
    ) -> Dict:
        """
        Converte o módulo SWORD para SQLite OpenBible.
        
        Args:
            output_path: Caminho do arquivo SQLite de saída
            metadata: Metadados opcionais (name, abbreviation, source, license)
        
        Returns:
            Estatísticas da conversão
        
        Raises:
            ConversionError: Em caso de erro durante a conversão
        """
        # Obter a bíblia
        try:
            bible = self.modules.get_bible_from_module(self.module_name)
        except Exception as e:
            raise ConversionError(
                f"Erro ao carregar módulo '{self.module_name}': {e}"
            )
        
        if bible is None:
            raise ConversionError(
                f"Módulo '{self.module_name}' não encontrado ou não é uma bíblia"
            )
        
        # Obter estrutura
        structure = bible.get_structure()
        books = structure.get_books()
        
        # Criar banco de dados
        output_path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(output_path))
        self._create_schema(conn)
        
        try:
            # Inserir metadados
            if metadata:
                self._insert_metadata(conn, metadata)
            
            # Processar livros
            self._process_books(conn, bible, books)
            
            conn.commit()
            
            # Validar resultados
            if self.stats["verses_processed"] == 0:
                raise ConversionError("Nenhum versículo foi processado")
            
            if self.stats["books_processed"] == 0:
                raise ConversionError("Nenhum livro foi processado")
            
            # Verificar se todos os 66 livros protestantes foram encontrados
            if not self.include_apocrypha:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM book WHERE testament_reference_id IN (1, 2)")
                count = cursor.fetchone()[0]
                if count < 66:
                    missing_info = ""
                    if self.stats["unmapped_books"]:
                        missing_info = f" Livros não mapeados: {', '.join(self.stats['unmapped_books'])}"
                    raise ConversionError(
                        f"Esperados 66 livros do cânon protestante, mas apenas {count} foram processados.{missing_info}"
                    )
            
            return self.stats
            
        except Exception as e:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def _create_schema(self, conn: sqlite3.Connection):
        """Cria o esquema OpenBible no banco de dados."""
        cursor = conn.cursor()
        
        # Tabela metadata
        cursor.execute("""
            CREATE TABLE metadata (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        """)
        
        # Tabela book
        cursor.execute("""
            CREATE TABLE book (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                testament_reference_id INTEGER NOT NULL
            )
        """)
        
        # Tabela verse
        cursor.execute("""
            CREATE TABLE verse (
                book_id INTEGER NOT NULL,
                chapter INTEGER NOT NULL,
                verse INTEGER NOT NULL,
                text TEXT NOT NULL,
                PRIMARY KEY (book_id, chapter, verse)
            )
        """)
        
        conn.commit()
    
    def _insert_metadata(self, conn: sqlite3.Connection, metadata: Dict[str, str]):
        """Insere metadados no banco."""
        cursor = conn.cursor()
        for key, value in metadata.items():
            if value:  # Só insere se tiver valor
                cursor.execute(
                    "INSERT INTO metadata (key, value) VALUES (?, ?)",
                    (key, value)
                )
        conn.commit()
    
    def _process_books(self, conn: sqlite3.Connection, bible, books: Dict):
        """
        Processa todos os livros da bíblia.
        
        Args:
            conn: Conexão SQLite
            bible: Objeto SwordBible
            books: Estrutura de livros do SWORD
        """
        cursor = conn.cursor()
        
        # books é um dict com chaves como 'ot', 'nt'
        for testament_key, book_list in books.items():
            for book in book_list:
                book_name = book.name
                
                # Verificar se é apócrifo
                if is_apocrypha(book_name):
                    if not self.include_apocrypha:
                        self.stats["apocrypha_skipped"] += 1
                        continue
                
                # Obter informações do livro
                book_info = get_book_info(book_name, self.include_apocrypha)
                if not book_info:
                    self.stats["unmapped_books"].append(book_name)
                    self.stats["books_skipped"] += 1
                    continue
                
                book_id, testament_id, standard_name = book_info
                
                # Inserir livro
                cursor.execute(
                    "INSERT OR REPLACE INTO book (id, name, testament_reference_id) VALUES (?, ?, ?)",
                    (book_id, standard_name, testament_id)
                )
                
                # Processar versículos
                verses_in_book = self._process_verses(cursor, bible, book_name, book_id)
                
                if verses_in_book > 0:
                    self.stats["books_processed"] += 1
                else:
                    self.stats["books_skipped"] += 1
        
        conn.commit()
    
    def _process_verses(
        self,
        cursor: sqlite3.Cursor,
        bible,
        book_name: str,
        book_id: int
    ) -> int:
        """
        Processa todos os versículos de um livro.
        
        Args:
            cursor: Cursor SQLite
            bible: Objeto SwordBible
            book_name: Nome do livro no SWORD
            book_id: ID do livro no OpenBible
        
        Returns:
            Número de versículos processados
        """
        verse_count = 0
        
        try:
            # Usar get_iter para iterar eficientemente
            # clean=True remove marcação OSIS por padrão
            clean = not self.keep_markup
            
            for verse_data in bible.get_iter(books=[book_name], clean=clean):
                if verse_data:
                    # verse_data é uma tupla (book, chapter, verse, text)
                    _, chapter, verse, text = verse_data
                    
                    if text and text.strip():
                        cursor.execute(
                            "INSERT OR REPLACE INTO verse (book_id, chapter, verse, text) VALUES (?, ?, ?, ?)",
                            (book_id, chapter, verse, text.strip())
                        )
                        verse_count += 1
                        self.stats["verses_processed"] += 1
        
        except Exception as e:
            # Alguns livros podem não ter conteúdo ou causar erros
            # Log mas não falha toda a conversão
            print(f"Aviso: Erro ao processar versículos de {book_name}: {e}")
        
        return verse_count
