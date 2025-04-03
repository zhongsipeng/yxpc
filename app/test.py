from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

engine = create_engine('sqlite:///instance/database.db')
Base = automap_base()
Base.prepare(engine, reflect=True)

print(Base.classes.game_data)
# 访问生成的类
User = Base.classes.game_data
# flask-sqlacodegen sqlite:///instance/database.db --outfile models.py --flask
