import unittest

class PokerCard(object):

    cards = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
    suits = ["C", "D", "H", "S"]

    def __init__(self, val):
        if not isinstance(val, str):
            raise TypeError("input must be a string")
        elif len(val) != 2:
            raise ValueError("input must be 2 chars long, of number and suit")
        self.val = val[0]
        self.suit = val[1]

    def __lt__(self, other):
        if other == None:   # None is default lowest possible card.
            return False
        return self.cards.index(self.val) < self.cards.index(other.val)

    def __eq__(self, other):
        if other == None:
            return False
        return self.cards.index(self.val) == self.cards.index(other.val)


class PokerHand(object):

    def __init__(self, cards):
        assert(isinstance(cards, list))
        assert(len(cards) == 5)
        self.cards = sorted([PokerCard(c) for c in cards])

    def get_pairs(self):
        vals_count = [0 for _ in range(len(PokerCard.cards))]
        for c1 in self.cards:
            vals_count[PokerCard.cards.index(c1.val)] += 1
        pairs = []
        for c_val, count in zip(PokerCard.cards, vals_count):
            if count == 2:
                pairs.append(PokerCard(c_val+"H"))  # Suit is irrelevant to result, only care about number
        return pairs

    def has_1pair(self):
        return len(self.get_pairs()) > 0

    def has_2pairs(self):
        return len(self.get_pairs()) > 1

    def get_3kind(self):
        vals_count = [0 for _ in range(len(PokerCard.cards))]
        for c1 in self.cards:
            vals_count[PokerCard.cards.index(c1.val)] += 1
        threes_val = None
        for c_val, count in zip(PokerCard.cards, vals_count):
            if count == 3:
                threes_val = PokerCard(c_val+"H")
        return threes_val

    def has_3kind(self):
        return self.get_3kind() != None

    def get_4kind(self):
        vals_count = [0 for _ in range(len(PokerCard.cards))]
        for c1 in self.cards:
            vals_count[PokerCard.cards.index(c1.val)] += 1
        fours_val = None
        for c_val, count in zip(PokerCard.cards, vals_count):
            if count == 4:
                fours_val = PokerCard(c_val+"H")
        return fours_val

    def has_4kind(self):
        return self.get_4kind() != None

    def has_full_house(self):
        return self.has_3kind() and self.has_1pair()

    def get_full_house(self):
        if self.has_full_house():
            return self.get_3kind()
        else:
            return None

    def has_straight(self):
        count = 0
        prev_val = self.cards[0].val
        for card in self.cards[1:]:
            c_val = card.val
            if PokerCard.cards.index(c_val) == (PokerCard.cards.index(prev_val) + 1):
                count += 1
            prev_val = card.val
        return count == 4

    def get_straight(self):
        if self.has_straight():
            return max(self.cards)
        else:
            return None

    def has_flush(self):
        return all(c1.suit == c2.suit for c1 in self.cards for c2 in self.cards)

    def get_flush(self):
        if self.has_flush():
            return max(self.cards)
        else:
            return None

    def has_straight_flush(self):
        return self.has_straight() and self.has_flush()

    def get_straight_flush(self):
        if self.has_straight_flush():
            return max(self.cards)
        else:
            return None

    def __lt__(self, other):
        """
        Precedence of hands:
        straight flush > 4 of a kind > full house > flush > straight > 3 of a kind > pairs > single
        """
        if self.get_straight_flush() != other.get_straight_flush():
            return self.get_straight_flush() < other.get_straight_flush()
        elif self.get_4kind() != other.get_4kind():
            return self.get_4kind() < other.get_4kind()
        elif self.get_full_house() != other.get_full_house():
            return self.get_full_house() < other.get_full_house()
        elif self.get_flush() != other.get_flush():
            return self.get_flush() < other.get_flush()
        elif self.get_straight() != other.get_straight():
            return self.get_straight() < other.get_straight()
        elif self.get_3kind() != other.get_3kind():
            return self.get_3kind() < other.get_3kind()
        elif self.get_pairs() != other.get_pairs():
            if len(self.get_pairs()) != len(other.get_pairs):
                return len(self.get_pairs()) < len(other.get_pairs)
            elif self.get_pairs()[0] != other.get_pairs[0]:
                return self.get_pairs()[0] < other.get_pairs()[0]
            elif len(self.get_pairs()) == 2:
                return self.get_pairs()[1] < other.get_pairs()[1]
            else:
                return False
        else:
            # Compare from largest to smallest
            return list(reversed(self.cards)) < list(reversed(other.cards))

    def __eq__(self, other):
        return not ((self < other) or (other < self))


