import pytest
from scrape_bwin.final_scraper import get_match_data


class TestGetMatchData(object):
    def test_get_match_data_with_invalid_match_id(self):
        # Arrange
        match_id = "invalid_match_id"
        # Act
        match_data = get_match_data(match_id)
        # Assert
        self.assertIsNone(match_data)

    def test_get_match_data_with_match_id_that_does_not_exist(self):
        # Arrange
        match_id = 12345679
        # Act
        match_data = get_match_data(match_id)
        # Assert
        self.assertIsNone(match_data)

    def test_get_match_data_with_match_id_that_is_not_associated_with_any_matches(self):
        # Arrange
        match_id = 987654321
        # Act
        match_data = get_match_data(match_id)
        # Assert
        self.assertIsNone(match_data)

    def test_get_match_data_with_match_id_that_has_incomplete_or_incorrect_data(self):
        # Arrange
        match_id = 12345680
        # Act
        match_data = get_match_data(match_id)
        # Assert
        self.assertIsNone(match_data)

    def test_get_match_data_with_match_id_from_different_sport_or_league(self):
        # Arrange
        match_id = 12345681
        # Act
        match_data = get_match_data(match_id)
        # Assert
        self.assertIsNone(match_data)

    def test_get_match_data_with_match_id_from_different_time_period(self):
        # Arrange
        match_id = 12345682
        # Act
        match_data = get_match_data(match_id)
        # Assert
        self.assertIsNone(match_data)

    def test_get_match_data_with_match_id_from_different_country(self):
        # Arrange
        match_id = 12345683
        # Act
        match_data = get_match_data(match_id)
        # Assert
        self.assertIsNone(match_data)
