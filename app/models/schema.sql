CREATE TABLE IF NOT EXISTS sellers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    cpf TEXT UNIQUE,
    phone TEXT,
    email TEXT,
    commission_rate REAL DEFAULT 5.0,
    active INTEGER DEFAULT 1,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    os_number TEXT,
    client_name TEXT,
    phone TEXT,
    purchase_type TEXT,
    store TEXT,
    lab TEXT,
    payment_status TEXT,
    payment_method TEXT,
    installments INTEGER,
    lab_paid INTEGER DEFAULT 0,
    exam_date TEXT,
    delivery_date TEXT,
    cpf TEXT,
    receita_fora INTEGER DEFAULT 0,
    nome_doutor_fora TEXT,
    valor_pago REAL DEFAULT 0,
    entrada REAL DEFAULT 0,
    valor_retirada REAL DEFAULT 0,
    nome_doutor_otica TEXT,
    endereco TEXT,
    seller_id INTEGER,
    deleted_at TEXT DEFAULT NULL,
    FOREIGN KEY(seller_id) REFERENCES sellers(id)
);

CREATE TABLE IF NOT EXISTS accounts_payable (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    supplier TEXT,
    amount REAL NOT NULL,
    due_date TEXT NOT NULL,
    payment_date TEXT,
    status TEXT DEFAULT 'Pendente',
    category TEXT,
    notes TEXT,
    order_id INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(order_id) REFERENCES orders(id)
);

CREATE TABLE IF NOT EXISTS accounts_receivable (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    installment_number INTEGER DEFAULT 1,
    total_installments INTEGER DEFAULT 1,
    amount REAL NOT NULL,
    due_date TEXT NOT NULL,
    payment_date TEXT,
    status TEXT DEFAULT 'Pendente',
    payment_method TEXT,
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(order_id) REFERENCES orders(id)
);

CREATE TABLE IF NOT EXISTS cash_flow (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    type TEXT NOT NULL,
    category TEXT,
    description TEXT,
    amount REAL NOT NULL,
    payment_method TEXT,
    order_id INTEGER,
    seller_id INTEGER,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(order_id) REFERENCES orders(id),
    FOREIGN KEY(seller_id) REFERENCES sellers(id)
);

CREATE TABLE IF NOT EXISTS graus (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER,
    lens_for TEXT,
    eye TEXT,
    esf TEXT,
    cil TEXT,
    eixo TEXT,
    dnp TEXT,
    indice TEXT,
    lens_type TEXT,
    adicao TEXT,
    FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS partial_payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    payment_date TEXT NOT NULL,
    payment_method TEXT,
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    cash_flow_id INTEGER,
    FOREIGN KEY(order_id) REFERENCES orders(id) ON DELETE CASCADE
);

-- Tabelas para Sistema de Permissões
CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    is_system INTEGER DEFAULT 0,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resource TEXT NOT NULL,
    action TEXT NOT NULL,
    description TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(resource, action)
);

CREATE TABLE IF NOT EXISTS role_permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(role_id) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY(permission_id) REFERENCES permissions(id) ON DELETE CASCADE,
    UNIQUE(role_id, permission_id)
);

-- Inserir roles padrão (apenas se não existirem)
INSERT OR IGNORE INTO roles (id, name, description, is_system) VALUES 
(1, 'admin', 'Administrador do sistema', 1),
(2, 'gerente', 'Gerente de loja', 0),
(3, 'operador', 'Operador', 0);

-- Inserir permissões padrão
INSERT OR IGNORE INTO permissions (resource, action, description) VALUES 
('orders', 'create', 'Criar nova ordem'),
('orders', 'read', 'Visualizar ordens'),
('orders', 'update', 'Editar ordens'),
('orders', 'delete', 'Deletar ordens'),
('cashflow', 'create', 'Criar movimentação de caixa'),
('cashflow', 'read', 'Visualizar caixa'),
('cashflow', 'update', 'Editar caixa'),
('cashflow', 'delete', 'Deletar caixa'),
('reports', 'read', 'Visualizar relatórios'),
('reports', 'export', 'Exportar relatórios'),
('dashboard', 'read', 'Visualizar dashboard'),
('settings', 'manage', 'Gerenciar configurações'),
('users', 'manage', 'Gerenciar usuários');

