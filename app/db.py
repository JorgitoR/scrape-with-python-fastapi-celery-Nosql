import pathlib
import os
from dotenv import load_dotenv

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.cqlengine.connection import register_connection, set_default_connection

from . import (config)

settings = config.get_setting()

BASE_DIR = pathlib.Path(__file__).parent
CLUSTER_BUNDLE = str(BASE_DIR / "ignore" / "connect.zip")

load_dotenv()

CLIENT_ID = settings.db_client_id
CLIENT_SECRET = settings.db_client_secret

def get_cluster():
    cloud_config= {
      'secure_connect_bundle': CLUSTER_BUNDLE
    }
    auth_provider = PlainTextAuthProvider(CLIENT_ID, CLIENT_SECRET)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    return cluster

def get_session():
    cluster = get_cluster()
    session = cluster.connect()
    register_connection(str(session), session=session)
    set_default_connection(str(session))
    return session


"""
row = get_session().execute("select release_version from system.local").one()
if row:
  print(row[0])
else:
  print("An error occurred.")
"""