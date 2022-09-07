import hashlib
import json
import os

from bip39 import bip39_generate
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

from .helpful_scripts import json_dumps

BLOCKCHAIN_API_URL = os.environ.get(
    "BLOCKCHAIN_API_URL", "https://api.engi.prod.zmvp.host/graphql"
)

transport = AIOHTTPTransport(url=BLOCKCHAIN_API_URL)

# Create a GraphQL client using the defined transport
client = Client(transport=transport, fetch_schema_from_transport=True)


async def get_health():
    query = gql(
        """
    query EngiHealthStatusQuery {
        health {
          chain
          nodeName
          version
          status
          peerCount
        }
    }
    """
    )
    return await client.execute_async(query)


async def get_account(id):
    query = gql(
        """
        query Account($id: String!) {
            account(id: $id) {
                consumers
                data {
                feeFrozen
                free
                miscFrozen
                reserved
                }
                nonce
                providers
                sufficients
            }
        }
        """
    )
    return await client.execute_async(query, variable_values={"id": id})


def get_mnemonic_salt(mnemonic, password=""):
    return hashlib.sha512(str.encode(mnemonic + password)).hexdigest()


async def create_user(name, password, mnemonic=None):
    if mnemonic is None:
        # generate a random mnemonic string of 12 words with default language (English)
        mnemonic = bip39_generate(12)
    query = gql(
        """
      mutation CreateUser(
        $name: String!
        $mnemonic: String!
        $mnemonicSalt: String!
        $password: String
      ) {
        createUser(
          user: {
            name: $name
            mnemonic: $mnemonic
            mnemonicSalt: $mnemonicSalt
            password: $password
          }
        ) {
          name
          address
          createdOn
          encoded
          metadata {
            content
            type
            version
          }
        }
      }
    """
    )
    return (
        mnemonic,
        await client.execute_async(
            query,
            variable_values={
                "name": name,
                "mnemonic": mnemonic,
                "mnemonicSalt": get_mnemonic_salt(mnemonic, password),
                "password": password,
            },
        ),
    )


class User(object):
    def __init__(self, name=None, password1=None, password2=None):
        self.name = name
        self.password1 = password1
        self.password2 = password2
        self.mnemonic = None
        self.wallet_address = None
        self.extra = None

    @property
    def error(self):
        return not (self.valid_password and self.passwords_match)

    @property
    def passwords_match(self):
        return self.password1 == self.password2

    @property
    def valid_password(self):
        return True

    def __repr__(self):
        return self.json()

    def json(self):
        return json_dumps(
            {
                "UserName": self.name,
                "Mnemonic": self.mnemonic,
                "WalletAddress": self.wallet_address,
                "Extra": self.extra,
            }
        )

    def load_dict(self, user_obj):
        self.name = user_obj["UserName"]
        self.password1 = self.password2 = None
        self.mnemonic = user_obj["Mnemonic"]
        self.wallet_address = user_obj["WalletAddress"]
        self.extra = user_obj["Extra"]

    def loads(self, s):
        return self.load_dict(json.loads(s))


class GraphQLUser(User):
    async def create(self):
        self.mnemonic, self.extra = await create_user(self.name, self.password1, self.mnemonic)
        self.wallet_address = self.extra["createUser"]["address"]

    @property
    def encoded(self):
        """We use this property to make subsequent API calls"""
        return self.extra["createUser"]["encoded"]
