import json

from .gvar import *

config_file_name = 'data/config/config.json'

with open(config_file_name, 'r') as fp:
    config_data = json.load(fp)

template_sufix = ['', '_jp', '_in', '_inb', '_nec', '_jp' , '_ibo', '_jp3', '_jp4', '_sbt', '_sbtl' ]
template_codes = ['', 'JP_', 'IN_', 'INB_', 'NEC_', 'JP2_', 'IBO_', 'JP3_', 'JP4_', 'SBT_', 'SBT_LOWER' ]
template_num = config_data['template_num']

template_num = gvar.get('template_num', template_num)

if template_num == 1:
    from .jp_merc_fin import *

if template_num == 2:
    from .invest_news import *

if template_num == 3:
    from .invest_news_black import *

if template_num == 4:
    from .necton import *

if template_num == 5:
    from .jp_merc_fin_2 import *

if template_num == 6:
    from .jp_ibope import *

if template_num == 7:
    from .jp_merc_fin_3 import *

if template_num == 8:
    from .jp_merc_fin_4 import *

if template_num == 9:
    from .sbt import *

if template_num == 10:
    from .sbt_lower import *