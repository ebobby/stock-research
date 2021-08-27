#!/usr/bin/env python
"""Functions to populate the database for the first time."""

import logging
import sys
from datetime import date, datetime

from research.api import EOD
from research.db.config import db
from research.db.model import (
    BalanceSheet,
    CashFlowStatement,
    CompanyProfile,
    DailyPrice,
    IncomeStatement,
    Statistics,
    Stock,
)
from research.utils import parse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(f"./logs/seed-{date.today().strftime('%Y-%m-%d')}.log"),
        logging.StreamHandler(sys.stdout),
    ],
)

__author__ = "Francisco Soto"


DATE_FORMAT = "%Y-%m-%d"


def stocks():
    """Import stocks from polygon and eod into the database."""
    logger = logging.getLogger("stock sync")

    logger.info("Stocks sync started")

    # APIs
    eod_api = EOD()

    # Fetch all available stocks
    logger.info("Fetching current stock list from EOD")
    eod_tickers = [
        ticker
        for ticker in eod_api.exchange_symbol_list()
        if ticker["Type"] == "Common Stock"
        and ticker["Exchange"] in ["NASDAQ", "NYSE", "NYSE ARCA", "NYSE MKT"]
        and "test" not in ticker["Name"].lower()
    ]
    logger.info(f"{len(eod_tickers)} stocks found")

    # First set all stocks to inactive.
    db.table("stocks").update(active=False)

    # Update all tickers
    for ticker in eod_tickers:
        stock = Stock.where_symbol(ticker["Code"]).first() or Stock()

        stock.symbol = ticker["Code"]
        stock.name = ticker["Name"]
        stock.country = ticker["Country"]
        stock.currency = ticker["Currency"]
        stock.exchange = ticker["Exchange"]
        stock.active = True
        stock.source = "eod"
        stock.save()

    active = Stock.where_active(True).count()
    inactive = Stock.where_active(False).count()

    logger.info(
        f"Stock sync finished, {active} active stocks, {inactive} inactive stocks"
    )


def fundamentals():
    """Import historical fundamentals from EOD into the database."""
    logger = logging.getLogger("fundamentals sync")

    logger.info("Fundamentals sync starting")

    api = EOD()

    stocks = list(Stock.where("active", True).order_by("symbol").get())
    # stocks = list(
    #    Stock.where("active", True)
    #    .where_raw("id NOT IN (SELECT stock_id FROM company_profiles)")
    #    .order_by("symbol")
    #    .get()
    # )

    logger.info(f"{len(stocks)} active stocks found")

    report_time = datetime.timestamp(datetime.now())
    processed = 0

    for stock in stocks:
        data = api.fundamentals(stock.symbol_for_api)

        if data and "error" not in data:
            process_company_profile(stock, data, logger)
            process_company_stats(stock, data, logger)

            ic_statements = data.get("Financials", {}).get("Income_Statement")
            if ic_statements:
                process_income_statements(
                    stock, "Y", list(ic_statements["yearly"].values()), logger
                )
                process_income_statements(
                    stock, "Q", list(ic_statements["quarterly"].values()), logger
                )
            else:
                stock.add_error("No income statements found.", "eod")
                logger.warning(f"No income statements for {stock.symbol}.")

            b_sheets = data.get("Financials", {}).get("Balance_Sheet")
            if b_sheets:
                process_balance_sheets(
                    stock, "Y", list(b_sheets["yearly"].values()), logger
                )
                process_balance_sheets(
                    stock, "Q", list(b_sheets["quarterly"].values()), logger
                )
            else:
                stock.add_error("No balance sheets found.", "eod")
                logger.warning(f"No balance sheets for {stock.symbol}.")

            cf_statements = data.get("Financials", {}).get("Cash_Flow")
            if cf_statements:
                process_cash_flow_statements(
                    stock, "Y", list(cf_statements["yearly"].values()), logger
                )
                process_cash_flow_statements(
                    stock, "Q", list(cf_statements["quarterly"].values()), logger
                )
            else:
                stock.add_error("No cash flow statements found.", "eod")
                logger.warning(f"No cash flow statements for {stock.symbol}.")

            processed += 1
        else:
            stock.add_error("No fundamental data found.", "eod")
            logger.warning(f"Failed to find fundamental data for {stock.symbol}")

        # Report current progress
        if datetime.timestamp(datetime.now()) - report_time >= 60:
            logger.info(f"{processed} stocks processed.")
            report_time = datetime.timestamp(datetime.now())

    logger.info(f"Fundamentals sync finished, {processed} stocks processed.")


