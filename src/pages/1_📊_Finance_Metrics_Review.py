import sys
from pathlib import Path
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent
sys.path.append(str(project_root))


import streamlit as st

st.set_page_config(page_title="Finance Metrics Reviews", page_icon=":bar_chart:", layout="wide", initial_sidebar_state="collapsed")

st.title(":chart_with_upwards_trend: Finance Metrics Review")
st.info("""
Simply input the ticker symbol of your desired company and hit the 'Generate Insights' button. Allow a few moments for the system to compile the data and insights tailored to the selected company. Once done, you have the option to browse through these insights directly on the platform or download a comprehensive report by selecting 'Generate PDF', followed by 'Download PDF'.
""")
        

from src.income_statement import income_statement
from src.balance_sheet import balance_sheet
from src.cash_flow import cash_flow
from src.news_sentiment import top_news
from src.company_overview import company_overview
from src.utils import round_numeric, format_currency, create_donut_chart, create_bar_chart
from src.pdf_gen import gen_pdf
from src.ticker_symbol import get_all_company_names, get_ticker_symbol

OPENAI_API_KEY = st.sidebar.text_input("Enter OpenAI API key", type="password")

if not OPENAI_API_KEY:
    st.error("Please enter your OpenAI API Key")
else:


    col1, col2 = st.columns([0.25, 0.75], gap="medium")

    with col1:
        st.write("""
        ### Select Insights
        """)
        with st.expander("**Income Statement Insights**", expanded=True):
            revenue_health = st.toggle("Revenue Health", value=True)
            operational_efficiency = st.toggle("Operational Efficiency", value=True)
            r_and_d_focus = st.toggle("R&D Focus", value=True)
            debt_management = st.toggle("Debt Management", value=True)
            profit_retention = st.toggle("Profit Retention", value=True)

            income_statement_feature_list = [revenue_health, operational_efficiency, r_and_d_focus, debt_management, profit_retention]

        with st.expander("**Balance Sheet Insights**", expanded=True):
            liquidity_position = st.toggle("Liquidity Position", value=True)
            operational_efficiency2 = st.toggle("Operational efficiency", value=True)
            capital_structure = st.toggle("Capital Structure", value=True)
            inventory_management = st.toggle("Inventory Management", value=True)
            overall_solvency = st.toggle("Overall Solvency", value=True)

            balance_sheet_feature_list = [liquidity_position, operational_efficiency2, capital_structure, inventory_management, overall_solvency]

        with st.expander("**Cash Flow Insights**", expanded=True):
            operational_cash_efficiency = st.toggle("Operational Cash Efficiency", value=True)
            investment_capability = st.toggle("Investment Capability", value=True)
            financial_flexibility = st.toggle("Financial Flexibility", value=True)
            dividend_sustainability = st.toggle("Dividend Sustainability", value=True)
            debt_service_capability = st.toggle("Debt Service Capability", value=True)

            cash_flow_feature_list = [operational_cash_efficiency, investment_capability, financial_flexibility, dividend_sustainability, debt_service_capability]


    with col2:
        ticker = st.text_input("**Enter ticker symbol**")
        st.warning("Example Tickers: Apple Inc. - AAPL, Microsoft Corporation - MSFT, Tesla Inc. - TSLA")

        if "company_overview" not in st.session_state:
            st.session_state.company_overview = None

        if "income_statement" not in st.session_state:
            st.session_state.income_statement = None

        if "balance_sheet" not in st.session_state:
            st.session_state.balance_sheet = None

        if "cash_flow" not in st.session_state:
            st.session_state.cash_flow = None

        if "news" not in st.session_state:
            st.session_state.news = None

        if "all_outputs" not in st.session_state:
            st.session_state.all_outputs = None

        if ticker:
            if st.button("Generate Insights"):

                with st.status("**Generating Insights...**"):

                    st.write("Getting company overview...")
                    st.session_state.company_overview = company_overview(ticker)
                        
                    st.write("Generating income statement insights...")
                    if any(income_statement_feature_list):
                        st.session_state.income_statement = income_statement(ticker, income_statement_feature_list, OPENAI_API_KEY)
                    
                    st.write("Generating balance sheet insights...")
                    if any(balance_sheet_feature_list):
                        st.session_state.balance_sheet = balance_sheet(ticker, balance_sheet_feature_list, OPENAI_API_KEY)
                    
                    st.write("Generating cash flow insights...")
                    if any(cash_flow_feature_list):
                        st.session_state.cash_flow = cash_flow(ticker, cash_flow_feature_list, OPENAI_API_KEY)
                    
                    st.write('Getting latest news...')
                    st.session_state.news = top_news(ticker, 10)

                    if st.session_state.company_overview and st.session_state.income_statement and st.session_state.balance_sheet and st.session_state.cash_flow and st.session_state.news:
                        st.session_state.all_outputs = True

                    if st.session_state.company_overview == None:
                        st.error(f"No Data available")

        if st.session_state.all_outputs:
            st.toast("Insights successfully Generated!")
            if st.button("Generate PDF"):
                gen_pdf(st.session_state.company_overview["Name"], 
                    st.session_state.company_overview,
                    st.session_state.income_statement,
                    st.session_state.balance_sheet,
                    st.session_state.cash_flow,
                    None)
                st.toast("PDF successfully generated!")
                with open("pdf/final_report.pdf", "rb") as file:
                    st.download_button(
                        label="Download PDF",
                        data=file,
                        file_name="final_report.pdf",
                        mime="application/pdf"
                    )

            

        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Company Overview", "Income Statement", "Balance Sheet", "Cash Flow", "News Sentiment"])


        if st.session_state.company_overview:
            with tab1:
                with st.container():
                    
                    st.write("# Company Overview")
                    # st.markdown("### Company Name:")
                    st.markdown(f"""### {st.session_state.company_overview["Name"]}""")
                    col1, col2, col3 = st.columns(3)
                    col1.markdown("### Symbol:")
                    col1.write(st.session_state.company_overview["Symbol"])
                    col2.markdown("### Exchange:")
                    col2.write(st.session_state.company_overview["Exchange"])
                    col3.markdown("### Currency:")
                    col3.write(st.session_state.company_overview["Currency"])

                    col1, col2, col3 = st.columns(3)
                    col1.markdown("### Sector:")
                    col1.write(st.session_state.company_overview["Sector"])
                    col2.markdown("### Industry:")
                    col2.write(st.session_state.company_overview["Industry"])
                    col3.write()
                    st.markdown("### Description:")
                    st.write(st.session_state.company_overview["Description"])
                    
                    col1, col2, col3 = st.columns(3)
                    col1.markdown("### Country:")
                    col1.write(st.session_state.company_overview["Country"])
                    col2.markdown("### Address:")
                    col2.write(st.session_state.company_overview["Address"])
                    col3.write()

                    col1, col2, col3 = st.columns(3)
                    col1.markdown("### Fiscal Year End:")
                    col1.write(st.session_state.company_overview["FiscalYearEnd"])
                    col2.markdown("### Latest Quarter:")
                    col2.write(st.session_state.company_overview["LatestQuarter"])
                    col3.markdown("### Market Capitalization:")
                    col3.write(format_currency(st.session_state.company_overview["MarketCapitalization"]))


        if st.session_state.income_statement:

            with tab2:
                
                st.write("# Income Statement")
                st.write("## Metrics")

                with st.container():

                    col1, col2, col3 = st.columns(3)

                    col1.metric("Gross Profit Margin", round_numeric(st.session_state.income_statement["metrics"]["gross_profit_margin"], 2))
                    col2.metric("Operating Profit Margin", round_numeric(st.session_state.income_statement["metrics"]["operating_profit_margin"], 2))
                    col3.metric("Net Profit Margin", round_numeric(st.session_state.income_statement["metrics"]["net_profit_margin"], 2))
                    col1.metric("Cost Efficiency", round_numeric(st.session_state.income_statement["metrics"]["cost_efficiency"], 2))
                    col2.metric("SG&A Efficiency", round_numeric(st.session_state.income_statement["metrics"]["sg_and_a_efficiency"], 2))
                    col3.metric("Interest Coverage Ratio", round_numeric(st.session_state.income_statement["metrics"]["interest_coverage_ratio"], 2))
            
                
                st.write("## Insights")

                try:
                    if revenue_health:
                    
                        st.write("### Revenue Health")
                        st.markdown(st.session_state.income_statement["insights"]["revenue_health"])
                        total_revenue_chart = create_bar_chart(st.session_state.income_statement["chart_data"], 
                                                                    "total_revenue", 
                                                                    "Revenue Growth")
                        st.write(total_revenue_chart)
                except:
                    st.error("This insight has not been generated")


                try:
                    if operational_efficiency:
                        st.write("### Operational Efficiency")
                        st.write(st.session_state.income_statement["insights"]["operational_efficiency"])
                except:
                    st.error("This insight has not been generated")

                try:
                    if r_and_d_focus:
                        st.write("### R&D Focus")
                        st.write(st.session_state.income_statement["insights"]["r_and_d_focus"])
                except:
                    st.error("This insight has not been generated")

                try:
                    if debt_management:
                        st.write("### Debt Management")
                        st.write(st.session_state.income_statement["insights"]["debt_management"])
                        interest_expense_chart = create_bar_chart(st.session_state.income_statement["chart_data"], 
                                                                        "interest_expense", 
                                                                        "Debt Service Obligation")
                        st.write(interest_expense_chart)
                except:
                    st.error("This insight has not been generated")

                try:
                    if profit_retention:
                        st.write("### Profit Retention")
                        st.write(st.session_state.income_statement["insights"]["profit_retention"])
                        net_income_chart = create_bar_chart(st.session_state.income_statement["chart_data"], 
                                                                "net_income",
                                                                "Profitability Trend")
                        st.write(net_income_chart)
                except:
                    st.error("This insight has not been generated")


        if st.session_state.balance_sheet:
            with tab3:
                
                st.write("# Balance Sheet")
                st.write("## Metrics")

                with st.container():

                    col1, col2, col3 = st.columns(3)

                    col1.metric("Current Ratio", round_numeric(st.session_state.balance_sheet['metrics']['current_ratio'], 2))
                    col2.metric("Debt to Equity Ratio", round_numeric(st.session_state.balance_sheet['metrics']['debt_to_equity_ratio'], 2))
                    col3.metric("Quick Ratio", round_numeric(st.session_state.balance_sheet['metrics']['quick_ratio'], 2))
                    col1.metric("Asset Turnover", round_numeric(st.session_state.balance_sheet['metrics']['asset_turnover'], 2))
                    col2.metric("Equity Multiplier", round_numeric(st.session_state.balance_sheet['metrics']['equity_multiplier'], 2))



                st.write("## Insights")

                try:
                    if liquidity_position:
                        st.write("### Liquidity Position")
                        st.write(st.session_state.balance_sheet['insights'].liquidity_position)
                        asset_comp_chart = create_donut_chart(st.session_state.balance_sheet["chart_data"],"asset_composition")
                        st.write(asset_comp_chart)
                except:
                    st.error("This insight has not been generated")     

                try:
                    if operational_efficiency2:
                        st.write("### Operational Efficiency")
                        st.write(st.session_state.balance_sheet['insights'].operational_efficiency)
                except:
                    st.error("This insight has not been generated")

                try:
                    if capital_structure:
                        st.write("### Capital Structure")
                        st.write(st.session_state.balance_sheet['insights'].capital_structure)
                        liabilities_comp_chart = create_donut_chart(st.session_state.balance_sheet["chart_data"],"liabilities_composition")
                        st.write(liabilities_comp_chart)
                except:
                    st.error("This insight has not been generated")

                try:
                    if inventory_management:
                        st.write("### Inventory Management")
                        st.write(st.session_state.balance_sheet['insights'].inventory_management)
                except:
                    st.error("This insight has not been generated")

                try:
                    if overall_solvency:
                        st.write("### Overall Solvency")
                        st.write(st.session_state.balance_sheet['insights'].overall_solvency)
                        liabilities_comp_chart = create_donut_chart(st.session_state.balance_sheet["chart_data"],"debt_structure")
                        st.write(liabilities_comp_chart)
                except:
                    st.error("This insight has not been generated")

        if st.session_state.cash_flow:
            with tab4:
                    
                st.write("# Cash Flow")
                st.write("## Metrics")

                with st.container():

                    col1, col2, col3 = st.columns(3)

                    col1.metric("Operating Cash Flow Margin", round_numeric(st.session_state.cash_flow['metrics']['operating_cash_flow_margin'], 2))
                    col2.metric("Capital Expenditure Coverage Ratio", round_numeric(st.session_state.cash_flow['metrics']['capital_expenditure_coverage_ratio'], 2))
                    col3.metric("Dividend Coverage Ratio", round_numeric(st.session_state.cash_flow['metrics']['dividend_coverage_ratio'], 2))
                    col1.metric("Cash Flow to Debt Ratio", round_numeric(st.session_state.cash_flow['metrics']['cash_flow_to_debt_ratio'], 2))
                    
                    col2.metric("Free Cash Flow", format_currency(st.session_state.cash_flow['metrics']['free_cash_flow']))
                    
                try:
                    if operational_cash_efficiency:
                        st.write("## Insights")
                        st.write("### Operational Cash Efficiency")
                        st.write(st.session_state.cash_flow['insights'].operational_cash_efficiency)
                        operating_cash_flow_chart = create_bar_chart(st.session_state.cash_flow["chart_data"], 
                                                                            "operating_cash_flow", 
                                                                            "Operating Cash Flow Trend")
                        st.write(operating_cash_flow_chart)
                except:
                    st.error("This insight has not been generated")

                try:
                    if investment_capability  :      
                        st.write("### Investment Capability")
                        st.write(st.session_state.cash_flow['insights'].investment_capability)
                        cash_flow_from_investment_chart = create_bar_chart(st.session_state.cash_flow["chart_data"], 
                                                                                "cash_flow_from_investment", 
                                                                                "Investment Capability Trend")
                        st.write(cash_flow_from_investment_chart)
                except:
                    st.error("This insight has not been generated")

                try:
                    if financial_flexibility:
                        st.write("### Financial Flexibility")
                        st.write(st.session_state.cash_flow['insights'].financial_flexibility)
                        cash_flow_from_financing_chart = create_bar_chart(st.session_state.cash_flow["chart_data"], 
                                                                                "cash_flow_from_financing", 
                                                                                "Financial Flexibility Trend")
                        st.write(cash_flow_from_financing_chart)
                except:
                    st.error("This insight has not been generated")

                try:
                    if dividend_sustainability:
                        st.write("### Dividend Sustainability")
                        st.write(st.session_state.cash_flow['insights'].dividend_sustainability)
                except:
                    st.error("This insight has not been generated")

                try: 
                    if debt_service_capability:
                        st.write("### Debt Service Capability")
                        st.write(st.session_state.cash_flow['insights'].debt_service_capability)
                except:
                    st.error("This insight has not been generated")


        if st.session_state.news:
            
            with tab5:
                st.markdown("## Top News")
                column_config = {
                        "title": st.column_config.Column(
                            "Title",
                            width="large",
                        ),
                        "url": st.column_config.LinkColumn(
                            "Link",
                            width="medium",
                        ),
                        "authors": st.column_config.ListColumn(
                            "Authors",
                            width = "medium"
                        ),
                        "topics": st.column_config.ListColumn(
                            "Topics",
                            width="large"
                        ),
                        "sentiment_score" : st.column_config.ProgressColumn(
                            "Sentiment Score",
                            min_value=-0.5,
                            max_value=0.5
                        ),
                        "sentiment_label": st.column_config.Column(
                        "Sentiment Label" 
                        )

                    }

                st.metric("Mean Sentiment Score", 
                        value=round_numeric(st.session_state.news["mean_sentiment_score"]), 
                        delta=st.session_state.news["mean_sentiment_class"])
                
                st.dataframe(st.session_state.news["news"], column_config=column_config)

