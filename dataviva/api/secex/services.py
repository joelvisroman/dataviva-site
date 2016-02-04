from dataviva.api.attrs.models import Bra, Wld
from dataviva.api.secex.models import Ymp, Ymbp, Ympw, Ymbpw
from dataviva import db
from sqlalchemy import func, desc

class Product:
    def __init__(self, product_id):
        self.product_id = product_id
        self.ymp_max_year_query = db.session.query(
            func.max(Ymp.year)).filter_by(hs_id=product_id)
        self.ymbp_max_year_query = db.session.query(
            func.max(Ymbp.year)).filter_by(hs_id=product_id)
        self.ympw_max_year_query = db.session.query(
            func.max(Ympw.year)).filter_by(hs_id=product_id)
        self._secex_values = None

    def __secex_values__(self):
        if not self._secex_values:
            ymp_query = Ymp.query.filter(
                Ymp.hs_id==self.product_id,
                Ymp.year==self.ymp_max_year_query,
                Ymp.month==0
            ).limit(1)

            ymp_data = ymp_query.values(
                Ymp.year,
                Ymp.export_val,
                Ymp.import_val,
                Ymp.export_kg,
                Ymp.import_kg
            )

            secex_values = {}

            for year, export_val, import_val, export_kg, import_kg in ymp_data:
                export_val = export_val or 0
                import_val = import_val or 0
                export_kg = export_kg or 0
                import_kg = import_kg or 0

                secex_values['year'] = year
                secex_values['export_val'] = export_val
                secex_values['import_val'] = import_val
                secex_values['export_kg'] = export_kg
                secex_values['import_kg'] = import_kg
                secex_values['trade_balance'] = export_val - import_val

                if export_val == 0:
                    secex_values['export_net_weight'] = None
                else:
                    secex_values['export_net_weight'] = export_kg / export_val

                if import_val == 0:
                    secex_values['import_net_weight'] = None
                else:
                    secex_values['import_net_weight'] = import_kg / import_val

            self._secex_values = secex_values

        return self._secex_values

    def year(self):
        return self.__secex_values__()['year']

    def export_val(self):
        return self.__secex_values__()['export_val']

    def import_val(self):
        return self.__secex_values__()['import_val']

    def export_kg(self):
        return self.__secex_values__()['export_kg']

    def trade_balance(self):
        return self.__secex_values__()['trade_balance']

    def export_net_weight(self):
        return self.__secex_values__()['export_net_weight']

    def import_net_weight(self):
        return self.__secex_values__()['import_net_weight']

    def __destination_with_more_exports__(self):
        ympw_query = Ympw.query.join(Wld).filter(
            Ympw.hs_id==self.product_id,
            Ympw.year==self.ympw_max_year_query,
            Ympw.wld_id_len==5,
            Ympw.month==0
        ).order_by(desc(Ympw.export_val)).limit(1)

        ympw_wld_data = ympw_query.one()

        return ympw_wld_data

    def destination_with_more_exports(self):
        ympw = self.__destination_with_more_exports__()
        return ympw.wld.name()

    def highest_export_value_by_destination(self):
        ympw = self.__destination_with_more_exports__()
        return ympw.export_val

    def __origin_with_more_imports__(self):
        ympw_query = Ympw.query.join(Wld).filter(
            Ympw.hs_id==self.product_id,
            Ympw.year==self.ympw_max_year_query,
            Ympw.wld_id_len==5,
            Ympw.month==0
        ).order_by(desc(Ympw.import_val)).limit(1)

        ympw_wld_data = ympw_query.one()

        return ympw_wld_data

    def origin_with_more_imports(self):
        ympw = self.__origin_with_more_imports__()
        return ympw.wld.name()

    def highest_import_value_by_origin(self):
        ympw = self.__origin_with_more_imports__()
        return ympw.import_val

    def __municipality_with_more_exports__(self):
        ymbp_query = Ymbp.query.join(Bra).filter(
            Ymbp.hs_id==self.product_id,
            Ymbp.year==self.ymbp_max_year_query,
            Ymbp.bra_id_len==9,
            Ymbp.month==0
        ).order_by(desc(Ymbp.export_val)).limit(1)

        ymbp_bra_data = ymbp_query.one()

        return ymbp_bra_data

    def municipality_with_more_exports(self):
        ymbp = self.__municipality_with_more_exports__()
        return ymbp.bra.name()

    def highest_export_value_by_municipality(self):
        ymbp = self.__municipality_with_more_exports__()
        return ymbp.export_val

    def __municipality_with_more_imports__(self):
        ymbp_query = Ymbp.query.join(Bra).filter(
            Ymbp.hs_id==self.product_id,
            Ymbp.year==self.ymbp_max_year_query,
            Ymbp.bra_id_len==9,
            Ymbp.month==0
        ).order_by(desc(Ymbp.import_val)).limit(1)

        ymbp_bra_data = ymbp_query.one()

        return ymbp_bra_data

    def municipality_with_more_imports(self):
        ymbp = self.__municipality_with_more_imports__()
        return ymbp.bra.name()

    def highest_import_value_by_municipality(self):
        ymbp = self.__municipality_with_more_imports__()
        return ymbp.import_val


