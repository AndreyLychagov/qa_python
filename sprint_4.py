import pytest
from main import BooksCollector

@pytest.fixture
def collector():
    return BooksCollector()

def test_add_new_book_success(collector):
    collector.add_new_book("За миллиард лет до конца света")
    assert "За миллиард лет до конца света" in collector.get_books_genre()

def test_add_new_book_empty_name(collector):
    collector.add_new_book("")
    assert not collector.get_books_genre()

def test_add_new_book_long_name(collector):
    long_name = "Ы" * 41
    collector.add_new_book(long_name)
    assert not collector.get_books_genre()

@pytest.mark.parametrize("book_name, genre", [
    ("Голый пистолет", "Комедии"),
    ("Пила", "Ужасы"),
])
def test_set_book_genre_success(collector, book_name, genre):
    collector.add_new_book(book_name)
    collector.set_book_genre(book_name, genre)
    assert collector.get_book_genre(book_name) == genre

def test_set_book_genre_not_added(collector):
    collector.set_book_genre("Случайная книга", "Фантастика")
    assert collector.get_book_genre("Случайная книга") is None

def test_get_books_with_specific_genre(collector):
    collector.add_new_book("Над пропостью во ржи")
    collector.add_new_book("Шерлок Холмс")
    collector.set_book_genre("Над пропостью во ржи", "Фантастика")
    collector.set_book_genre("Шерлок Холмс", "Детективы")
    assert sorted(collector.get_books_with_specific_genre("Фантастика")) == ["Над пропостью во ржи"]
    assert sorted(collector.get_books_with_specific_genre("Детективы")) == ["Шерлок Холмс"]

def test_get_books_for_children(collector):
    collector.add_new_book("Волшебник изумрудного города")
    collector.add_new_book("Лолита")
    collector.set_book_genre("Волшебник изумрудного города", "Фантастика")
    collector.set_book_genre("Лолита", "Ужасы")
    assert collector.get_books_for_children() == ["Волшебник изумрудного города"]

def test_add_book_in_favorites_success(collector):
    collector.add_new_book("Пикник на обочине")
    collector.add_book_in_favorites("Пикник на обочине")
    assert "Пикник на обочине" in collector.get_list_of_favorites_books()

def test_add_book_in_favorites_not_in_books_genre(collector):
    collector.add_book_in_favorites("Случайная книга")
    assert "Случайная книга" not in collector.get_list_of_favorites_books()

def test_get_list_of_favorites_books(collector):
    collector.add_new_book("Мастер и Маргарита")
    collector.add_new_book("1984")
    collector.add_book_in_favorites("Мастер и Маргарита")
    collector.add_book_in_favorites("1984")
    assert sorted(collector.get_list_of_favorites_books()) == sorted(["Мастер и Маргарита", "1984"])


def test_delete_book_from_favorites(collector):
    collector.add_new_book("Мастер и Маргарита")
    collector.add_book_in_favorites("Мастер и Маргарита")
    assert "Мастер и Маргарита" in collector.get_list_of_favorites_books()
    collector.delete_book_from_favorites("Мастер и Маргарита")
    assert "Мастер и Маргарита" not in collector.get_list_of_favorites_books()