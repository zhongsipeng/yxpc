from functools import wraps
from typing import Dict, List, Any, Tuple, Union

from flask import request
from jsonschema import ValidationError

def validate_json_with_template(
    template: Dict[str, Any], 
    data: Dict[str, Any],
    parent_key: str = ""
) -> Tuple[bool, str]:
    """
    根据模板校验JSON数据结构
    
    参数:
        template: 定义期望结构的模板字典
        data: 待校验的数据字典
        parent_key: 用于递归时跟踪父级键名
        
    返回:
        Tuple[bool, str]: (是否有效, 错误信息)
    """
    # 1. 检查数据是否为字典
    if not isinstance(data, dict):
        return False, f"期望得到字典类型，但得到 {type(data).__name__}"
    
    # 2. 检查所有必须字段是否存在
    for key in template.keys():
        full_key = f"{parent_key}.{key}" if parent_key else key
        if key not in data:
            return False, f"缺少必须字段: {full_key}"
    
    # 3. 逐个字段校验
    for key, expected_type in template.items():
        full_key = f"{parent_key}.{key}" if parent_key else key
        value = data[key]
        
        # 处理嵌套字典
        if isinstance(expected_type, dict):
            if not isinstance(value, dict):
                return False, f"字段 {full_key} 应该是字典类型"
            is_valid, msg = validate_json_with_template(expected_type, value, full_key)
            if not is_valid:
                return False, msg
            continue
        
        # 处理数组类型
        if isinstance(expected_type, list):
            if not isinstance(value, list):
                return False, f"字段 {full_key} 应该是数组类型"
            
            # 如果模板数组不为空，使用第一个元素作为数组元素的模板
            if expected_type:
                item_template = expected_type[0]
                for i, item in enumerate(value):
                    if isinstance(item_template, dict):
                        if not isinstance(item, dict):
                            return False, f"字段 {full_key}[{i}] 应该是字典类型"
                        is_valid, msg = validate_json_with_template(item_template, item, f"{full_key}[{i}]")
                        if not is_valid:
                            return False, msg
                    elif isinstance(item_template, str):
                        type_check = get_type_checker(item_template)
                        if not type_check(item):
                            return False, f"字段 {full_key}[{i}] 应该是 {item_template} 类型"
            continue
        
        # 处理基本类型
        if isinstance(expected_type, str):
            type_check = get_type_checker(expected_type)
            if not type_check(value):
                return False, f"字段 {full_key} 应该是 {expected_type} 类型"
            continue
            
        return False, f"模板字段 {full_key} 有无效的类型定义"
    
    return True, "校验通过"

def get_type_checker(type_name: str):
    """根据类型名称返回对应的类型检查函数"""
    type_checkers = {
        "Number": lambda x: isinstance(x, (int, float)),
        "String": lambda x: isinstance(x, str),
        "Boolean": lambda x: isinstance(x, bool),
        "Object": lambda x: isinstance(x, dict),
        "Array": lambda x: isinstance(x, list),
        "Any": lambda x: True
    }
    return type_checkers.get(type_name, lambda x: False)

def validate_json(schema = None, template = None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if template:
                data = request.get_json()
                is_valid, message = validate_json_with_template(template, data)
                if not is_valid:
                    raise ValidationError(message)
            else:
                data = schema.load(request.get_json())
            return f(data, *args, **kwargs)

        return wrapper
    return decorator