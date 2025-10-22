from huggingface_hub import HfApi, login, create_repo, hf_hub_download
import os
import torch
import torch.nn as nn

class HFClient:
    def __init__(self, token: str = None, username: str = None):
        self.token = os.getenv('HF_TOKEN') if token is None else token
        self.username = os.getenv('HF_USERNAME') if username is None else username
        self.api = HfApi(token=self.token)
        self._logged_in = False

        self._download_dir = "./downloads"
        os.makedirs(self._download_dir, exist_ok=True)

    def login(self) -> bool:
        if self.token is None:
            raise ValueError("HF_TOKEN is not set")
        
        try:
            login(token=self.token)
            self._logged_in = True
            print(f"Logged in successfully")    
        except Exception as e:
            print(f"Error logging in: {e}")
            return False
        
        return True

    def create_repo(self, repo_name: str, private: bool = False, exist_ok: bool = False) -> bool:
        
        if not self._logged_in:
            raise ValueError("Not logged in")
        
        if self.username is None:
            raise ValueError("HF_USERNAME is not set")
        
        repo_id = f"{self.username}/{repo_name}"

        try:
            create_repo(repo_id=repo_id, private=private, exist_ok=exist_ok)
            print(f"Repo {repo_name} created successfully")
        except Exception as e:
            print(f"Error creating repo: {e}")
            return False
        

    def upload_file(self, repo_name, file_path, path_in_repo: str = None, private: bool = False) -> bool:
        if not self._logged_in:
            if not self.login():
                raise ValueError("Failed to login")

        repo_id = f"{self.username}/{repo_name}"

        if not self.create_repo(repo_name=repo_name, private=private, exist_ok=True):
            # raise Exception("Failed to create repo")
            print(f"Repo {repo_name} already exists, skipping creation")
        
        if path_in_repo is None:
            path_in_repo = os.path.basename(file_path)
        else:
            path_in_repo = os.path.join(path_in_repo, os.path.basename(file_path))

        try:
            self.api.upload_file(
                repo_id=repo_id, 
                path_or_fileobj=file_path, 
                path_in_repo=path_in_repo,
                token=self.token
            )
            print(f"File {file_path} uploaded successfully")
        except Exception as e:
            print(f"Error uploading file: {e}")
            return False
        
        return True

    def download_file(self, repo_name, filename):
        if not self._logged_in:
            raise ValueError("Not logged in")

        repo_id = f"{self.username}/{repo_name}"

        try:
            file_path = hf_hub_download(
                repo_id=repo_id, 
                filename=filename, 
                local_dir=self._download_dir, 
                token=self.token
            )
            print(f"File saved at {file_path}")
            return file_path

        except Exception as e:
            print(f"Error downloading file: {e}")
            return None

    def load_model(
        self, 
        repo_id: str, 
        model_class: nn.Module, 
        device: torch.device = torch.device('cpu'), 
        filename: str = 'model.pth'
    ):
        
        if not self._logged_in:
            if not self.login():
                raise ValueError("Failed to login")

        # repo_id = f"{self.username}/{repo_id}"

        file_path = self.download_file(repo_name=repo_id, filename=filename)
        if file_path is None:
            raise Exception("Failed to download model")

        model = model_class().to(device)
        model.load_state_dict(torch.load(file_path, map_location=device))
        return model
    
    def save_and_upload_model(
            self, 
            model: nn.Module, 
            repo_name: str, 
            temp_dir: str = "./temp", 
            filename: str = None
    ) -> bool:

        if not self._logged_in:
            raise ValueError("Not logged in")
        
        os.makedirs(temp_dir, exist_ok=True)

        if filename is None:
            filename = f"{model.__class__.__name__}.pth"
        else:
            filename = f"{filename}.pth"

        temp_file_path = os.path.join(temp_dir, filename)
        torch.save(model.state_dict(), temp_file_path)

        print(f"[1/3] Model saved to {temp_file_path}")

        try:
            uploaded = self.upload_file(repo_name=repo_name, file_path=temp_file_path)
            if not uploaded:
                raise Exception("Failed to upload model")
            print(f"[2/3] Model {filename} uploaded successfully")

            os.remove(temp_file_path)
            print(f"[3/3] Model {filename} removed from temp directory")

        except Exception as e:
            print(f"Error uploading model: {e}")
            return False
        
        return True