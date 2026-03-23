-- 99_drop_all.sql
-- Run only when you need to reset schema objects.

BEGIN
    EXECUTE IMMEDIATE 'DROP TRIGGER trg_todos_set_updated_at';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -4080 THEN
            RAISE;
        END IF;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE todos CASCADE CONSTRAINTS PURGE';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN
            RAISE;
        END IF;
END;
/

BEGIN
    EXECUTE IMMEDIATE 'DROP TABLE categories CASCADE CONSTRAINTS PURGE';
EXCEPTION
    WHEN OTHERS THEN
        IF SQLCODE != -942 THEN
            RAISE;
        END IF;
END;
/
