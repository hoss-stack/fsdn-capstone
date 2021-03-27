import os
import unittest
import json

from app import create_app
from models import setup_db, Movie, Actor

# Tokens are formatted as such to limit lenght on a line
CASTING_ASSISTANT = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZid09VeFFBcU5ZMzVWSDczSVdyViJ9.eyJpc3MiOiJodHRwczovL2hvc3Mtc3RhY2suZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwNWU1NDdmMDhiOWM5MDA3MTI1ZjJhMiIsImF1ZCI6ImF1dGhvcml6ZSIsImlhdCI6MTYxNjg2MDkxOSwiZXhwIjoxNjE2ODY4MTE5LCJhenAiOiI0ekxaWlZuYzVwb3Z6QXZPcWo3UnRRTDhvYlZpYldMcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.kKUI1PtL6cAc3LmKVDbR2TMdoCgojVWImG01j18gde8L56dskrSK5QIDAiRfBfzL6XOakbZl2z5xt0EBSZbJ0As1JbRZm7G4N6Y5MryrTTbXXSf09TivuZ8Ye7hNAjEgfK0E87EbDFbm2SQACcPrFNvB6Y-yoHWPvTOIT0BnOApaOSsSc-oiaksDURVDc6QBP7X8K1is338Q5WikJdHJEbrka19W7mahoKyL9Rt0jx68j3EKoK86_RJM2gCJvNlAXb2n9YA-NgRze0zRYNtulp1szUWcynS_Pv0GHs4TPLwqJj93RWLbieovxIMY45H9-i3aFktuqRpyy1Ni93I45w')

CASTING_DIRECTOR = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZid09VeFFBcU5ZMzVWSDczSVdyViJ9.eyJpc3MiOiJodHRwczovL2hvc3Mtc3RhY2suZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwNTg5YTc0MjMzMDYwMDA3MGI1YTkwMiIsImF1ZCI6ImF1dGhvcml6ZSIsImlhdCI6MTYxNjg2MTAwNiwiZXhwIjoxNjE2ODY4MjA2LCJhenAiOiI0ekxaWlZuYzVwb3Z6QXZPcWo3UnRRTDhvYlZpYldMcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiXX0.BZegjHySbL7SvgKuZyZskzC9Rnqi2DQAXLKqVsOjMBQX1AISfE7JsRGNtiHOyfwFhQOieTLf4XVhIf37Ss4uMz27fWNycOkP30o2o2319YcXg2gChopr4TRJa2-YzDCYJ2FNxcM4V-hT62rW2Af3RCa3esnjXepftkVxZ1CiOXsTlBhQY-5DJARRq_u1lcVWFldel73xVfwcZZroBS80usL5UJ-ND4j0oFlO5ZG4ASie5W4fdAORz2Kcu_YwgcWZ-Y1OXOcZ80pDcsuoBdyiKcr0f0LlGwmqNXm4A98NFXueyLM4--60WIQvZoCjUyYF3_uMuZ_rY5voyNx6f1Gi3A')

EXECUTIVE_PRODUCER = ('eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InZid09VeFFBcU5ZMzVWSDczSVdyViJ9.eyJpc3MiOiJodHRwczovL2hvc3Mtc3RhY2suZXUuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwNTg5YTM2NmZjMThhMDA2OGEyMmNlMiIsImF1ZCI6ImF1dGhvcml6ZSIsImlhdCI6MTYxNjg2MDc4NiwiZXhwIjoxNjE2ODY3OTg2LCJhenAiOiI0ekxaWlZuYzVwb3Z6QXZPcWo3UnRRTDhvYlZpYldMcSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9ycyIsImRlbGV0ZTptb3ZpZXMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.gcsNlSMMaKedgK9Dq85lC-n_WUiv73-CLNpgz0ikgX9c4uGoq0AGQ3bSbin-RUhn4CyAYTqqnWynkt2zyz6V5dNlxEg1LMBaycO_EYtkZtKuFdETVWaqczZLe8nyJsRvXiN1fp8f6txloAYSOH_mpfCV1ogX8N5No-1osjx_NPz70aFLOs5uH0qTyv0p7-92yZRpTxdaguTRkCulFLiYrW3c62qM1nhBWb7__rpu3uI97pLNGoOMmv8S5ch2dYNKo5-weY2T1Ognxg2BJaNwV9zXfQ_8KfOHY3fMQQcZTjH0DYHeTsKtDwkmblj7mZs5LXfaxi7irPd_gjEacl3ffg')


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
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    # Test get a movie by id
    def test_get_movie_by_id(self):
        response = self.client().get(
            '/movies/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
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
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
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
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
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
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
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
            headers={'Authorization': f'Bearer {CASTING_DIRECTOR}'}
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
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
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
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
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
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
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
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    # Test delete a movie
    def test_delete_movie(self):
        response = self.client().delete(
            '/movies/2',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    # Test delete a movie invalid id
    def test_delete_movie_invalid_id(self):
        response = self.client().delete(
            '/movies/22321',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
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
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

    #  Tests get all actors
    def test_get_all_actors(self):
        response = self.client().get(
            '/actors',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    # Test get actor by id
    def test_get_actor_by_id(self):
        response = self.client().get(
            '/actors/1',
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
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
            headers={"Authorization": "Bearer " + CASTING_ASSISTANT}
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
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
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
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
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
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
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
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
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
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
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
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
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
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
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
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['message'])

    # Test delete an actor invalid id
    def test_delete_actor_invalid_id(self):
        response = self.client().delete(
            '/actors/22321',
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
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
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')


# Make the tests executable
if __name__ == "__main__":
    unittest.main()
