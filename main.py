from view.app import App
from model.db_access import DbAccess


def main():
    vf = DbAccess()
    vf.create_tables()
    result = vf.user_verify()
    vf.close_connection()
    
    app = App(result)
    app.mainloop()

if __name__ == "__main__":
    main()
