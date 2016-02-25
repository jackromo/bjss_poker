import unittest
from poker import PokerCard, PokerHand


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
