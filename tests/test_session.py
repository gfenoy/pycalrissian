import base64
import os
import ast
import unittest
from loguru import logger
from pycalrissian.context import CalrissianContext

os.environ.setdefault("KUBECONFIG", os.path.expanduser("~/.kube/kubeconfig-t2-dev.yaml"))

STORAGE_CLASS = os.getenv("STORAGE_CLASS", "standard")


class TestCalrissianExecution(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logger.info(f"-----\n------------------------------  unit test for test_session.py   ------------------------------\n\n")
        cls.namespace = "deleted-namespace"

        username = os.getenv("TEST_REGISTRY_USERNAME", "")
        password = os.getenv("TEST_REGISTRY_PASSWORD", "")
        email = os.getenv("TEST_REGISTRY_EMAIL", "")
        registry = os.getenv("TEST_REGISTRY_URL", "https://index.docker.io/v1/")

        auth = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode(
            "utf-8"
        )

        secret_config = {
            "auths": {
                registry: {
                    "username": username,
                    "password": password,
                    "email": email,
                    "auth": auth,
                },
                "registry.gitlab.com": {
                    "auth": os.getenv("TEST_GITLAB_AUTH", ""),
                },
            }
        }

        session = CalrissianContext(
            namespace=cls.namespace,
            storage_class=STORAGE_CLASS,
            volume_size="1G",
            image_pull_secrets=secret_config,
        )

        session.initialise()

        cls.session = session

    
        
        