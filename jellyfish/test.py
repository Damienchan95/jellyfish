# -*- coding: utf-8 -*-
import sys
if sys.version_info[0] < 3:
    import unicodecsv as csv
else:
    import csv
import platform
import pytest


def assertAlmostEqual(a, b, places=3):
    assert abs(a - b) < (0.1**places)


if platform.python_implementation() == 'CPython':
    implementations = ['python', 'c']
else:
    implementations = ['python']


@pytest.fixture(params=implementations)
def jf(request):
    if request.param == 'python':
        from jellyfish import _jellyfish as jf
    else:
        from jellyfish import cjellyfish as jf
    return jf

def _load_data(name):
    with open('testdata/{}.csv'.format(name)) as f:
        for data in csv.reader(f):
            yield data

@pytest.mark.parametrize("s1,s2,value", _load_data('jaro_winkler'), ids=str)
def test_jaro_winkler(jf, s1, s2, value):
    value = float(value)
    assertAlmostEqual(jf.jaro_winkler(s1, s2), value, places=3)


@pytest.mark.parametrize("s1,s2,value", _load_data('jaro_distance'), ids=str)
def test_jaro_distance(jf, s1, s2, value):
    value = float(value)
    assertAlmostEqual(jf.jaro_distance(s1, s2), value, places=3)


@pytest.mark.parametrize("s1,s2,value", _load_data('hamming'), ids=str)
def test_hamming_distance(jf, s1, s2, value):
    value = int(value)
    assert jf.hamming_distance(s1, s2) == value


@pytest.mark.parametrize("s1,s2,value", _load_data('levenshtein'), ids=str)
def test_levenshtein_distance(jf, s1, s2, value):
    value = int(value)
    assert jf.levenshtein_distance(s1, s2) == value


@pytest.mark.parametrize("s1,s2,value", _load_data('damerau_levenshtein'), ids=str)
def test_damerau_levenshtein_distance(jf, s1, s2, value):
    value = int(value)
    assert jf.damerau_levenshtein_distance(s1, s2) == value


@pytest.mark.parametrize("s1,code", _load_data('soundex'), ids=str)
def test_soundex(jf, s1, code):
    assert jf.soundex(s1) == code


@pytest.mark.parametrize("s1,code", _load_data('metaphone'), ids=str)
def test_metaphone(jf, s1, code):
    assert jf.metaphone(s1) == code


@pytest.mark.parametrize("s1,s2", _load_data('nysiis'), ids=str)
def test_nysiis(jf, s1, s2):
    assert jf.nysiis(s1) == s2


@pytest.mark.parametrize("s1,s2", _load_data('match_rating_codex'), ids=str)
def test_match_rating_codex(jf, s1, s2):
    assert jf.match_rating_codex(s1) == s2


@pytest.mark.parametrize("s1,s2,value", _load_data('match_rating_comparison'), ids=str)
def test_match_rating_comparison(jf, s1, s2, value):
    value = {'True': True, 'False': False, 'None': None}[value]
    assert jf.match_rating_comparison(s1, s2) is value


def test_porter_stem(jf):
    with open('testdata/porter.csv') as f:
        reader = csv.reader(f)
        for (a, b) in reader:
            assert jf.porter_stem(a) == b


if platform.python_implementation() == 'CPython':
    def test_match_rating_comparison_segfault():
        import hashlib
        from jellyfish import cjellyfish as jf
        sha1s = [u'{}'.format(hashlib.sha1(str(v).encode('ascii')).hexdigest())
                 for v in range(100)]
        # this segfaulted on 0.1.2
        assert [[jf.match_rating_comparison(h1, h2) for h1 in sha1s] for h2 in sha1s]

    def test_damerau_levenshtein_distance_type():
        from jellyfish import cjellyfish as jf
        jf.damerau_levenshtein_distance(u'abc', u'abc')
        with pytest.raises(TypeError) as exc:
            jf.damerau_levenshtein_distance(b'abc', b'abc')
            assert 'expected' in str(exc.value)


##def test_levenshtein_distance_type(jf):
##    assert jf.levenshtein_distance(u'abc', u'abc') == 0
##    assert jf.levenshtein_distance(b'abc', b'abc') == 0


##def test_jaro_distance_type(jf):
##    assert jf.jaro_distance(u'abc', u'abc') == 1
##    assert jf.jaro_distance(b'abc', b'abc') == 1


##def test_jaro_winkler_type(jf):
##    assert jf.jaro_winkler(u'abc', u'abc') == 1
##    assert jf.jaro_winkler(b'abc', b'abc') == 1


def test_mra_comparison_type(jf):
    assert jf.match_rating_comparison(u'abc', u'abc') is True
    with pytest.raises(TypeError) as exc:
        jf.match_rating_comparison(b'abc', b'abc')
        assert 'expected' in str(exc.value)


##def test_hamming_type(jf):
##    assert jf.hamming_distance(u'abc', u'abc') == 0
##    assert jf.hamming_distance(b'abc', b'abc') == 0


##def test_soundex_type(jf):
##    assert jf.soundex(u'ABC') == 'A120'
##    assert jf.soundex(b'ABC') == 'A120'


##def test_metaphone_type(jf):
##    assert jf.metaphone(u'abc') == 'ABK'
##    assert jf.metaphone(b'abc') == 'ABK'


##def test_nysiis_type(jf):
##    assert jf.nysiis(u'abc') == 'ABC'
##    assert jf.nysiis(b'abc') == 'ABC'


def test_mr_codex_type(jf):
    assert jf.match_rating_codex(u'abc') == 'ABC'
    with pytest.raises(TypeError) as exc:
        jf.match_rating_codex(b'abc')
        assert 'expected' in str(exc.value)


##def test_porter_type(jf):
##    assert jf.porter_stem(u'abc') == 'abc'
##    assert jf.porter_stem(b'abc') == 'abc'
