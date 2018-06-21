import unittest
import library

NUM_CORPUS = '''
On the 5th of May every year, Mexicans celebrate Cinco de Mayo. This tradition
began in 1845 (the twenty-second anniversary of the Mexican Revolution), and
is the 1st example of a national independence holiday becoming popular in the
Western Hemisphere. (The Fourth of July didn't see regular celebration in the
US until 15-20 years later.) It is celebrated by 77.9% of the population--
trending toward 80.                                                                
'''


class TestCase(unittest.TestCase):

    # Helper function
    def assert_extract(self, text, extractors, *expected):
        actual = [x[1].group(0) for x in library.scan(text, extractors)]
        self.assertEquals(str(actual), str([x for x in expected]))

    # First unit test; prove that if we scan NUM_CORPUS looking for mixed_ordinals,
    # we find "5th" and "1st".
    def test_mixed_ordinals(self):
        self.assert_extract(NUM_CORPUS, library.mixed_ordinals, '5th', '1st')

    # Second unit test; prove that if we look for integers, we find four of them.
    def test_integers(self):
        self.assert_extract(NUM_CORPUS, library.integers, '1845', '15', '20', '80')

    # Third unit test; prove that if we look for integers where there are none, we get no results.
    def test_no_integers(self):
        self.assert_extract("no integers", library.integers)

    # Fourth unit test; prove that if we can scan date from given text
    def test_dates_ios8601(self):
        self.assert_extract("I was born on 2015-07-25.", library.dates_iso8601, '2015-07-25')

    # Fifth unit test; prove if invalid dates are not scanned
    def test_no_dates(self):
        self.assert_extract("I was born on 2015-13-25.", library.dates_iso8601)

    # Sixth unit test; prove that we are able to scan other date formats
    def test_dates_other_format(self):
        self.assert_extract("I was born on 25 Jan 2017.", library.dates_other, '25 Jan 2017')

    # ---------- test cases for new requirements

    # Unit test; 2018-06-22 18:22:19.123".
    def test_dates_ios8601_with_timestamp_with_space_delim(self):
        self.assert_extract("I was born on 2018-06-22 18:22:19.123.", library.dates_iso8601,
                            '2018-06-22 18:22:19.123')

    # Unit test; 2018-06-22T18:22:19.123".
    def test_dates_ios8601_with_timestamp_with_T_delim(self):
        self.assert_extract("I was born on 2018-06-22T18:22:19.123.", library.dates_iso8601,
                            '2018-06-22T18:22:19.123')

    # Unit test; 2018-06-22 18:22:19.123".
    def test_dates_ios8601_with_timestamp_till_millis(self):
        self.assert_extract("I was born on 2018-06-22 18:22:19.123.", library.dates_iso8601, '2018-06-22 18:22:19.123')

    # Unit test; 2018-06-22 18:22:19".
    def test_dates_ios8601_with_timestamp_till_second(self):
        self.assert_extract("I was born on 2018-06-22 18:22:19.", library.dates_iso8601, '2018-06-22 18:22:19')

    # Unit test; 2018-06-22 18:22".
    def test_dates_ios8601_with_timestamp_till_minute(self):
        self.assert_extract("I was born on 2018-06-22 18:22.", library.dates_iso8601, '2018-06-22 18:22')

    # Unit test; 2018-06-22 18:22:19.123 MDT".
    def test_dates_ios8601_with_timestamp_with_timezone_format1(self):
        self.assert_extract("I was born on 2018-06-22 18:22:19.123 MDT.", library.dates_iso8601, '2018-06-22 18:22:19.123 MDT')

    # Unit test; 2018-06-22 18:22:19.123 +05:30".
    def test_dates_ios8601_with_timestamp_with_timezone_format2(self):
        self.assert_extract("I was born on 2018-06-22 18:22:19.123 +05:30.", library.dates_iso8601, '2018-06-22 18:22:19.123 +05:30')

    # Unit test; 2018-06-22 18:22:19.123 +0530".
    def test_dates_ios8601_with_timestamp_with_timezone_format3(self):
        self.assert_extract("I was born on 2018-06-22 18:22:19.123 +0530.", library.dates_iso8601,
                            '2018-06-22 18:22:19.123 +0530')

    # Unit test; 2018-06-22 18:22:19.123 Z".
    def test_dates_ios8601_with_timestamp_with_timezone_format4(self):
        self.assert_extract("I was born on 2018-06-22 18:22:19.123 Z.", library.dates_iso8601, '2018-06-22 18:22:19.123 Z')

    # Unit test; other date format with comma, 25 Jan, 2017
    def test_dates_other_format_1(self):
        self.assert_extract("I was born on 25 Jan, 2017.", library.dates_other, '25 Jan, 2017')

    # Unit test; extracting numbers with comma in between
    def test_integers_other_format_1(self):
        self.assert_extract("123,456,789", library.integers, '123', '456', '789')


if __name__ == '__main__':
    unittest.main()
