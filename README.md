# sword2openbible

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

CLI para converter módulos de bíblias SWORD da CrossWire em bancos de dados SQLite compatíveis com o plugin [OpenBible](https://github.com/open-mission/obsidian-open-bible) para Obsidian.

## Por que este projeto existe?

O OpenBible lê bíblias locais em formato SQLite através do sql.js. Ele **NÃO** lê arquivos `.bzz/.bzv/.bzs` do SWORD nativamente. Este CLI é o pipeline recomendado:

```
Módulo SWORD (ZIP) → sword2openbible → SQLite → OpenBible
```

## Características

- ✅ **Conversão completa**: Processa todos os 66 livros do cânon protestante
- ✅ **Mapeamento inteligente**: Normaliza automaticamente nomes de livros (ex: `I Samuel` → `1 Samuel`, `Revelation of John` → `Revelation`)
- ✅ **Esquema OpenBible**: Gera SQLite no formato exato esperado pelo plugin
- ✅ **Suporte a apócrifos**: Opcionalmente inclui livros deuterocanônicos/apócrifos (IDs 67+)
- ✅ **Texto limpo**: Remove marcação OSIS/Strong's por padrão (configurável)
- ✅ **Múltiplas fontes**: Aceita ZIPs ou diretórios SWORD
- ✅ **Validação robusta**: Verifica 66 livros, reporta estatísticas detalhadas

## Abordagem validada

Este projeto usa a biblioteca [`pysword`](https://pypi.org/project/pysword/) e foi validado com sucesso no módulo **KJVA** (King James Version with Apocrypha) da CrossWire.

O KJVA apresenta desafios específicos:
- Usa numerais romanos (`I Samuel`, `II Kings`, `III John`)
- Nomeia Apocalipse como `Revelation of John`
- Mistura apócrifos na lista do Antigo Testamento

Todos estes casos são tratados corretamente.

## Instalação

### Pré-requisitos

- Python 3.10 ou superior
- pip

### Instalar do repositório

```bash
git clone https://github.com/open-mission/sword2openbible.git
cd sword2openbible
pip install -e .
```

### Instalar para desenvolvimento

```bash
git clone https://github.com/open-mission/sword2openbible.git
cd sword2openbible
pip install -e ".[dev]"
```

## Uso

### Comando básico

```bash
sword2openbible convert KJVA.zip -o bibles_KJVA.sqlite
```

### Especificar módulo explicitamente

Se o ZIP contém múltiplos módulos:

```bash
sword2openbible convert modules.zip --module KJVA -o bibles_KJVA.sqlite
```

### Listar módulos disponíveis

```bash
sword2openbible convert modules.zip --list-modules
```

### Adicionar metadados

```bash
sword2openbible convert KJVA.zip \
  -o bibles_KJVA.sqlite \
  --name "King James Version with Apocrypha" \
  --abbreviation "KJVA" \
  --source "CrossWire" \
  --license "Public Domain"
```

### Incluir livros apócrifos

Por padrão, apenas os 66 livros do cânon protestante são incluídos. Para incluir apócrifos:

```bash
sword2openbible convert KJVA.zip \
  -o bibles_KJVA.sqlite \
  --include-apocrypha
```

**Nota**: O OpenBible atualmente assume o cânon de 66 livros. Livros apócrifos receberão IDs 67+ e podem requerer modificações futuras no plugin para exibição ideal.

### Manter marcação OSIS

Por padrão, tags OSIS e códigos Strong's são removidos. Para mantê-los:

```bash
sword2openbible convert KJVA.zip \
  -o bibles_KJVA.sqlite \
  --keep-markup
```

**Nota**: O OpenBible atualmente espera texto plano. Marcação OSIS pode não renderizar corretamente.

### Usar diretório SWORD local

Além de ZIPs, você pode usar um diretório SWORD existente:

```bash
sword2openbible convert /path/to/sword/datapath -o output.sqlite
```

## Importar no OpenBible

Após converter seu módulo:

1. **Localize o arquivo SQLite gerado** (ex: `bibles_KJVA.sqlite`)

2. **Copie para seu vault Obsidian**:
   - Opção A: Cole na pasta de bíblias configurada no OpenBible
   - Opção B: Cole em qualquer pasta e use o caminho completo

3. **Importe no OpenBible**:
   - Abra Obsidian
   - Vá em Settings → OpenBible → Import
   - Selecione o arquivo `.sqlite`
   - Confirme a importação

4. **Verifique**:
   - Use o comando OpenBible para abrir uma passagem
   - Exemplo: `João 3:16`

## Esquema do banco de dados

O SQLite gerado segue exatamente o esquema esperado pelo OpenBible (`BibleDatabaseService.ts`):

```sql
-- Metadados opcionais
CREATE TABLE metadata (
  key TEXT PRIMARY KEY,
  value TEXT
);

-- Livros da bíblia
CREATE TABLE book (
  id INTEGER PRIMARY KEY,           -- 1-39: AT, 40-66: NT, 67+: Apócrifos
  name TEXT NOT NULL,               -- Nome padrão em inglês
  testament_reference_id INTEGER NOT NULL  -- 1: AT, 2: NT
);

-- Versículos
CREATE TABLE verse (
  book_id INTEGER NOT NULL,
  chapter INTEGER NOT NULL,
  verse INTEGER NOT NULL,
  text TEXT NOT NULL,
  PRIMARY KEY (book_id, chapter, verse)
);
```

### Convenção de nomes

O padrão usado pelo registro de bíblias do OpenBible:

```
bibles_{ABBREVIATION}.sqlite
```

Exemplo: `bibles_KJVA.sqlite`, `bibles_ESV.sqlite`

## Mapeamento do cânon protestante

O conversor mapeia 66 livros padrão:

### Antigo Testamento (IDs 1-39)
Genesis, Exodus, Leviticus, Numbers, Deuteronomy, Joshua, Judges, Ruth, 1 Samuel, 2 Samuel, 1 Kings, 2 Kings, 1 Chronicles, 2 Chronicles, Ezra, Nehemiah, Esther, Job, Psalms, Proverbs, Ecclesiastes, Song of Solomon, Isaiah, Jeremiah, Lamentations, Ezekiel, Daniel, Hosea, Joel, Amos, Obadiah, Jonah, Micah, Nahum, Habakkuk, Zephaniah, Haggai, Zechariah, Malachi

### Novo Testamento (IDs 40-66)
Matthew, Mark, Luke, John, Acts, Romans, 1 Corinthians, 2 Corinthians, Galatians, Ephesians, Philippians, Colossians, 1 Thessalonians, 2 Thessalonians, 1 Timothy, 2 Timothy, Titus, Philemon, Hebrews, James, 1 Peter, 2 Peter, 1 John, 2 John, 3 John, Jude, Revelation

### Normalização automática

O conversor reconhece automaticamente variações:

- **Numerais romanos**: `I Samuel` → `1 Samuel`, `II Kings` → `2 Kings`, `III John` → `3 John`
- **Nomes alternativos**: `Revelation of John` → `Revelation`
- **Abreviações**: `Gen`, `Ex`, `Matt`, `Rev`, etc.

### Livros apócrifos (IDs 67+, com `--include-apocrypha`)

Tobit, Judith, Additions to Esther, Wisdom, Sirach, Baruch, Letter of Jeremiah, Prayer of Azariah, Susanna, Bel and the Dragon, 1 Maccabees, 2 Maccabees, 3 Maccabees, 4 Maccabees, 1 Esdras, 2 Esdras, Prayer of Manasseh

## Obter módulos SWORD

### CrossWire oficial

Baixe módulos de bíblias no [repositório oficial da CrossWire](https://crosswire.org/sword/modules/ModDisp.jsp?modType=Bibles).

### Exemplo: Baixar KJVA

```bash
# Baixar o módulo KJVA
wget https://crosswire.org/ftpmirror/pub/sword/packages/rawzip/KJVA.zip

# Converter
sword2openbible convert KJVA.zip \
  -o bibles_KJVA.sqlite \
  --name "King James Version with Apocrypha" \
  --abbreviation "KJVA"
```

**⚠️ Importante sobre licenças**: Cada módulo SWORD tem sua própria licença (veja `DistributionLicense` no `.conf`). Você é responsável por respeitar os termos de uso, especialmente se planeja distribuir o SQLite convertido. Muitos módulos são de domínio público, mas alguns têm restrições.

## Desenvolvimento

### Executar testes

```bash
pytest
```

### Executar com cobertura

```bash
pytest --cov=sword2openbible --cov-report=html
```

### Estrutura do projeto

```
sword2openbible/
├── src/
│   └── sword2openbible/
│       ├── __init__.py      # Exports públicos
│       ├── canon.py          # Mapeamento do cânon protestante
│       ├── converter.py      # Lógica de conversão SWORD → SQLite
│       └── cli.py            # Interface de linha de comando
├── tests/
│   ├── conftest.py           # Configuração pytest
│   ├── test_canon.py         # Testes de mapeamento de livros
│   └── test_converter.py     # Testes do conversor
├── pyproject.toml            # Configuração do projeto
├── README.md                 # Este arquivo
└── .gitignore
```

## Solução de problemas

### Erro: "Nenhum módulo SWORD encontrado"

- Verifique se o ZIP está corrompido
- Tente extrair manualmente e apontar para o diretório
- Use `--list-modules` para ver o que foi detectado

### Erro: "Múltiplos módulos encontrados"

Use `--module` para especificar qual módulo converter:

```bash
sword2openbible convert modules.zip --list-modules
sword2openbible convert modules.zip --module KJVA -o output.sqlite
```

### Erro: "Esperados 66 livros mas apenas X foram processados"

Possíveis causas:
- Módulo incompleto ou corrompido
- Nomes de livros não reconhecidos (abra uma issue com os nomes)
- Módulo não é uma bíblia completa (ex: apenas NT)

Verifique os "livros não mapeados" no output e abra uma issue se necessário.

### Livros apócrifos não aparecem no OpenBible

O OpenBible atualmente assume 66 livros. Se você usou `--include-apocrypha`, os livros extras estarão no banco mas podem não aparecer na UI do plugin. Isto requer modificações futuras no OpenBible.

## Contribuir

Contribuições são bem-vindas! Por favor:

1. Faça fork do repositório
2. Crie um branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para o branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

### Áreas para contribuição

- Suporte a mais variações de nomes de livros
- Melhorias na detecção de encoding
- Testes com mais módulos SWORD
- Documentação e exemplos
- Integração com o registro oficial de bíblias do OpenBible

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

**Nota**: A licença MIT aplica-se apenas ao código deste conversor. Os módulos SWORD que você converte estão sujeitos às suas próprias licenças, que você deve verificar e respeitar.

## Links relacionados

- [OpenBible Plugin](https://github.com/open-mission/obsidian-open-bible) - Plugin Obsidian para leitura de bíblias
- [CrossWire](https://crosswire.org/) - Projeto SWORD e biblioteca de módulos
- [pysword](https://pypi.org/project/pysword/) - Biblioteca Python para ler módulos SWORD

## Créditos

- Desenvolvido pela comunidade [Open Mission](https://github.com/open-mission)
- Usa [pysword](https://github.com/jasonsperske/pysword) de Jason Sperske
- Inspirado no formato de dados do [OpenBible](https://github.com/open-mission/obsidian-open-bible)

---

**Feito com ❤️ para a comunidade OpenBible**
