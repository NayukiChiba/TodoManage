import argparse

from src.todoService import TodoService


def buildParser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="命令行待办事项管理工具")
    # 不强制要求子命令，这样直接运行时可以优雅打印帮助，而不是抛参数错误
    subparsers = parser.add_subparsers(dest="command", required=False)

    # 添加命令
    add_parser = subparsers.add_parser("add", help="添加新的待办事项")
    add_parser.add_argument("title", type=str, help="待办事项标题")
    add_parser.add_argument("--description", type=str, default="", help="待办事项描述")
    add_parser.add_argument(
        "--priority",
        type=str,
        choices=["low", "medium", "high"],
        default="medium",
        help="优先级",
    )
    add_parser.add_argument("--due-date", type=str, help="截止日期 (YYYY-MM-DD)")
    add_parser.add_argument("--tags", type=str, nargs="*", default=[], help="标签列表")

    # 列表命令
    list_parser = subparsers.add_parser("list", help="列出待办事项")
    list_parser.add_argument(
        "--status",
        type=str,
        choices=["todo", "in_progress", "done"],
        help="过滤条件: todo / in_progress / done",
    )

    # 删除命令
    delete_parser = subparsers.add_parser("delete", help="删除待办事项")
    delete_parser.add_argument("id", type=int, help="待办事项ID")

    # 更新命令
    update_parser = subparsers.add_parser("update", help="更新待办事项")
    update_parser.add_argument("id", type=int, help="待办事项ID")
    update_parser.add_argument("--title", type=str, help="新的标题")
    update_parser.add_argument("--description", type=str, help="新的描述")
    update_parser.add_argument(
        "--status",
        type=str,
        choices=["todo", "in_progress", "done"],
        help="新的状态: todo / in_progress / done",
    )
    update_parser.add_argument(
        "--priority", type=str, choices=["low", "medium", "high"], help="新的优先级"
    )
    update_parser.add_argument("--due-date", type=str, help="新的截止日期 (YYYY-MM-DD)")
    update_parser.add_argument("--tags", type=str, nargs="*", help="新的标签列表")

    # 完成命令
    complete_parser = subparsers.add_parser("done", help="标记待办事项为完成")
    complete_parser.add_argument("id", type=int, help="待办事项ID")

    return parser


def printItem(item) -> None:
    print(f"ID: {item.id}")
    print(f"标题: {item.title}")
    print(f"描述: {item.description}")
    print(f"状态: {item.status}")
    print(f"优先级: {item.priority}")
    print(f"创建时间: {item.created_at}")
    print(f"更新时间: {item.updated_at}")
    print(f"截止日期: {item.due_date}")
    print(f"标签: {', '.join(item.tags)}")
    print("-" * 40)


def main() -> None:
    """
    CLI主入口: 解析参数 -> 分发命令 -> 调用TodoService -> 输出结果
    """
    parser = buildParser()
    args = parser.parse_args()

    # 未提供子命令时，显示帮助并退出（退出码0，表示正常提示）
    if not getattr(args, "command", None):
        parser.print_help()
        return

    service = TodoService()

    if args.command == "add":
        item = service.add(
            title=args.title,
            description=args.description,
            priority=args.priority,
            due_date=args.due_date,
            tags=args.tags,
        )
        print("待办事项添加成功:")
        printItem(item)

    elif args.command == "list":
        items = service.list(status=args.status)
        if not items:
            print("没有待办事项")
        else:
            for item in items:
                printItem(item)

    elif args.command == "delete":
        try:
            service.delete(args.id)
            print(f"待办事项 {args.id} 删除成功")
        except ValueError as e:
            print(e)

    elif args.command == "update":
        kwargs = {
            k: v
            for k, v in vars(args).items()
            if k not in ["id", "command"] and v is not None
        }
        try:
            item = service.update(args.id, **kwargs)
            print("待办事项更新成功:")
            printItem(item)
        except ValueError as e:
            print(e)

    elif args.command == "done":
        try:
            item = service.markDone(args.id)
            print("待办事项标记为完成:")
            printItem(item)
        except ValueError as e:
            print(e)


if __name__ == "__main__":
    main()
