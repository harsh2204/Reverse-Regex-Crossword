import numpy as np
from random import randint, sample, choices, choice, random, shuffle
import string
from collections import deque, Counter, defaultdict
from pprint import pprint
import re

"""
    Bottom of the barrel. str_target can be anything but max_len will always be 1.    
        nice single character addin for the ends of a string
        "^"      Matches the start of the string.
        "$"      Matches the end of the string or just before the newline at
                the end of the string.
        adds extra ambiguity for the simple price of 1 character
        "+"      Matches 1 or more (greedy) repetitions of the preceding RE. this one can be used to reduce ambiguity compared to the others.
        "?"      Matches 0 or 1 (greedy) of the preceding RE.
        "*"      Matches 0 or more (greedy) repetitions of the preceding RE.
                 Greedy means that it will match as many repetitions as possible.
        useless, but also ambiguity > 9000
        "."      Matches any character except a newline.
        

    # *?,+?,?? Non-greedy versions of the previous threeexponential decay formula simpleng RE.
    Repetition patterns, have a higher intrinsic ambiguity, but can be introduced early with simple repetition ranges like {1} or {2}
        {m,n}    Matches from m to n repetitions of the preceding RE.
        {m,n}?   Non-greedy version of the above.

    Case for Special characters:

        "\\"     Either escapes special characters or signals a special sequence.

        High(maybe) difficulty stuff here, the target string must be a repetitions with a string of length >1 separating the repetitions.
            \number  Matches the contents of the group of the same number.
        Weird maybe not that useful..
            \A       Matches only at the start of the string.
            \Z       Matches only at the end of the string.
        This can be solid for multiple occurrences of non-word tokens. Only great if used in clusters of 2 or more.
            \b       Matches the empty string, but only at the start or end of a word.
        Good for increasing ambiguity in the puzzle
            \B       Matches the empty string, but not at the start or end of a word. this becomes basically the same as, "word\B" => "word.*"
        Solid for matching empty space and always has a length >= 2
            \s       Matches any whitespace character; equivalent to [ \t\n\r\f\v] in
            \S       Matches any non-whitespace character; equivalent to [^\s].
        Simple decimal placement for mostly isolated target strings of length (maybe) <=3
            \d       Matches any decimal digit; equivalent to the set [0-9] in
                    bytes patterns or string patterns with the ASCII flag.
                    In string patterns without the ASCII flag, it will match the whole
                    range of Unicode digits.
        A solid way to increase ambiguity in the puzzle
            \D       Matches any non-digit character; equivalent to [^\d].
                bytes patterns or string patterns with the ASCII flag.
                In string patterns without the ASCII flag, it will match the whole
                range of Unicode whitespace characters.
        Another bang for the buck ambiguity booster, but also kinda useless for most scenarios
            \w       Matches any alphanumeric character; equivalent to [a-zA-Z0-9_]
                    in bytes patterns or string patterns with the ASCII flag.
                    In string patterns without the ASCII flag, it will match the
                    range of Unicode alphanumeric characters (letters plus digits
                    plus underscore).
                    With LOCALE, it will match the set [0-9_] plus characters defined
                    as letters for the current locale.
            \W       Matches the complement of \w.
        OK
            \\       Matches a literal backslash.


    Good practice pattern to introduce early for easing the players into the game. 
    Though the max_lengths of these things can make some puzzles look scary, they're usually pretty easy to solve and learn the basics.
    Highly valuable for large match lengths.
        []       Indicates a set of characters.
                A "^" as the first character indicates a complementing set.

    Amazing if you want to make really long patterns, and may also be decent for a single character with length always >=3
        "|"      A|B, creates an RE that will match either A or B.

    Not really dealing with the rest of these for now.
        (...)    Matches the RE inside the parentheses.
                The contents can be retrieved or matched later in the string.
        (?aiLmsux) The letters set the corresponding flags defined below.
        (?:...)  Non-grouping version of regular parentheses.
        (?P<name>...) The substring matched by the group is accessible by name.
        (?P=name)     Matches the text matched earlier by the group named name.
        (?#...)  A comment; ignored.
        (?=...)  Matches if ... matches next, but doesn't consume the string.
        (?!...)  Matches if ... doesn't match next.
        (?<=...) Matches if preceded by ... (must be fixed length).
        (?<!...) Matches if not preceded by ... (must be fixed length).
        (?(id/name)yes|no) Matches yes pattern if the group with id/name matched,
                        the (optional) no pattern otherwise.
"""
# class Pattern(object):
#     pattern:str
#     ambiguity:float


