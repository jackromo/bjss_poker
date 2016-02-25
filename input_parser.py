from poker import PokerHand


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
