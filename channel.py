import ddb
import utils


class Channel(object):
    table_name = "Channel"

    def __init__(self):
        self.ddb = ddb.DDB(self.table_name, [('channel_key', 'S')])
        self.table = self.ddb.get_table()

    def batch_get_channel(self, cids):
        return self.ddb.batch_hash_get(cids)

    def batch_upload(self, channels):
        with self.table.batch_writer() as batch:
            for channel in channels:
                cid = channel['id']
                cname = channel.get("name")
                created = channel['created']
                members = channel['num_members']
                values = {'created': created, 'members': members}
                for k, v in [[cid, cname], [cname, cid]]:
                    row = {
                        'channel_key': k,
                        'channel_name': v
                    }
                    for i in values:
                        row[i] = values[i]
                    row = utils.prune_empty(row)
                    batch.put_item(row)

    def get(self, key):
        response = self.table.get_item(Key={'channel_key': key})
        if 'Item' not in response:
            return None
        result = response['Item']
        result['name'] = result.get('channel_name')
        return result
