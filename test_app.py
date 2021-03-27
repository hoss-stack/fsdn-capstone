import os
import unittest
import json

from app import create_app
from models import setup_db, Movie, Actor

CASTING_ASSISTANT_TOKEN = os.environ['CASTING_ASSISTANT_TOKEN']
CASTING_DIRECTOR_TOKEN = os.environ['CASTING_DIRECTOR_TOKEN']
EXECUTIVE_PRODUCER_TOKEN = os.environ['EXECUTIVE_PRODUCER_TOKEN']


class CastingAgencyTest(unittest.TestCase):
    """Setup test suite for the routes"""
    def setUp(self):
        """Setup application """
        self.app = create_app()
        self.client = self.app.test_client
        self.test_movie = {
            'title': 'Kungfu Masters',
            'release_date': '2020-05-06',
        }
        self.database_path = os.environ['TEST_DATABASE_URL']

        setup_db(self.app, self.database_path)

    def tearDown(self):
        """Executed after each test"""
        pass

    #  Tests get all movies
    def test_get_all_movies(self):
        response = self.client().get(
            '/movies',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT_TOKEN}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # Test get a movie by id
    def test_get_movie_by_id(self):
        response = self.client().get(
            '/movies/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT_TOKEN}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'Terminator Dark Fate')

    # Test get a movie by invalid id
    def test_get_movie_by_id_invalid_id(self):
        response = self.client().get(
            '/movies/100',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT_TOKEN}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # Test create a movie
    def test_post_movie(self):
        response = self.client().post(
            '/movies',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER_TOKEN}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'Kungfu Masters')
        self.assertEqual(
                    data['movie']['release_date'],
                    'Wed, 06 May 2020 00:00:00 GMT'
                    )

    # Test create a movie with no data
    def test_post_movie_no_data(self):
        response = self.client().post(
            '/movies',
            json={},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER_TOKEN}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # Test create a movie with unauthorized token
    def test_post_movie_unauthorized(self):
        response = self.client().post(
            '/movies',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {CASTING_DIRECTOR_TOKEN}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # Test update a movie
    def test_patch_movie(self):
        response = self.client().patch(
            '/movies/1',
            json={'title': 'Revelations', 'release_date': "2019-11-12"},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER_TOKEN}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], 'Revelations')
        self.assertEqual(
            data['movie']['release_date'],
            'Tue, 12 Nov 2019 00:00:00 GMT'
            )

    # Test update a movie invalid id
    def test_patch_movie_invallid_id(self):
        response = self.client().patch(
            '/movies/12323',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER_TOKEN}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # Test update a movie with no data
    def test_patch_movie_no_data(self):
        response = self.client().patch(
            '/movies/1',
            json={},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER_TOKEN}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # Test update a movie with unauthorized token
    def test_patch_movie_unauthorized(self):
        response = self.client().patch(
            '/movies/1',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT_TOKEN}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # Test delete a movie
    def test_delete_movie(self):
        response = self.client().delete(
            '/movies/2',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER_TOKEN}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    # Test delete a movie invalid id
    def test_delete_movie_invalid_id(self):
        response = self.client().delete(
            '/movies/22321',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER_TOKEN}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # Test delete a movie with unauthorized token
    def test_delete_movie_unothorized(self):
        response = self.client().delete(
            '/movies/2',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT_TOKEN}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    #  Tests get all actors
    def test_get_all_actors(self):
        response = self.client().get(
            '/actors',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT_TOKEN}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # Test get actor by id
    def test_get_actor_by_id(self):
        response = self.client().get(
            '/actors/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT_TOKEN}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['name'], 'Will Smith')

    # Test get actor by id invalid
    def test_get_actor_by_id_invalid_id(self):
        response = self.client().get(
            '/actors/100',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT_TOKEN}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # Test create an actor
    def test_post_actor(self):
        response = self.client().post(
            '/actors',
            json={'name': 'Karl', 'age': 20, "gender": "male"},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER_TOKEN}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['name'], 'Karl')
        self.assertEqual(data['actor']['age'], 20)
        self.assertEqual(data['actor']['gender'], 'male')

    # Test create an actor no data
    def test_post_actor_no_data(self):
        response = self.client().post(
            '/actors',
            json={},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER_TOKEN}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # Test create an actor with unoothorized token
    def test_post_actor_unauthorized(self):
        response = self.client().post(
            '/actors',
            json={'name': 'Mary', 'age': 22, "gender": "female"},
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT_TOKEN}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # Test update an actor
    def test_patch_actor(self):
        response = self.client().patch(
            '/actors/1',
            json={'name': 'Mariam', 'age': 25, "gender": "female"},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER_TOKEN}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['actor']['name'], 'Mariam')
        self.assertEqual(data['actor']['age'], 25)
        self.assertEqual(data['actor']['gender'], 'female')

    # Test update an actor no data
    def test_patch_actor_no_data(self):
        response = self.client().patch(
            '/actors/1',
            json={},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER_TOKEN}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 400)
        self.assertEqual(data['message'], 'bad request')

    # Test update an actor with unoothorized token
    def test_patch_actor_unauthorized(self):
        response = self.client().patch(
            '/actors/1',
            json={'name': 'John', 'age': 25, "gender": "male"},
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT_TOKEN}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # Test update an actor invalid id
    def test_patch_actor_invalid_id(self):
        response = self.client().patch(
            '/actor/12323',
            json={'name': 'Johnathan', 'age': 25, "gender": "male"},
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER_TOKEN}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # Test delete an actor
    def test_delete_actor(self):
        response = self.client().delete(
            '/actors/2',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER_TOKEN}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    # Test delete an actor invalid id
    def test_delete_actor_invalid_id(self):
        response = self.client().delete(
            '/actors/22321',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER_TOKEN}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    # Test delete an actor with unoothorized token
    def test_delete_actor_unothorized(self):
        response = self.client().delete(
            '/actors/2',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT_TOKEN}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')


# Make the tests executable
if __name__ == "__main__":
    unittest.main()
