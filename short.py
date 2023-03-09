# BCD Library Full Text Index Search for BCD Members site

import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode

# Sets page title and favicon for browser tab

st.set_page_config(page_title="Full text index",page_icon="bcdlogo.png", layout="centered", initial_sidebar_state="auto", menu_items=None)

# Changes colour and increases font size of help box label / link consistent with BCD Members site

def init_style():
    return st.markdown(
        """
    <style>
    .streamlit-expanderHeader {
        color:#0FBE7C;
    }
    .css-184tjsw p {
        font-size: 20px;
    }
    
    </style>
""",
        unsafe_allow_html=True,
    )

init_style()

# Splits heading into two columns for BCD logo and page headings

col1, col2 = st.columns([1,1])
with col1:
	st.image('BCD-transparent-background-75.png')
	
with col2:
	st.subheader("BCD Magazines")
	st.subheader("Full Text Index")
	
# Defines data for searching, imported from Excel csv file	

excel_file = 'full_index2.csv'
sheet_name = 'sheet1'

# Defines caching time for page, to keep results live for long enough
# Reads in the Excel csv file

@st.cache(ttl=24*3600)
def read_sheet():
     return pd.read_csv(excel_file)

df = read_sheet()

# Sets up the content of the help box, using ** Markdown code for bold text

with st.expander("**Help on using the BCD Magazines - Full Text Index Search**", expanded=True):
       st.write("""
	- Hover over a column heading and click on the three-bar menu that appears in the column 
	  heading (or just long press on the heading with a tablet) to open the column search box.
	- Tap on the table rows anywhere to hide the column search boxes.
	- Refresh the browser window to clear the search boxes.
	- Note that page numbers are those in the pdf viewer, not those printed on the page.
	- Logged in BCD Members can click on the Issue number to open the Magazine in another tab.
	- Click on "Help on using the Index" above to open or close this help box.
     """)

# Defines the options and data labels for the AgGrid table display

gb = GridOptionsBuilder.from_dataframe(df)
  
gb.configure_default_column(wrapText=True, autoHeight=True, cellStyle={'word-break': 'break-word'})

# Changes the Issue number column to a hyperlink to the magazine - for BCD Members only, who are logged in and validated

gb.configure_column("issue",
                            headerName="ISSUE",
                            cellRenderer=JsCode('''function(params) {return "<a href="https://thebcd.co.uk/bcd_members_only/issue-" + params.value + " target="_blank">"+ params.value+ "</a>"}'''),
                            width=100)
gb.configure_column("word",
                            headerName="WORD",
                            width=300)
gb.configure_column("pages",
                            headerName="PAGES",
                            width=400)
           

gridOptions = gb.build()

app_update_mode = GridUpdateMode.FILTERING_CHANGED|GridUpdateMode.SORTING_CHANGED|GridUpdateMode.MODEL_CHANGED

# Displays the AgGrid datatable of the imported Excel csv file, and the theme etc. for the display

grid_response = AgGrid(
    df,
    gridOptions=gridOptions,
    update_mode=app_update_mode,
    allow_unsafe_jscode=True,
    reload_data=False,
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED, 
    fit_columns_on_grid_load=True,
    theme='streamlit', #Add theme color to the table
    enable_enterprise_modules=False,
    height=2000, 
)
