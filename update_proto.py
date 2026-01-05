import os
import shutil
import subprocess
from pathlib import Path
import git

from git import Repo, NoSuchPathError, InvalidGitRepositoryError
from loguru import logger
import requests
import sys
from platform import architecture
from zipfile import ZipFile


class Proto:
    def __init__(self, nsl_root_path=f"{Path.home()}/ProtoServices/services-layer"):
        """
        prtotoc_path: path where protoc converter binary is installed
        generator_path: path where all converted data is placed

        :param nsl_root_path: root path of services-layer repo
        """
        self.home = Path().home()
        self.protoc_path = Path(f"{self.home}/protoc/bin/protoc")
        self.generator_root_path = (
            Path(os.getcwd())
            if Path(os.getcwd()).parts[-1] == "clinical-data-generator"
            else FileNotFoundError(
                f"data generator does not exist at: {os.getcwd()} | Make sure you are in clinical-data-generator root"
            )
        )
        self.nsl_root_path = (
            Path(nsl_root_path)
            if Path(nsl_root_path).exists()
            else FileNotFoundError(
                f"services layer repo does not exist at: {nsl_root_path} | Make sure you set services-layer root path"
            )
        )
        logger.debug(f"Home dir is: {self.home}")
        logger.debug(f"Generator root path is: {self.generator_root_path}")
        self.check_if_protoc_exists()

    def download_and_install_protoc(self):
        """
        This function downloads latest version of protoc from official repo,
        which is used for converting protobuf format into python code.
        If success, we need to export path into our ENV variables
        """
        download_file_path = None

        platfroms = {"darwin": "osx"}

        architectures = {"64bit": "x86_64", "32bit": "x86_32"}

        platform = (
            platfroms[sys.platform] if sys.platform in platfroms else sys.platform
        )
        arch = (
            architectures[architecture()[0]]
            if architecture()[0] in architectures
            else EnvironmentError(f"No arch found: {architecture()}")
        )

        url = "https://api.github.com/repos/protocolbuffers/protobuf/releases/latest"
        github_resp = requests.get(url)
        assert (
            github_resp.status_code == 200
        ), f"Response code is {github_resp.status_code} | exiting..."

        for asset in github_resp.json()["assets"]:
            filename = asset["browser_download_url"].split("/")[-1]
            download_url = asset["browser_download_url"]
            if platform in filename:
                if arch in filename:
                    logger.debug("Protoc is downloading...")
                    download_file_path = f"{self.home}/{filename}"
                    protoc_file = requests.get(download_url, stream=True)
                    with open(download_file_path, "wb") as f:
                        for chunk in protoc_file.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)
        with ZipFile(download_file_path, "r") as zip:
            logger.debug(f"Extracting protoc to {self.home}...")
            zip.extractall(path=f"{self.home}/protoc")

        subprocess.call(["chmod", "755", self.protoc_path])
        logger.debug("Protoc version is:")
        subprocess.call([self.protoc_path, "--version"])
        logger.info(f"Run this in terminal:\nexport PATH=$PATH:{self.home}/protoc/bin")

    def check_if_protoc_exists(self):
        """Checks if the protoc exists on current environment"""
        if self.protoc_path.exists():
            subprocess.call(["chmod", "755", self.protoc_path])
            subprocess.call([self.protoc_path, "--version"])
        else:
            logger.debug("No protoc installed...")
            self.download_and_install_protoc()

    def convert_proto(self, proto_file):
        """
        Converts proto files from nsl root path to pythonic code and places it into generator root path
        """
        logger.debug(f"Converting proto File: {proto_file}")
        subprocess.call(
            [
                self.protoc_path,
                proto_file,
                f"--python_out={self.generator_root_path}",
                f"--proto_path={self.nsl_root_path}",
            ]
        )

    def recursive_dir_scan(self, path_to_scan):
        """
        Scanning path recursively and selecting only .proto files for further convertation.
        :param path_to_scan: path to dir with .proto files
        :return: converted *.proto -> *.py
        """
        if path_to_scan.is_dir():
            logger.debug(f"Scanning dir: {path_to_scan}")
            for path in path_to_scan.iterdir():
                self.recursive_dir_scan(path)
        elif path_to_scan.is_file():
            if path_to_scan.suffix == ".proto":
                self.convert_proto(path_to_scan)

    def convert_proto_recursively(self):
        """
        :return: list of items in specified path for further scanning
        """
        if self.nsl_root_path.exists():
            proto_models_path = Path(f"{self.nsl_root_path}/pkg/models")
            if proto_models_path.exists():
                for path in proto_models_path.iterdir():
                    self.recursive_dir_scan(path_to_scan=path)
        else:
            raise FileNotFoundError(f"Path | {self.nsl_root_path} | does not exist")


class ServicesLayerRepo:
    def __init__(self, nsl_root_path=f"{Path.home()}/ProtoServices/services-layer/"):
        self._nsl_root_path = Path(nsl_root_path)
        self._nsl_repo_url = f'https://{os.environ["GHA_AUTOMATION_PAT"]}@github.com/clinical-services/services-layer.git'
        try:
            self._nsl_repo = Repo(self._nsl_root_path)
        except NoSuchPathError:
            logger.warning(
                f"{self._nsl_root_path} repo don't exist locally. Trying to clone"
            )
            self._clone_repo_and_convert_proto()
        except InvalidGitRepositoryError:
            logger.warning(
                f"{self._nsl_root_path} repo is invalid. Trying to remove and clone"
            )
            shutil.rmtree(self._nsl_root_path)
            self._clone_repo_and_convert_proto()
        self._git_console = git.Git(self._nsl_root_path)

    def update(self):
        self._clean_changes()
        self._reset_changes()
        self._pull_branch()
        assert self.local_branch_is_same_as_remote(), logger.error(
            "Local branch is not same as remote. Try to resolve it manually"
        )

    def _clone_repo_and_convert_proto(self):
        logger.debug(
            f"git clone clinical-services/services-layer.git to {self._nsl_root_path}"
        )
        git.Repo.clone_from(self._nsl_repo_url, self._nsl_root_path)
        self._nsl_repo = Repo(self._nsl_root_path)
        logger.debug("Converting proto files from services layer root path to pythonic")
        Proto().convert_proto_recursively()

    def _pull_branch(self):
        logger.debug('Performing "git pull" command')
        self._nsl_repo.remotes.origin.pull()

    def _clean_changes(self):
        logger.debug('Performing "git clean -f -d" command')
        self._nsl_repo.git.clean("-f", "-d")

    def _reset_changes(self):
        logger.debug('Performing "git reset --hard" command')
        self._nsl_repo.git.reset("--hard")

    def local_branch_is_same_as_remote(self):
        logger.debug("Verifying local branch is same as remote")
        return (
            self._git_console.status("-uno")
            == "On branch master\nYour branch is up to date with 'origin/"
            "master'.\n\nnothing to commit (use -u to show untracked files)"
        )


if __name__ == "__main__":
    services_repo = ServicesLayerRepo()
    if not services_repo.local_branch_is_same_as_remote():
        services_repo.update()
        Proto().convert_proto_recursively()