def prices(day=date.today()):
    """Imports day stocks prices EOD into the database."""
    logger = logging.getLogger("stock price sync")

    api = EOD()

    logger.info(f"Stock price sync for {day} started")

    if day.weekday() > 4:
        logger.info("No price data during weekends.")
        return

    # Fetch all available stocks
    logger.info(f"Fetching day eod stock prices for {day} from EOD")
    eod_list = api.bulk_eod("US", date=day.strftime(DATE_FORMAT))

    if not eod_list:
        logger.info("No price data. Maybe holiday?")
        return

    if "error" in eod_list:
        logger.error(f"Error while fetching end of day price data: {eod_list['error']}")
        return

    # Turn EOD list into a dict for faster lookup.
    eod_data = {p["code"]: p for p in eod_list}
    eod_list = None

    stocks = list(Stock.where("active", True).order_by("symbol").get())

    saved = 0
    for stock in stocks:

        def money_field(report, field):
            value = parse.float_or(report.get(field, 0.0), 0.0)

            if len(format(value, "f").split(".")[0]) > 15:
                stock.add_error(
                    f"Invalid value {value} in column {field} for end-of-day price for {date}.",
                    "eod",
                )
                logger.error(
                    f"Invalid value {value} in column {field} for end-of-day price for {date}.",
                )
                return 0.0

            return value

        daily_price = stock.daily_prices().where("date", day).first() or DailyPrice()

        price = eod_data.get(stock.symbol_for_api)

        if not price:
            logger.info(f"End-of-day price data not found for {stock.symbol_for_api}")
            continue

        daily_price.date = day
        daily_price.open = money_field(price, "open")
        daily_price.high = money_field(price, "high")
        daily_price.low = money_field(price, "low")
        daily_price.close = money_field(price, "close")
        daily_price.adjusted_close = money_field(price, "adjusted_close")
        daily_price.volume = int(money_field(price, "volume"))
        daily_price.source = "eod"

        if "created_at" in daily_price.attributes_to_dict():
            daily_price.save()
        else:
            stock.daily_prices().save(daily_price)

        saved += 1

    logger.info(f"Stock end-of-day prices sync finished, saved={saved}")


def process_income_statements(stock, report_type, reports, logger):
    for report in reports:
        report_date = datetime.strptime(report["date"], DATE_FORMAT)

        statement = (
            stock.income_statements()
            .where("report_type", report_type)
            .where("report_date", report_date)
            .first()
        )

        if not statement:
            statement = IncomeStatement()

        def money_field(report, field):
            value = parse.float_or(report.get(field, 0.0), 0.0)

            if len(format(value, "f").split(".")[0]) > 15:
                stock.add_error(
                    f"Invalid value {value} in column {field} for income statement {report_type}-{report['date']}.",
                    "eod",
                )
                logger.error(
                    f"Invalid value {value} in column {field} for report {report['date']} for {stock.symbol}."
                )
                return 0.0

            return value

        statement.report_date = report_date
        statement.report_type = report_type
        statement.filing_date = (
            datetime.strptime(report["filing_date"], DATE_FORMAT)
            if report["filing_date"]
            else report_date
        )
        statement.currency = report.get("currency_symbol", "")
        statement.total_revenue = money_field(report, "totalRevenue")
        statement.cost_of_revenue = money_field(report, "costOfRevenue")
        statement.gross_profit = money_field(report, "grossProfit")
        statement.sga_expense = money_field(
            report, "sellingGeneralAdministrative"
        ) + money_field(report, "sellingAndMarketingExpenses")
        statement.research_and_development = money_field(report, "researchDevelopment")
        statement.depreciation_and_amortization = money_field(
            report, "depreciationAndAmortization"
        )
        statement.operating_expenses = money_field(report, "totalOperatingExpenses")
        statement.operating_income = money_field(report, "operatingIncome")
        statement.interest_expense = money_field(report, "interestExpense")
        statement.interest_income = money_field(report, "interestIncome")
        statement.other_expenses = money_field(report, "totalOtherIncomeExpenseNet")
        statement.income_before_tax = money_field(report, "incomeBeforeTax")
        statement.income_tax = money_field(report, "incomeTaxExpense")
        statement.net_income_after_tax = money_field(
            report, "netIncomeFromContinuingOps"
        )
        statement.discontinued_operations = money_field(
            report, "discontinuedOperations"
        )
        statement.net_earnings = money_field(report, "netIncome")

        statement.source = "eod"

        if "created_at" in statement.attributes_to_dict():
            statement.save()
        else:
            stock.income_statements().save(statement)


