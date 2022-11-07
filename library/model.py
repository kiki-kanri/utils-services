from kikiutils.time import now_time_utc
from mongoengine import Document, fields, QuerySet


class BaseModel(Document):
    meta = {
        'abstract': True
    }


class BaseQuerySet(QuerySet):
    def id(self, id):
        try:
            return self.filter(id=id).first()
        except:
            return None

    def get_or_create(self, defaults: dict = {}, **kwargs):
        model = self.filter(**kwargs).first()

        if model is None:
            model = self.create(**defaults, **kwargs)

        return model

    def get_or_none(self, **kwargs):
        return self.filter(**kwargs).first()

    def update_or_create(self, defaults: dict = {}, **kwargs):
        return self.filter(**kwargs).modify(
            new=True,
            upsert=True,
            **defaults
        )
