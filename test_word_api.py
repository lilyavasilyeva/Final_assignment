import unittest
import requests
import random
import string

host = 'https://wordsapiv1.p.rapidapi.com'
auth_key = {'X-RapidAPI-Key': '66ef45eb8amsh5471d964edc9042p12b4dajsn80565566cd70',
                         'Accept': 'application/json'}
auth_key_wrong = {'X-RapidAPI-Key': '66ef45eb8amsh5471d964edc9042p12b4dajsn80565566cd7',
                         'Accept': 'application/json'}
host_wrong = 'https://wordsapiv1.p.mashape.com'
auth_key_no_accept = {'X-RapidAPI-Key': '66ef45eb8amsh5471d964edc9042p12b4dajsn80565566cd70'}
auth_key_host_in_header = {'X-RapidAPI-Key': '66ef45eb8amsh5471d964edc9042p12b4dajsn80565566cd7',
                         'Accept': 'application/json',
                         'Host': 'https://wordsapiv1.p.rapidapi.com'}
auth_key_no_key = {'Accept': 'application/json'}
auth_key_empty_key = {'X-RapidAPI-Key': '',
                         'Accept': 'application/json'}

details = ['definitions', 'synonyms', 'antonyms', 'examples', 'typeOf', 'hasTypes', 'partOf', 'hasParts',
            'instanceOf', 'hasInstances', 'similarTo', 'also', 'entails', 'memberOf', 'hasMembers',
            'substanceOf', 'hasSubstances', 'inCategory', 'hasCategories', 'usageOf', 'hasUsages', 'inRegion',
            'regionOf', 'pertainsTo']
detail_non_existent = 'hasSynonyms'
json_body = ['results', 'definition', 'partOfSpeech', 'synonyms', 'typeOf', 'derivation']
word = 'word'
detail = random.choice(details)

