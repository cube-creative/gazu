import unittest
import json
import requests_mock

import gazu.client
import gazu.shot


class ShotTestCase(unittest.TestCase):

    def test_all_shots_for_project(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url('data/projects/project-1/shots'),
                text='[{"name": "Shot 01", "project_id": "project-1"}]'
            )
            project = {
                "id": "project-1"
            }
            shots = gazu.shot.all_shots_for_project(project)
            self.assertEquals(len(shots), 1)
            shot_instance = shots[0]
            self.assertEquals(shot_instance["name"], "Shot 01")
            self.assertEquals(shot_instance["project_id"], "project-1")

    def test_all_shots_for_sequence(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url('data/sequences/sequence-1/shots'),
                text=json.dumps(
                    [
                        {
                            "name": "Shot 01",
                            "project_id": "project-1",
                            "parent_id": "sequence-1"
                        }
                    ]
                )
            )
            sequence = {
                "id": "sequence-1"
            }
            shots = gazu.shot.all_shots_for_sequence(sequence)
            self.assertEquals(len(shots), 1)
            shot_instance = shots[0]
            self.assertEquals(shot_instance["name"], "Shot 01")
            self.assertEquals(shot_instance["project_id"], "project-1")
            self.assertEquals(shot_instance["parent_id"], "sequence-1")

    def test_all_sequences(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url('data/sequences'),
                text='[{"name": "Sequence 01", "project_id": "project-1"}]'
            )
            sequences = gazu.shot.all_sequences()
            sequence_instance = sequences[0]
            self.assertEquals(sequence_instance["name"], "Sequence 01")

    def test_all_sequences_for_project(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url(
                    'data/projects/project-1/sequences'
                ),
                text='[{"name": "Sequence 01", "project_id": "project-1"}]'
            )
            project = {
             "id": "project-1"
            }
            sequences = gazu.shot.all_sequences(project=project)
            self.assertEquals(len(sequences), 1)
            sequence_instance = sequences[0]
            self.assertEquals(sequence_instance["name"], "Sequence 01")
            self.assertEquals(sequence_instance["project_id"], "project-1")

    def test_all_sequences_for_episode(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url(
                    "data/episodes/episode-1/sequences"
                ),
                text=json.dumps([{
                    "name": "Sequence 01",
                    "project_id": "project-1",
                    "parent_id": "episode-1"
                }])
            )
            episode = {
                "id": "episode-1"
            }
            sequences = gazu.shot.all_sequences_for_episode(episode)
            self.assertEquals(len(sequences), 1)
            sequence_instance = sequences[0]
            self.assertEquals(sequence_instance["name"], "Sequence 01")
            self.assertEquals(sequence_instance["project_id"], "project-1")
            self.assertEquals(sequence_instance["parent_id"], "episode-1")

    def test_all_episodes_for_project(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url(
                    'data/projects/project-1/episodes'
                ),
                text='[{"name": "Episode 01", "project_id": "project-1"}]'
            )
            project = {
                "id": "project-1"
            }
            episodes = gazu.shot.all_episodes_for_project(project)
            self.assertEquals(len(episodes), 1)
            episode_instance = episodes[0]
            self.assertEquals(episode_instance["name"], "Episode 01")
            self.assertEquals(episode_instance["project_id"], "project-1")

    def test_get_episode(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url("data/episodes/episode-1"),
                text='{"name": "Episode 01", "project_id": "project-1"}'
            )
            episode = gazu.shot.get_episode('episode-1')
            self.assertEquals(episode["name"], "Episode 01")

    def test_get_episode_from_sequence(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url("data/episodes/episode-1"),
                text=json.dumps(
                    {"name": "Episode 01", "project_id": "project-1"}
                )
            )
            episode = gazu.shot.get_episode_from_sequence({
                "id": "shot-1",
                "parent_id": "episode-1"
            })
            self.assertEquals(episode["name"], "Episode 01")

    def test_get_sequence(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url("data/sequences/sequence-1"),
                text=json.dumps(
                    {"name": "Sequence 01", "project_id": "project-1"}
                )
            )
            sequence = gazu.shot.get_sequence("sequence-1")
            self.assertEquals(sequence["name"], "Sequence 01")

    def test_get_sequence_from_shot(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url("data/sequences/sequence-1"),
                text=json.dumps(
                    {"name": "Sequence 01", "project_id": "project-1"}
                )
            )
            sequence = gazu.shot.get_sequence_from_shot({
                "id": "shot-1",
                "parent_id": "sequence-1"
            })
            self.assertEquals(sequence["name"], "Sequence 01")

    def test_get_shot(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url("data/shots/shot-1"),
                text='{"name": "Shot 01", "project_id": "project-1"}'
            )
            shot = gazu.shot.get_shot('shot-1')
            self.assertEquals(shot["name"], "Shot 01")

    def test_get_shot_by_name(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url(
                    "data/shots/all?parent_id=sequence-1&name=Shot01"
                ),
                text=json.dumps([
                    {"name": "Shot01", "project_id": "project-1"}
                ])
            )
            sequence = {"id": "sequence-1"}
            shot = gazu.shot.get_shot_by_name(sequence, "Shot01")
            self.assertEquals(shot["name"], "Shot01")

    def test_get_sequence_by_name(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url(
                    "data/sequences?project_id=project-1&name=Sequence01"
                ),
                text=json.dumps([
                    {"name": "Sequence01", "project_id": "project-1"}
                ])
            )
            project = {"id": "project-1"}
            sequence = gazu.shot.get_sequence_by_name(project, "Sequence01")
            self.assertEquals(sequence["name"], "Sequence01")

    def test_new_episode(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url(
                    "data/episodes?project_id=project-1&name=Episode 01"
                ),
                text=json.dumps([])
            )
            mock.post(
                gazu.client.get_full_url(
                    "data/projects/project-1/episodes"
                ),
                text=json.dumps({"id": "episode-01", "project_id": "project-1"})
            )
            project = {"id": "project-1"}
            shot = gazu.shot.new_episode(project, 'Episode 01')
            self.assertEquals(shot["id"], "episode-01")

    def test_new_sequence(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url(
                    "data/sequences?parent_id=episode-1&name=Sequence 01"
                ),
                text=json.dumps([])
            )
            mock.post(
                gazu.client.get_full_url(
                    "data/projects/project-1/sequences"
                ),
                text=json.dumps({
                    "id": "sequence-01",
                    "project_id": "project-1"
                })
            )
            project = {"id": "project-1"}
            episode = {"id": "episode-1"}
            shot = gazu.shot.new_sequence(project, episode, 'Sequence 01')
            self.assertEquals(shot["id"], "sequence-01")

    def test_new_shot(self):
        with requests_mock.mock() as mock:
            mock.get(
                gazu.client.get_full_url(
                    "data/shots/all?parent_id=sequence-1&name=Shot 01"
                ),
                text=json.dumps([])
            )
            mock = mock.post(
                gazu.client.get_full_url(
                    "data/projects/project-1/shots"
                ),
                text=json.dumps({"id": "shot-01", "project_id": "project-1"})
            )
            project = {"id": "project-1"}
            sequence = {"id": "sequence-1"}
            shot = gazu.shot.new_shot(
                project,
                sequence,
                "Shot 01",
                frame_in=10,
                frame_out=20
            )
            self.assertEquals(shot["id"], "shot-01")
            sent_data = json.loads(mock.request_history[0].text)
            self.assertEquals(10, sent_data["data"]["frame_in"])

    def test_update_shot(self):
        with requests_mock.mock() as mock:
            mock = mock.put(
                gazu.client.get_full_url("data/entities/shot-1"),
                text=json.dumps({"id": "shot-01", "project_id": "project-1"})
            )
            shot = {
                "id": "shot-1",
                "name": "S02"
            }
            shot = gazu.shot.update_shot(shot)
            self.assertEquals(shot["id"], "shot-01")

    def test_get_asset_instances(self):
        with requests_mock.mock() as mock:
            result = [{"id": "asset-instance-01"}]
            mock = mock.get(
                gazu.client.get_full_url(
                    "data/shots/shot-1/asset-instances"
                ),
                text=json.dumps(result)
            )
            shot = {"id": "shot-1"}
            asset_instances = gazu.shot.get_asset_instances_for_shot(shot)
            self.assertEqual(asset_instances[0]["id"], "asset-instance-01")

    def test_add_asset_instance(self):
        with requests_mock.mock() as mock:
            result = {"id": "asset-instance-01"}
            mock = mock.post(
                gazu.client.get_full_url(
                    "data/shots/shot-1/asset-instances"
                ),
                text=json.dumps(result)
            )
            shot = {"id": "shot-1"}
            asset_instance = {"id": "asset-instance-1"}
            asset_instance = gazu.shot.add_asset_instance_to_shot(
                shot, asset_instance
            )
            self.assertEquals(asset_instance, result)

    def test_remove_asset_instance(self):
        with requests_mock.mock() as mock:
            mock = mock.delete(
                gazu.client.get_full_url(
                    "data/shots/shot-1/asset-instances/asset-instance-1"
                )
            )
            shot = {"id": "shot-1"}
            asset_instance = {"id": "asset-instance-1"}
            asset_instance = gazu.shot.remove_asset_instance_from_shot(
                shot, asset_instance
            )

    def test_get_shot(self):
        with requests_mock.mock() as mock:
            mock = mock.put(
                gazu.client.get_full_url("data/shots/shot-1/casting"),
                text=json.dumps({"success": True})
            )
            shot = {"id": "shot-1"}
            casting = [
                {"asset_id": "asset-1", "nb_occurences": 2},
                {"asset_id": "asset-2", "nb_occurences": 1}
            ]
            gazu.shot.update_casting(shot, casting)