class PatternBase(object):

    def __init__(self, str_target, max_len, no_filter=True, *args, **kwargs):
        self.target = str_target
        self.max_len = max_len
        self.ambiguity = 0
        self.no_filter = no_filter
        self.charset = string.ascii_letters + string.digits + \
            string.punctuation + string.whitespace

    def generate_batch(self, batch_size=1, ambiguity_threshold=4):
        for _ in range(batch_size):
            r, amb = self.__generate__()
            if self.no_filter or amb <= ambiguity_threshold:
                yield (r, amb)
            else:
                print(
                    f'Pattern {r} was excluded due to high ambiguity score:{amb}')

    def generate(self, ambiguity_threshold=4, sort_idx=2):
        print(ambiguity_threshold, sort_idx)
        if patterns := self.__generate__():
            # Sort by ambiguity
            ranked = sorted(patterns, key=lambda x: x[sort_idx], reverse=True)
            for p in ranked:
                if self.no_filter or p[sort_idx] <= ambiguity_threshold:
                    yield p
                else:
                    print(
                        f'Pattern {p[1]} was excluded due to high ambiguity score:{p[sort_idx]}')

    def split_maxlen(self, maxlen=3):
        if len(self.target) < maxlen or self.no_split:
            target = [self.target]
        else:
            target = self.random_split(self.target)
        self._target = target
        return target

    @staticmethod
    def random_split(t):
        if len(t) <= 1:
            return t
        splits = [0] + sorted(sample(range(1, len(t) - 1),
                                     k=int(len(t)**(0.5)))) + [len(t)-1]
        t = [t[splits[i]:splits[i+1]] for i in range(len(splits) - 1)]
        return t


class SingletonPattern(PatternBase):

    """
        USAGE
        for i, _s in enumerate(t.split(' ')):
            pos = -1 if i == len(t.split(' '))-1 else i
            max_len = 1 if pos <=0 else len(_s)
            s = SingletonPattern(_s , max_len, pos)
            # r, amb = s.__generate__()
            # print(amb, r)
            for r, amb in s.generate_batch(2, 7):
                print(amb, r)
    """

    def __init__(self, str_target, max_len, pos, *args, **kwargs):
        # IMPORTANT : pos must be -1 for the character before termination string ie last character/word
        super().__init__(str_target, max_len)
        self.position = pos
        # Sorted by their ambiguity in ascending order
        self.charset = ['^', '$', '?', '+', '*', '.']

    def __generate__(self, amb_norm=10, p_decay=0.5):
        # generate for the given max_len and str_target.
        re_str = None
        p_weights = [amb_norm*(1-p_decay)**i for i in range(4)]
        ambs = [(amb_norm-x)+1 for x in p_weights]
        charset = dict(zip(self.charset[2:], ambs))

        if self.max_len == 1:
            if self.position == 0:
                re_str = self.charset[0]
            elif self.position == -1:
                re_str = self.charset[1]
        else:
            re_str = choices(self.charset[2:],
                             weights=p_weights, k=self.max_len)
            self.ambiguity = sum(
                map(lambda x: charset[x] * re_str.count(x), charset.keys()))

        self.ambiguity += sum(map(lambda x: re_str.count(x),
                              self.charset)) if re_str else 0
        return rf'{re_str}', self.ambiguity


class RepetitionWordPattern(PatternBase):
    """
    USAGE
    t = 'A happy hippo hopped and hiccupped'
    for i, _s in enumerate(t.split(' ')):
        s = RepetitionWordPattern(_s )
        for i, r, amb in s.generate():
            print(amb, r)
    """

    def __init__(self, str_target, max_len=5):
        super().__init__(str_target, max_len)

    def __generate__(self):
        # Greedy search for repetitions of length 2 or more
        rep_regr = re.compile(r"(.+?)\1+")
        r = []
        for match in rep_regr.finditer(self.target):
            index, match_str, reps = match.start(), match.group(
                1), int(len(match.group(0))/len(match.group(1)))

            if reps > 2:
                reps_str = f'{"1" if random() < 0.5 else "0"}, {reps}'
            else:
                reps_str = reps

            r.append((index, rf'{match_str}{{{reps_str}}}',
                     ((index + 1) * len(match_str) * reps)-1))

        return r

    def generate(self, ambiguity_threshold=10, sort_idx=2):
        return super().generate(ambiguity_threshold, sort_idx)


