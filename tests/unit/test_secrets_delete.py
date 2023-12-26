



# Dependencies:
# pip install pytest-mock
import unittest
from unittest import patch, MagicMock

class TestDeleteAction(unittest.TestCase):

    # Deletes a resource policy successfully
    def test_deletes_resource_policy_successfully(self, mocker):
        # Mock the delete_resource_policy method
        mocker.patch.object(secretsmanager, 'delete_resource_policy')
        # Create an instance of the secretsmanager class
        sm = secretsmanager('resourceType', 'region', 'resourceName', {'resourceType': {'delete': 'delete_resource_policy'}})
        # Call the delete_action method
        status = sm.delete_action()
        # Assert that the delete_resource_policy method was called
        secretsmanager.delete_resource_policy.assert_called_once_with(SecretI='resourceName')
        # Assert that the status is 'true'
        self.assertEqual(status, 'true')
    