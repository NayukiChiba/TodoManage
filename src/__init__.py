"""TodoManage 核心包。

对外导出常用类型和服务，便于外部统一导入：
from src import TodoService, TodoItem
"""

from .models import TodoItem
from .storage import JsonStorage
from .todoService import TodoService

__all__ = ["TodoItem", "JsonStorage", "TodoService"]