class SpecialCharSeqPattern(PatternBase):
    """
    USAGE
    t = '(May) the local multiplayer be with you hahaha'
    t = PatternBase.random_split(t)

    pprint(t)
    for i, _s in enumerate(t):
        pos = -1 if i == len(t)-1 else i
        max_len = 1 if pos <= 0 else len(_s)
        s = SpecialCharSeqPattern(_s, max_len, pos)
        pprint(s.__generate__())
        # for p in s.generate():
        #     print(p)
        print(s.ambiguity)
        print("*"*20)

    """

    def __init__(self, str_target, max_len, pos, *args, **kwargs):
        super().__init__(str_target, max_len)
        # Sorted by their ambiguity in ascending order
        self.position = pos
        self.charset = {
            'ends': (
                '\A',  # Matches start of string, similar to ^
                '\b',  # Matches empty string at the begining or end of a string, not in use in this implementation
                '\Z',  # Matches end of string, similar to $
            ),
            'groups': (
                '\s',  # Matches whitespace
                '\w',  # Matches alphanumeric characters only
                '\d',  # Matches digits only
                # '\B',  # Matches empty string NOT at the begining or end of a string
                '\W',  # Matches the complement of any alphanumeric character, mostly special chars
                '\S',  # Matches non-whitespace characters
                '\D',  # Matches non-digit characters
            ),
            'specials':
                f'[{string.punctuation}]'  # Matches escaped special characters
        }

    def __generate__(self, amb_norm=10, p_decay=0.5):
        r = []
        for i, ch in enumerate(self.target):
            # Enumerate all possible patterns that match the token 'ch'
            matches = deque()
            # ends
            if (self.position == 0 and i == 0) or (self.position == -1 and i == self.max_len):
                matches.append(self.charset['ends'][self.position])
            # groups
            for pat in self.charset['groups']:
                p = re.compile(pat)
                if p.match(ch):
                    matches.append(pat)
            # special chars
            spec_pat = re.compile(self.charset['specials'])
            if m := spec_pat.match(ch):
                matches.appendleft(f'\\{m.string}')

            # Rank them based on ambiguity
            p_weights = [amb_norm*(1-p_decay)**i for i in range(len(matches))]
            ambs = [(amb_norm-x)+1 for x in p_weights]

            # Randomly choose one pattern per token
            picks = choices(range(len(matches)), weights=p_weights, k=2)

            # Store the ambiguity of each pattern
            r.append((matches[picks[0]], ambs[picks[0]]))

        self.ambiguity = sum([x[1] for x in r])
        return r

    def generate(self, ambiguity_threshold=10, sort_idx=1):
        return super().generate(ambiguity_threshold, sort_idx)


