import unittest

class PokerCard(object):

    cards = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
    suits = ["C", "D", "H", "S"]

    def __init__(self, val):
        self.val = val[0]
        if len(val) == 1:
            self.suit = "H"
        else:
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
                pairs.append(PokerCard(c_val))
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
                threes_val = PokerCard(c_val)
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
                fours_val = PokerCard(c_val)
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
            return self.cards < other.cards


class PokerTester(unittest.TestCase):

    def test_card_compare(self):
        for i, c1_val in enumerate(PokerCard.cards):
            for j, c2_val in enumerate(PokerCard.cards[i+1:]):
                card1 = PokerCard(c1_val)
                card2 = PokerCard(c2_val)
                assert(card1 < card2)
                assert(max(card1, card2).val == c2_val)
            assert(PokerCard(c1_val) == PokerCard(c1_val))

    def test_card_sorted(self):
        card_vals = PokerCard.cards
        cards = [PokerCard("2")] + [PokerCard(val) for val in list(reversed(card_vals))]
        sorted_vals = sorted(cards)
        assert([c.val for c in sorted_vals] == ["2"] + card_vals)

    def test_hand_1pair(self):
        hand = PokerHand(["2", "3", "4", "4", "5"])
        assert(hand.has_1pair())
        hand2 = PokerHand(["2", "3", "4", "5", "6"])
        assert(not hand2.has_1pair())
        hand3 = PokerHand(["2", "3", "3", "3", "6"])
        assert(not hand3.has_1pair())

    def test_hand_get_pair_vals(self):
        hand = PokerHand(["4", "2", "2", "3", "3"])
        assert(hand.get_pairs() == [PokerCard("2"), PokerCard("3")])

    def test_hand_2pairs(self):
        hand = PokerHand(["5", "3", "3", "4", "4"])
        assert(hand.has_2pairs())
        hand2 = PokerHand(["2", "3", "4", "4", "5"])
        assert(not hand2.has_2pairs())
        hand3 = PokerHand(["2", "3", "4", "5", "6"])
        assert(not hand3.has_2pairs())

    def test_hand_3kind(self):
        hand = PokerHand(["5", "3", "3", "3", "4"])
        assert(hand.has_3kind())
        hand2 = PokerHand(["2", "3", "4", "4", "5"])
        assert(not hand2.has_3kind())

    def test_hand_get_3kind(self):
        hand = PokerHand(["5", "3", "3", "3", "4"])
        assert(hand.get_3kind() == PokerCard("3"))
        hand2 = PokerHand(["2", "3", "4", "4", "5"])
        assert(hand2.get_3kind() == None)

    def test_hand_4kind(self):
        hand = PokerHand(["2", "4", "4", "4", "4"])
        assert(hand.has_4kind())
        hand2 = PokerHand(["2", "3", "4", "5", "6"])
        assert(not hand2.has_4kind())

    def test_hand_get_4kind(self):
        hand = PokerHand(["5", "3", "3", "3", "3"])
        assert(hand.get_4kind() == PokerCard("3"))
        hand2 = PokerHand(["2", "3", "4", "4", "4"])
        assert(hand2.get_4kind() == None)

    def test_hand_full_house(self):
        hand = PokerHand(["3", "3", "3", "2", "2"])
        assert(hand.has_full_house())
        hand2 = PokerHand(["2", "3", "4", "5", "6"])
        assert(not hand2.has_full_house())

    def test_hand_get_full_house(self):
        hand = PokerHand(["5", "5", "3", "3", "3"])
        assert(hand.get_full_house() == PokerCard("3"))
        hand2 = PokerHand(["2", "3", "4", "4", "4"])
        assert(hand2.get_full_house() == None)

    def test_hand_straight(self):
        hand = PokerHand(["2", "3", "4", "5", "6"])
        assert(hand.has_straight())
        hand2 = PokerHand(["2", "3", "5", "6", "7"])
        assert(not hand2.has_straight())

    def test_hand_get_straight(self):
        hand = PokerHand(["2", "3", "4", "5", "6"])
        assert(hand.get_straight() == PokerCard("6"))
        hand2 = PokerHand(["2", "3", "5", "6", "7"])
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


def main():
    suite = unittest.TestLoader().loadTestsFromTestCase(PokerTester)
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    main()
