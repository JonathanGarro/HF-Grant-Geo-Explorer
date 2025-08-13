import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from io import BytesIO

# page config
st.set_page_config(
    page_title="Geographic Grant Distribution",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def get_m49_country_mapping():
    """
    Hardcoded UN M49 geographic classification mapping.
    Previously used a separate file but I switched to this hardcoded mapping to avoid requiring users to upload a file.
    """
    return {
        # africa
        'Algeria': {'region': 'Africa', 'sub_region': 'Northern Africa', 'intermediate_region': None},
        'Angola': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Middle Africa'},
        'Benin': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Western Africa'},
        'Botswana': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Southern Africa'},
        'Burkina Faso': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Western Africa'},
        'Burundi': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Eastern Africa'},
        'Cabo Verde': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Western Africa'},
        'Cameroon': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Middle Africa'},
        'Central African Republic': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Middle Africa'},
        'Chad': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Middle Africa'},
        'Comoros': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Eastern Africa'},
        'Congo': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Middle Africa'},
        "Côte d'Ivoire": {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Western Africa'},
        "Cote d'Ivoire": {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Western Africa'},
        'Democratic Republic of the Congo': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Middle Africa'},
        'Djibouti': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Eastern Africa'},
        'Egypt': {'region': 'Africa', 'sub_region': 'Northern Africa', 'intermediate_region': None},
        'Equatorial Guinea': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Middle Africa'},
        'Eritrea': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Eastern Africa'},
        'Eswatini': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Southern Africa'},
        'Ethiopia': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Eastern Africa'},
        'Gabon': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Middle Africa'},
        'Gambia': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Western Africa'},
        'Ghana': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Western Africa'},
        'Guinea': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Western Africa'},
        'Guinea-Bissau': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Western Africa'},
        'Kenya': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Eastern Africa'},
        'Lesotho': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Southern Africa'},
        'Liberia': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Western Africa'},
        'Libya': {'region': 'Africa', 'sub_region': 'Northern Africa', 'intermediate_region': None},
        'Madagascar': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Eastern Africa'},
        'Malawi': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Eastern Africa'},
        'Mali': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Western Africa'},
        'Mauritania': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Western Africa'},
        'Mauritius': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Eastern Africa'},
        'Morocco': {'region': 'Africa', 'sub_region': 'Northern Africa', 'intermediate_region': None},
        'Mozambique': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Eastern Africa'},
        'Namibia': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Southern Africa'},
        'Niger': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Western Africa'},
        'Nigeria': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Western Africa'},
        'Rwanda': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Eastern Africa'},
        'São Tomé and Príncipe': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Middle Africa'},
        'Senegal': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Western Africa'},
        'Seychelles': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Eastern Africa'},
        'Sierra Leone': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Western Africa'},
        'Somalia': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Eastern Africa'},
        'South Africa': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Southern Africa'},
        'South Sudan': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Eastern Africa'},
        'Sudan': {'region': 'Africa', 'sub_region': 'Northern Africa', 'intermediate_region': None},
        'Tanzania': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Eastern Africa'},
        'Togo': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Western Africa'},
        'Tunisia': {'region': 'Africa', 'sub_region': 'Northern Africa', 'intermediate_region': None},
        'Uganda': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Eastern Africa'},
        'Zambia': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Eastern Africa'},
        'Zimbabwe': {'region': 'Africa', 'sub_region': 'Sub-Saharan Africa', 'intermediate_region': 'Eastern Africa'},

        # americas
        'Antigua and Barbuda': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'Caribbean'},
        'Argentina': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'South America'},
        'Bahamas': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'Caribbean'},
        'Barbados': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'Caribbean'},
        'Belize': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'Central America'},
        'Bolivia': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'South America'},
        'Brazil': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'South America'},
        'Canada': {'region': 'Americas', 'sub_region': 'Northern America', 'intermediate_region': None},
        'Chile': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'South America'},
        'Colombia': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'South America'},
        'Costa Rica': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'Central America'},
        'Cuba': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'Caribbean'},
        'Dominica': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'Caribbean'},
        'Dominican Republic': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'Caribbean'},
        'Ecuador': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'South America'},
        'El Salvador': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'Central America'},
        'Grenada': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'Caribbean'},
        'Guatemala': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'Central America'},
        'Guyana': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'South America'},
        'Haiti': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'Caribbean'},
        'Honduras': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'Central America'},
        'Jamaica': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'Caribbean'},
        'Mexico': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'Central America'},
        'Nicaragua': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'Central America'},
        'Panama': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'Central America'},
        'Paraguay': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'South America'},
        'Peru': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'South America'},
        'Saint Kitts and Nevis': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'Caribbean'},
        'Saint Lucia': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'Caribbean'},
        'Saint Vincent and the Grenadines': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'Caribbean'},
        'Suriname': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'South America'},
        'Trinidad and Tobago': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'Caribbean'},
        'United States': {'region': 'Americas', 'sub_region': 'Northern America', 'intermediate_region': None},
        'Uruguay': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'South America'},
        'Venezuela': {'region': 'Americas', 'sub_region': 'Latin America and the Caribbean', 'intermediate_region': 'South America'},

        # asia
        'Afghanistan': {'region': 'Asia', 'sub_region': 'Southern Asia', 'intermediate_region': None},
        'Armenia': {'region': 'Asia', 'sub_region': 'Western Asia', 'intermediate_region': None},
        'Azerbaijan': {'region': 'Asia', 'sub_region': 'Western Asia', 'intermediate_region': None},
        'Bahrain': {'region': 'Asia', 'sub_region': 'Western Asia', 'intermediate_region': None},
        'Bangladesh': {'region': 'Asia', 'sub_region': 'Southern Asia', 'intermediate_region': None},
        'Bhutan': {'region': 'Asia', 'sub_region': 'Southern Asia', 'intermediate_region': None},
        'Brunei': {'region': 'Asia', 'sub_region': 'South-eastern Asia', 'intermediate_region': None},
        'Cambodia': {'region': 'Asia', 'sub_region': 'South-eastern Asia', 'intermediate_region': None},
        'China': {'region': 'Asia', 'sub_region': 'Eastern Asia', 'intermediate_region': None},
        'Cyprus': {'region': 'Asia', 'sub_region': 'Western Asia', 'intermediate_region': None},
        'Georgia': {'region': 'Asia', 'sub_region': 'Western Asia', 'intermediate_region': None},
        'India': {'region': 'Asia', 'sub_region': 'Southern Asia', 'intermediate_region': None},
        'Indonesia': {'region': 'Asia', 'sub_region': 'South-eastern Asia', 'intermediate_region': None},
        'Iran': {'region': 'Asia', 'sub_region': 'Southern Asia', 'intermediate_region': None},
        'Iraq': {'region': 'Asia', 'sub_region': 'Western Asia', 'intermediate_region': None},
        'Israel': {'region': 'Asia', 'sub_region': 'Western Asia', 'intermediate_region': None},
        'Japan': {'region': 'Asia', 'sub_region': 'Eastern Asia', 'intermediate_region': None},
        'Jordan': {'region': 'Asia', 'sub_region': 'Western Asia', 'intermediate_region': None},
        'Kazakhstan': {'region': 'Asia', 'sub_region': 'Central Asia', 'intermediate_region': None},
        'Kuwait': {'region': 'Asia', 'sub_region': 'Western Asia', 'intermediate_region': None},
        'Kyrgyzstan': {'region': 'Asia', 'sub_region': 'Central Asia', 'intermediate_region': None},
        'Laos': {'region': 'Asia', 'sub_region': 'South-eastern Asia', 'intermediate_region': None},
        'Lebanon': {'region': 'Asia', 'sub_region': 'Western Asia', 'intermediate_region': None},
        'Malaysia': {'region': 'Asia', 'sub_region': 'South-eastern Asia', 'intermediate_region': None},
        'Maldives': {'region': 'Asia', 'sub_region': 'Southern Asia', 'intermediate_region': None},
        'Mongolia': {'region': 'Asia', 'sub_region': 'Eastern Asia', 'intermediate_region': None},
        'Myanmar': {'region': 'Asia', 'sub_region': 'South-eastern Asia', 'intermediate_region': None},
        'Nepal': {'region': 'Asia', 'sub_region': 'Southern Asia', 'intermediate_region': None},
        'North Korea': {'region': 'Asia', 'sub_region': 'Eastern Asia', 'intermediate_region': None},
        'Oman': {'region': 'Asia', 'sub_region': 'Western Asia', 'intermediate_region': None},
        'Pakistan': {'region': 'Asia', 'sub_region': 'Southern Asia', 'intermediate_region': None},
        'Palestine': {'region': 'Asia', 'sub_region': 'Western Asia', 'intermediate_region': None},
        'Philippines': {'region': 'Asia', 'sub_region': 'South-eastern Asia', 'intermediate_region': None},
        'Qatar': {'region': 'Asia', 'sub_region': 'Western Asia', 'intermediate_region': None},
        'Saudi Arabia': {'region': 'Asia', 'sub_region': 'Western Asia', 'intermediate_region': None},
        'Singapore': {'region': 'Asia', 'sub_region': 'South-eastern Asia', 'intermediate_region': None},
        'South Korea': {'region': 'Asia', 'sub_region': 'Eastern Asia', 'intermediate_region': None},
        'Sri Lanka': {'region': 'Asia', 'sub_region': 'Southern Asia', 'intermediate_region': None},
        'Syria': {'region': 'Asia', 'sub_region': 'Western Asia', 'intermediate_region': None},
        'Tajikistan': {'region': 'Asia', 'sub_region': 'Central Asia', 'intermediate_region': None},
        'Thailand': {'region': 'Asia', 'sub_region': 'South-eastern Asia', 'intermediate_region': None},
        'Timor-Leste': {'region': 'Asia', 'sub_region': 'South-eastern Asia', 'intermediate_region': None},
        'Turkey': {'region': 'Asia', 'sub_region': 'Western Asia', 'intermediate_region': None},
        'Turkmenistan': {'region': 'Asia', 'sub_region': 'Central Asia', 'intermediate_region': None},
        'United Arab Emirates': {'region': 'Asia', 'sub_region': 'Western Asia', 'intermediate_region': None},
        'Uzbekistan': {'region': 'Asia', 'sub_region': 'Central Asia', 'intermediate_region': None},
        'Viet Nam': {'region': 'Asia', 'sub_region': 'South-eastern Asia', 'intermediate_region': None},
        'Vietnam': {'region': 'Asia', 'sub_region': 'South-eastern Asia', 'intermediate_region': None},
        'Yemen': {'region': 'Asia', 'sub_region': 'Western Asia', 'intermediate_region': None},

        # europe
        'Albania': {'region': 'Europe', 'sub_region': 'Southern Europe', 'intermediate_region': None},
        'Andorra': {'region': 'Europe', 'sub_region': 'Southern Europe', 'intermediate_region': None},
        'Austria': {'region': 'Europe', 'sub_region': 'Western Europe', 'intermediate_region': None},
        'Belarus': {'region': 'Europe', 'sub_region': 'Eastern Europe', 'intermediate_region': None},
        'Belgium': {'region': 'Europe', 'sub_region': 'Western Europe', 'intermediate_region': None},
        'Bosnia and Herzegovina': {'region': 'Europe', 'sub_region': 'Southern Europe', 'intermediate_region': None},
        'Bulgaria': {'region': 'Europe', 'sub_region': 'Eastern Europe', 'intermediate_region': None},
        'Croatia': {'region': 'Europe', 'sub_region': 'Southern Europe', 'intermediate_region': None},
        'Czech Republic': {'region': 'Europe', 'sub_region': 'Eastern Europe', 'intermediate_region': None},
        'Denmark': {'region': 'Europe', 'sub_region': 'Northern Europe', 'intermediate_region': None},
        'Estonia': {'region': 'Europe', 'sub_region': 'Northern Europe', 'intermediate_region': None},
        'Finland': {'region': 'Europe', 'sub_region': 'Northern Europe', 'intermediate_region': None},
        'France': {'region': 'Europe', 'sub_region': 'Western Europe', 'intermediate_region': None},
        'Germany': {'region': 'Europe', 'sub_region': 'Western Europe', 'intermediate_region': None},
        'Greece': {'region': 'Europe', 'sub_region': 'Southern Europe', 'intermediate_region': None},
        'Hungary': {'region': 'Europe', 'sub_region': 'Eastern Europe', 'intermediate_region': None},
        'Iceland': {'region': 'Europe', 'sub_region': 'Northern Europe', 'intermediate_region': None},
        'Ireland': {'region': 'Europe', 'sub_region': 'Northern Europe', 'intermediate_region': None},
        'Italy': {'region': 'Europe', 'sub_region': 'Southern Europe', 'intermediate_region': None},
        'Latvia': {'region': 'Europe', 'sub_region': 'Northern Europe', 'intermediate_region': None},
        'Liechtenstein': {'region': 'Europe', 'sub_region': 'Western Europe', 'intermediate_region': None},
        'Lithuania': {'region': 'Europe', 'sub_region': 'Northern Europe', 'intermediate_region': None},
        'Luxembourg': {'region': 'Europe', 'sub_region': 'Western Europe', 'intermediate_region': None},
        'Malta': {'region': 'Europe', 'sub_region': 'Southern Europe', 'intermediate_region': None},
        'Moldova': {'region': 'Europe', 'sub_region': 'Eastern Europe', 'intermediate_region': None},
        'Monaco': {'region': 'Europe', 'sub_region': 'Western Europe', 'intermediate_region': None},
        'Montenegro': {'region': 'Europe', 'sub_region': 'Southern Europe', 'intermediate_region': None},
        'Netherlands': {'region': 'Europe', 'sub_region': 'Western Europe', 'intermediate_region': None},
        'North Macedonia': {'region': 'Europe', 'sub_region': 'Southern Europe', 'intermediate_region': None},
        'Norway': {'region': 'Europe', 'sub_region': 'Northern Europe', 'intermediate_region': None},
        'Poland': {'region': 'Europe', 'sub_region': 'Eastern Europe', 'intermediate_region': None},
        'Portugal': {'region': 'Europe', 'sub_region': 'Southern Europe', 'intermediate_region': None},
        'Romania': {'region': 'Europe', 'sub_region': 'Eastern Europe', 'intermediate_region': None},
        'Russia': {'region': 'Europe', 'sub_region': 'Eastern Europe', 'intermediate_region': None},
        'San Marino': {'region': 'Europe', 'sub_region': 'Southern Europe', 'intermediate_region': None},
        'Serbia': {'region': 'Europe', 'sub_region': 'Southern Europe', 'intermediate_region': None},
        'Slovakia': {'region': 'Europe', 'sub_region': 'Eastern Europe', 'intermediate_region': None},
        'Slovenia': {'region': 'Europe', 'sub_region': 'Southern Europe', 'intermediate_region': None},
        'Spain': {'region': 'Europe', 'sub_region': 'Southern Europe', 'intermediate_region': None},
        'Sweden': {'region': 'Europe', 'sub_region': 'Northern Europe', 'intermediate_region': None},
        'Switzerland': {'region': 'Europe', 'sub_region': 'Western Europe', 'intermediate_region': None},
        'Ukraine': {'region': 'Europe', 'sub_region': 'Eastern Europe', 'intermediate_region': None},
        'United Kingdom': {'region': 'Europe', 'sub_region': 'Northern Europe', 'intermediate_region': None},
        'United Kingdom of Great Britain and Northern Ireland': {'region': 'Europe', 'sub_region': 'Northern Europe', 'intermediate_region': None},
        'England': {'region': 'Europe', 'sub_region': 'Northern Europe', 'intermediate_region': None},
        'Vatican City': {'region': 'Europe', 'sub_region': 'Southern Europe', 'intermediate_region': None},

        # oceania
        'Australia': {'region': 'Oceania', 'sub_region': 'Australia and New Zealand', 'intermediate_region': None},
        'Fiji': {'region': 'Oceania', 'sub_region': 'Melanesia', 'intermediate_region': None},
        'Kiribati': {'region': 'Oceania', 'sub_region': 'Micronesia', 'intermediate_region': None},
        'Marshall Islands': {'region': 'Oceania', 'sub_region': 'Micronesia', 'intermediate_region': None},
        'Micronesia': {'region': 'Oceania', 'sub_region': 'Micronesia', 'intermediate_region': None},
        'Nauru': {'region': 'Oceania', 'sub_region': 'Micronesia', 'intermediate_region': None},
        'New Zealand': {'region': 'Oceania', 'sub_region': 'Australia and New Zealand', 'intermediate_region': None},
        'Palau': {'region': 'Oceania', 'sub_region': 'Micronesia', 'intermediate_region': None},
        'Papua New Guinea': {'region': 'Oceania', 'sub_region': 'Melanesia', 'intermediate_region': None},
        'Samoa': {'region': 'Oceania', 'sub_region': 'Polynesia', 'intermediate_region': None},
        'Solomon Islands': {'region': 'Oceania', 'sub_region': 'Melanesia', 'intermediate_region': None},
        'Tonga': {'region': 'Oceania', 'sub_region': 'Polynesia', 'intermediate_region': None},
        'Tuvalu': {'region': 'Oceania', 'sub_region': 'Polynesia', 'intermediate_region': None},
        'Vanuatu': {'region': 'Oceania', 'sub_region': 'Melanesia', 'intermediate_region': None},
    }