class InputParser(object):
    """
    Takes file input and performs comparisons on pairs of hands.
    """

    def get_hand_from_line(self, line):
        return PokerHand(line.split(" "))

    def get_results_lines(self, lines):
        result = []
        for l1, l2 in lines:
            hand1 = self.get_hand_from_line(l1)
            hand2 = self.get_hand_from_line(l2)
            if hand1 < hand2:
                result.append(-1)
            elif hand2 < hand1:
                result.append(1)
            else:
                result.append(0)
        return result

    def parse_file(self, fdir):
        """
        File should be several pairs of adjacent lines.
        Each line has a series of 5 space-separated string representations of cards in a hand.
        """
        f = open(fdir, "r")
        lines = f.read().split("\n")
        line_pairs = [(lines[i], lines[i+1]) for i in range(0, len(lines), 2)]
        return self.get_results_lines(line_pairs)


class PokerTester(unittest.TestCase):

    def test_card_compare(self):
        for i, c1_val in enumerate(PokerCard.cards):
            for j, c2_val in enumerate(PokerCard.cards[i+1:]):
                card1 = PokerCard(c1_val+"H")
                card2 = PokerCard(c2_val+"H")
                assert(card1 < card2)
                assert(max(card1, card2).val == c2_val)
            assert(PokerCard(c1_val+"H") == PokerCard(c1_val+"H"))

    def test_card_sorted(self):
        card_vals = PokerCard.cards
        cards = [PokerCard("2C")] + [PokerCard(val + "C") for val in list(reversed(card_vals))]
        sorted_vals = sorted(cards)
        assert([c.val + c.suit for c in sorted_vals] == ["2C"] + [c+"C" for c in card_vals])

    def test_hand_1pair(self):
        hand = PokerHand(["2H", "3H", "4H", "4H", "5H"])
        assert(hand.has_1pair())
        hand2 = PokerHand(["2H", "3H", "4H", "5H", "6H"])
        assert(not hand2.has_1pair())
        hand3 = PokerHand(["2H", "3H", "3H", "3H", "6H"])
        assert(not hand3.has_1pair())

    def test_hand_get_pair_vals(self):
        hand = PokerHand(["4H", "2H", "2H", "3H", "3H"])
        assert(hand.get_pairs() == [PokerCard("2H"), PokerCard("3H")])

    def test_hand_2pairs(self):
        hand = PokerHand(["5H", "3H", "3H", "4H", "4H"])
        assert(hand.has_2pairs())
        hand2 = PokerHand(["2H", "3H", "4H", "4H", "5H"])
        assert(not hand2.has_2pairs())
        hand3 = PokerHand(["2H", "3H", "4H", "5H", "6H"])
        assert(not hand3.has_2pairs())

    def test_hand_3kind(self):
        hand = PokerHand(["5H", "3H", "3H", "3H", "4H"])
        assert(hand.has_3kind())
        hand2 = PokerHand(["2H", "3H", "4H", "4H", "5H"])
        assert(not hand2.has_3kind())

    def test_hand_get_3kind(self):
        hand = PokerHand(["5H", "3H", "3H", "3H", "4H"])
        assert(hand.get_3kind() == PokerCard("3H"))
        hand2 = PokerHand(["2H", "3H", "4H", "4H", "5H"])
        assert(hand2.get_3kind() == None)

    def test_hand_4kind(self):
        hand = PokerHand(["2H", "4H", "4H", "4H", "4H"])
        assert(hand.has_4kind())
        hand2 = PokerHand(["2H", "3H", "4H", "5H", "6H"])
        assert(not hand2.has_4kind())

    def test_hand_get_4kind(self):
        hand = PokerHand(["5H", "3H", "3H", "3H", "3H"])
        assert(hand.get_4kind() == PokerCard("3H"))
        hand2 = PokerHand(["2H", "3H", "4H", "4H", "4H"])
        assert(hand2.get_4kind() == None)

    def test_hand_full_house(self):
        hand = PokerHand(["3H", "3H", "3H", "2H", "2H"])
        assert(hand.has_full_house())
        hand2 = PokerHand(["2H", "3H", "4H", "5H", "6H"])
        assert(not hand2.has_full_house())

    def test_hand_get_full_house(self):
        hand = PokerHand(["5H", "5H", "3H", "3H", "3H"])
        assert(hand.get_full_house() == PokerCard("3H"))
        hand2 = PokerHand(["2H", "3H", "4H", "4H", "4H"])
        assert(hand2.get_full_house() == None)

    def test_hand_straight(self):
        hand = PokerHand(["2H", "3H", "4H", "5H", "6H"])
        assert(hand.has_straight())
        hand2 = PokerHand(["2H", "3H", "5H", "6H", "7H"])
        assert(not hand2.has_straight())

    def test_hand_get_straight(self):
        hand = PokerHand(["2H", "3H", "4H", "5H", "6H"])
        assert(hand.get_straight() == PokerCard("6H"))
        hand2 = PokerHand(["2H", "3H", "5H", "6H", "7H"])
        assert(hand2.get_straight() == None)

    def test_hand_flush(self):
        hand = PokerHand(["2H", "3H", "4H", "5H", "6H"])
        assert(hand.has_flush())
        hand2 = PokerHand(["2H", "3H", "5H", "6H", "7C"])
        assert(not hand2.has_flush())

    def test_hand_get_flush(self):
        hand = PokerHand(["2H", "3H", "4H", "5H", "6H"])
        assert(hand.get_flush() == PokerCard("6H"))
        hand2 = PokerHand(["2H", "3H", "5H", "6H", "7C"])
        assert(hand2.get_flush() == None)

    def test_hand_straight_flush(self):
        hand = PokerHand(["2H", "3H", "4H", "5H", "6H"])
        assert(hand.has_straight_flush())
        hand2 = PokerHand(["2H", "3H", "5H", "6H", "7C"])
        assert(not hand2.has_straight_flush())
        hand3 = PokerHand(["2H", "3H", "5H", "6H", "8H"])
        assert(not hand3.has_straight_flush())

    def test_hand_get_straight_flush(self):
        hand = PokerHand(["2H", "3H", "4H", "5H", "6H"])
        assert(hand.get_straight_flush() == PokerCard("6H"))
        hand2 = PokerHand(["2H", "3H", "5H", "6H", "7C"])
        assert(hand2.get_straight_flush() == None)
        hand3 = PokerHand(["2H", "3H", "5H", "6H", "8H"])
        assert(hand3.get_straight_flush() == None)

    def test_hand_lt(self):
        hand = PokerHand(["2H", "3H", "4H", "5H", "6H"])
        hand2 = PokerHand(["2H", "3H", "4H", "5H", "5C"])
        assert(hand2 < hand)

    def test_hand_eq(self):
        hand = PokerHand(["2H", "3H", "4H", "5H", "6H"])
        hand2 = PokerHand(["2H", "3H", "4H", "5H", "6H"])
        assert(hand2 == hand)


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
        self.assertEqual(parser.parse_file("./Input_Hands.txt"), [-1, 0, -1, -1])


def main():
    # Test PokerCard and PokerHand
    suite_poker = unittest.TestLoader().loadTestsFromTestCase(PokerTester)
    unittest.TextTestRunner(verbosity=2).run(suite_poker)
    # Test InputParser
    suite_parser = unittest.TestLoader().loadTestsFromTestCase(InputParserTester)
    unittest.TextTestRunner(verbosity=2).run(suite_parser)

if __name__ == "__main__":
    main()