def process_balance_sheets(stock, report_type, reports, logger):
    for report in reports:
        report_date = datetime.strptime(report["date"], DATE_FORMAT)

        sheet = (
            stock.balance_sheets()
            .where("report_type", report_type)
            .where("report_date", report_date)
            .first()
        )

        if not sheet:
            sheet = BalanceSheet()

        def money_field(report, field):
            value = parse.float_or(report.get(field, 0.0), 0.0)

            if len(format(value, "f").split(".")[0]) > 15:
                stock.add_error(
                    f"Invalid value {value} in column {field} for balance sheet {report_type}-{report['date']}.",
                    "eod",
                )
                logger.error(
                    f"Invalid value {value} in column {field} for report {report['date']} for {stock.symbol}."
                )
                return 0.0

            return value

        sheet.report_date = report_date
        sheet.report_type = report_type
        sheet.filing_date = (
            datetime.strptime(report["filing_date"], DATE_FORMAT)
            if report["filing_date"]
            else report_date
        )
        sheet.currency = report.get("currency_symbol", "")

        sheet.total_assets = money_field(report, "totalAssets")
        sheet.total_current_assets = money_field(report, "totalCurrentAssets")
        sheet.cash_and_short_term = money_field(report, "cashAndShortTermInvestments")
        sheet.inventory = money_field(report, "inventory")
        sheet.receivables = money_field(report, "netReceivables")
        sheet.other_current_assets = money_field(report, "otherCurrentAssets")
        sheet.total_non_current_assets = money_field(report, "nonCurrentAssetsTotal")
        sheet.property_plant_equipment = money_field(
            report, "propertyPlantAndEquipmentGross"
        )
        sheet.good_will = money_field(report, "goodWill")
        sheet.intangible_assets = money_field(report, "intangibleAssets")
        sheet.long_term_investments = money_field(report, "longTermInvestments")
        sheet.other_non_current_assets = money_field(report, "nonCurrrentAssetsOther")
        sheet.total_liabilities = money_field(report, "totalLiab")
        sheet.total_current_liabilities = money_field(report, "totalCurrentLiabilities")
        sheet.accounts_payable = money_field(report, "accountsPayable")
        sheet.short_term_debt = money_field(report, "shortTermDebt")
        sheet.other_current_liabilities = money_field(report, "otherCurrentLiab")
        sheet.total_non_current_liabilities = money_field(
            report, "nonCurrentLiabilitiesTotal"
        )
        sheet.long_term_debt = money_field(report, "longTermDebt")
        sheet.deferred_long_term_liabilities = money_field(
            report, "deferredLongTermLiab"
        )
        sheet.other_non_current_liabilities = money_field(
            report, "nonCurrentLiabilitiesOther"
        )
        sheet.total_stockholder_equity = money_field(report, "totalStockholderEquity")
        sheet.preferred_stock_equity = money_field(report, "preferredStockTotalEquity")
        sheet.common_stock_equity = money_field(report, "commonStockTotalEquity")
        sheet.paid_in_capital = money_field(report, "additionalPaidInCapital")
        sheet.retained_earnings = money_field(report, "retainedEarnings")
        sheet.treasury_stock = money_field(report, "treasuryStock")
        sheet.gain_losses = money_field(report, "accumulatedOtherComprehensiveIncome")
        sheet.non_controlling_interest = money_field(
            report, "noncontrollingInterestInConsolidatedEntity"
        )
        sheet.capital_lease_obligations = money_field(report, "capitalLeaseObligations")
        sheet.net_tangible_assets = money_field(report, "netTangibleAssets")
        sheet.net_working_capital = money_field(report, "netWorkingCapital")
        sheet.net_invested_capital = money_field(report, "netInvestedCapital")
        sheet.short_long_term_debt_total = money_field(report, "shortLongTermDebtTotal")
        sheet.net_debt = money_field(report, "netDebt")
        sheet.common_stock_shares_outstanding = money_field(
            report, "commonStockSharesOutstanding"
        )

        sheet.total_capitalization = (
            sheet.long_term_debt + sheet.total_stockholder_equity
        )

        sheet.source = "eod"

        if "created_at" in sheet.attributes_to_dict():
            sheet.save()
        else:
            stock.balance_sheets().save(sheet)


