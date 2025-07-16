-- Сущность: "Группа кредиторов от предпринимательской деятельности"
CREATE TABLE IF NOT EXISTS creditors_from_entrepreneurship (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id TEXT NOT NULL,
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (message_id) REFERENCES extrajudicial_bankruptcy_message(id) ON DELETE CASCADE
);

-- Сущность: "Группа кредиторов не от предпринимательской деятельности"
CREATE TABLE IF NOT EXISTS creditors_non_from_entrepreneurship (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id TEXT NOT NULL,
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (message_id) REFERENCES extrajudicial_bankruptcy_message(id) ON DELETE CASCADE
);

-- Сущность: "Обязательные платежи от предпринимательской деятельности"
CREATE TABLE IF NOT EXISTS obligatory_payments_from_entrepreneurship (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    creditor_from_id INTEGER NOT NULL,
    name TEXT,
    sum REAL,
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (creditor_from_id) REFERENCES creditors_from_entrepreneurship(id) ON DELETE CASCADE
);

-- Сущность: "Обязательные платежи не от предпринимательской деятельности"
CREATE TABLE IF NOT EXISTS obligatory_payments_non_from_entrepreneurship (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    creditor_non_id INTEGER NOT NULL,
    name TEXT,
    sum REAL,
    penalty_sum REAL,
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (creditor_non_id) REFERENCES creditors_non_from_entrepreneurship(id) ON DELETE CASCADE
);

-- Сущность: "Денежные обязательства"
CREATE TABLE IF NOT EXISTS monetary_obligations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    creditor_non_id INTEGER NOT NULL,
    creditor_name TEXT,
    content TEXT,
    basis TEXT,
    total_sum REAL,
    debt_sum REAL,
    penalty_sum REAL,
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (creditor_non_id) REFERENCES creditors_non_from_entrepreneurship(id) ON DELETE CASCADE
);

-- Сущность: "Банк"
CREATE TABLE IF NOT EXISTS bank (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    bik TEXT,
    created_at DATETIME,
    updated_at DATETIME
);

-- Сущность-связка M-t-M: "Внесудебное сообщение о банкротстве при участии Банков"
CREATE TABLE IF NOT EXISTS extrajudicial_bankruptcy_message_bank (
    message_id TEXT NOT NULL,
    bank_id INTEGER NOT NULL,
    created_at DATETIME,
    updated_at DATETIME,
    PRIMARY KEY (message_id, bank_id),
    FOREIGN KEY (message_id) REFERENCES extrajudicial_bankruptcy_message(id) ON DELETE CASCADE,
    FOREIGN KEY (bank_id) REFERENCES bank(id) ON DELETE CASCADE
);

-- Сущность: "Должник"
CREATE TABLE IF NOT EXISTS debtor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    birth_date DATE,
    birth_place TEXT,
    inn TEXT UNIQUE,
    snils TEXT UNIQUE,
    created_at DATETIME,
    updated_at DATETIME
);

-- Сущность: "Адрес"
CREATE TABLE IF NOT EXISTS address (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    debtor_id INTEGER UNIQUE,
    full_address TEXT,
    postal_code TEXT,
    region TEXT,
    district TEXT,
    settlement  TEXT,
    street TEXT,
    building TEXT,
    apartment TEXT,
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (debtor_id) REFERENCES debtor(id) ON DELETE CASCADE
);

-- Сущность: "Прошлые наименования"
CREATE TABLE IF NOT EXISTS previous_name (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    value TEXT UNIQUE NOT NULL,
    created_at DATETIME,
    updated_at DATETIME
);

-- Сущность-связка M-t-M: "Прошлые наименования должников"
CREATE TABLE IF NOT EXISTS debtor_previous_name (
    debtor_id INTEGER NOT NULL,
    previous_name_id INTEGER NOT NULL,
    created_at DATETIME,
    updated_at DATETIME,
    PRIMARY KEY (debtor_id, previous_name_id),
    FOREIGN KEY (debtor_id) REFERENCES debtor(id) ON DELETE CASCADE,
    FOREIGN KEY (previous_name_id) REFERENCES previous_name(id) ON DELETE CASCADE
);

-- Сущность "Издатель"
CREATE TABLE IF NOT EXISTS publisher (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    inn TEXT UNIQUE NOT NULL,
    name TEXT UNIQUE NOT NULL,
    ogrn TEXT UNIQUE NOT NULL,
    created_at DATETIME,
    updated_at DATETIME
);

-- Сущность "Тип сообщения о внесудебном банкротстве"
CREATE TABLE IF NOT EXISTS message_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT UNIQUE NOT NULL,
    created_at DATETIME,
    updated_at DATETIME
);

-- Сущность "Сообщение о внесудебном банкротстве"
CREATE TABLE IF NOT EXISTS extrajudicial_bankruptcy_message (
    id TEXT PRIMARY KEY,
    number TEXT UNIQUE,
    type_id INTEGER,
    publish_date TEXT,
    finish_reason TEXT,
    publisher_id INTEGER,
    debtor_id INTEGER,
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (type_id) REFERENCES message_types(id),
    FOREIGN KEY (publisher_id) REFERENCES publisher(id),
    FOREIGN KEY (debtor_id) REFERENCES debtor(id)
);
