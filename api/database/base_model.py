# -*- coding: utf-8 -*-

# inspired from https://wakatime.com/blog/32-flask-part-1-sqlalchemy-models-to-json

from api.app import db

class BaseModel(db.Model):
    __abstract__ = True

    def as_dict(self, show=None, _hide=[], _path=None):
        ret_data = {}

        hidden = self._hidden_fields if hasattr(self, "_hidden_fields") else []

        if not _path:
            _path = self.__tablename__.lower()

            def prepend_path(item):
                item = item.lower()
                if item.split(".", 1)[0] == _path:
                    return item
                if len(item) == 0:
                    return item
                if item[0] != ".":
                    item = ".%s" % item
                item = "%s%s" % (_path, item)
                return item

            _hide[:] = [prepend_path(x) for x in _hide]

        columns = self.__table__.columns.keys()

        for key in columns:
            if key.startswith("_"):
                continue
            check = "%s.%s" % (_path, key)
            if check in _hide or key in hidden:
                continue
            # if check in show or key in default:
            else:
                ret_data[key] = getattr(self, key)

        return ret_data