@st.cache_data
def load_and_process_data(grants_file):
    """
    Load the grant data and build the hierarchical structure using hardcoded M49 data
    """

    grants_df = pd.read_csv(grants_file)

    # use hardcoded M49 mapping
    country_mapping = get_m49_country_mapping()

    # US states with regional classification
    # this might require some tweaks based on how teams think about regions
    us_regions = {
        'South': [
            'Alabama', 'Arkansas', 'Delaware', 'Florida', 'Georgia', 'Kentucky',
            'Louisiana', 'Maryland', 'Mississippi', 'North Carolina', 'Oklahoma',
            'South Carolina', 'Tennessee', 'Texas', 'Virginia', 'West Virginia',
            'District of Columbia', 'South'
        ],
        'Northeast': [
            'Connecticut', 'Maine', 'Massachusetts', 'New Hampshire', 'New Jersey',
            'New York', 'Pennsylvania', 'Rhode Island', 'Vermont'
        ],
        'West': [
            'Alaska', 'Arizona', 'California', 'Colorado', 'Hawaii', 'Idaho',
            'Montana', 'Nevada', 'New Mexico', 'Oregon', 'Utah', 'Washington', 'Wyoming'
        ],
        'Midwest': [
            'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Michigan', 'Minnesota',
            'Missouri', 'Nebraska', 'North Dakota', 'Ohio', 'South Dakota', 'Wisconsin'
        ],
        'Territories': [
            'Puerto Rico', 'American Samoa', 'Guam', 'Northern Mariana Islands',
            'U.S. Virgin Islands'
        ]
    }

    # create reverse mapping state > region
    state_to_region = {}
    for region, states in us_regions.items():
        for state in states:
            state_to_region[state] = region

    # US states and territories
    all_us_entities = [state for states in us_regions.values() for state in states]

    # process each grant to build hierarchy
    categorized_grants = []

    for _, row in grants_df.iterrows():
        entity = row['Geographic Entity']
        amount = row['Request: Amount'] or 0

        if entity == 'United States' or entity in all_us_entities:
            # US branch
            if entity == 'United States':
                hierarchy = {
                    'level1': 'United States',
                    'level2': 'Federal/National',
                    'level3': 'National Programs',
                    'level4': None
                }
            else:
                us_region = state_to_region.get(entity, 'Other US')
                level4_name = entity if us_region != entity else None

                hierarchy = {
                    'level1': 'United States',
                    'level2': 'Federal/National',
                    'level3': us_region,
                    'level4': level4_name
                }
        else:
            # international branch
            m49_info = country_mapping.get(entity)

            if m49_info and pd.notna(m49_info['region']):
                # recognized country
                hierarchy = {
                    'level1': 'International',
                    'level2': m49_info['region'],
                    'level3': m49_info['intermediate_region'] or m49_info['sub_region'],
                    'level4': entity
                }
            else:
                # regional or special entity
                region = 'Other'
                sub_region = None

                if 'Africa' in entity or entity == 'Africa':
                    region = 'Africa'
                    if entity in ['Eastern Africa', 'Western Africa', 'Southern Africa', 'Northern Africa']:
                        sub_region = entity
                elif 'America' in entity or entity in ['Latin America & Caribbean', 'Northern America']:
                    region = 'Americas'
                    if entity == 'Latin America & Caribbean':
                        sub_region = 'Latin America and the Caribbean'
                    elif entity == 'Northern America':
                        sub_region = 'Northern America'
                elif entity == 'Asia':
                    region = 'Asia'
                elif entity in ['International', 'Developing Countries']:
                    region = 'Global/Special'

                # plotly wants to duplicate hierarchies sometimes, this avoids that
                if sub_region and sub_region == entity:
                    level4_name = None
                elif sub_region:
                    level4_name = entity
                else:
                    level4_name = entity

                hierarchy = {
                    'level1': 'International',
                    'level2': region,
                    'level3': sub_region,
                    'level4': level4_name
                }

        categorized_grants.append({
            **row.to_dict(),
            **hierarchy,
            'amount': amount
        })

    return pd.DataFrame(categorized_grants)