def process_cash_flow_statements(stock, report_type, reports, logger):
    for report in reports:
        report_date = datetime.strptime(report["date"], DATE_FORMAT)

        statement = (
            stock.cash_flow_statements()
            .where("report_type", report_type)
            .where("report_date", report_date)
            .first()
        )

        if not statement:
            statement = CashFlowStatement()

        def money_field(report, field):
            value = parse.float_or(report.get(field, 0.0), 0.0)

            if len(format(value, "f").split(".")[0]) > 15:
                stock.add_error(
                    f"Invalid value {value} in column {field} for cash flow statement {report_type}-{report['date']}.",
                    "eod",
                )
                logger.error(
                    f"Invalid value {value} in column {field} for report {report['date']} for {stock.symbol}."
                )
                return 0.0

            return value

        statement.report_date = report_date
        statement.report_type = report_type
        statement.filing_date = (
            datetime.strptime(report["filing_date"], DATE_FORMAT)
            if report["filing_date"]
            else report_date
        )
        statement.currency = report.get("currency_symbol", "")

        statement.net_income = money_field(report, "netIncome")
        statement.depreciation = money_field(report, "depreciation")
        statement.other_cash_from_operating_activites = money_field(
            report, "cashFlowsOtherOperating"
        )
        statement.total_cash_from_operating_activities = money_field(
            report, "totalCashFromOperatingActivities"
        )
        statement.capital_expenditures = money_field(report, "capitalExpenditures")
        statement.investments = money_field(report, "investments")
        statement.other_cash_from_investing_activities = money_field(
            report, "otherCashflowsFromInvestingActivities"
        )
        statement.total_cash_from_investing_activities = money_field(
            report, "totalCashflowsFromInvestingActivities"
        )
        statement.net_borrowing = money_field(report, "netBorrowings")
        statement.dividends_paid = money_field(report, "dividendsPaid")
        statement.sale_or_purchase_of_stock = money_field(report, "salePurchaseOfStock")
        statement.other_cash_from_financing_activities = money_field(
            report, "otherCashflowsFromFinancingActivities"
        )
        statement.total_cash_from_financing_activities = money_field(
            report, "totalCashFromFinancingActivities"
        )
        statement.initial_cash = money_field(report, "beginPeriodCashFlow")
        statement.change_in_cash = money_field(report, "changeInCash")
        statement.final_cash = money_field(report, "endPeriodCashFlow")
        statement.free_cash_flow = money_field(report, "freeCashFlow")

        statement.source = "eod"

        if "created_at" in statement.attributes_to_dict():
            statement.save()
        else:
            stock.cash_flow_statements().save(statement)


def process_company_profile(stock, response, logger):
    profile = stock.company_profile

    data = response.get("General", {})

    if not profile:
        profile = CompanyProfile()

    profile.name = data.get("Name", "")
    profile.description = data.get("Description", "") or ""
    profile.address = data.get("Address", "") or ""
    profile.phone = data.get("Phone", "") or ""
    profile.url = data.get("WebURL", "") or ""
    profile.logo_url = (
        f"https://eodhistoricaldata.com{data['LogoURL']}"
        if "LogoURL" in data and data["LogoURL"]
        else ""
    )

    profile.exchange = data.get("Exchange", "") or ""
    profile.currency = data.get("CurrencyCode", "") or ""
    profile.country = data.get("CountryISO", "") or ""
    profile.location = data.get("InternationalDomestic", "") or ""

    profile.sector = data.get("Sector", "") or ""
    profile.industry = data.get("Industry", "") or ""
    profile.category = data.get("HomeCategory", "") or ""

    profile.isin = data.get("ISIN", "") or ""
    profile.cusip = data.get("CUSIP", "") or ""
    profile.cik = data.get("CIK", "") or ""

    profile.is_delisted = data.get("IsDelisted", False) or False

    profile.fulltime_employees = data.get("FullTimeEmployees", 0) or 0

    profile.ipo_date = (
        datetime.strptime(data["IPODate"], DATE_FORMAT)
        if "IPODate" in data and data["IPODate"]
        else None
    )
    profile.last_update_date = (
        datetime.strptime(data["UpdatedAt"], DATE_FORMAT)
        if "UpdatedAt" in data and data["UpdatedAt"]
        else None
    )

    profile.source = "eod"

    if "created_at" in profile.attributes_to_dict():
        profile.save()
    else:
        stock.company_profile().save(profile)


