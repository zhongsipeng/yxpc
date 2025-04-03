from app.extensions import db
# from sqlalchemy import text 

# def querySQL(sql: str, db_name: str = "DB", params: dict[str: int | str] = None, page: int = None, rows: int = None) -> dict:
#     result = {}
#     db = getDB(db_name)
#     count = len([i for i in db.session.execute(text(sql), params)])
#     if (page != None and rows != None):
#         sql = f'select * from ({sql}) limit {rows} offset {(page-1) * 10}'
#         result["pages"] = page
#         result["rows"] = rows
#     data = db.session.execute(text(sql), params)
#     result["data"] = [list(item) for item in data]
#     result["count"] = count
#     return result

# def getDB(db_name: str):
#     return db