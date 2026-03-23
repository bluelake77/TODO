-- 02_constraints_indexes.sql

ALTER TABLE categories
    ADD CONSTRAINT uq_categories_name UNIQUE (name);

ALTER TABLE categories
    ADD CONSTRAINT ck_categories_color_hex
    CHECK (REGEXP_LIKE(color, '^#[0-9A-Fa-f]{6}$'));

ALTER TABLE todos
    ADD CONSTRAINT ck_todos_completed
    CHECK (completed IN (0, 1));

ALTER TABLE todos
    ADD CONSTRAINT ck_todos_priority
    CHECK (priority IN (1, 2, 3));

ALTER TABLE todos
    ADD CONSTRAINT fk_todos_category
    FOREIGN KEY (category_id)
    REFERENCES categories (id)
    ON DELETE SET NULL;

CREATE INDEX ix_todos_created_at ON todos (created_at);
CREATE INDEX ix_todos_category_id ON todos (category_id);
CREATE INDEX ix_todos_completed ON todos (completed);
CREATE INDEX ix_todos_priority ON todos (priority);
