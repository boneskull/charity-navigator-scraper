from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request
from scrapy.project import crawler

from charitynav.items import YearOfCharityData

class CharityAlphaDirSpider(BaseSpider):
    name = "CharityAlphaDir"
    allowed_domains = 'http://www.charitynavigator.org'
    start_urls = [ 'http://www.charitynavigator.org/index.cfm?bay=search.alpha' ]

    def parse(self, response): # find all indexes 1 - Z and request them
        hxs = HtmlXPathSelector(response)
        alpha_categories = hxs.select('//div[@id="maincontent2"]/p/a/@href').extract()
        for category in alpha_categories:
            yield Request(url = category, callback = self.parse_charity_list, dont_filter=True)

    def parse_charity_list(self, response): # find charities listed in the response and request each charity's
        print "! * parse_charity_list * !"
        hxs = HtmlXPathSelector(response)
        charity_rec_url = hxs.select('//div[@id="maincontent2"]/a/@href').extract()
        for url in charity_rec_url:
           yield Request(url, callback = self.parse_charity_rec, dont_filter=True)

    def parse_charity_rec(self, response):
        print "! * parse_charity_rec * !"
        orgid = ""
        slice1 = response.url.find('&orgid=')
        if slice1 == -1:
            url = response.url
            print '^^^ :) NO ORG ID :( &&& '
            return
        else:
            orgid =  response.url[slice1 + len('&orgid='):]
            print 'ORG ID = ' + orgid
            url = 'http://www.charitynavigator.org/index.cfm?bay=search.history_detail&orgid=' + orgid  + '&print=1'
            yield Request(url, callback = self.parse_charity_history, dont_filter=True)

    def parse_cell(self, cell):
        if cell.find('N/A') != -1:
            return 'N/A'
        else:
            if cell.find('checked.gif') != -1:
                return 'true'
            elif cell.find('checkboxX.gif') != -1:
                return 'false'
            elif cell.find('checkboxOptOut.png') != -1:
                return 'opt_out'
            else:
                return cell

    def get_cells(self, slice1, cell_count, response):
        cells = []
        for i in range(cell_count):
            slice1 = response.body.find('<td',slice1)
            slice1 = response.body.find('>',slice1) + 1
            slice2 = response.body.find('</td>', slice1)
            cell = response.body[slice1:slice2]
            cells.append(self.parse_cell(cell))
        return cells

    def parse_charity_history(self, response):
        items = []
        print '! * parse_charity_history * !'
        hxs = HtmlXPathSelector(response)

        name = hxs.select('//h1[@class="charityname"]/text()').extract()
        dates_published = hxs.select('//tr/th[@align="left"]/following-sibling::th[not(@*)]/h3/text()').extract()
        oa_stars = hxs.select('//td[@align="center"]/img[@width="61"]/@alt').extract()
        oa_percent = hxs.select('//img[@width="61"]/../text()').extract()
        slice1 = response.body.find('&nbsp;&nbsp;Financial Rating')
        finance_rating_stars = []
        finance_rating_percent = []
        fye = []
        for i, da_date in enumerate(dates_published):
            slice1 = response.body.find('<td align="center">', slice1) + len('<td align="center">')
            slice2 = response.body.find('</td>', slice1)
            cell = response.body[slice1:slice2]
            cell_slice1 = cell.find('alt="') + len('alt="')
            cell_slice2 = cell.find('"', cell_slice1)
            finance_rating_stars.append(cell[cell_slice1:cell_slice2])
            cell_slice1 = cell.find('<br />', cell_slice2) + len('<br />')
            cell_slice2 = cell.find('<br />', cell_slice1)
            finance_rating_percent.append(cell[cell_slice1:cell_slice2])
            cell_slice1 = cell.find('<strong>', cell_slice2) + len('<strong>')
            cell_slice2 = cell.find('</strong>', cell_slice1)
            fye.append(cell[cell_slice1:cell_slice2])
            slice1 = slice2

        slice1 = response.body.find('&nbsp;&nbsp;Accountability &amp; Transparency Rating')
        accountability_transperancy_stars = []
        accountability_transperancy_percent = []
        for i, da_date in enumerate(dates_published):
            slice1 = response.body.find('<td align="center">', slice1) + len('<td align="center">')
            slice2 = response.body.find('</td>', slice1)
            cell = response.body[slice1:slice2]
            if cell.strip() == 'N/A':
                accountability_transperancy_stars.append('N/A')
                accountability_transperancy_percent.append('N/A')
            else:
                cell_slice1 = cell.find('alt="') + len('alt="')
                cell_slice2 = cell.find('"', cell_slice1)
                accountability_transperancy_stars.append(cell[cell_slice1:cell_slice2])
                cell_slice1 = cell.find('<br />', cell_slice2) + len('<br />')
                accountability_transperancy_percent.append(cell[cell_slice1:])
            slice1 = slice2

        slice0 = response.body.find('Financial Metrics')

        fm_program_expenses = self.get_cells(response.body.find('Program Expenses', slice0), len(dates_published), response)

        fm_administrative_expenses = self.get_cells(response.body.find('Administrative Expenses', slice0), len(dates_published), response)

        fm_fundraising_expenses = self.get_cells(response.body.find('Fundraising Expenses', slice0), len(dates_published), response)

        fm_fundraising_efficiency = self.get_cells(response.body.find('Fundraising Efficiency', slice0), len(dates_published), response)

        fm_primary_revenue_growth = self.get_cells(response.body.find('Primary Revenue Growth', slice0), len(dates_published), response)

        fm_program_expenses_growth = self.get_cells(response.body.find('Program Expenses Growth', slice0), len(dates_published), response)

        fm_working_capital_ratio = self.get_cells(response.body.find('Working Capital Ratio', slice0), len(dates_published), response)

        slice0 = response.body.find('Accountability &amp; Transparency Metrics')

        atm_independent_voting_bm = self.get_cells(response.body.find('Independent Voting Board Members', slice0), len(dates_published), response)

        atm_no_material_diversion_assets = self.get_cells(response.body.find('No Material diversion of assets', slice0), len(dates_published), response)

        atm_afp_x_ia = self.get_cells(response.body.find('Audited financials  prepared by independent accountant', slice0), len(dates_published), response)

        atm_dont_provide_or_receive_loans = self.get_cells(response.body.find('Does Not Provide Loan(s) to or Receive Loan(s) From related parties', slice0), len(dates_published), response)

        atm_doc_boardmeeting_minutes = self.get_cells(response.body.find('Documents Board Meeting Minutes', slice0), len(dates_published), response)

        atm_provide_990 = self.get_cells(response.body.find("Provided copy of Form 990  to organization's governing body in advance of filing", slice0), len(dates_published), response)

        atm_conflict_of_interest_policy = self.get_cells(response.body.find("Conflict of Interest  Policy", slice0), len(dates_published), response)

        atm_whistleblower_policy = self.get_cells(response.body.find("Whistleblower Policy", slice0), len(dates_published), response)

        atm_records_retention_policy = self.get_cells(response.body.find("Records Retention Policy", slice0), len(dates_published), response)

        atm_ceo_listed_with_salary = self.get_cells(response.body.find('CEO listed with  salary', slice0), len(dates_published), response)

        atm_process_4_determining_ceo_comp = self.get_cells(response.body.find("Process for determining  CEO compensation", slice0), len(dates_published), response)

        atm_doesnt_comp_any_bm = self.get_cells(response.body.find("Does Not Compensate Any Board Members", slice0), len(dates_published), response)

        slice0 = response.body.find("Does the charity's website include readily accessible information about the following:")

        www_donor_privacy_policy = self.get_cells(response.body.find('Donor Privacy  Policy', slice0), len(dates_published), response)

        www_board_members_listed = self.get_cells(response.body.find('Board Members Listed', slice0), len(dates_published), response)

        www_audited_financials = self.get_cells(response.body.find('Audited Financials', slice0), len(dates_published), response)

        www_form_990 = self.get_cells(response.body.find('Form 990', slice0), len(dates_published), response)

        www_key_staff_listed = self.get_cells(response.body.find('Key staff listed', slice0), len(dates_published), response)

        revenue_fye = hxs.select('//tr/th/h3[.="Revenue"]/../../th[@class="rightalign"]/text()').extract()

        slice0 = response.body.find("<h3>Revenue</h3>")

        revenue_primary_revenue = hxs.select('//tr/td/a[.="Primary Revenue"]/../../td[@align="right"]/text()').extract()

        revenue_contributions = self.get_cells(response.body.find('&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Contributions', slice0), len(dates_published), response)

        revenue_program_services = self.get_cells(response.body.find('Services </td>', slice0), len(dates_published), response)

        revenue_membership = self.get_cells(response.body.find('Membership', slice0), len(dates_published), response)

        revenue_other_revenue = hxs.select('//a[.="Other Revenue"]/../../td[@align="right"]/text()').extract()

        revenue_total_revenue = self.get_cells(response.body.find('Total Revenue', slice0), len(dates_published), response)

        functional_expenses_fye = hxs.select('//tr/th/h3[.="Functional Expenses"]/../../th[@class="rightalign"]/text()').extract()

        fe_program_expenses = hxs.select('//tr/td/a[.="Program Expenses"]/../../td[@align="right"]/text()').extract()

        fe_administrative_expenses = hxs.select('//tr/td/a[.="Administrative Expenses"]/../../td[@align="right"]/text()').extract()

        fe_fundraising_expenses = hxs.select('//tr/td/a[.="Fundraising Expenses"]/../../td[@align="right"]/text()').extract()

        fe_pay_2_affiliates = hxs.select('//tr/td/a[.="Payments to Affiliates"]/../../td[@align="right"]/text()').extract()

        fe_total_functional_expenses = self.get_cells(response.body.find('Total Functional Expenses', slice0), len(dates_published), response)

        fe_excess_or_deficit = hxs.select('//tr/td/a[.="Excess (or Deficit)"]/../../td[@align="right"]/text()').extract()

        slice0 = response.body.find("Balance Sheet")

        balance_sheet_fye = hxs.select('//tr/th/h3[.="Balance Sheet"]/../../th[@class="rightalign"]/text()').extract()

        balance_sheet_assets = self.get_cells(response.body.find('Assets', slice0), len(dates_published), response)

        balance_sheet_liabilities = self.get_cells(response.body.find('Liabilities', slice0), len(dates_published), response)

        balance_sheet_net_assets = hxs.select('//tr/td/a[.="Net Assets"]/../../td[@align="right"]/text()').extract()

        balance_sheet_working_capital = self.get_cells(response.body.find('Working Capital', slice0), len(dates_published), response)

        for i, da_date in enumerate(dates_published):
            item = YearOfCharityData()
            item['date'] = da_date
            item['name'] = name[0]
            item['overall_rating_stars'] = oa_stars[i]
            item['overall_rating_percent'] = oa_percent[i].strip()
            item['finance_rating_stars'] = finance_rating_stars[i]
            item['finance_rating_percent'] = finance_rating_percent[i].strip()
            item['fye'] = fye[i]
            item['accountability_transperancy_stars'] = accountability_transperancy_stars[i]
            item['accountability_transperancy_percent'] = accountability_transperancy_percent[i].strip()
            item['fm_program_expenses'] = fm_program_expenses[i]
            item['fm_administrative_expenses'] = fm_administrative_expenses[i].strip()
            item['fm_fundraising_expenses'] = fm_fundraising_expenses[i].strip()
            item['fm_fundraising_efficiency'] = fm_fundraising_efficiency[i].strip()
            item['fm_primary_revenue_growth'] = fm_primary_revenue_growth[i].strip()
            item['fm_program_expenses_growth'] = fm_program_expenses_growth[i].strip()
            item['fm_working_capital_ratio'] = fm_working_capital_ratio[i].strip()
            item['atm_independent_voting_bm'] = atm_independent_voting_bm[i]
            item['atm_no_material_diversion_assets'] = atm_no_material_diversion_assets[i]
            item['atm_afp_x_ia'] = atm_afp_x_ia[i]
            item['atm_dont_provide_or_receive_loans'] = atm_dont_provide_or_receive_loans[i]
            item['atm_doc_boardmeeting_minutes'] = atm_doc_boardmeeting_minutes[i]
            item['atm_provide_990'] = atm_provide_990[i]
            item['atm_conflict_of_interest_policy'] = atm_conflict_of_interest_policy[i]
            item['atm_whistleblower_policy'] = atm_whistleblower_policy[i]
            item['atm_records_retention_policy'] = atm_records_retention_policy[i]
            item['atm_ceo_listed_with_salary'] = atm_ceo_listed_with_salary[i]
            item['atm_process_4_determining_ceo_comp'] = atm_process_4_determining_ceo_comp[i]
            item['atm_doesnt_comp_any_bm'] = atm_doesnt_comp_any_bm[i]
            item['www_donor_privacy_policy'] = www_donor_privacy_policy[i]
            item['www_board_members_listed'] = www_board_members_listed[i]
            item['www_audited_financials'] = www_audited_financials[i]
            item['www_form_990'] = www_form_990[i]
            item['www_key_staff_listed'] = www_key_staff_listed[i]
            item['revenue_fye'] = revenue_fye[i]
            item['revenue_primary_revenue'] = revenue_primary_revenue[i]
            item['revenue_contributions'] = revenue_contributions[i]
            item['revenue_program_services'] = revenue_program_services[i]
            item['revenue_membership'] = revenue_membership[i]
            item['revenue_other_revenue'] = revenue_other_revenue[i]
            item['revenue_total_revenue'] = revenue_total_revenue[i]
            item['functional_expenses_fye'] = functional_expenses_fye[i]
            item['fe_program_expenses'] = fe_program_expenses[i]
            item['fe_administrative_expenses'] = fe_administrative_expenses[i]
            item['fe_fundraising_expenses'] = fe_fundraising_expenses[i]
            item['fe_pay_2_affiliates'] = fe_pay_2_affiliates[i]
            item['fe_total_functional_expenses'] = fe_total_functional_expenses[i]
            item['fe_excess_or_deficit'] = fe_excess_or_deficit[i]
            item['balance_sheet_fye'] = balance_sheet_fye[i]
            item['balance_sheet_assets'] = balance_sheet_assets[i]
            item['balance_sheet_liabilities'] = balance_sheet_liabilities[i]
            item['balance_sheet_net_assets'] = balance_sheet_net_assets[i]
            item['balance_sheet_working_capital'] = balance_sheet_working_capital[i]
            items.append(item)

        for item in items:
            print "date = " + item["date"]
            print "name = " + item["name"]
            print "over all rating stars = " + item['overall_rating_stars']
            print "over all rating percent = " + item['overall_rating_percent']
            print "finance_rating_stars = " + item['finance_rating_stars']
            print "finance_rating_percent = " + item['finance_rating_percent']
            print "fye = " + item['fye']
            print "accountability_transperancy_stars = " + item['accountability_transperancy_stars']
            print "accountability_transperancy_percent = " + item['accountability_transperancy_percent']
            print "fm_program_expenses = " + item['fm_program_expenses']
            print "fm_administrative_expenses = " + item['fm_administrative_expenses']
            print "fm_fundraising_expenses = " + item['fm_fundraising_expenses']
            print "fm_fundraising_efficiency = " + item['fm_fundraising_efficiency']
            print "fm_primary_revenue_growth = " + item['fm_primary_revenue_growth']
            print "fm_program_expenses_growth = " + item['fm_program_expenses_growth']
            print "fm_working_capital_ratio = " + item['fm_working_capital_ratio']
            print "atm_independent_voting_bm = " + item['atm_independent_voting_bm']
            print "atm_no_material_diversion_assets = " + item['atm_no_material_diversion_assets']
            print "Audited financials  prepared by independent accountant = " + item['atm_afp_x_ia']
            print "Does Not Provide Loan(s) to or Receive Loan(s) From related parties = " + item['atm_dont_provide_or_receive_loans']
            print "Documents Board Meeting Minutes = " + item['atm_doc_boardmeeting_minutes']
            print "Provided copy of Form 990  to organization's governing body in advance of filing = " + item['atm_provide_990']
            print "Conflict of Interest  Policy = " + item['atm_conflict_of_interest_policy']
            print "Whistleblower Policy = " + item['atm_whistleblower_policy']
            print "Records Retention Policy = " + item['atm_records_retention_policy']
            print "CEO Listed with Salary = " + item['atm_ceo_listed_with_salary']
            print "Process for determining  CEO compensation = " + item['atm_process_4_determining_ceo_comp']
            print "Does Not Compensate Any Board Members = " + item['atm_doesnt_comp_any_bm']
            print "Donor Privacy Policy on website = " + item['www_donor_privacy_policy']
            print "Board Members Listed on website = " + item['www_board_members_listed']
            print "Audited Financials on website = " + item['www_audited_financials']
            print "Form 990 on website = " + item['www_form_990']
            print "Key Staff Listed on website = " + item['www_key_staff_listed']
            print "Revenue FYE = " + item['revenue_fye']
            print "Revenue Primary Revenue = " + item['revenue_primary_revenue']
            print "Revenue Contributions = " + item['revenue_contributions']
            print "Revenue Program Services = " + item['revenue_program_services']
            print "Revenue Membership = " + item['revenue_membership']
            print "Revenue Other Revenue = " + item['revenue_other_revenue']
            print "Revenue Total Revenue = " + item['revenue_total_revenue']
            print "Functional Expenses FYE = " + item['functional_expenses_fye']
            print "Functional Expenses Program Expenses = " + item['fe_program_expenses']
            print "Functional Expenses Administrative Expenses = " + item['fe_administrative_expenses']
            print "Functional Expenses Fundraising Expenses = " + item['fe_fundraising_expenses']
            print "Functional Expenses Pay to Affiliates = " + item['fe_pay_2_affiliates']
            print "Functional Expenses Total Funtional Expenses = " + item['fe_total_functional_expenses']
            print "Functional Expenses Excess (or Deficit) = " + item['fe_excess_or_deficit']
            print "Balance Sheet FYE = " + item['balance_sheet_fye']
            print "Balance Sheet Assets = " + item['balance_sheet_assets']
            print "Balance Sheet Liabilities = " + item['balance_sheet_liabilities']
            print "Net Assets = " + item['balance_sheet_net_assets']
            print "Balance Sheet Working Capital = " + item['balance_sheet_working_capital']
            print

        return items