class ProductByLocation:
    def __init__(self, bra_id, product_id):
        self.bra_id = bra_id
        self.product_id = product_id
        self.ymp_max_year_query = db.session.query(
            func.max(Ymp.year)).filter_by(hs_id=product_id)
        self.ymbp_max_year_query = db.session.query(
            func.max(Ymbp.year)).filter_by(hs_id=product_id)
        self.ymbpw_max_year_query = db.session.query(
            func.max(Ymbpw.year)).filter_by(hs_id=product_id, bra_id=bra_id)
        self._secex_values = None

    def pci(self):
        ymp_pci_query = Ymp.query.filter(
            Ymp.hs_id==self.product_id,
            Ymp.year==self.ymp_max_year_query,
            Ymp.month==0
        ).limit(1)

        pci = ymp_pci_query.one().pci

        return pci

    def __secex_values__(self):
        if not self._secex_values:
            ymbp_query = Ymbp.query.filter(
                Ymbp.hs_id==self.product_id,
                Ymbp.year==self.ymbp_max_year_query,
                Ymbp.bra_id==self.bra_id,
                Ymbp.month==0
            ).limit(1)

            ymbp_data = ymbp_query.values(
                Ymbp.year,
                Ymbp.export_val,
                Ymbp.import_val,
                Ymbp.export_kg,
                Ymbp.import_kg,
                Ymbp.rca_wld,
                Ymbp.distance_wld,
                Ymbp.opp_gain_wld
            )

            secex_values = {}

            for year, export_val, import_val, export_kg, import_kg, rca_wld, distance_wld, opp_gain_wld in ymbp_data:
                export_val = export_val or 0
                import_val = import_val or 0
                export_kg = export_kg or 0
                import_kg = import_kg or 0

                secex_values['year'] = year
                secex_values['export_val'] = export_val
                secex_values['import_val'] = import_val
                secex_values['export_kg'] = export_kg
                secex_values['import_kg'] = import_kg
                secex_values['trade_balance'] = export_val - import_val

                if export_val == 0:
                    secex_values['export_net_weight'] = None
                else:
                    secex_values['export_net_weight'] = export_kg / export_val

                if import_val == 0:
                    secex_values['import_net_weight'] = None
                else:
                    secex_values['import_net_weight'] = import_kg / import_val

                secex_values['rca_wld'] = rca_wld
                secex_values['distance_wld'] = distance_wld
                secex_values['opp_gain_wld'] = opp_gain_wld

            self._secex_values = secex_values

        return self._secex_values

    def year(self):
        return self.__secex_values__()['year']

    def import_val(self):
        return self.__secex_values__()['export_val']

    def export_val(self):
        return self.__secex_values__()['import_val']

    def export_kg(self):
        return self.__secex_values__()['export_kg']

    def trade_balance(self):
        return self.__secex_values__()['trade_balance']

    def export_net_weight(self):
        return self.__secex_values__()['export_net_weight']

    def import_net_weight(self):
        return self.__secex_values__()['import_net_weight']

    def rca_wld(self):
        return self.__secex_values__()['rca_wld']

    def distance_wld(self):
        return self.__secex_values__()['distance_wld']

    def opp_gain_wld(self):
        return self.__secex_values__()['opp_gain_wld']

    def __destination_with_more_exports__(self):
        ymbpw_query = Ymbpw.query.join(Wld).filter(
            Ymbpw.hs_id==self.product_id,
            Ymbpw.year==self.ymbpw_max_year_query,
            Ymbpw.wld_id_len==5,
            Ymbpw.bra_id.like(str(self.bra_id)+'%'),
            Ymbpw.month==0
        ).order_by(desc(Ymbpw.export_val)).limit(1)

        ymbpw_wld_data = ymbpw_query.one()

        return ymbpw_wld_data

    def destination_with_more_exports(self):
        ymbpw = self.__destination_with_more_exports__()
        return ymbpw.wld.name()

    def highest_export_value_by_destination(self):
        ymbpw = self.__destination_with_more_exports__()
        return ymbpw.export_val

    def __origin_with_more_imports__(self):
        ymbpw_query = Ymbpw.query.join(Wld).filter(
            Ymbpw.hs_id==self.product_id,
            Ymbpw.year==self.ymbpw_max_year_query,
            Ymbpw.wld_id_len==5,
            Ymbpw.bra_id.like(str(self.bra_id)+'%'),
            Ymbpw.month==0
        ).order_by(desc(Ymbpw.import_val)).limit(1)

        ymbpw_wld_data = ymbpw_query.one()

        return ymbpw_wld_data

    def origin_with_more_imports(self):
        ymbpw = self.__origin_with_more_imports__()
        return ymbpw.wld.name()

    def highest_import_value_by_origin(self):
        ymbpw = self.__origin_with_more_imports__()
        return ymbpw.import_val

    def __municipality_with_more_exports__(self):
        ymbp_query = Ymbp.query.join(Bra).filter(
            Ymbp.hs_id==self.product_id,
            Ymbp.year==self.ymbp_max_year_query,
            Ymbp.bra_id_len==9,
            Ymbp.bra_id.like(str(self.bra_id)+'%'),
            Ymbp.month==0
        ).order_by(desc(Ymbp.export_val)).limit(1)

        ymbp_bra_data = ymbp_query.one()

        return ymbp_bra_data

    def municipality_with_more_exports(self):
        ymbp = self.__municipality_with_more_exports__()
        return ymbp.bra.name()

    def highest_export_value_by_municipality(self):
        ymbp = self.__municipality_with_more_exports__()
        return ymbp.export_val

    def __municipality_with_more_imports__(self):
        ymbp_query = Ymbp.query.join(Bra).filter(
            Ymbp.hs_id==self.product_id,
            Ymbp.year==self.ymbp_max_year_query,
            Ymbp.bra_id_len==9,
            Ymbp.bra_id.like(str(self.bra_id)+'%'),
            Ymbp.month==0
        ).order_by(desc(Ymbp.import_val)).limit(1)

        ymbp_bra_data = ymbp_query.one()

        return ymbp_bra_data

    def municipality_with_more_imports(self):
        ymbp = self.__municipality_with_more_imports__()
        return ymbp.bra.name()

    def highest_import_value_by_municipality(self):
        ymbp = self.__municipality_with_more_imports__()
        return ymbp.import_val