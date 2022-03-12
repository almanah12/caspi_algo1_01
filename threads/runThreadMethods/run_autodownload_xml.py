
import os
from google.cloud import storage

from helpers import resource_path

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = resource_path(r'data_files/ServiceKey_GoogleCloud/alash-scrap'
                                                             r'-c4bc016b7411.json')


def upload_to_bucket_xml(blob_name, file_path, bucket_name):
    storage_client = storage.Client()

    bucket = storage_client.get_bucket(bucket_name)

    policy = bucket.get_iam_policy(requested_policy_version=3)
    policy.bindings.append(
        {"role": "roles/storage.objectViewer", "members": {"allUsers"}}
    )
    bucket.set_iam_policy(policy)
    blob = bucket.blob(blob_name=blob_name)
    blob.upload_from_filename(file_path)

