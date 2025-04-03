# coding: utf-8
from app.extensions import db
from sqlalchemy.inspection import inspect

class BaseModelMixin:
    def to_dict(self, exclude=None):
        if exclude is None:
            exclude = []
        
        mapper = inspect(self.__class__)
        return {
            column.key: getattr(self, column.key)
            for column in mapper.attrs
            if column.key not in exclude
        }

# # 示例排除字段（如密码、内部状态）
# class User(db.Model, BaseModelMixin):
#     def to_dict(self):
#         return super().to_dict(exclude=["password_hash", "_sa_instance_state"])
class GameData(db.Model, BaseModelMixin):
    __tablename__ = 'game_data'

    id = db.Column(db.Integer, primary_key=True)
    yxm = db.Column(db.Text, nullable=False)
    yxlx = db.Column(db.Text)
    zplx = db.Column(db.Text)
    flbq = db.Column(db.Text)
    fsrq = db.Column(db.Text)
    gxrq = db.Column(db.Text)
    st = db.Column(db.Text)
    rzdz = db.Column(db.Text)
    yxbh = db.Column(db.Text)
    wjdx = db.Column(db.Text)
    fms = db.Column(db.Text)
    pf = db.Column(db.Text)
    pfrs = db.Column(db.Text)
    zcyy = db.Column(db.Text)
    cjsj = db.Column(db.Text)
    bz = db.Column(db.Text)
    yxym = db.Column(db.Text)
