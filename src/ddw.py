import datadotworld


class DDW:
    """Handles dataset creation and uploading to Data.World."""

    def __init__(self, files: list, owner_id: str):
        self.api_client = datadotworld.api_client()
        self.files = files
        self.owner_id = owner_id

    def upload_to_dataset(self, dataset_key: str):
        self.api_client.upload_files(dataset_key=dataset_key, files=self.files, expand_archives=True)

    def create_dataset(self, title: str, description: str):
        self.api_client.create_dataset(
            owner_id=self.owner_id, title=title, description=description, 
            visibility='OPEN', license='Public Domain'
        )
