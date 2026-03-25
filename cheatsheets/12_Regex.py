import re

# ── BASIC METHODS ────────────────────────────────────────────
re.match(r'Hello', 'Hello World')       # match only at START of string → match object
re.search(r'World', 'Hello World')      # scan entire string → first match or None
re.findall(r'\d+', '10 apples, 20 oranges')  # all matches → ['10', '20']
re.finditer(r'\d+', '10 apples, 20')   # like findall but returns iterator of match objects

# re.fullmatch — cały string musi pasować do wzorca (nic nie może wystawać)
re.fullmatch(r'\d{3}', '123')   # match
re.fullmatch(r'\d{3}', '1234')  # None — za długi

# always check for None before calling .group()
m = re.search(r'BTS_\w+', 'ERROR BTS_WRO_01')
if m:
    print(m.group())    # 'BTS_WRO_01' — full match
    print(m.start())    # index where match starts
    print(m.end())      # index where match ends
    print(m.span())     # (start, end) as tuple

# ── MODIFYING STRINGS ────────────────────────────────────────
re.sub(r'red', 'blue', 'red house, red car')        # 'blue house, blue car'
re.sub(r'red', 'blue', 'red house, red car', count=1)  # replace only first occurrence
re.split(r'\s*,\s*', 'apple, banana,  cherry')      # ['apple','banana','cherry']

# re.subn — jak sub, ale zwraca też liczbę zamian
result, n = re.subn(r'red', 'blue', 'red house, red car')
# result = 'blue house, blue car', n = 2

# ── COMPILE — reuse a pattern many times ─────────────────────
pattern = re.compile(r'\d{3}')          # compile once
pattern.findall('123 and 456')          # ['123', '456']
pattern.search('abc 789')              # match object

# skompilowany wzorzec ma te same metody co moduł re:
# pattern.match(), pattern.search(), pattern.findall(), pattern.sub() itd.

# ── META-CHARACTERS ──────────────────────────────────────────
# .        any character except newline
# ^        start of string (or line with re.MULTILINE)
# $        end of string (or line with re.MULTILINE)
# |        OR operator:  cat|dog matches 'cat' or 'dog'
# \        escape a special character: \. matches a literal dot

re.search(r'^Start.*End$', 'Start to End')   # anchors: must start AND end as specified

# ── QUANTIFIERS ──────────────────────────────────────────────
# *        0 or more:   ab*  matches 'a', 'ab', 'abbb'
# +        1 or more:   ab+  matches 'ab', 'abbb'  (not 'a')
# ?        0 or 1:      ab?  matches 'a' or 'ab'
# {n}      exactly n:   \d{4}  matches '2026'
# {n,m}    between n and m:  \d{2,4}  matches '12', '123', '1234'

re.findall(r'ab*', 'abbb')      # ['abbb']
re.findall(r'\d{2,4}', '1 12 123 1234 12345')  # ['12', '123', '1234', '1234']

# ── GREEDY VS NON-GREEDY ─────────────────────────────────────
# quantifiers are greedy by default — match as MUCH as possible
re.search(r'<.*>', '<a> <b>').group()    # '<a> <b>'  — eats everything

# add ? to make non-greedy — match as LITTLE as possible
re.search(r'<.*?>', '<a> <b>').group()  # '<a>'  — stops at first >

# ── SPECIAL SEQUENCES ────────────────────────────────────────
# \d   any digit 0-9          \D  any non-digit
# \w   word char (a-z A-Z 0-9 _)  \W  non-word char
# \s   whitespace (space \t \n)   \S  non-whitespace
# \b   word boundary              \B  non-boundary
# \A   start of string (unlike ^ nie zmienia się z re.MULTILINE)
# \Z   end of string   (unlike $ nie zmienia się z re.MULTILINE)

re.findall(r'\d', 'ID: 123')            # ['1','2','3']
re.findall(r'\D', 'ID: 123')            # ['I','D',':',' ']
re.findall(r'\w+', 'Python_3.10 cool!') # ['Python_3', '10', 'cool']
re.findall(r'\s', 'A B C')             # [' ',' ']
re.findall(r'\S+', 'A B C')            # ['A','B','C']
re.findall(r'\bcat\b', 'cat concatenate')  # ['cat'] — whole word only

re.search(r'\AHello', 'Hello World')   # zawsze startuje od początku stringa
re.search(r'World\Z', 'Hello World')   # zawsze kończy na końcu stringa

# ── CHARACTER SETS & RANGES ──────────────────────────────────
# [abc]    matches a, b, or c
# [^abc]   matches anything except a, b, c
# [a-z]    any lowercase letter
# [A-Z]    any uppercase letter
# [0-9]    any digit (same as \d)
# [a-zA-Z0-9_]  same as \w

re.findall(r'[aeiou]', 'interactive')   # all vowels
re.findall(r'[^0-9]', 'Room 101')       # everything except digits
re.findall(r'[A-Z]{2,}', 'ERROR BTS_WRO_01 ACTIVE')  # ['ERROR','BTS','WRO','ACTIVE']

# ── GROUPS & CAPTURING ───────────────────────────────────────
# (...)    capturing group — extract parts of the match
# (?:...)  non-capturing group — group without storing

m = re.search(r'(\d+)-(\w+)', '123-ABC')
m.group(0)  # '123-ABC' — full match
m.group(1)  # '123'     — first group
m.group(2)  # 'ABC'     — second group
m.groups()  # ('123', 'ABC') — all groups as tuple

# named groups — more readable than numbered
m = re.search(r'(?P<year>\d{4})-(?P<month>\d{2})', '2026-03-14')
m.group('year')     # '2026'
m.group('month')    # '03'
m.groupdict()       # {'year': '2026', 'month': '03'}

