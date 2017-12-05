#!/usr/bin/python
# -*- coding: utf-8 -*-

from database.datamodel import DataModel

class DMCheckIn(DataModel):
    def __init__(self, cls):
        super().__init__(cls)

    def select(self, business_id):
        self.query_sql = u'SELECT `date`, `count` FROM `checkin` WHERE ' \
            + u'business_id = "%s"' % (business_id)
        ret = super().execute()
        result = dict()
        for entry in ret:
            k_date = entry[0]
            result[k_date] = result.get(k_date, 0) + entry[1]
        return result

    def del_sql(self, business_id):
        self.query_sql = u'DELETE FROM `checkin` WHERE business_id=%s'
        self.query_args = (business_id,)
        return self

    def delete(self, business_id, checkin):
        if len(checkin) == 0:
            self.query_sql = self.del_sql(business_id).toquery()
            super().commit()
        for key, val in checkin.items():
            self.query_sql = \
                u'DELETE FROM `checkin` WHERE business_id="%s" AND `date`="%s"' \
                % (business_id, key)
            super().commit()

    def insert(self, business_id, checkin):
        from datamodel.business import business
        if len(business.select(business_id)) < 1:
            business.insert(business_id, {})
        for key, val in checkin.items():
            self.query_sql = \
                u'INSERT INTO `checkin`(`business_id`, `date`, `count`) ' \
                + 'VALUES("%s", "%s", %s)' \
                % (business_id, key, val)
            super().commit()

    def update(self, business_id, checkin, old_checkin):
        for key, val in checkin.items():
            if key in old_checkin:
                self.query_sql = \
                    u'UPDATE `checkin` SET count=%s WHERE ' % (val) \
                    + 'business_id="%s" AND date="%s" AND count=%s' \
                    % (business_id, key, old_checkin[key])
            else:
                self.query_sql = \
                    u'UPDATE `checkin` SET count=%s WHERE ' % (val) \
                    + 'business_id="%s" AND date="%s"' \
                    % (business_id, key)
            super().commit()
