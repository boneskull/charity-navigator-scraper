# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/topics/items.html

from scrapy.item import Item, Field

class YearOfCharityData(Item):
    # define the fields for your item here like:
    name = Field()
    date = Field()
    overall_rating_stars = Field()
    overall_rating_percent = Field()
    finance_rating_stars = Field()
    finance_rating_percent = Field()
    fye = Field()
    accountability_transperancy_stars = Field()
    accountability_transperancy_percent = Field()
    fm_program_expenses = Field()
    fm_administrative_expenses = Field()
    fm_fundraising_expenses = Field()
    fm_fundraising_efficiency = Field()
    fm_primary_revenue_growth = Field()
    fm_program_expenses_growth = Field()
    fm_working_capital_ratio = Field()
    atm_independent_voting_bm = Field()
    atm_no_material_diversion_assets = Field()
    atm_afp_x_ia = Field()
    atm_dont_provide_or_receive_loans = Field()
    atm_doc_boardmeeting_minutes = Field()
    atm_provide_990 = Field()
    atm_conflict_of_interest_policy = Field()
    atm_whistleblower_policy = Field()
    atm_records_retention_policy = Field()
    atm_ceo_listed_with_salary = Field()
    atm_process_4_determining_ceo_comp = Field()
    atm_doesnt_comp_any_bm = Field()
    www_donor_privacy_policy = Field()
    www_board_members_listed = Field()
    www_audited_financials = Field()
    www_form_990 = Field()
    www_key_staff_listed = Field()
    revenue_fye = Field()
    revenue_primary_revenue = Field()
    revenue_contributions = Field()
    revenue_program_services = Field()
    revenue_membership = Field()
    revenue_other_revenue = Field()
    revenue_total_revenue = Field()
    functional_expenses_fye = Field()
    fe_program_expenses = Field()
    fe_administrative_expenses = Field()
    fe_fundraising_expenses = Field()
    fe_pay_2_affiliates = Field()
    fe_total_functional_expenses = Field()
    fe_excess_or_deficit = Field()
    balance_sheet_fye = Field()
    balance_sheet_assets = Field()
    balance_sheet_liabilities = Field()
    balance_sheet_net_assets = Field()
    balance_sheet_working_capital = Field()
