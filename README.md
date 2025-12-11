# 🕶️ Gestão Ótica

Sistema completo de gestão para óticas, desenvolvido para gerenciar ordens de serviço, clientes, graus de lentes e pagamentos.

## 📋 Sobre o Projeto

O **Gestão Ótica** é uma aplicação web desenvolvida para facilitar o gerenciamento de óticas, permitindo o controle completo de ordens de serviço (OS), cadastro de clientes, registro de graus de lentes, acompanhamento de pagamentos e muito mais.

## 🚀 Tecnologias Utilizadas

### Backend
- **Python 3** - Linguagem de programação principal
- **Flask** - Framework web minimalista e poderoso
- **SQLite3** - Banco de dados relacional embutido
- **Threading** - Gerenciamento de threads para abrir navegador automaticamente
- **Logging** - Sistema de logs para rastreamento de erros

### Frontend
- **HTML5** - Estrutura das páginas
- **CSS3** - Estilização customizada
- **JavaScript (ES6+)** - Interatividade e funcionalidades dinâmicas
- **Bootstrap 5** - Framework CSS responsivo para interface moderna

### Build & Deployment
- **PyInstaller** - Empacotamento da aplicação em executável standalone (.exe)

### Bibliotecas Python Adicionais
- `webbrowser` - Abertura automática do navegador
- `json` - Manipulação de dados JSON
- `mimetypes` - Configuração de tipos MIME para arquivos estáticos

## ✨ Funcionalidades

- ✅ **Gestão de Ordens de Serviço (OS)**
  - Criar, editar e excluir ordens de serviço
  - Numeração de OS personalizada
  - Status de pagamento (Pendente/Pago)
  - Visualização detalhada de cada OS
  
- 👥 **Cadastro de Clientes**
  - Nome, telefone, CPF e endereço
  - Histórico completo de compras por cliente
  - Controle de receitas externas e exames feitos na ótica

- 👓 **Registro de Graus**
  - Cadastro detalhado de graus para cada olho (OD/OE)
  - Campos: ESF, CIL, Eixo, Adição, DNP, Índice
  - Tipo de lente (Multifocal, Bifocal, etc.)
  - Suporte para lentes de longe e perto
  - Edição individual de graus

- 💰 **Controle Financeiro**
  - Métodos de pagamento (Dinheiro, Cartão, Pix)
  - Parcelamento para cartão
  - Controle de entrada e valor na retirada
  - Status de pagamento ao laboratório
  - **Pagamentos parciais** com histórico completo

- 💵 **Fluxo de Caixa**
  - Registro de entradas e saídas
  - Categorização de movimentações
  - Cálculo automático de saldo
  - Filtros por tipo, data e categoria
  - Resumo mensal de movimentações
  - Edição e exclusão de movimentações
  - Integração com pagamentos de ordens de serviço

- 📊 **Dashboard e Relatórios**
  - Dashboard com visão geral do negócio
  - Relatórios de vendas e financeiro
  - Filtros por status, loja e busca
  - Exportação de dados (JSON e TXT)
  
- 🎨 **Interface Moderna**
  - Design responsivo e intuitivo
  - Tema claro/escuro
  - Sistema de flash messages para feedback ao usuário
  - Navegação simplificada

## 🛠️ Instalação e Uso

### Pré-requisitos
- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. Clone o repositório ou extraia os arquivos do projeto

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
python main.py
```

4. O navegador abrirá automaticamente em `http://127.0.0.1:5000`

### Executável Windows

Para usar a versão executável (.exe):

1. Execute `GestaoOtica.exe`
2. O sistema iniciará automaticamente e abrirá no navegador
3. Não é necessário instalar Python ou dependências

## 📦 Gerando o Executável

Para gerar um novo executável:

```bash
pyinstaller GestaoOtica_OneFile.spec
```

O executável será gerado na pasta `dist/`.

## 📁 Estrutura do Projeto

