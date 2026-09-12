"""Interface de linha de comando para sword2openbible."""

import argparse
import sys
from pathlib import Path
from typing import Optional

from .converter import SwordConverter, ConversionError


def create_parser() -> argparse.ArgumentParser:
    """Cria o parser de argumentos CLI."""
    parser = argparse.ArgumentParser(
        prog="sword2openbible",
        description="Converte módulos SWORD da CrossWire em bancos de dados SQLite compatíveis com OpenBible",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos:
  # Converter um módulo ZIP
  sword2openbible convert KJVA.zip -o bibles_KJVA.sqlite
  
  # Especificar módulo explicitamente
  sword2openbible convert modules.zip --module KJVA -o bibles_KJVA.sqlite
  
  # Incluir livros apócrifos
  sword2openbible convert KJVA.zip -o bibles_KJVA.sqlite --include-apocrypha
  
  # Listar módulos disponíveis
  sword2openbible convert modules.zip --list-modules
  
  # Usar um diretório SWORD local
  sword2openbible convert /path/to/sword/datapath -o output.sqlite

Para mais informações: https://github.com/open-mission/sword2openbible
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Comando a executar")
    
    # Comando convert
    convert_parser = subparsers.add_parser(
        "convert",
        help="Converte um módulo SWORD para SQLite OpenBible",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    convert_parser.add_argument(
        "sword_path",
        type=str,
        help="Caminho para o ZIP do SWORD ou diretório datapath"
    )
    
    convert_parser.add_argument(
        "-o", "--output",
        type=str,
        help="Caminho do arquivo SQLite de saída (ex: bibles_KJVA.sqlite)"
    )
    
    convert_parser.add_argument(
        "--module",
        type=str,
        help="Nome do módulo SWORD (ex: KJVA). Auto-detectado se apenas um módulo estiver disponível"
    )
    
    convert_parser.add_argument(
        "--abbreviation",
        type=str,
        help="Abreviação da tradução para metadados (ex: KJVA)"
    )
    
    convert_parser.add_argument(
        "--name",
        type=str,
        help="Nome completo da tradução para metadados (ex: 'King James Version with Apocrypha')"
    )
    
    convert_parser.add_argument(
        "--source",
        type=str,
        help="Fonte/origem da tradução para metadados"
    )
    
    convert_parser.add_argument(
        "--license",
        type=str,
        help="Licença da tradução para metadados"
    )
    
    convert_parser.add_argument(
        "--include-apocrypha",
        action="store_true",
        help="Inclui livros apócrifos (IDs 67+). Requer suporte futuro no OpenBible"
    )
    
    convert_parser.add_argument(
        "--keep-markup",
        action="store_true",
        help="Mantém marcação OSIS/Strong's no texto. Padrão: limpa para texto plano"
    )
    
    convert_parser.add_argument(
        "--list-modules",
        action="store_true",
        help="Lista módulos disponíveis no caminho SWORD e sai"
    )
    
    return parser


def list_modules(sword_path: str) -> int:
    """
    Lista os módulos disponíveis em um caminho SWORD.
    
    Args:
        sword_path: Caminho para o ZIP ou diretório
    
    Returns:
        Código de saída
    """
    try:
        from pysword.modules import SwordModules
        
        modules = SwordModules(sword_path)
        modules.parse_modules()
        
        available = []
        if hasattr(modules, 'modules'):
            available = list(modules.modules.keys())
        
        if not available:
            print(f"❌ Nenhum módulo encontrado em: {sword_path}")
            return 1
        
        print(f"📚 Módulos disponíveis em {sword_path}:")
        for module_name in available:
            print(f"  • {module_name}")
        
        return 0
        
    except Exception as e:
        print(f"❌ Erro ao listar módulos: {e}", file=sys.stderr)
        return 1


def convert_command(args: argparse.Namespace) -> int:
    """
    Executa o comando de conversão.
    
    Args:
        args: Argumentos parseados
    
    Returns:
        Código de saída (0 = sucesso)
    """
    # Verificar se é apenas listagem
    if args.list_modules:
        return list_modules(args.sword_path)
    
    # Validar argumentos
    sword_path = Path(args.sword_path)
    if not sword_path.exists():
        print(f"❌ Erro: Caminho não encontrado: {sword_path}", file=sys.stderr)
        return 1
    
    if not args.output:
        print("❌ Erro: Argumento --output é obrigatório", file=sys.stderr)
        print("Exemplo: sword2openbible convert module.zip -o bibles_KJVA.sqlite", file=sys.stderr)
        return 1
    
    output_path = Path(args.output)
    
    # Preparar metadados
    metadata = {}
    if args.name:
        metadata["name"] = args.name
    if args.abbreviation:
        metadata["abbreviation"] = args.abbreviation
    if args.source:
        metadata["source"] = args.source
    if args.license:
        metadata["license"] = args.license
    
    # Executar conversão
    try:
        print(f"🔄 Iniciando conversão...")
        print(f"   Origem: {sword_path}")
        if args.module:
            print(f"   Módulo: {args.module}")
        print(f"   Destino: {output_path}")
        print()
        
        converter = SwordConverter(
            sword_path=sword_path,
            module_name=args.module,
            include_apocrypha=args.include_apocrypha,
            keep_markup=args.keep_markup
        )
        
        print(f"📖 Módulo detectado: {converter.module_name}")
        
        stats = converter.convert(
            output_path=output_path,
            metadata=metadata
        )
        
        # Exibir resultados
        print()
        print("✅ Conversão concluída com sucesso!")
        print()
        print("📊 Estatísticas:")
        print(f"   • Livros processados: {stats['books_processed']}")
        print(f"   • Versículos processados: {stats['verses_processed']}")
        
        if stats['apocrypha_skipped'] > 0:
            print(f"   • Apócrifos omitidos: {stats['apocrypha_skipped']}")
            print(f"     (Use --include-apocrypha para incluí-los)")
        
        if stats['books_skipped'] > 0:
            print(f"   • Livros ignorados: {stats['books_skipped']}")
        
        if stats['unmapped_books']:
            print(f"   • Livros não mapeados: {', '.join(stats['unmapped_books'])}")
        
        print()
        print(f"💾 Arquivo criado: {output_path}")
        print()
        print("📝 Próximos passos:")
        print("   1. Copie o arquivo .sqlite para a pasta de bíblias do seu vault Obsidian")
        print("   2. No OpenBible, vá em Settings → Import → selecione o arquivo")
        print("   3. Verifique os direitos de distribuição conforme a licença do módulo")
        
        return 0
        
    except ConversionError as e:
        print(f"❌ Erro na conversão: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ Erro inesperado: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


def main() -> int:
    """Ponto de entrada principal do CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    if args.command == "convert":
        return convert_command(args)
    
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
