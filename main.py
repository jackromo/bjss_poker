import unittest
import poker_tester
import input_parser_tester


def run_tests():
    # Test PokerCard and PokerHand
    suite_poker = unittest.TestLoader().loadTestsFromTestCase(poker_tester.PokerTester)
    unittest.TextTestRunner(verbosity=2).run(suite_poker)
    # Test InputParser
    suite_parser = unittest.TestLoader().loadTestsFromTestCase(input_parser_tester.InputParserTester)
    unittest.TextTestRunner(verbosity=2).run(suite_parser)

if __name__ == "__main__":
    run_tests()
