#!/usr/local/bin/python
#
#  Roman Numeral Calculator kata
#
#  From
#  <http://codingdojo.org/cgi-bin/wiki.pl?KataRomanCalculator>
#
#  Problem Description
#
#  "As a Roman Bookkeeper I want to add Roman numbers because doing it
#  manually is too tedious." Given the Roman numerals, (IVXLCDM which
#  means one, five, ten, fifty, hundred, fivehundred and a thousand
#  respectively), create two numbers and add them. As we are in Rome
#  there is no such thing as decimals or int, we need to do this with the
#  strings. An example would be "XIV" + "LX" = "LXXIV"
#
#  There are some rules to a Roman number:
#
#  - Numerals can be concatenated to form a larger numeral
#    ("XX" + "II" = "XXII")
#
#  - If a lesser numeral is put before a bigger it means subtraction of the
#    lesser from the bigger ("IV" means four, "CM" means ninehundred)
#
#  - If the numeral is I, X or C you can't have more than three
#    ("II" + "II" = "IV")
#
#  - If the numeral is V, L or D you can't have more than one
#    ("D" + "D" = "M")
#
#
#  Run this file at the command-line to run the test suite, or
#    import romancalc
#  to use the RomanNum class in another program.
#
#  Copyright (C) 2013  Alexander Park Chamberlain
#
#  Author: Alex Chamberlain <apchamberlain@gmail.com>
#  Version: 1.0
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.


import unittest
import re


class RomanNum:
    char_dict = {"I": 1, "V": 5, "X": 10, "L": 50, \
                 "C": 100, "D": 500, "M": 1000}
    runlimits = ["IIII", "VV", "XXXX", "LL", "CCCC", "DD"]
    subtract_dict = {"IV": "IIII", "IX": "VIIII", "XL": "XXXX", \
                     "XC": "LXXXX", "CD": "CCCC", "CM": "DCCCC"}

    @staticmethod
    def charToInt(c):
        return RomanNum.char_dict[c]

    @staticmethod
    def calc(x):
        """
        Given one of two patterns <roman numeral> <operator> <roman numeral>
        or just <roman numeral>, parse out (with simple regexps)
        the number(s) and operator, instantiate RomanNum objects as
        necessary to convert to Arabic, and evaluate the arithmetic
        expression if necessary.
        """
        num_cat_op = re.compile(r'([IVXLCDM]+)\s*(\+|\-|\*|\/|)\s*(.*)")')
        just_num = re.compile(r'([IVXLCDM]+)')

        expr = ""
        parsed = True
        while (parsed):
            parsed = re.match(num_cat_op, x)
            if (parsed):
                expr += ("RomanNum('" + parsed.group(1) + "') " + parsed.group(2))
                x = parsed.group(3)
            else:
                parsed = re.match(just_num, x)
                if (parsed):
                    expr += ("RomanNum('" + parsed.group(1) + "') ")
                    x = ""
        return eval(expr)

    def __init__(self, s=""):
        try:
            self._integer_representation = int(s)
            self._string_representation = ""
            self.toStr()
        except ValueError:
            # Check for bad chars.
            for c in list(s):
                if not (c in RomanNum.char_dict.keys()):
                    raise ValueError
            # TODO: Check for too many chars of the same kind in a row here
            # using the runlimits dict.
            self._string_representation = s
            self._integer_representation = 0
            self.toInt()

    def toInt(self):
        # Works because there's no zero in Roman numerals.
        if (self._integer_representation):
            return self._integer_representation
        else:
            # Gotta build it!

            # Translate a "subtraction sequence" temporarily into something
            # that is not correct Roman numeral form, but can be handled by
            # the naive Roman-to-Arabic algorithm labeled as such below
            # (strict one-to-one additive letter-to-number translation).

            # test9a, test9d

            s = self._string_representation
            r = range(len(s))
            for u in RomanNum.subtract_dict.keys():
                for i in r:
                    if s[i:(i + len(u))] == u:
                        # Modifying the sequence r inside the 2nd for loop here
                        # is somewhat dangerous magic, but we have to do
                        # it in order to make sure that we scan the entire
                        # string s for possible expansions, since every
                        # such expansion makes it grow.
                        for j in range(len(RomanNum.subtract_dict[u]) - len(u)):
                            r += [(r[-1:][0] + 1)]
                            s = s[:i] + RomanNum.subtract_dict[u] \
                                + s[(i + len(u)):]
            slist = list(s)
            # "Hi, I'm a naive algorithm"
            n = 0
            for c in slist:
                n += RomanNum.charToInt(c)
            self._integer_representation = n
            return n

    def toStr(self):
        if (self._string_representation \
                or not self._integer_representation):
            return self._string_representation
        else:
            # gotta build it!
            s = ""
            # Turn the chars-to-numbers dict inside out.
            num_dict = dict([(RomanNum.char_dict[k], k) \
                             for k in RomanNum.char_dict.keys()])
            m = self._integer_representation
            for n in sorted(num_dict.keys(), reverse=True):
                (quotient, modulus) = divmod(m, n)
                s += num_dict[n] * quotient
                m = modulus

            # test9e: search _backwards_ through _string_representation
            # and replace with "subtraction patterns" from an inside-out
            # version of subtract_dict.  Sort of feels like peephole
            # optimization of intermediate code in a compiler.

#DEBUG
#            changed_flag = 0
#_DEBUG
            tract_sub_dict = dict([(RomanNum.subtract_dict[k], k) \
                                   for k in RomanNum.subtract_dict.keys()])
            for u in sorted(tract_sub_dict.keys(), \
                            key=lambda x: RomanNum(x).toInt(), \
                            reverse=True):
                for i in range(len(s) - 1, -1, -1):
                    if s[i:(i+len(u))] == u:
#DEBUG
#                        if changed_flag == 0:
#                            print "DEBUG: in toStr():"
#                            changed_flag = 1
#                        print s + ":" + u + " --> " + tract_sub_dict[u]
#                        print (" " * i) + ("^" * len(u))
#_DEBUG
                        s = s[:i] + tract_sub_dict[u] + s[(i+len(u)):]

            self._string_representation = s
            return s

        def __cmp__(self, other):
            return self.toInt() - other.toInt()

        def __add__(self, other):
            return RomanNum(self.toInt() + other.toInt())

        def __sub__(self, other):
            return RomanNum(self.toInt() - other.toInt())

        def __mul__(self, other):
            return RomanNum(self.toInt() * other.toInt())

        def __div__(self, other):
            return RomanNum(self.toInt() / other.toInt())


class TestRomanCalculator(unittest.TestCase):
    rtest_i = RomanNum("I")
    rtest_z = RomanNum()
    rtest_ii = RomanNum("II")
    rtest_ii_2 = RomanNum("II")
    rtest_7 = RomanNum(7)
    rtest_7a = RomanNum("VII")

    def test1(self):
        self.failUnless(TestRomanCalculator.rtest_i.toInt() == 1)

    def test2(self):
        self.failIf(TestRomanCalculator.rtest_z.toInt() != 0)

    def test2a(self):
        self.failIf(TestRomanCalculator.rtest_z.toStr() != "")

    def test3(self):
        # rtest_z ought to be a properly instantiated object,
        # just 0 and "" internally.
        self.failUnless(TestRomanCalculator.rtest_z)

    def test4(self):
        self.failUnless(TestRomanCalculator.rtest_ii.toInt() == 2)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
