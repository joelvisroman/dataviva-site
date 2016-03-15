# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, g, request
from dataviva.apps.general.views import get_locale
from dataviva.api.rais.services import Industry, IndustryOccupation, IndustryMunicipality, IndustryByLocation
from dataviva import db
from sqlalchemy import func, desc
from dataviva.api.rais.models import Yi, Ybi

mod = Blueprint('industry', __name__,
                template_folder='templates',
                url_prefix='/<lang_code>/industry')


@mod.url_value_preprocessor
def pull_lang_code(endpoint, values):
    g.locale = values.pop('lang_code')


@mod.url_defaults
def add_language_code(endpoint, values):
    values.setdefault('lang_code', get_locale())


@mod.route('/<cnae_id>')
def index(cnae_id):

    bra_id = request.args.get('bra_id')

    industry = {}
    header = {}
    body = {}

    industry['cnae_id'] = cnae_id
    industry['section_id'] = cnae_id[0]

    if bra_id is None:
        industry['flag_preview_headers'] = False
        industry['county'] = True  # view county where no country
    else:
        industry['flag_preview_headers'] = True
        industry['bra_id'] = bra_id

        if len(bra_id) == 9:  # municipatity
            industry['county'] = False
        else:
            industry['county'] = True

    if len(cnae_id) == 6:  # class
        industry['class'] = True
    else:
        industry['class'] = False

    if bra_id:
        industry_service = IndustryByLocation(bra_id=bra_id, cnae_id=cnae_id)
        header['name_bra'] = industry_service.name()
        header['rca'] = industry_service.rca()
        header['distance'] = industry_service.distance()
        header['opportunity_gain'] = industry_service.opportunity_gain()
    else:
        industry_service = Industry(cnae_id=cnae_id)

    industry_occupation_service = IndustryOccupation(
        bra_id=bra_id, cnae_id=cnae_id)
    industry_municipality_service = IndustryMunicipality(
        bra_id=bra_id, cnae_id=cnae_id)

    header['name'] = industry_service.get_name()
    header['year'] = industry_service.get_year()

    header[
        'average_monthly_income'] = industry_service.average_monthly_income()
    header['salary_mass'] = industry_service.salary_mass()
    header['num_jobs'] = industry_service.num_jobs()
    header['num_establishments'] = industry_service.num_establishments()

    body[
        'occ_with_more_number_jobs_name'] = industry_occupation_service.occupation_with_more_jobs()
    body[
        'occ_with_more_number_jobs_value'] = industry_occupation_service.highest_number_of_jobs()

    body[
        'occ_with_more_wage_avg_name'] = industry_occupation_service.occupation_with_biggest_wage_average()
    body[
        'occ_with_more_wage_avg_value'] = industry_occupation_service.biggest_wage_average()
    body[
        'state_with_more_jobs'] = industry_municipality_service.state()
    body[
        'state_with_more_jobs_value'] = industry_municipality_service.state_num_jobs()

    if bra_id is None or len(bra_id) != 9:
        body[
            'municipality_with_more_num_jobs_value'] = industry_municipality_service.highest_number_of_jobs()
        body[
            'municipality_with_more_num_jobs_name'] = industry_municipality_service.municipality_with_more_num_jobs()

        body['municipality_with_more_wage_avg_name'] = industry_municipality_service.\
            municipality_with_more_wage_average()
        body[
            'municipality_with_more_wage_avg_value'] = industry_municipality_service.biggest_wage_average()

    if bra_id:

        ybi_max_year = db.session.query(
            func.max(Ybi.year)).filter_by(cnae_id=cnae_id, bra_id=bra_id)
        list_rais = Ybi.query.filter(
            Ybi.year == ybi_max_year,
            Ybi.bra_id == bra_id,
            Ybi.cnae_id_len == func.length(cnae_id)
        ).order_by(desc(Ybi.num_jobs)).all()

    else:

        yi_max_year = db.session.query(
            func.max(Yi.year)).filter_by(cnae_id=cnae_id)
        list_rais = Yi.query.filter(
            Yi.year == yi_max_year,
            Yi.cnae_id_len == func.length(cnae_id)
        ).order_by(desc(Yi.num_jobs)).all()

    for index, rais in enumerate(list_rais):
        if rais.cnae_id == cnae_id:
            header['ranking'] = index+1
            break

    header['RAIS'] = rais.cnae_id

    industry_service_num_establishments = Industry(cnae_id=cnae_id)
    header[
        'num_establishments_brazil'] = industry_service_num_establishments.num_establishments()

    return render_template(
        'industry/index.html',
        body_class='perfil-estado',
        header=header,
        body=body,
        industry=industry)