@st.cache_data
def build_plotly_hierarchy(df):
    """
    Convert the hierarchical data to Plotly sunburst format. See API documentation for more details.
    """

    hierarchy_data = []

    # level 1: US vs international
    level1_groups = df.groupby('level1').agg({
        'amount': 'sum',
        'Request: Reference Number': 'count'
    }).reset_index()

    for _, row in level1_groups.iterrows():
        hierarchy_data.append({
            'ids': row['level1'],
            'labels': row['level1'],
            'parents': '',
            'values': row['amount'],
            'grant_count': row['Request: Reference Number']
        })

    # level 2: regions and states
    level2_groups = df.groupby(['level1', 'level2']).agg({
        'amount': 'sum',
        'Request: Reference Number': 'count'
    }).reset_index()

    for _, row in level2_groups.iterrows():
        if pd.notna(row['level2']):
            hierarchy_data.append({
                'ids': f"{row['level1']}/{row['level2']}",
                'labels': row['level2'],
                'parents': row['level1'],
                'values': row['amount'],
                'grant_count': row['Request: Reference Number']
            })

    # level 3: sub-regions
    level3_groups = df.groupby(['level1', 'level2', 'level3']).agg({
        'amount': 'sum',
        'Request: Reference Number': 'count'
    }).reset_index()

    for _, row in level3_groups.iterrows():
        if pd.notna(row['level3']):
            hierarchy_data.append({
                'ids': f"{row['level1']}/{row['level2']}/{row['level3']}",
                'labels': row['level3'],
                'parents': f"{row['level1']}/{row['level2']}",
                'values': row['amount'],
                'grant_count': row['Request: Reference Number']
            })

    # level 4: countries/states
    level4_groups = df.groupby(['level1', 'level2', 'level3', 'level4']).agg({
        'amount': 'sum',
        'Request: Reference Number': 'count'
    }).reset_index()

    for _, row in level4_groups.iterrows():
        if pd.notna(row['level4']) and pd.notna(row['level3']):
            hierarchy_data.append({
                'ids': f"{row['level1']}/{row['level2']}/{row['level3']}/{row['level4']}",
                'labels': row['level4'],
                'parents': f"{row['level1']}/{row['level2']}/{row['level3']}",
                'values': row['amount'],
                'grant_count': row['Request: Reference Number']
            })

    return pd.DataFrame(hierarchy_data)

