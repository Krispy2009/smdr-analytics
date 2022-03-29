import pdb
import sqlite3

db = sqlite3.connect("calls.db")


# "Station Number","CO","Time","Start","Direction","Dialed","Cost","Account Code"


def create():
    if len(check_table_exists()):
        print("table already exists")
        return
    db.execute(
        """
        CREATE TABLE call_logs
            (
                station integer, 
                co number, 
                duration integer, 
                call_start integer, 
                direction text, 
                dialed text, 
                cost real, 
                account_code integer
            )
        """
    )


def check_table_exists():
    c = db.execute(
        """
    SELECT 
        name
    FROM 
        sqlite_schema
    WHERE 
        type ='table' AND 
        name = 'call_logs';
    """
    ).fetchall()
    return c


if __name__ == "__main__":
    create()
