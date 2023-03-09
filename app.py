# BCD Library Contents Pages Search for BCD Members site

import pandas as pd
import streamlit as st

# Sets page title and favicon for browser tab

st.set_page_config(page_title="Article contents",page_icon="bcdlogo.png")

import streamlit.components.v1 as components
import numpy as np
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, JsCode

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
	st.subheader("Article Contents")
	
# Defines data for searching, imported from Excel sheet	
	
excel_file = 'article_contents_sheet.xlsx'
sheet_name = 'Sheet1'

# Defines caching time for page, to keep results live for long enough
# Reads in the Excel sheet using columns A to E

@st.cache(ttl=24*3600)
def read_sheet():
      return pd.read_excel(excel_file,
				   sheet_name=sheet_name,
				   usecols='A:E',
				   header=0)

df = read_sheet()

# Sets up the content of the help box, using ** Markdown code for bold text

url = "https://github.com/dajavous/bcdpublic/edit/main/app.py"

with st.expander("**Help on using the BCD Magazines - Article Contents Search**", expanded=True):
       st.write("""
	- Using the column headings, you can sort by clicking on a heading, rearrange columns and
	  change column widths by clicking and dragging, and remove columns by dragging off the page.
	- Hover over a column heading and click on the three-bar menu that appears in the column 
	  heading (or just long press on the heading with a tablet) to open the column search box.
	- Press the shift key and click headings to combine sorting and searching on multiple columns.
	- Tap on the table rows anywhere (other than links!) to hide the column search boxes.
	- Refresh the browser window to clear the search boxes.
	- Note that page numbers are those printed on the page, not those in the pdf viewer.
	- Logged in BCD Members can click on the Issue number to open the Magazine in another tab.
	- Click on "Help on using the Index" above to open or close this help box.
	- [Source Code at GitHub] % url
     """)

# Defines the options and data labels for the AgGrid table display

gb = GridOptionsBuilder.from_dataframe(df)

gb.configure_default_column(wrapText=True, autoHeight=True, cellStyle={'word-break': 'break-word'})

# Changes the Issue number column to a hyperlink to the magazine - for BCD Members only, who are logged in and validated

gb.configure_column("ISSUE",
                            headerName="ISSUE", 
                            cellRenderer=JsCode('''function(params) {return '<a href="https://thebcd.co.uk/bcd_members_only/issue-' + params.value + '" target="_blank">'+ params.value+'</a>'}'''),
                            width=200)
gb.configure_column("PAGE",
                            headerName="PAGE",
                            width=200)
gb.configure_column("KEYWORDS",
                            headerName="KEYWORDS",
                            width=400)

gb.configure_column("ARTICLE",
                            headerName="ARTICLE",
                            width=500)
gb.configure_column("AUTHOR",
                            headerName="AUTHOR",
                            width=300)

gridOptions = gb.build()

app_update_mode = GridUpdateMode.FILTERING_CHANGED|GridUpdateMode.SORTING_CHANGED|GridUpdateMode.MODEL_CHANGED

# Displays the AgGrid datatable of the imported Excel sheet, and the theme etc. for the display

grid_response = AgGrid(
    df,
    gridOptions=gridOptions,
    key=None,
    allow_unsafe_jscode=True,
    data_return_mode=DataReturnMode.FILTERED_AND_SORTED, 
    update_mode=app_update_mode,
    fit_columns_on_grid_load=True,
    theme="streamlit", #Add theme color to the table
    enable_enterprise_modules=False,
    height=2000, 
    reload_data=False
)