def create_sunburst_chart(hierarchy_df, grants_df):
    """
    Create the interactive Plotly sunburst chart
    """

    # hover text
    hover_text = []
    for _, row in hierarchy_df.iterrows():
        percentage = (row['values'] / grants_df['amount'].sum()) * 100
        text = f"<b>{row['labels']}</b><br>"
        text += f"Amount: ${row['values']:,.0f}<br>"
        text += f"Grants: {row['grant_count']}<br>"
        text += f"Share: {percentage:.1f}%"
        hover_text.append(text)

    # sunburst chart
    fig = go.Figure(go.Sunburst(
        ids=hierarchy_df['ids'],
        labels=hierarchy_df['labels'],
        parents=hierarchy_df['parents'],
        values=hierarchy_df['values'],
        branchvalues="total",
        hovertemplate='%{hovertext}<extra></extra>',
        hovertext=hover_text,
        maxdepth=4,
        insidetextorientation='radial'
    ))

    # custom chart config to increase size
    fig.update_layout(
        title={
            'text': f'Geographic Grant Distribution<br><span style="font-size: 24px; color: #27ae60;">Total: ${grants_df["amount"].sum():,.0f}</span>',
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 36}
        },
        font_size=16,
        width=1400,
        height=1400,
        margin=dict(t=150, b=80, l=80, r=80)
    )

    return fig

