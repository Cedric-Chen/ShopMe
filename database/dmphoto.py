#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.datamodel import DataModel

class DMPhoto(DataModel):
    def __init__(self, cls):
        super().__init__(cls)
        self.dm_attr = [u'id', u'business_id', u'caption', u'label']

    def select(self, business_id):
        self.query_sql = u'SELECT %s ' % (u', '.join(self.dm_attr)) \
            + u'FROM photo WHERE business_id = "%s"' % (business_id)
        ret = super().select()
        result = dict()
        for entry in ret:
            result[entry[0]] = {
                self.dm_attr[index]: value \
                for index, value in enumerate(entry)
            }
        return result

    def delete(self, business_id, photo):
        if len(photo) == 0:
            self.query_sql = u'DELETE FROM `photo` WHERE business_id="%s"' \
                % (business_id)
            super().execute()
        for key, val in photo.items():
            pair = [u'id=%s' % (self.quote_sql(key))]
            for k, v in val.items():
                if k != 'id':
                    pair.append(u'%s=%s' % (k, self.quote_sql(v)))
            self.query_sql = u'DELETE FROM `photo` WHERE %s' \
                % (' AND '.join(pair))
            super().execute()

    def insert(self, business_id, photo):
        from datamodel.business import business
        if len(business.select(business_id)) < 1:
            business.insert(business_id, {})
        for key, val in photo.items():
            k = [u'id']
            v = [self.quote_sql(key)]
            for attr in self.dm_attr:
                if attr in val and attr != u'id':
                    k.append(attr)
                    v.append(self.quote_sql(val[attr]))
            self.query_sql = u'INSERT INTO `photo`(%s) ' % (u','.join(k)) \
                + 'VALUES(%s)' % (u','.join(v))
            super().execute()

    def update(self, business_id, photo, old_photo):
        for key, val in photo.items():
            if key not in old_photo and key not in self.select(business_id):
                self.insert(business_id, {key: val})
            else:
                pair = [u'id=%s' % (self.quote_sql(key))]
                for k, v in val.items():
                    if k != 'id':
                        pair.append(u'%s=%s' % (k, self.quote_sql(v)))
                self.query_sql = u'UPDATE photo SET %s WHERE id="%s"' \
                    % (u', '.join(pair), key)
                super().execute()