# non-capturing group — used for grouping without extracting
re.findall(r'(?:cat|dog)s?', 'cats and dogs')  # ['cats', 'dogs']

# OR operator
re.findall(r'cat|dog', 'The cat and the dog')   # ['cat', 'dog']

# ── BACKREFERENCES ───────────────────────────────────────────
# \1, \2, ... odwołują się do poprzednio dopasowanej grupy
# przydatne do wykrywania powtórzeń

re.search(r'(\w+) \1', 'the the fox')           # dopasuje 'the the'
re.findall(r'(\w+) \1', 'ha ha ho ho yes')      # ['ha', 'ho']

# w re.sub można używać \1 lub \g<1> / \g<name> w stringu zastępującym
re.sub(r'(\w+) \1', r'\1', 'the the fox')       # 'the fox' — usuwa duplikat

# named backreference
re.search(r'(?P<word>\w+) (?P=word)', 'ha ha')  # dopasuje 'ha ha'

# ── LOOKAHEAD & LOOKBEHIND (zero-width assertions) ───────────
# Sprawdzają co jest przed/po dopasowaniu, ale NIE konsumują znaków
# (dopasowanie nie zawiera tego co jest w lookahead/lookbehind)

# (?=...)   positive lookahead  — to co następuje MUSI pasować
re.findall(r'\d+(?= zł)', '100 zł i 200 euro')         # ['100'] — tylko liczba przed " zł"

# (?!...)   negative lookahead  — to co następuje NIE MOŻE pasować
re.findall(r'\d+(?! zł)', '100 zł i 200 euro')         # ['200']

# (?<=...)  positive lookbehind — to co poprzedza MUSI pasować
re.findall(r'(?<=@)\w+', 'user@example.com')            # ['example']

# (?<!...)  negative lookbehind — to co poprzedza NIE MOŻE pasować
re.findall(r'(?<!\d)\d{3}(?!\d)', 'abc 123 4567')       # ['123'] — dokładnie 3 cyfry

# praktyczny przykład: cena bez jednostki
prices = 'buty: 299zł, t-shirt: 89zł'
re.findall(r'(?<=: )\d+', prices)                       # ['299', '89']

# ── FLAGS ────────────────────────────────────────────────────
re.findall(r'python', 'PYTHON is great', re.IGNORECASE)  # ['PYTHON']
re.findall(r'python', 'PYTHON', re.I)           # shorthand

text = "Hello\nWorld"
re.findall(r'^\w+', text, re.MULTILINE)         # ['Hello','World'] — ^ matches each line
re.search(r'.+', 'A\nB', re.DOTALL)            # . matches newline too

# combine flags with |
re.findall(r'python', 'PYTHON\nPython', re.I | re.M)

# re.VERBOSE — pozwala na komentarze i wcięcia wewnątrz wzorca
email_pattern = re.compile(r'''
    ^               # start stringa
    [\w.+-]+        # lokalna część (user)
    @               # małpa
    [\w-]+          # domena
    \.              # kropka
    [a-z]{2,}       # TLD
    $               # koniec stringa
''', re.VERBOSE | re.IGNORECASE)

email_pattern.match('user@example.com')  # match

# ── re.escape — ucieczka ze znaków specjalnych ───────────────
# używaj gdy szukasz dosłownego stringa, który może zawierać znaki specjalne
user_input = 'file.txt (v2.0)'
safe_pattern = re.escape(user_input)    # 'file\\.txt\\ \\(v2\\.0\\)'
re.search(safe_pattern, 'Found: file.txt (v2.0)')  # match — bezpieczne

# ── PRACTICAL PATTERNS ───────────────────────────────────────
# validate station ID: 3 uppercase letters, underscore, digits
def validate_id(station_id):
    return bool(re.match(r'^[A-Z]{3}_\d+$', station_id))

validate_id('WRO_101')  # True
validate_id('wro_101')  # False

# extract all numbers from a log line
log = 'ERROR 2026-03-03 BTS_WRO_01 Temp: 55C'
re.findall(r'\d+', log)                 # ['2026', '03', '03', '01', '55']

# validate email (simplified)
re.match(r'^[\w.+-]+@[\w-]+\.[a-z]{2,}$', 'user@example.com')

# validate Polish phone number
re.match(r'^(\+48)?[\s-]?\d{3}[\s-]?\d{3}[\s-]?\d{3}$', '+48 123 456 789')

# redact sensitive data
re.sub(r'BTS_\w+', 'REDACTED', log)     # 'ERROR 2026-03-03 REDACTED Temp: 55C'

# split on any whitespace or comma
re.split(r'[\s,]+', 'one, two  three,four')  # ['one','two','three','four']

# extract date and convert format YYYY-MM-DD → DD.MM.YYYY
re.sub(r'(?P<y>\d{4})-(?P<m>\d{2})-(?P<d>\d{2})', r'\g<d>.\g<m>.\g<y>', '2026-03-25')
# '25.03.2026'

# find all URLs in text
re.findall(r'https?://[\w./-]+', 'visit https://example.com and http://test.pl/page')
# ['https://example.com', 'http://test.pl/page']

# remove HTML comments
re.sub(r'<!--.*?-->', '', '<!-- comment --> <p>text</p>', flags=re.DOTALL)
# ' <p>text</p>'

# camelCase → snake_case
def camel_to_snake(name):
    name = re.sub(r'(?<=[a-z])(?=[A-Z])', '_', name)   # lookbehind + lookahead
    return name.lower()

camel_to_snake('camelCaseVariable')  # 'camel_case_variable'