def filter_data_by_selection(df, selected_path):
    """
    Filter the dataframe based on the selected path in the sunburst
    """
    if not selected_path:
        return df

    # parse the selected path
    path_parts = selected_path.split('/')

    # filter conditions
    conditions = pd.Series([True] * len(df))

    if len(path_parts) >= 1 and path_parts[0]:
        conditions &= (df['level1'] == path_parts[0])
    if len(path_parts) >= 2 and path_parts[1]:
        conditions &= (df['level2'] == path_parts[1])
    if len(path_parts) >= 3 and path_parts[2]:
        conditions &= (df['level3'] == path_parts[2])
    if len(path_parts) >= 4 and path_parts[3]:
        conditions &= (df['level4'] == path_parts[3])

    return df[conditions]

def create_summary_stats(df):
    """
    Create summary statistics for the filtered data
    """
    total_amount = df['amount'].sum()
    total_grants = len(df)
    avg_grant = df['amount'].mean()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="Total Amount",
            value=f"${total_amount:,.0f}",
            delta=f"{len(df)} grants"
        )

    with col2:
        st.metric(
            label="Average Grant Size",
            value=f"${avg_grant:,.0f}",
            delta=None
        )

    with col3:
        unique_entities = df['Geographic Entity'].nunique()
        st.metric(
            label="Geographic Entities",
            value=unique_entities,
            delta=None
        )