class get_a_word(unittest.TestCase):

    def test_happy_path(self):
        self.response = requests.get(f'{host}/words/{word}', headers=auth_key)
        self.json = self.response.json()
        self.time = self.response.elapsed.total_seconds()
        self.assertTrue(self.response.status_code == 200, f'Status code is {self.response.status_code}')
        self.assertTrue(self.time < 120, f'Long response time: {self.time}')
        self.assertTrue(
            all([json_body[key] in self.json['results'][result].keys()
                 for key in range(len(json_body)) for result in range(len(self.json['results']))]), f'Wrong response json body structure'
        )

    def test_non_existent_word(self):
        word_ne = 'yuio78'
        self.response = requests.get(f'{host}/words/{word_ne}', headers=auth_key)
        self.json = self.response.json()
        self.time = self.response.elapsed.total_seconds()
        self.assertTrue(self.response.status_code == 404, f'Status code is {self.response.status_code}')
        self.assertTrue(self.time < 120, f'Long response time: {self.time}')
        self.assertTrue(self.json['message'] == 'word not found' and self.json['success'] == False, f'Wrong response json body structure')

    def test_no_word(self):
        word_empty = ''
        self.response = requests.get(f'{host}/words/{word_empty}', headers=auth_key)
        self.json = self.response.json()
        self.time = self.response.elapsed.total_seconds()
        self.assertTrue(self.response.status_code == 400, f'Status code is {self.response.status_code}')
        self.assertTrue(self.time < 120, f'Long response time: {self.time}')
        self.assertTrue(self.json['message'] == 'Word is required.' and self.json['success'] == False, f'Wrong response json body structure')

    def test_happy_path_digits(self):
        word_number = str(random.randint(0, 1000000))
        self.response = requests.get(f'{host}/words/{word_number}', headers=auth_key)
        self.json = self.response.json()
        self.time = self.response.elapsed.total_seconds()
        self.assertTrue(self.response.status_code == 200 or self.response.status_code == 404, f'Status code is {self.response.status_code}')
        self.assertTrue(self.time < 120, f'Long response time: {self.time}')
        if self.response.status_code == 200:
            self.assertTrue(
                all([json_body[key] in self.json['results'][result].keys()
                     for key in range(len(json_body)) for result in range(len(self.json['results']))]),
                f'Wrong response json body structure'
        )
        if self.response.status_code == 404:
            self.assertTrue(self.json['message'] == 'word not found' and self.json['success'] == False,
                            f'Wrong response json body structure')
        #not every number has a definition in the dictionary

    def test_russian_word(self):
        word_ru = 'слово'
        self.response = requests.get(f'{host}/words/{word_ru}', headers=auth_key)
        self.json = self.response.json()
        self.time = self.response.elapsed.total_seconds()
        self.assertTrue(self.response.status_code == 404, f'Status code is {self.response.status_code}')
        self.assertTrue(self.time < 120, f'Long response time: {self.time}')
        self.assertTrue(self.json['message'] == 'word not found' and self.json['success'] == False, f'Wrong response json body structure')

    def test_long_input(self):
        word_long = ''.join([random.choice(string.ascii_letters) for i in range(1000)])
        self.response = requests.get(f'{host}/words/{word_long}', headers=auth_key)
        self.json = self.response.json()
        self.time = self.response.elapsed.total_seconds()
        self.assertTrue(self.response.status_code == 404, f'Status code is {self.response.status_code}')
        self.assertTrue(self.time < 120, f'Long response time: {self.time}')
        self.assertTrue(self.json['message'] == 'word not found' and self.json['success'] == False, f'Wrong response json body structure')

    def test_short_input(self):
        self.response = requests.get(f'{host}/words/a', headers=auth_key)
        self.json = self.response.json()
        self.time = self.response.elapsed.total_seconds()
        self.assertTrue(self.response.status_code == 200, f'Status code is {self.response.status_code}')
        self.assertTrue(self.time < 120, f'Long response time: {self.time}')
        self.assertTrue(
            all([json_body[key] in self.json['results'][result].keys()
                 for key in range(len(json_body)) for result in range(len(self.json['results']))]),
            f'Wrong response json body structure'
        )

    def special_character(self):
        word_spchar = ''.join([random.choice('!@#$%^&*()_+=-?:;№"`~./,\\\'') for i in range(5)])
        self.response = requests.get(f'{host}/words/{word_spchar}', headers=auth_key)
        self.json = self.response.json()
        self.time = self.response.elapsed.total_seconds()
        self.assertTrue(self.response.status_code == 404, f'Status code is {self.response.status_code}')
        self.assertTrue(self.time < 120, f'Long response time: {self.time}')
        self.assertTrue(self.json['message'] == 'word not found' and self.json['success'] == False, f'Wrong response json body structure')

    def test_wrong_auth_key(self):
        self.response = requests.get(f'{host}/words/{word}', headers=auth_key_wrong)
        self.json = self.response.json()
        self.time = self.response.elapsed.total_seconds()
        self.assertTrue(self.response.status_code == 403, f'Status code is {self.response.status_code}')
        self.assertTrue(self.time < 120, f'Long response time: {self.time}')
        self.assertTrue(self.json['message'] == 'You are not subscribed to this API.',
                        f'Wrong response json body structure')

    def test_no_auth_key_with_accept(self):
        self.response = requests.get(f'{host}/words/{word}', headers=auth_key_no_key)
        self.json = self.response.json()
        self.time = self.response.elapsed.total_seconds()
        self.assertTrue(self.response.status_code == 401, f'Status code is {self.response.status_code}')
        self.assertTrue(self.time < 120, f'Long response time: {self.time}')
        self.assertTrue(self.json['message'] == 'Invalid API key. Go to https://docs.rapidapi.com/docs/keys for more info.',
                        f'Wrong response json body structure')
    def test_no_auth_key_no_accept(self):
        self.response = requests.get(f'{host}/words/{word}')
        self.json = self.response.json()
        self.time = self.response.elapsed.total_seconds()
        self.assertTrue(self.response.status_code == 401, f'Status code is {self.response.status_code}')
        self.assertTrue(self.time < 120, f'Long response time: {self.time}')
        self.assertTrue(self.json['message'] == 'Invalid API key. Go to https://docs.rapidapi.com/docs/keys for more info.',
                        f'Wrong response json body structure')

    def test_empty_auth_key_value(self):
        self.response = requests.get(f'{host}/words/{word}', headers=auth_key_empty_key)
        self.json = self.response.json()
        self.time = self.response.elapsed.total_seconds()
        self.assertTrue(self.response.status_code == 401, f'Status code is {self.response.status_code}')
        self.assertTrue(self.time < 120, f'Long response time: {self.time}')
        self.assertTrue(self.json['message'] == 'Invalid API key. Go to https://docs.rapidapi.com/docs/keys for more info.',
                        f'Wrong response json body structure')

    def test_no_accept_in_header(self):
        self.response = requests.get(f'{host}/words/{word}', headers=auth_key_no_accept)
        self.json = self.response.json()
        self.time = self.response.elapsed.total_seconds()
        self.assertTrue(self.response.status_code == 200, f'Status code is {self.response.status_code}')
        self.assertTrue(self.time < 120, f'Long response time: {self.time}')
        self.assertTrue(
            all([json_body[key] in self.json['results'][result].keys()
                 for key in range(len(json_body)) for result in range(len(self.json['results']))]),
            f'Wrong response json body structure'
        )

    def test_host_in_header(self):
        self.response = requests.get(f'{host}/words/{word}', headers=auth_key_host_in_header)
        self.json = self.response.json()
        self.time = self.response.elapsed.total_seconds()
        self.assertTrue(self.response.status_code == 400, f'Status code is {self.response.status_code}')
        self.assertTrue(self.time < 120, f'Long response time: {self.time}')

    @unittest.skip('freezes')
    def test_wrong_host(self):
        self.response = requests.get(f'{host_wrong}/words/{word}', headers=auth_key)
        self.json = self.response.json()
        self.time = self.response.elapsed.total_seconds()
        self.assertTrue(self.response.status_code == 401, f'Status code is {self.response.status_code}')
        self.assertTrue(self.time < 120, f'Long response time: {self.time}')
        self.assertTrue(self.json['message'] == 'Invalid API key. Go to https://docs.rapidapi.com/docs/keys for more info.',
                        f'Wrong response json body structure')

