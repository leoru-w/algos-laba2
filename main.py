from datetime import *


class Node:
    def __init__(self, url: str, is_bookmark: bool = False):
        self.url = url
        self.visit_time = datetime.now()
        self.is_bookmark = is_bookmark
        self.prev = None
        self.next = None


class BrowserHistory:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None

    def visit(self, url: str, is_bookmark: bool = False):
        if not url:
            print("URL пустой.")
            return

        node = Node(url, is_bookmark)

        if self.current and self.current.next:
            self.current.next = None
            self.tail = self.current

        if not self.head:
            self.head = node
            self.tail = node
        else:
            self.tail.next = node
            node.prev = self.tail
            self.tail = node

        self.current = self.tail
        print(f"Посещено: {url}")

    def back(self):
        if not self.current or not self.current.prev:
            print("Назад идти некуда")
            return
        self.current = self.current.prev
        print(f"Назад к: {self.current.url}")

    def forward(self):
        if not self.current or not self.current.next:
            print("Вперед идти некуда")
            return
        self.current = self.current.next
        print(f"Вперед к: {self.current.url}")

    def clear_history(self):
        self.head = None
        self.tail = None
        self.current = None
        print("История очищена.")

    def search_by_domain(self, keyword: str):
        print(f"\nРезультаты поиска '{keyword}':")
        node = self.head
        found = False

        results = []
        while node:
            if keyword.lower() in node.url.lower():
                results.append(node)
                found = True
            node = node.next

        if found:
            self._print_columns(results)
        else:
            print("Ничего не найдено.")

    def display_full_history(self):
        print("\nИстория посещений:")
        nodes_list = []
        node = self.head
        while node:
            nodes_list.append(node)
            node = node.next

        self._print_columns(nodes_list)

    def _print_columns(self, nodes_list):
        if not nodes_list:
            print("История пуста.")
            return

        print(f"{'URL':<30} | {'Время посещения':<20} | {'Закладка':<8}")
        print("-" * 65)

        for node in nodes_list:
            time_str = node.visit_time.strftime("%Y-%m-%d %H:%M:%S")
            bookmark_status = "Да" if node.is_bookmark else "Нет"
            row = f"{node.url:<30} | {time_str:<20} | {bookmark_status:<8}"

            if node == self.current:
                print(f"{row} [текущая]")
            else:
                print(f"{row}")

    def print_period(self, start_time: datetime, end_time: datetime):
        start_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
        end_str = end_time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"\nИстория за период с {start_str} по {end_str}")

        node = self.head
        results = []
        while node:
            if start_time <= node.visit_time <= end_time:
                results.append(node)
            node = node.next

        if results:
            self._print_columns(results)
        else:
            print("За этот период нет записей")


if __name__ == "__main__":
    browser = BrowserHistory()

    browser.visit("google.com", is_bookmark=True)
    browser.visit("github.com/profile")
    browser.visit("habr.com/ru/post/1", is_bookmark=True)

    browser.display_full_history()

    browser.back()
    browser.back()
    browser.forward()

    browser.visit("youtube.com")
    browser.display_full_history()

    browser.search_by_domain("hub")

    now = datetime.now()
    past = now - timedelta(minutes=5)
    future = now + timedelta(minutes=5)

    browser.print_period(past, future)

    print("\nОчистка истории")
    browser.clear_history()
    browser.display_full_history()