def to_excel(df):
    """
    Convert dataframe to Excel for download.
    Not sure we need to keep this as user is providing raw data and streamlit isnt transforming anything
    TODO: Decide on excel output
    """
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Filtered_Grants', index=False)
    return output.getvalue()

# streamlit App
def main():
    st.title("Hewlett Geographic Grant Distribution Explorer")
    st.markdown("*Interactive visualization designed to explore the distribution of grants across geographic hierarchies. Code by Hewlett Data Officer [Jonathan Garro](https://github.com/jonathangarro).*")

    # Sidebar for file upload
    st.sidebar.header("📁 Data Upload")

    grants_file = st.sidebar.file_uploader(
        "Upload Grant Data CSV",
        type=['csv'],
        help="Upload your grant portfolio CSV file"
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    **Geographic Classifications**
    
    UN M49 geographic codes are built-in. GMS mostly adheres to this system but some tweaks may be needed. 
    
    Includes all countries and regions for:
    • Africa (all sub-regions)
    • Americas (North/Central/South America + Caribbean)  
    • Asia (all sub-regions)
    • Europe (all sub-regions)
    • Oceania
    """)

    if grants_file is not None:
        try:
            # load and process data
            with st.spinner('Processing data...'):
                processed_df = load_and_process_data(grants_file)
                hierarchy_df = build_plotly_hierarchy(processed_df)

            # initialize session state for selections
            if 'selected_path' not in st.session_state:
                st.session_state.selected_path = None

            # create and display the sunburst chart - full width
            fig = create_sunburst_chart(hierarchy_df, processed_df)

            # display chart with click handling - full container width
            selected_data = st.plotly_chart(
                fig,
                use_container_width=True,
                on_select="rerun",
                selection_mode="points"
            )

            if selected_data and selected_data['selection']['points']:
                # get the selected point
                point = selected_data['selection']['points'][0]
                selected_id = point.get('id', '')
                st.session_state.selected_path = selected_id

                # display selection info as a banner
                st.success(f"**Selected:** {selected_id.split('/')[-1]} | **Path:** {' → '.join(selected_id.split('/'))}")

                # add clear selection button
                if st.button("🔄 Clear Selection", type="secondary"):
                    st.session_state.selected_path = None
                    st.rerun()

            # filter data based on selection
            if st.session_state.selected_path:
                filtered_df = filter_data_by_selection(processed_df, st.session_state.selected_path)
                section_title = f"Grants in: {st.session_state.selected_path.split('/')[-1]}"
            else:
                filtered_df = processed_df
                section_title = "All Grants"

            st.markdown("---")

            # summary stats
            st.subheader(f"Summary Statistics - {section_title}")
            create_summary_stats(filtered_df)

            # filtered data table
            st.subheader(f"Grant Details - {section_title}")

            # prepare display columns
            display_columns = [
                'Geographic Entity', 'Request: Amount', 'Request: PO',
                'Request: Reference Number', 'level1', 'level2', 'level3', 'level4'
            ]

            # rename columns for better display
            display_df = filtered_df[display_columns].copy()
            display_df.columns = [
                'Geographic Entity', 'Amount ($)', 'Program Officer',
                'Reference Number', 'Level 1', 'Level 2', 'Level 3', 'Level 4'
            ]

            # format amount column
            display_df['Amount ($)'] = display_df['Amount ($)'].apply(lambda x: f"${x:,.0f}")

            # display the table
            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True
            )

            # additional insights
            if len(filtered_df) > 0:
                st.subheader("Quick Insights")

                col1, col2 = st.columns(2)

                with col1:
                    # top entities by amount
                    top_entities = filtered_df.groupby('Geographic Entity')['amount'].sum().sort_values(ascending=False).head(5)
                    st.write("**Top 5 Entities by Amount:**")
                    for entity, amount in top_entities.items():
                        st.write(f"• {entity}: ${amount:,.0f}")

                with col2:
                    # PO distribution
                    po_distribution = filtered_df.groupby('Request: PO')['amount'].sum().sort_values(ascending=False).head(5)
                    st.write("**Top 5 Program Officers by Amount:**")
                    for po, amount in po_distribution.items():
                        st.write(f"• {po}: ${amount:,.0f}")

        except Exception as e:
            st.error(f"Error processing data: {str(e)}")
            st.write("Please make sure your files are in the correct format.")

    else:
        # show instructions when no files are uploaded
        st.info("Upload grant data CSV file in the sidebar to begin.")

        st.subheader("📋 Required File")

        st.markdown("""
        **Grant Data CSV:**
        - Create a report in the GMS of type: Geographical Areas Served with Request
            - Report must contain Request: `Reference Number`, `Geographical Area Served: Geographical Area Served Name`, `Geographic Entity`, and `Request: Amount`
            - Export the file as a CSV (not XLSX)
        
        **Geographic Classifications (Built-in):**
        - GMS uses UN M49 codes which I've already included as hardcoded data into this app
        - Supports all countries and regions worldwide based on limited testing
        """)

if __name__ == "__main__":
    try:
        # check if we're running in Streamlit
        import streamlit as st
        main()
    except ImportError:
        print("Streamlit not installed. Install with: pip install streamlit")
    except Exception as e:
        print("This is a Streamlit app. Run with: streamlit run app.py")
        print(f"Error: {e}")