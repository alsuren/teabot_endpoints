from unittest import TestCase
from playhouse.test_utils import test_database
from teabot_endpoints.models import State, PotMaker
from peewee import SqliteDatabase
from datetime import datetime, timedelta

test_db = SqliteDatabase(':memory:')


class TestModels(TestCase):

    def run(self, result=None):
        with test_database(test_db, [State, PotMaker]):
            super(TestModels, self).run(result)

    def test_get_latest_state_none(self):
        result = State.get_newest_state()
        self.assertIsNone(result)

    def test_get_latest_state(self):
        State.create(
            state="TEAPOT_FULL",
            timestamp=datetime.utcnow().isoformat(),
            num_of_cups=3
        )
        State.create(
            state="TEAPOT_EMPTY",
            timestamp=datetime.utcnow() - timedelta(weeks=1),
            num_of_cups=0
        )
        result = State.get_newest_state()
        self.assertEqual(result.state, "TEAPOT_FULL")
        self.assertEqual(result.num_of_cups, 3)

    def test_get_number_of_new_teapots(self):
        State.create(
            state="FULL_TEAPOT",
            timestamp=datetime.utcnow().isoformat(),
            num_of_cups=3
        )
        State.create(
            state="FULL_TEAPOT",
            timestamp=datetime.utcnow() - timedelta(weeks=1),
            num_of_cups=0
        )
        State.create(
            state="EMPTY_TEAPOT",
            timestamp=datetime.utcnow() - timedelta(weeks=1),
            num_of_cups=0
        )
        result = State.get_number_of_new_teapots()
        self.assertEqual(result, 2)

    def test_latest_full_teapot(self):
        State.create(
            state="FULL_TEAPOT",
            timestamp=datetime(2015, 1, 1).isoformat(),
            num_of_cups=3
        )
        State.create(
            state="FULL_TEAPOT",
            timestamp=datetime(2016, 1, 1).isoformat(),
            num_of_cups=4
        )
        State.create(
            state="FULL_TEAPOT",
            timestamp=datetime(2017, 1, 1).isoformat(),
            num_of_cups=5
        )
        result = State.get_latest_full_teapot()
        self.assertEqual(result.num_of_cups, 5)

    def test_get_all_pots(self):
        PotMaker.create(
            name='aaron',
            number_of_pots_made=1,
            total_weight_made=12,
            number_of_cups_made=5,
            largest_single_pot=2
        )
        PotMaker.create(
            name='aaron2',
            number_of_pots_made=12,
            total_weight_made=24,
            number_of_cups_made=45,
            largest_single_pot=22
        )
        result = PotMaker.get_all()
        self.assertEqual(len(result), 2)

    def test_get_single_pot_maker(self):
        PotMaker.create(
            name='aaron',
            number_of_pots_made=1,
            total_weight_made=12,
            number_of_cups_made=5,
            largest_single_pot=2
        )
        result = PotMaker.get_single_pot_maker('aaron')
        self.assertEqual(result.name, 'aaron')

    def test_flip_requested_teapot_false_true(self):
        PotMaker.create(
            name='aaron',
            number_of_pots_made=1,
            total_weight_made=12,
            number_of_cups_made=5,
            largest_single_pot=2,
            mac_address='123'
        )
        maker = PotMaker.get_single_pot_maker('aaron')
        self.assertFalse(maker.requested_teapot)
        PotMaker.flip_requested_teapot('123')
        maker = PotMaker.get_single_pot_maker('aaron')
        self.assertTrue(maker.requested_teapot)

    def test_flip_requested_teapot_true_false(self):
        PotMaker.create(
            name='aaron',
            number_of_pots_made=1,
            total_weight_made=12,
            number_of_cups_made=5,
            largest_single_pot=2,
            mac_address='123',
            requested_teapot=True
        )
        maker = PotMaker.get_single_pot_maker('aaron')
        self.assertTrue(maker.requested_teapot)
        PotMaker.flip_requested_teapot('123')
        maker = PotMaker.get_single_pot_maker('aaron')
        self.assertFalse(maker.requested_teapot)

    def test_get_single_pot_maker_by_mac_address(self):
        PotMaker.create(
            name='aaron',
            number_of_pots_made=1,
            total_weight_made=12,
            number_of_cups_made=5,
            largest_single_pot=2,
            mac_address='123'
        )
        result = PotMaker.get_single_pot_maker_by_mac_address('123')
        self.assertEqual(result.name, 'aaron')

    def test_get_number_of_teapot_requests(self):
        PotMaker.create(
            name='aaron',
            number_of_pots_made=1,
            total_weight_made=12,
            number_of_cups_made=5,
            largest_single_pot=2,
            mac_address='123'
        )
        PotMaker.create(
            name='gareth',
            number_of_pots_made=1,
            total_weight_made=12,
            number_of_cups_made=5,
            largest_single_pot=2,
            mac_address='123',
            requested_teapot=True
        )
        PotMaker.create(
            name='mario',
            number_of_pots_made=1,
            total_weight_made=12,
            number_of_cups_made=5,
            largest_single_pot=2,
            mac_address='123',
            requested_teapot=True
        )
        result = PotMaker.get_number_of_teapot_requests()
        self.assertEqual(result, 2)