def process_company_stats(stock, response, logger):
    stats = stock.statistics

    highlights = response.get("Highlights", {})
    valuation = response.get("Valuation", {})
    share_stats = response.get("SharesStats", {})
    technicals = response.get("Technicals", {})
    earnings = response.get("Earnings", {}).get("Trend", {}).values()

    if not stats:
        stats = Statistics()

    def money_field(report, field):
        value = parse.float_or(report.get(field, 0.0), 0.0)

        if len(format(value, "f").split(".")[0]) > 15:
            stock.add_error(
                f"Invalid value {value} in column {field} for company statistics.",
                "eod",
            )
            logger.error(
                f"Invalid value {value} in column {field} for company statistics.",
            )
            return 0.0

        return parse.float_or(report.get(field, 0.0), 0.0)

    stats.market_capitalization = money_field(highlights, "MarketCapitalization")
    stats.wallstreet_target_price = money_field(highlights, "WallStreetTargetPrice")
    stats.pe_ratio = money_field(highlights, "PERatio")
    stats.peg_ratio = money_field(highlights, "PEGRatio")
    stats.book_value_per_share = money_field(highlights, "BookValue")
    stats.earnings_per_share = money_field(highlights, "EarningsShare")
    stats.dividend_per_share = money_field(highlights, "DividendShare")
    stats.dividend_yield = money_field(highlights, "DividendYield")
    stats.profit_margin = money_field(highlights, "ProfitMargin")
    stats.diluted_eps_ttm = money_field(highlights, "DilutedEpsTTM")
    stats.gross_profit_ttm = money_field(highlights, "GrossProfitTTM")
    stats.price_to_sales_ttm = money_field(valuation, "PriceSalesTTM")
    stats.operating_margin_ttm = money_field(highlights, "OperatingMarginTTM")
    stats.return_on_assets_ttm = money_field(highlights, "ReturnOnAssetsTTM")
    stats.return_on_equity_ttm = money_field(highlights, "ReturnOnEquityTTM")
    stats.revenue_per_share_ttm = money_field(highlights, "RevenuePerShareTTM")
    stats.revenue_ttm = money_field(highlights, "RevenueTTM")
    stats.price_to_book_mrq = money_field(valuation, "PriceBookMRQ")
    stats.quarterly_revenue_growth_yoy = money_field(
        highlights, "QuarterlyRevenueGrowthYOY"
    )
    stats.quarterly_earnings_growth_yoy = money_field(
        highlights, "QuarterlyEarningsGrowthYOY"
    )
    stats.outstanding_shares = money_field(share_stats, "SharesOutstanding")
    stats.floating_shares = money_field(share_stats, "SharesFloat")
    stats.percent_insiders = money_field(share_stats, "PercentInsiders")
    stats.percent_institutions = money_field(share_stats, "PercentInstitutions")
    stats.short_ratio = money_field(share_stats, "ShortRatio")
    stats.short_percent = money_field(share_stats, "ShortPercentOutstanding")
    stats.beta = money_field(technicals, "Beta")
    stats.eps_estimate_current_year = money_field(highlights, "EPSEstimateCurrentYear")
    stats.eps_estimate_next_year = money_field(highlights, "EPSEstimateNextYear")
    stats.eps_estimate_current_quarter = money_field(
        highlights, "EPSEstimateCurrentQuarter"
    )
    stats.eps_estimate_next_quarter = money_field(highlights, "EPSEstimateNextQuarter")

    one_year = [e for e in earnings if "period" in e and e["period"] == "+1y"]
    if one_year:
        one_year = one_year[0]
        stats.growth_estimate_next_year = money_field(one_year, "growth")
    else:
        stats.growth_estimate_next_year = 0.0

    current_year = [e for e in earnings if "period" in e and e["period"] == "0y"]
    if current_year:
        current_year = current_year[0]
        stats.growth_estimate_current_year = money_field(current_year, "growth")
    else:
        stats.growth_estimate_current_year = 0.0

    current_quarter = [e for e in earnings if "period" in e and e["period"] == "0q"]
    if current_quarter:
        current_quarter = current_quarter[0]
        stats.growth_estimate_current_quarter = money_field(current_quarter, "growth")
    else:
        stats.growth_estimate_current_quarter = 0.0

    stats.most_recent_quarter = (
        datetime.strptime(highlights["MostRecentQuarter"], DATE_FORMAT)
        if "MostRecentQuarter" in highlights
        and highlights["MostRecentQuarter"]
        and highlights["MostRecentQuarter"] != "0000-00-00"
        else None
    )

    stats.source = "eod"

    if "created_at" in stats.attributes_to_dict():
        stats.save()
    else:
        stock.statistics().save(stats)
