
from src.models import TodoItem, now_iso
from src.storage import JsonStorage


class TodoService:
    """
    业务层
    对外提供: 增删改查等操作
    内部使用JsonStorage进行数据持久化
    """

    def __init__(self, storage: JsonStorage | None = None) -> None:
        """
        支持依赖注入:
        - 如果外部提供了JsonStorage实例, 就使用它
        - 否则就创建一个默认的JsonStorage实例
        """
        self.storage = storage or JsonStorage()

    def _load(self) -> list[TodoItem]:
        """从存储加载待办事项列表"""
        return self.storage.load()

    def _save(self, items: list[TodoItem]) -> None:
        """把待办事项列表保存到存储"""
        self.storage.save(items)

    def add(
        self,
        title: str,
        description: str = "",
        priority: str = "medium",
        due_date: str | None = None,
        tags: list[str] | None = None,
    ) -> TodoItem:
        """
        新增待办事项
        关键:
        - 生成唯一ID: 通过现有ID的最大值加1来生成新ID
        - 设置默认值: description默认为空字符串, priority默认为"medium", due_date默认为None, tags默认为空列表
        """
        items = self._load()
        next_id = max((item.id for item in items), default=0) + 1

        todo = TodoItem(
            id=next_id,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            tags=tags or [],
        )
        items.append(todo)
        self._save(items)
        return todo

    def list(self, status: str | None = None) -> list[TodoItem]:
        """
        查询待办事项列表

        - status为空, 返回所有待办事项
        - status不为空, 只返回匹配状态的待办事项
        """
        items = self._load()
        if status:
            items = [item for item in items if item.status == status]
        return items

    def update(self, id: int, **kwargs) -> TodoItem | None:
        items = self._load()

        for item in items:
            if item.id == id:
                for key, value in kwargs.items():
                    if hasattr(item, key):
                        setattr(item, key, value)
                    else:
                        raise ValueError(f"Invalid field: {key}")
                item.updated_at = now_iso()  # 更新时间戳
                self._save(items)
                return item

        raise ValueError(f"Todo item with id {id} not found")

    def markDone(self, id: int) -> TodoItem | None:
        """把待办事项标记为完成"""
        return self.update(id, status="done")

    def delete(self, id: int) -> None:
        """
        删除待办事项
        """
        items = self._load()
        new_items = [item for item in items if item.id != id]
        if len(new_items) == len(items):
            raise ValueError(f"Todo item with id {id} not found")
        self._save(new_items)