class SetPattern(PatternBase):
    """
    USAGE
    t = 'Six sick hicks nick six slick bricks with picks and sticks'

    t = PatternBase.random_split(t)

    pprint(t)
    print("*"*20)

    for i, _s in enumerate(t):
        s = SetPattern(_s)
        pprint(s.__generate__())
        print("*"*20)
    """

    def __init__(self, str_target, max_len=2, allow_complement=False, max_ambiguity=3, greedy_threshold=0.25, no_split=False):
        super().__init__(str_target, max_len)
        self.max_len = len(str_target) + max_len + \
            max_ambiguity + int(allow_complement)
        self.complement = allow_complement
        self.max_amb = max_ambiguity
        self.greedy_threshold = greedy_threshold
        self.no_split = no_split

    def stringify(self, s, length=-1):
        if length > 1 or len(self.target) > 1:
            s += choice(['+', '*'])
        elif random() < self.greedy_threshold:
            s += choice(['?', '*'])
        return s

    def __generate__(self, amb_multiplier=2):
        c = Counter(self.target)
        s = [x if x != ' ' else '\s' for x in c.keys()]
        # Add extra garbage chars, one or more
        extra_garbage = choices(
            self.charset[:len(self.charset)//2], k=randint(1, self.max_amb))

        # Remove dupes if any
        s = list(set().union(s, extra_garbage))
        shuffle(s)

        if self.complement:
            s = list(set(string.ascii_letters) - set(s))[:len(s)]

        self.ambiguity = amb_multiplier * len(extra_garbage) + sum(c.values())

        return self.stringify(f"[{'^' if self.complement else ''}{''.join(s)}]"), self.ambiguity

    def generate(self, ambiguity_threshold=6, sort_idx=1):
        return super().generate(ambiguity_threshold, sort_idx)


class RangeSetPattern(SetPattern):
    """
    USAGE
    t = 'Six sick hicks nick six slick bricks with picks and sticks'
    t = PatternBase.random_split(t)
    pprint(t)
    print("*"*20)

    for i, _s in enumerate(t):
        s = RangeSetPattern(_s)
        pprint(s.__generate__())
        print(s._target) # List of sets generated for the given target
        print("*"*20)
    """

    def rand_range_offset(self, lower, upper, offset_lo, offset_hi, bound_lo, bound_hi):
        return max(bound_lo, lower - randint(offset_lo, offset_hi)), min(bound_hi, upper + randint(offset_lo, offset_hi))

    def __generate__(self, min_offset=1, max_offset=10):
        target = self.split_maxlen()

        r = []
        for t in target:
            # Group the ords by the following ranges:
            upper_case, lower_case = [91, 64], [123, 96]
            pat = []  # this will contain anything inside the [] for the current target
            for x in t:
                chord = ord(x)
                # consolidate the groups into minimal range sets
                if x.isupper():
                    upper_case = min(upper_case[0], chord), max(
                        upper_case[1], chord)
                elif x.islower():
                    lower_case = min(lower_case[0], chord), max(
                        lower_case[1], chord)
                elif ('\s' not in pat) and chord == 32:
                    # if space has 0 amb -> don't use it
                    pat.append(('\s', not(self.complement)))
                else:
                    pat.append((x, 2))

            for i, v in enumerate([upper_case, lower_case]):
                real_bounds = (65, 90) if not(i) else (97, 122)
                if v[0] > v[1]:
                    continue

                if self.complement:
                    # Alternatively, we could use set.difference of the respective upper/lower case
                    # letters and string.ascii_* to collect the excluded letters,but this method works
                    # slightly better for ranges in this case since we're already calculating range bounds.
                    if abs(v[0] - real_bounds[0]) > abs(v[1] - real_bounds[1]):
                        v = [real_bounds[0] +
                             round(random()), v[0] - (max_offset + 1)]
                    else:
                        v = [v[1] + (max_offset + 1),
                             real_bounds[1] - round(random())]

                # add the offsets to the bounds
                left_b, right_b = self.rand_range_offset(
                    v[0], v[1], min_offset, max_offset, *real_bounds)
                pat.append((f"{chr(left_b)}-{chr(right_b)}",
                            (v[0] - left_b + right_b - v[1])))

            shuffle(pat)
            # calculate the ambiguity values based on the offsets
            amb = sum([x[1] for x in pat])

            if self.complement:
                pat.insert(0, ('^', 2*amb))

            # stringify and return each val
            r.append((self.stringify(
                f'[{"".join([x[0] for x in pat])}]', len(t)), amb))
        return r

    def generate(self, ambiguity_threshold=6, sort_idx=1):
        return super().generate(ambiguity_threshold, sort_idx)


class ORPattern(PatternBase):
    """
    USAGE
    t = 'Six sick hicks nick six slick bricks with picks and sticks'

    t = PatternBase.random_split(t)

    pprint(t)
    print("*"*20)

    for i, _s in enumerate(t):
        # pos = -1 if i == len(t)-1 else i
        # max_len = 1 if pos <= 0 else len(_s)
        s = ORPattern(_s)
        pprint(s.__generate__())
        print(s._target)
        # for p in s.generate():
        #     print(p)
        # print(s.ambiguity)
        print("*"*20)
    """

    def __init__(self, str_target, max_len=2, no_split=False):
        assert max_len >= 2
        super().__init__(str_target, max_len)
        self.no_split = no_split

    def __generate__(self, amb_multiplier=5):
        r = []
        target = self.split_maxlen()
        for t in target:
            s = t.replace(' ', '\s')
            pat = [s]
            pat += ["".join(choices(string.ascii_letters, k=len(t)))
                    for k in range(self.max_len-1)]
            x = "|".join(pat)

            if not(self.no_split):
                # replace this with group pattern at some point
                x = f'({x})'

            r.append((x, int((amb_multiplier + self.max_len)/(len(t)**0.5))))
        # calculate ambiguity values
        return r

    def generate(self, ambiguity_threshold=6, sort_idx=1):
        return super().generate(ambiguity_threshold, sort_idx)


# class GroupPattern(PatternBase):
#     """
#     """

#     def __init__(self, str_target, max_len):
#         raise NotImplementedError()


class PatternGenerator(object):

    generators = {
        'simple': SingletonPattern,
        'reps': RepetitionWordPattern,
        'spec_chars': SpecialCharSeqPattern,
        'set': SetPattern,
        'range': RangeSetPattern,
        'lor': ORPattern
    }

    def __init__(self, s: str, max_chunk_len: int, batch_size):
        self.s = s
        self.chunk_size = max_chunk_len
        self.batch_size = batch_size
        self.list = []
        raise NotImplementedError()

    def __iter__(self):
        for x in self.list:
            yield x


if __name__ == '__main__':

    # Extend your PC with your phone.
    # t = 'Two-player gaming made easy with socketJoy'
    # t = 'May the local multiplayer be with you hahaha'
    # t = 'Wireless game controller For Any Game'
    # t = 'A happy hippo hopped and hiccupped'
    t = 'Six sick hicks nick six slick bricks with picks and sticks'

    t = PatternBase.random_split(t)

    pprint(t)
    print("*"*20)

    for i, _s in enumerate(t):
        # pos = -1 if i == len(t)-1 else i
        # max_len = 1 if pos <= 0 else len(_s)
        s = ORPattern(_s)
        pprint(s.__generate__())
        print(s._target)
        # for p in s.generate():
        #     print(p)
        # print(s.ambiguity)
        print("*"*20)
