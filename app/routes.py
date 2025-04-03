
from flask import send_file, send_from_directory, Blueprint, Response, current_app, json, jsonify, request
from app.services.game import GameService
from app.tools.json import validate_json
from app.tools.resultmodel import successModel, failModel
from flasgger import swag_from
from app.config.config import config
bp = Blueprint('main', __name__)


@bp.route('/test', methods=['POST'])
# @validate_json(template={"a": "String"})
def test():
    GameService.test()
    return "1"
@bp.route('/file/<path:filename>')
def file_download(filename):
    return send_from_directory(
        directory=config.FILE_PATH,
        path=filename,
        as_attachment=True
    )
# '''
# 查询接口
# 接收参数：
#     游戏名 模糊查找
#     发售日期 yyyy-MM-dd
#     标签 模糊查找
#     游戏类型
# ''' 
@bp.route('/gameDataQuery', methods=['POST'])
@swag_from('specs/game_data_query.yml')
def game_data_query():
    params = request.get_json()
    # params = {
    #     "page": 1,
    #     "rows": 10,
    #     # "yxm": "魔法少女",
    #     # "yxlx": "RPG",
    #     # "flbq": "女",
    #     "fsrq": "2022-02-28,2025-04-15"
    # }
    
    data = successModel(GameService.game_data_query(params))
    # print(data)
    return data
@bp.route('/gameDataDelete', methods=['POST'])

def game_data_delete():
    
    params = request.get_json()
    
    GameService.game_data_delete(params.get("ids", []))
    data = successModel(None, "删除成功")
    return data
@bp.route('/gameDataUpdate', methods=['POST'])
# @swag_from(os.path.join('specs', 'game_data_update.yml'))
def game_data_update():
    # """
    #     A simple endpoint
    #     ---
    #     tags:
    #     - Test
    #     responses:
    #     200:
    #         description: A greeting
    # """
    params = request.get_json()
    # params = {
    #     "id": 6999,
    #     "yxm": "测色11",
    #     "yxm11": "测色"
    # }
    
    GameService.game_data_merge(params)
    data = successModel(None, "保存成功")
    return data

@bp.route('/gameDataUpdateByYxbh', methods=['POST'])
# @swag_from(os.path.join('specs', 'game_data_update.yml'))
def game_data_update_by_yxbh():
    # """
    #     A simple endpoint
    #     ---
    #     tags:
    #     - Test
    #     responses:
    #     200:
    #         description: A greeting
    # """
    params = request.get_json()
    # params = {
    #     "id": 6999,
    #     "yxm": "测色11",
    #     "yxm11": "测色"
    # }
    
    GameService.game_data_update_by_yxbh(params.get("yxbh"))
    data = successModel(None, "更新成功")
    return data
@bp.route('/gameDataOutput', methods=['GET', 'POST'])
def game_data_output():
    data = successModel(GameService.game_data_output())
    return data