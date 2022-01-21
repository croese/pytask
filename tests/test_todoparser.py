from pytask.core.todoparser import TodoParser
from io import StringIO
from datetime import date


class TestTodoParser:
    def test_it_parses_description(self):
        f = StringIO("Post signs around the neighborhood")

        p = TodoParser(f)
        tasks = p.parse()

        assert len(tasks) == 1
        assert tasks[0].description == "Post signs around the neighborhood"

    def test_it_parses_multiple_lines(self):
        f = StringIO(
            """Post signs around the neighborhood
Schedule Goodwill pickup
Thank Mom for the meatballs"""
        )

        p = TodoParser(f)
        tasks = p.parse()

        assert len(tasks) == 3
        assert tasks[0].description == "Post signs around the neighborhood"
        assert tasks[1].description == "Schedule Goodwill pickup"
        assert tasks[2].description == "Thank Mom for the meatballs"

    def test_it_parses_leading_priority_correctly(self):
        f = StringIO(
            """(A) Call Mom
Put up (B) sign
(b) Get back to the boss
(B)->Submit TPS report"""
        )

        p = TodoParser(f)
        tasks = p.parse()

        assert tasks[0].priority == "A"
        assert tasks[0].description == "Call Mom"
        assert tasks[1].priority is None
        assert tasks[1].description == "Put up (B) sign"
        assert tasks[2].priority is None
        assert tasks[2].description == "(b) Get back to the boss"
        assert tasks[3].priority is None
        assert tasks[3].description == "(B)->Submit TPS report"

    def test_it_parses_complete_tasks(self):
        f = StringIO(
            """x Call Mom
xylophone lesson
X 2012-01-01 Make resolutions
(A) x Find ticket prices
x (B) Do stuff"""
        )

        p = TodoParser(f)
        tasks = p.parse()

        assert tasks[0].is_done
        assert tasks[0].description == "Call Mom"
        assert not tasks[1].is_done
        assert not tasks[2].is_done
        assert not tasks[3].is_done
        assert tasks[4].is_done
        assert tasks[4].priority == "B"

    def test_it_parses_creation_date(self):
        f = StringIO(
            """2011-03-02 Document task format
(A) 2015-07-16 Call Mom
x (C) 2021-01-21 Call Mom
(B) Call Mom 2011-03-02"""
        )

        p = TodoParser(f)
        tasks = p.parse()

        assert tasks[0].created_date == date.fromisoformat("2011-03-02")
        assert tasks[0].description == "Document task format"
        assert tasks[1].created_date == date.fromisoformat("2015-07-16")
        assert tasks[2].created_date == date.fromisoformat("2021-01-21")
        assert tasks[3].created_date == None
        assert tasks[3].description == "Call Mom 2011-03-02"

    def test_it_parses_contexts(self):
        f = StringIO(
            """(A) Call Mom +Family +PeaceLoveAndHappiness @iphone @phone
Email SoAndSo at soandso@example.com"""
        )

        p = TodoParser(f)
        tasks = p.parse()

        assert tasks[0].contexts == {"iphone", "phone"}
        assert len(tasks[1].contexts) == 0