```
semi_final/
├── main.py                      # Ponto de entrada da aplicação
├── data.db                      # Banco de dados SQLite (não versionado)
├── requirements.txt             # Dependências Python
├── GestaoOtica_OneFile.spec    # Configuração PyInstaller
├── INICIO_RAPIDO.md            # Guia de início rápido
├── app/                         # Pacote principal da aplicação
│   ├── __init__.py             # Inicialização do app Flask
│   ├── config.py               # Configurações da aplicação
│   ├── utils.py                # Funções utilitárias
│   ├── models/                 # Modelos de dados
│   │   ├── __init__.py         # Conexão com banco de dados
│   │   └── schema.sql          # Schema do banco de dados
│   ├── routes/                 # Rotas da aplicação
│   │   ├── __init__.py         # Registro de blueprints
│   │   ├── main_routes.py      # Rotas principais
│   │   ├── order_routes.py     # Rotas de ordens de serviço
│   │   ├── cashflow_routes.py  # Rotas de fluxo de caixa
│   │   ├── dashboard_routes.py # Rotas do dashboard
│   │   ├── report_routes.py    # Rotas de relatórios
│   │   └── print_routes.py     # Rotas de impressão
│   ├── services/               # Lógica de negócio
│   │   ├── cashflow_service.py # Serviços de fluxo de caixa
│   │   └── report_service.py   # Serviços de relatórios
│   ├── templates/              # Templates HTML
│   │   ├── navbar.html         # Barra de navegação
│   │   ├── index.html          # Lista de ordens de serviço
│   │   ├── form_full.html      # Formulário de OS
│   │   ├── details.html        # Detalhes da OS
│   │   ├── edit_grau.html      # Edição de graus
│   │   ├── cashflow.html       # Fluxo de caixa
│   │   ├── dashboard.html      # Dashboard
│   │   ├── reports.html        # Relatórios
│   │   ├── print_order.html    # Impressão de OS
│   │   └── 500.html            # Página de erro
│   ├── static/                 # Arquivos estáticos
│   │   ├── bootstrap.min.css   # Bootstrap CSS
│   │   ├── bootstrap.bundle.min.js # Bootstrap JS
│   │   ├── custom.css          # Estilos customizados
│   │   └── image/              # Imagens e ícones
│   │       └── logo.ico        # Ícone da aplicação
│   └── migrations/             # Migrações do banco de dados
│       └── *.sql               # Scripts de migração
└── dist/                        # Executáveis gerados (não versionado)
```

## 🗄️ Estrutura do Banco de Dados

### Tabela `orders`
Armazena as ordens de serviço com informações do cliente, pagamento e datas.

**Campos principais:**
- `id`, `os_number`, `client_name`, `phone`, `cpf`, `endereco`
- `purchase_type`, `store`, `lab`, `lab_paid`
- `payment_status`, `payment_method`, `installments`
- `valor_pago`, `entrada`, `valor_retirada`
- `exam_date`, `delivery_date`
- `receita_fora`, `nome_doutor_fora`, `nome_doutor_otica`

### Tabela `graus`
Armazena os graus de lentes associados a cada ordem de serviço.

**Campos principais:**
- `id`, `order_id` (FK)
- `lens_for` (longe/perto), `eye` (OD/OE)
- `esf`, `cil`, `eixo`, `adicao`, `dnp`
- `indice`, `lens_type`

### Tabela `cash_flow`
Registra todas as movimentações financeiras (entradas e saídas).

**Campos principais:**
- `id`, `date`, `type` (entrada/saida)
- `category`, `description`, `amount`
- `payment_method`, `order_id` (FK opcional)
- `created_at`

### Tabela `partial_payments`
Armazena pagamentos parciais de ordens de serviço.

**Campos principais:**
- `id`, `order_id` (FK), `amount`
- `payment_date`, `payment_method`, `notes`
- `cash_flow_id` (FK), `created_at`

## 🔧 Configuração

### Modo Debug
Para desenvolvimento, edite `app/config.py`:
```python
DEBUG = True  # Ativa modo debug
```

### Porta do Servidor
Para alterar a porta padrão (5000), edite `main.py`:
```python
app.run(debug=debug_mode, host='127.0.0.1', port=5000)
```

### Banco de Dados
O banco de dados SQLite (`data.db`) é criado automaticamente na primeira execução. Para resetar o banco, delete o arquivo `data.db` e reinicie a aplicação.

## 📝 Logs

Os erros são registrados automaticamente em `error.log` no diretório da aplicação.

**Nota:** O arquivo `error.log` e o banco de dados `data.db` não são versionados no Git por conterem dados sensíveis.

## 🤝 Contribuindo

Este é um projeto proprietário e **não aceita contribuições externas** no momento.

## 📄 Licença

⚠️ **Software Proprietário** - Todos os direitos reservados.

O uso deste software **requer licença**. Entre em contato para obter autorização de uso.

## 👨‍💻 Autor

Demoro viu.....

---

**Versão:** 2.0  
**Última atualização:** Dezembro 2025
