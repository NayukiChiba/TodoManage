import json
from pathlib import Path

from src.models import TodoItem


class JsonStorage:
    """
    JSON存储类, 用于存储和加载待办事项

    职责:
    从 data/todos.json 读取并且转换成 TodoItem 对象列表
    把 TodoItem 对象列表转换成 JSON 格式并且写入 data/todos.json
    """

    def __init__(self, file_path: str = "data/todos.json") -> None:
        """
        初始化 JsonStorage 对象, 设置文件路径

        - 确保文件存在, 如果不存在就创建一个空的 JSON 文件
        """
        self.file_path = Path(file_path)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)  # 确保目录存在
        if not self.file_path.exists():
            self.save([])  # 创建一个空的 JSON 文件

    def load(self) -> list[TodoItem]:
        """
        读取 JSON 并且返回TodoItem对象列表

        容错策略:
        - JSON 解析失败: 返回空列表
        - 数据格式不正确: 返回空列表
        """
        try:
            raw = json.loads(self.file_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            raw = []

        if not isinstance(raw, list):
            raw = []

        return [TodoItem.from_dict(item) for item in raw]

    def save(self, items: list[TodoItem]) -> None:
        """
        把TodoItem对象列表转换成JSON格式并且写入文件
        """
        payload = [item.to_dict() for item in items]
        self.file_path.write_text(
            json.dumps(payload, indent=4, ensure_ascii=False), encoding="utf-8"
        )
