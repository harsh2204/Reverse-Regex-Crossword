# import numpy as np
from random import randint, sample, choices, random
import string
from pprint import pprint
import re
from collections import Counter

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

class PatternBase(object):

    def __init__(self, str_target, max_len, no_filter=True, *args, **kwargs):
        self.target = str_target
        self.max_len = max_len
        self.ambiguity = 0
        self.no_filter = no_filter


    def random_splice(t, lo, hi):
        no_splices = randint(lo, hi)
        splices = [0] + sorted(choices(range(1, len(t)-1), k=no_splices)) + [len(t)-1] # small chance of adding extra entries
        spliced = [t[splices[i]:splices[i+1]] for i in range(len(splices)-1)]
        return spliced


    def generate_batch(self, batch_size= 1, ambiguity_threshold=4):
        for _ in range(batch_size):
            r, amb = self.__generate__()
            if self.no_filter or amb <= ambiguity_threshold:
                yield (r, amb)
            else:
                print(f'Pattern {r} was excluded due to high ambiguity score:{amb}')
    

    def generate(self, ambiguity_threshold= 4, sort_idx=2):
        if patterns := self.__generate__():
            ranked = sorted(patterns, key=lambda x: x[sort_idx], reverse=True) # Sort by ambiguity
            for p in ranked:
                if self.no_filter or p[sort_idx] <= ambiguity_threshold:
                    yield p
                else:
                    print(f'Pattern {p[1]} was excluded due to high ambiguity score:{p[sort_idx]}')


    # class SimplePattern(PatternBase):
    # class SimpleORS(PatternBase):
    # class ORS(PatternBase):
    # class Range(PatternBase):
    # class RangeSet(PatternBase):
    # class Pattern(object):

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
        super().__init__(str_target, max_len)
        self.position = pos
        # Sorted by their ambiguity in ascending order
        self.charset = ['^', '$', '?', '+', '*', '.']

    def __generate__(self, amb_norm = 10, p_decay = 0.5):
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
            re_str = choices(self.charset[2:], weights=p_weights, k = self.max_len)
            self.ambiguity = sum(map(lambda x: charset[x] * re_str.count(x), charset.keys()))
                 
        
        self.ambiguity += sum(map(lambda x: re_str.count(x), self.charset)) if re_str else 0
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
    def __init__(self, str_target):
        super().__init__(str_target, 5)
        
    def __generate__(self):
        rep_regr = re.compile(r"(.+?)\1+") # Greedy search for repetitions of length 2 or more
        r = []
        for match in rep_regr.finditer(self.target):
            index, match_str, reps = match.start(), match.group(1), int(len(match.group(0))/len(match.group(1)))

            if reps > 2:
                reps_str = f'{"1" if random() < 0.5 else "0"}, {reps}'
            else:
                reps_str = reps

            r.append((index, rf'{match_str}{{{reps_str}}}', ((index + 1)* len(match_str)* reps)-1))

        return r

        
    def generate(self, ambiguity_threshold= 10, sort_idx=2):
        return super().generate(ambiguity_threshold, sort_idx)

class SpecialCharPattern(PatternBase):
    """
    t = 'Six sick hicks nick six slick bricks with picks and sticks'
    print(len(t), t)
    spliced = PatternBase.random_splice(t, 3, 6)
    print(spliced)
    for i, _s in enumerate(spliced):
        s = SpecialCharPattern(_s, 0)
        s.__generate__()
    """

    def __init__(self, str_target, pos, max_len=2, amb_norm = 10, p_decay = 0.5, *args, **kwargs):
        super().__init__(str_target, max_len)
        self.position = pos
        self.charset = {
                        'whitespace':[
                            (r'\S', lambda s,t: ('whitespace_0', t)), # matches non-whitespace/words
                            (r'\s', lambda s,t: ('whitespace_1', t)), # matches whitespace
                        ],
                        'digits':[
                            (r'\D', lambda s,t: ('digits_0', t)), # matches non digit, same as [^0-9]
                            (r'\d', lambda s,t: ('digits_1', t)), # matches digit
                        ],
                        'ends':[
                            (r'\A' , lambda s,t: ('ends_0', t)), # ^
                            (r'\Z' , lambda s,t: ('ends_1', t)), # $
                            (r'\b' , lambda s,t: ('ends_2', t)), # matches non-words/whitespace in ends. USE to mark begining/end of string
                            (r'\B' , lambda s,t: ('ends_3', t)), # matches digits and words not in the end. example 'py\B' => 'py2', 'python', but not 'py.' or 'py!'
                        ],
                        'words':[
                            (r'\W' , lambda s,t: ('words_0', t)), # matches non-words, includes special chars like !@#$%^...
                            (r'\w' , lambda s,t: ('words_1', t)), # matches words
                        ],
                        # '\\n'  # backref to the nth matching group
                        }


        for i, c in enumerate(self.charset.items(), 1):
            k, v = c
            p_weights = [amb_norm*(1-p_decay)**j for j in range(len(v))]
            ambs = [(amb_norm-x)+i for x in p_weights]
            if k == 'ends':
                p_weights = [5, 5, 2.5, 1]
                ambs = [2, 2, 5, 10]
            self.charset[k] = list(zip(v, p_weights, ambs))


    def __generate__(self, ambiguity_threshold=6):
        r = []
        # Ends management
        if random() > 0.25:
            if self.position == 0:
                r.append((0, self.charset['ends'][0][0], self.charset['ends'][0][-1]))
            elif self.position == -1:
                r.append((-1, self.charset['ends'][1][0], self.charset['ends'][1][-1]))
        else:
            if self.position <=0:
                r.append((self.position, self.charset['ends'][2][0], self.charset['ends'][2][-1]))
    
        # The rest
        for k, v in self.charset.items():
            pats = choices(v, weights=[x[1] for x in v], k = len(v))
            scanner_list = [x[0] for x in v if self.no_filter or x[-1] <= ambiguity_threshold]

            # print('*'*80)
            sc = re.Scanner(scanner_list)
            stuff = sc.scan(self.target)
            print(len(stuff), k, stuff)
            if stuff[0]:
                counts = Counter([(x[0]) for x in stuff[0]])
                pprint(counts)
                if len(counts) > 1:
                    key = min(counts, key=counts.get)
                    pat = v[int(key.split('_')[-1])]
                    reg, amb = pat[0][0], pat[-1]
                    print(key, counts[key], reg, amb)
                    print('*'*80)
                else:
                    continue
                

            # if 


if __name__ == '__main__':
    # Extend your PC with your phone.
    # t = 'Two-player gaming made easy with socketJoy'
    # t = 'May the local multiplayer be with you hahaha'
    # t = 'Wireless game controller For Any Game'
    # t = 'A happy hippo hopped and hiccupped'
    t = 'Six sick hicks nick six slick, bricks with picks and sticks'
    print(len(t), t)
    spliced = PatternBase.random_splice(t, 3, 6)
    print(spliced)
    # for i, _s in enumerate(t.split(' ')[:1]):
    for i, _s in enumerate(spliced):
        s = SpecialCharPattern(_s, i)
        s.__generate__()
    # for i, r, amb in s.generate():
    #     print(i, amb, r)

