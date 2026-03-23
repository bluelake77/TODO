-- 03_triggers.sql

CREATE OR REPLACE TRIGGER trg_todos_set_updated_at
BEFORE UPDATE ON todos
FOR EACH ROW
BEGIN
    :NEW.updated_at := SYSTIMESTAMP;
END;
/
