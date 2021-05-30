import unittest

from clang.objects.index import Index
from clang.objects.translation_unit import TranslationUnit
from comments.comments_database import CommentsDatabase


class MyTestCase(unittest.TestCase):
    def test_parser_enum(self):
        path_file: str = "../input/enum.hh"
        index: Index = Index.create()
        translation_unit: TranslationUnit = index.parse(path_file)
        self.assertEqual(len(translation_unit.diagnostics), 0,
                         "The amount of diagnostic in the translation unit not is zero")
        database_comments = CommentsDatabase(path_file, translation_unit)
        self.assertEqual(len(database_comments), 3, "The amount of comments in the database not is 3 (comments)")
        self.assertEqual(repr(database_comments), "Comments: 3", "The representation of object not is equal")

    def test_parser_abstract(self):
        pass

    def test_parser_base(self):
        pass

    def test_parser_constructor(self):
        pass

    def test_parser_destructor(self):
        pass

    def test_parser_interface(self):
        pass

    def test_parser_method(self):
        pass

    def test_parser_namespace(self):
        pass

    def test_parser_struct(self):
        pass

    def test_parser_template(self):
        pass

    def test_parser_union(self):
        pass

    def test_parser_union_struct(self):
        pass

    def test_parser_utf8(self):
        pass

    def test_parser_virtual(self):
        pass


if __name__ == '__main__':
    unittest.main()
