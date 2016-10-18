#coding=utf-8
#!/usr/bin/python
import gearman
import pickle


class Encoder(gearman.DataEncoder):
    @classmethod
    def encode(cls, encodable_object):
        return pickle.dumps(encodable_object)

    @classmethod
    def decode(cls, decodeable_string):
        return pickle.loads(decodeable_string)


class JsonClient(gearman.GearmanClient):
    data_encoder = Encoder


def submit():
    gm_client = JsonClient(['localhost:4730'])
    result = gm_client.submit_job("index", {"title": "abc", "content": "helo world", "lc": "ru-ru"})
    print result


if __name__ == "__main__":
    submit()
