import unittest
from input_parser import InputParser
from poker import PokerHand


class InputParserTester(unittest.TestCase):

    def test_get_hand_from_line(self):
        parser = InputParser()
        self.assertEqual(parser.get_hand_from_line("2C 2H 3H 4C 4H"), PokerHand(["2C", "2H", "3H", "4C", "4H"]))

    def test_get_results_lines(self):
        parser = InputParser()
        lines = [("2C 2H 2D 2S 3C", "KC QC JC AC TC"),
                 ("KC QC JC AC TC", "2C 2H 2D 2S 3C"),
                 ("KC QC JC AC TC", "KC QC JC AC TC")]
        self.assertEqual(parser.get_results_lines(lines), [-1, 1, 0])

    def test_parse_file(self):
        parser = InputParser()
        self.assertEqual(parser.parse_file("./input_parser_test_data.txt"), [-1, 0, -1, -1])