class get_word_detailes(unittest.TestCase):
    def test_details_happy_path(self):
        for detail in details:
            self.response = requests.get(f'{host}/words/{word}/{detail}', headers=auth_key)
            self.json = self.response.json()
            self.time = self.response.elapsed.total_seconds()
            self.assertTrue(self.response.status_code == 200, f'Status code is {self.response.status_code}')
            self.assertTrue(detail in self.json, f'The detail is not in the response json body')
            self.assertTrue(self.time < 120, f'Long response time: {self.time}')

    @unittest.skip('freezes')
    def test_empty_detail(self):
        self.response = requests.get(f'{host}/words/{word}/', headers=auth_key)
        self.json = self.response.json()
        self.time = self.response.elapsed.total_seconds()
        self.assertTrue(self.time < 120, f'Long response time: {self.time}')

    def test_non_existent_detail(self):
        self.response = requests.get(f'{host}/words/{word}/{detail_non_existent}', headers=auth_key)
        self.json = self.response.json()
        self.time = self.response.elapsed.total_seconds()
        self.assertTrue(self.response.status_code == 400, f'Status code is {self.response.status_code}')
        self.assertFalse(detail_non_existent in self.json, f'The non-existent detail is in the response json body')
        self.assertTrue(self.time < 120, f'Long response time: {self.time}')

    def test_detail_empty_auth_key_value(self):
        self.response = requests.get(f'{host}/words/{word}/{detail}', headers=auth_key_empty_key)
        self.json = self.response.json()
        self.time = self.response.elapsed.total_seconds()
        self.assertTrue(self.response.status_code == 401, f'Status code is {self.response.status_code}')
        self.assertTrue(self.time < 120, f'Long response time: {self.time}')
        self.assertTrue(self.json['message'] == 'Invalid API key. Go to https://docs.rapidapi.com/docs/keys for more info.',
                        f'Wrong response json body structure')

    def test_detail_no_auth_key_with_accept(self):
        self.response = requests.get(f'{host}/words/{word}/{detail}', headers=auth_key_no_key)
        self.json = self.response.json()
        self.time = self.response.elapsed.total_seconds()
        self.assertTrue(self.response.status_code == 401, f'Status code is {self.response.status_code}')
        self.assertTrue(self.time < 120, f'Long response time: {self.time}')
        self.assertTrue(self.json['message'] == 'Invalid API key. Go to https://docs.rapidapi.com/docs/keys for more info.',
                        f'Wrong response json body structure')

    def test_detail_no_auth_key_no_accept(self):
        self.response = requests.get(f'{host}/words/{word}/{detail}', headers=None)
        self.json = self.response.json()
        self.time = self.response.elapsed.total_seconds()
        self.assertTrue(self.response.status_code == 401, f'Status code is {self.response.status_code}')
        self.assertTrue(self.time < 120, f'Long response time: {self.time}')
        self.assertTrue(self.json['message'] == 'Invalid API key. Go to https://docs.rapidapi.com/docs/keys for more info.',
                        f'Wrong response json body structure')

    def test_detail_wrong_key(self):
        self.response = requests.get(f'{host}/words/{word}/{detail}', headers=auth_key_wrong)
        self.json = self.response.json()
        self.time = self.response.elapsed.total_seconds()
        self.assertTrue(self.response.status_code == 403, f'Status code is {self.response.status_code}')
        self.assertTrue(self.time < 120, f'Long response time: {self.time}')
        self.assertTrue(self.json['message'] == 'You are not subscribed to this API.',
                        f'Wrong response json body structure')

    @unittest.skip('error')
    def test_detail_wrong_host(self):
        self.response = requests.get(f'{host_wrong}/words/{word}/{detail}', headers=auth_key)
        self.json = self.response.json()
        self.time = self.response.elapsed.total_seconds()
        self.assertTrue(self.response.status_code == 401, f'Status code is {self.response.status_code}')
        self.assertTrue(self.time < 120, f'Long response time: {self.time}')
        self.assertTrue(
            self.json['message'] == 'Invalid API key. Go to https://docs.rapidapi.com/docs/keys for more info.',
            f'Wrong response json body structure')
#error

    def test_detail_host_in_header(self):
        self.response = requests.get(f'{host}/words/{word}/{detail}', headers=auth_key_host_in_header)
        self.json = self.response.json()
        self.time = self.response.elapsed.total_seconds()
        self.assertTrue(self.response.status_code == 400, f'Status code is {self.response.status_code}')
        self.assertTrue(self.time < 120, f'Long response time: {self.time}')

    def test_detail_special_characters_non_existent_detail(self):
        detail_spchar = ''.join([random.choice('!@#$%^&*()_+=-?:;№"`~./,\\\'') for i in range(10)])
        self.response = requests.get(f'{host}/words/{word}/{detail_spchar}', headers=auth_key)
        self.json = self.response.json()
        self.time = self.response.elapsed.total_seconds()
        self.assertTrue(self.response.status_code == 400, f'Status code is {self.response.status_code}')
        self.assertTrue(self.time < 120, f'Long response time: {self.time}')



if __name__ == '__main__':
    unittest.main()
