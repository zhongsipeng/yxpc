import time
import uuid
from urllib.parse import urljoin
from flask import current_app
from sqlalchemy import Date, Float, Integer, and_, case, cast, func, or_
from app.config.config import config
from app.errors.exceptions import raiseBusinessMsg
from app.models import *
from app.tools.dlpc import build_game_data, output
from app.tools.file import network_path, path_info
def paginate(model, params):
    data = model.query.paginate(
        page=params["page"],
        per_page=params["rows"],
        error_out=False
    )
    result = {
        "data": [user.to_dict() for user in data.items],
        "total": data.total,
        "page": data.page,
        "rows": data.per_page,
    }
    return result
def filter_dict_by_model(model, data_dict):
    """根据模型字段过滤字典，只保留模型定义的字段"""
    model_fields = {column.name for column in model.__table__.columns}
    return {k: v for k, v in data_dict.items() if k in model_fields}
class GameService:
    @staticmethod
    def game_data_query_all(*columns):
        
        
        results = GameData.query.with_entities(
            *(getattr(GameData, col) for col in columns)
        ).all()
        return results
        
    @staticmethod
    def game_data_query(params):
        query = GameData.query
        if "yxm" in params and params["yxm"]:
            query = query.filter(or_(
                GameData.yxm.ilike( f'%{params["yxm"]}%' ),
                GameData.yxym.ilike( f'%{params["yxm"]}%' )
            ))
        if "flbq" in params and params["flbq"]:
            query = query.filter( GameData.flbq.ilike( f'%{params["flbq"]}%' ) )
        if "yxlx" in params and params["yxlx"]:
            query = query.filter( GameData.yxlx == params["yxlx"] )
        if "st" in params and params["st"]:
            query = query.filter( GameData.st == params["st"] )
        if "fsrq" in params and params["fsrq"]:
            start_date, end_date = params["fsrq"].split(",")
            query = query.filter(
                and_(
                    GameData.fsrq != None,
                    GameData.fsrq != "",
                    func.date(
                        func.substr(GameData.fsrq, 1, 4) + '-' +
                        func.substr(GameData.fsrq, 6, 2) + '-' +
                        func.substr(GameData.fsrq, 9, 2)
                    ).between(start_date, end_date)
                )
            )
        order_rules= []
        if "pxfs" in params and isinstance(params["pxfs"], list):
            for key in params["pxfs"]:
                field = getattr(GameData, key, None)
                match key:
                    case 'fms': 
                        order_rules.append(cast(field, Integer).desc())
                        break
                    case 'pf' : 
                        order_rules.append(cast(field, Float).desc())
                        break
                    case 'fsrq':
                        order_rules.append(func.date(
                            func.substr(field, 1, 4) + '-' +
                            func.substr(field, 6, 2) + '-' +
                            func.substr(field, 9, 2)
                        ).desc())
                        break
                    
            
        # 设置默认值（如果 params 中没有该键或值为 None/空）
        page = params.get("page", 1)  # 默认第1页
        rows = params.get("rows", 10)  # 默认每页10条
        # 转换为整数（如果传入的是字符串）
        try:
            page = int(page)
            rows = int(rows)
        except (ValueError, TypeError):
            page = 1
            rows = 10
        data = query.order_by(*order_rules).paginate(
            page = page,
            per_page = rows,
            error_out = False
        )
        result = {
            "data": [game.to_dict() for game in data.items],
            "total": data.total,
            "page": data.page,
            "rows": data.per_page,
        }
        return result
    
    @staticmethod
    def game_data_merge(game_data):
        
        game = GameData(**filter_dict_by_model(GameData, game_data))

        try:
            merged_obj = db.session.merge(game)
            db.session.commit()

            if not merged_obj:
                raiseBusinessMsg("合并失败")

            insp = inspect(merged_obj)
            if not insp.persistent:
                raise RuntimeError("对象未持久化")

        except Exception as e:
            db.session.rollback()
            print(f"操作失败: {str(e)}")
    @staticmethod
    def game_data_delete(ids):
        
        try:
            deleted_count = db.session.query(GameData)\
                .filter(GameData.id.in_(ids))\
                .delete(synchronize_session='fetch')
            # game = GameData.query.get(id)
            if deleted_count != len(ids):
                db.session.rollback()
                raise ValueError(f"成功删除 {deleted_count} 条，但有 {len(ids)-deleted_count} 条数据不存在")
            
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    @staticmethod
    def game_data_reload(params):
        pass
    @staticmethod
    def game_data_update_by_yxbh(yxbh):
        if not yxbh:
            raiseBusinessMsg("数据有误！")
        data = build_game_data(yxbh)
        data["cjsj"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        try:
            db.session.query(GameData).filter(
                GameData.yxbh == yxbh
            ).update(data)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e
    @staticmethod
    def game_data_output():
        template_path = config.TEMPLATE_FOLDER / "游戏.xlsx"
        output_path =  config.DATE_TEMP_FOLDER /  f"{uuid.uuid4()}.xlsx"

        data = GameService.game_data_query_all("yxm", "yxlx", "zplx", "flbq", "fsrq", "gxrq", "st", "rzdz")
        output(template_path, output_path, data)
        return {
            "url": network_path(output_path)
        }
            
    @staticmethod
    def test():
        r = []
        data = GameData.query.all()
        for game in data:
            parts = game.yxm.split(" | ")
            if len(parts) == 2:
                game.yxm, game.yxym = parts
            
        db.session.commit()
        pass
        
    