

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
