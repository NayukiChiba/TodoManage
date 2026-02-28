"""
models.py
"""
# 自动生成__init__, __repr__, __eq__等方法的装饰器
# field用于设置默认工厂, 比如list, dict等可变类型的默认值
from dataclasses import dataclass, field

from datetime import datetime
# Literal用于定义一个变量只能取特定的值, 例如状态码等
from typing import Literal, Optional

# 状态类型
Status = Literal["todo", "in_progress", "done"]
Priority = Literal["low", "medium", "high"]


def now_iso() -> str:
    """返回当前时间的ISO格式字符串"""
    return datetime.now().isoformat(timespec="seconds")


@dataclass
class TodoItem:
    """
    单条待办事项的数据模型

    这个类只负责"数据结构表达", 不包含任何业务逻辑
    """
    id: int # 唯一标识符
    title: str # 标题
    description: str = "" # 描述, 可选
    status: Status = "todo" # 状态, 默认为"todo"
    priority: Priority = "medium" # 优先级, 默认为"medium"

    # 创建时间
    created_at: str = field(default_factory=now_iso)

    # 更新时间
    updated_at: str = field(default_factory=now_iso)

    # 截止时间
    due_date: Optional[str] = None

    # tags
    tags: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """
        把TodoItem对象转换成字典, 方便序列化和存储
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "due_date": self.due_date,
            "tags": self.tags,
        }

    # 从字典创建TodoItem对象的工厂方法
    @classmethod
    def from_dict(cls, data: dict) -> "TodoItem":
        """
        从字典回复TodoItem对象, 方便从存储中加载数据

        - 使用 get 给默认值, 避免缺少字段导致错误
        - 用 str/list 做基本类型兜底
        """
        return cls(
            id = int(data.get("id", 0)),
            title = str(data.get("title", "")),
            description = str(data.get("description", "")),
            status = str(data.get("status", "todo")),
            priority = str(data.get("priority", "medium")),
            created_at = str(data.get("created_at", now_iso())),
            updated_at = str(data.get("updated_at", now_iso())),
            due_date = str(data.get("due_date", "")) if data.get("due_date") else None,
            tags = list(data.get("tags", [])),
        )