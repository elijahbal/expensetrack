import cli_extrack as cli
import random
from pprint import pprint
import json
import datetime

dec = json.JSONDecoder()

DEFAULT_ACCOUNT = {
    'username': 'DEFAULT_USR_NAME',
    'first_name': 'DEFAULT_FIRST_NAME',
    'last_name': 'DEFAULT_LAST_NAME',
    'password': 'DEFAULT_PASSWD',
    'email': 'DEFAULT_MAIL@DOMAIN.COM'
}


def random_account():
    token = "_{:08x}".format(random.randint(0, 16 ** 8))
    return {key: value + token for (key, value) in DEFAULT_ACCOUNT.items()}

def random_record():
    token = "{:08}".format(random.randint(0, 16 ** 8))
    now = datetime.datetime.now()
    DEFAULT_RECORD = {
        'user_id': 0,
        'value': random.random() * 1000,
        'date': now,
        'user_time': now.time(),
        'user_date': now.date(),
        'comment': 'THIS IS RANDOM COMMENT -- ' + token,
        'description': "FOOBAR -- " + token
    }
    return DEFAULT_RECORD

test_to_run = []
test_to_run += ['create_user']
test_to_run += ['create_record']
test_to_run += ['get_records']
# test_to_run += ['delete_record']
# test_to_run += ['update_record']

if 'create_user' in test_to_run:
    for x in range(2):
        my = cli.create_user( user=random_account() )
        # assert my.status_code == 200


if 'create_record' in test_to_run:
    user = dec.decode(cli.get_usr(4).text)
    for x in range(10):
        record = random_record()
        record['user_id']=4
        cli.create_record(user["id"], record=record)


if 'get_records' in test_to_run:
    my = cli.get_records_of_usr( 4 )
    status_code = my.status_code
    data = dec.decode(my.text)  # type: dict


if 'get' in test_to_run:
    data = dec.decode(cli.get_all_users().text)
    for key, username in data.items():
        user_data = cli.get_usr(int(key)).text
        pprint(dec.decode(user_data))

if 'delete' in test_to_run:
    data = dec.decode(cli.get_all_users().text)
    list_of_keys_to_delete = [ int(x) for x in data if int(x)>10 ]
    print(list_of_keys_to_delete)

    for key in list_of_keys_to_delete:
        print("we are deleting this user:")
        pprint(data[str(key)])
        my = cli.delete_user( key )
        print(my.status_code)