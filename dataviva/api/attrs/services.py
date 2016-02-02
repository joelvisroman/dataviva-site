from dataviva.api.attrs.models import Ybs, Stat
from dataviva import db
from sqlalchemy import func

class Location:
    def __init__(self, bra_id):
        self.bra_id = bra_id
        self.ybs_max_year_query = db.session.query(
            func.max(Ybs.year)).filter_by(bra_id=bra_id)

    def statistics(self):
        statistics_query = Ybs.query.join(Stat).filter(
            Ybs.bra_id == self.bra_id,
            Ybs.year == self.ybs_max_year_query)

        statistics_data = statistics_query.values(
            Stat.id,
            Stat.name_pt,
            Ybs.stat_val)

        statistics = {}

        for id, name_pt, stat_val in statistics_data:
            statistics[id] = {
                'name': name_pt,
                'value': stat_val,
            }

        return statistics