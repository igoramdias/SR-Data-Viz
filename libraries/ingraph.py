import plotly.graph_objects as go
from datetime import datetime
from .assets import *
from .ingpos import *
from .graphics import set_margins
from .graphics import add_image
from datetime import date
import pandas as pd

GS = 1.0
def set_001_GS(gs):
    global GS
    GS = gs

def set_layout(fig):

    # Colocado aqui para poder setar o GS
    logo_pgm_template = dict(
        layout=go.Layout(
            font_family=FONT,
            xaxis=dict(showgrid=False, showline=True, linewidth=1*GS, showspikes=True, spikethickness=3*GS),
            yaxis=dict(showgrid=False),
        )
    )

    pres_template = logo_pgm_template

    if TEMPLATE not in ['SBT', 'SBT_LOWER']:
        fig.update_layout(
            template = pres_template,
            margin=dict(t=MARGINT*GS, b=MARGINB*GS, l=MARGINL*GS,  r=MARGINR*GS, pad=MARGINPAD*GS),
            width=IMAGEW*GS, height=IMAGEH*GS,
            # paper_bgcolor='#EEEEEE',
            xaxis=dict(tickfont = dict(size=size_ticks * GS, color=color_ticks), color=color_ticks, ticks='outside',
                tickwidth=1*GS, ticklen=5*GS),
            yaxis=dict(tickfont = dict(size=size_ticks * GS, color=color_ticks)),
            # yaxis_separatethousands = True,
            yaxis_tickformat = ',.0f',  # 'digits'
            separators=',.',
        )
    else:
        if TEMPLATE == 'SBT':
            fig.update_layout(
                template = pres_template,
                margin=dict(t=MARGINT*GS, b=MARGINB*GS, l=MARGINL*GS,  r=MARGINR*GS, pad=MARGINPAD*GS),
                width=IMAGEW*GS, height=IMAGEH*GS,
                # paper_bgcolor='#EEEEEE',
                xaxis=dict(tickfont = dict(size=size_ticks * GS, color=color_ticks), color=color_ticks, ticks='outside',
                    tickwidth=0*GS, ticklen=5*GS, anchor='free', position=0.15, domain=(0.04, 0.97), linecolor='rgba(0,0,0,0)'),
                yaxis=dict(visible= False, showticklabels= False, anchor='free', domain=(0.15, 1)),
            )
        else:
            fig.update_layout(
                template = pres_template,
                margin=dict(t=MARGINT*GS, b=MARGINB*GS, l=MARGINL*GS,  r=MARGINR*GS, pad=MARGINPAD*GS),
                width=IMAGEW*GS, height=IMAGEH*GS,
                # paper_bgcolor='#EEEEEE',
                xaxis=dict(tickfont = dict(size=size_ticks * GS, color=color_ticks), color=color_ticks, ticks='outside',
                    tickwidth=0*GS, ticklen=5*GS, anchor='free', position=0.3, domain=(0.12, 0.88), linecolor='rgba(0,0,0,0)'),
                yaxis=dict(visible= False, showticklabels= False, anchor='free', domain=(0.15, 1)),
            )

    set_margins(fig, MARGINL, MARGINR, MARGINT, MARGINB, MARGINPAD)


def draw_block_info(fig):

    # Big rectangle
    fig.add_shape(type="rect",
        xref="paper", yref="paper",
        x0=block_info_x0, y0=block_info_y0,
        x1=block_info_x1, y1=block_info_y1,
        line=dict(width=0),
        fillcolor=GT_BLOCK_INFO_COLOR,
    )

    # Lines
    for col in range(2):
        fig.add_shape(type="line",
            xref="paper", yref="paper",
            x0=block_info_line_x[col], y0=(block_info_y0 + 0.1),
            x1=block_info_line_x[col], y1=(block_info_y1 - 0.1),
            line=dict(
                color='#FFFFFF',
                width=1*GS,
            )
)


def label_to_dict(lbl, text, xanchor='left', yref='paper', yanchor='middle'):

    return dict(
        xref="paper", yref=yref,
        x=lbl[LBL_POS_X], y=lbl[LBL_POS_Y],
        text=f'{text}',
        font=dict(color=lbl[LBL_POS_COLOR], size=lbl[LBL_POS_SIZE] * FONT_SIZE_MF * GS),
        xanchor = xanchor, yanchor = yanchor,
        showarrow=False)



# Labels                 x       y        color        size
pres_price_label    = [diff_x, diff_y, GT_PRES_PRICE_FC, 24]
diff_price_label    = [pp_x,   pp_y,   color_diff_pos,   GT_PRES_PRICE_FS]

title_label         = [title_x, title_y, color_text_4,   20]
time_label          = [time_x , time_y,  color_text_4,   GT_TIME_FS]
asset_label         = [asset_x, asset_y, color_text_4,   75]
dfont_label         = [dfont_x, dfont_y, color_text_4,   GT_DFONT_FS]

close_price_label   = [close_x, close_y, color_text_4,   GT_TICKS_FONT_SIZE]

if template_num == 1:
    pres_price_label    = [diff_x, diff_y, GT_PRES_PRICE_FC, 27]  # 30
    asset_label         = [asset_x, asset_y, color_text_4,   34]  # 40

if TEMPLATE == 'SBT':
    pres_dec_price_label    = [diff_x, diff_y, GT_PRES_PRICE_FC, 30]
    pres_price_label    = [diff_x, diff_y, GT_PRES_PRICE_FC, GT_PRES_PRICE_FS]
    diff_price_label    = [pp_x,   pp_y,   color_diff_pos,   GT_PRES_PRICE_FS] 

# Functions to format texts
# def set_price(price):
#     return f'<b>{money_format(price)}</b>'
def set_price(price, diff):
    if TEMPLATE in ["SBT", "SBT_LOWER"]:
        return f'<b>{money_format(diff)}</b>'
    else:
        return f'<b>{money_format(price)} ({money_format(diff)})</b>'

def set_diff(diff, price):
    if diff >= 0:
        pres_price_label[LBL_POS_COLOR] = color_diff_pos
        diff_arrow_chr = u'\u2191'
        diff_price_label[LBL_POS_COLOR] = color_diff_pos
    else:
        pres_price_label[LBL_POS_COLOR] = color_diff_neg
        diff_arrow_chr = u'\u2193'
        diff_price_label[LBL_POS_COLOR] = color_diff_neg

    diff_perc = diff / price * 100

    if TEMPLATE not in ["SBT", "SBT_LOWER"]:
        # return f'<b>{money_format(diff)} ({money_format(diff_perc)}%) {diff_arrow_chr}</b>'
        return f'<b>{money_format(diff_perc)}% {diff_arrow_chr}</b>'
    else:
        return f'<b>{money_format(diff_perc)}</b>'


def block_annotation_labels(annotations, prices, info_prices):
    if GT_INFO_52M:
        block_info_text=['ABERTURA', 'FECH. ANT.', 'ALTA', 'BAIXA', 'ALT 52 SEM', 'BAIX 52 SEM']
    else:
        if TEMPLATE != "SBT":
            block_info_text=['ABERTURA', 'FECH. ANT.', 'ALTA', 'BAIXA']
        else:
            block_info_text=['ABERTURA', 'FECHAMENTO']
    block_info_price=[]

    block_info_price.append(info_prices[1])  # Open
    block_info_price.append(info_prices[0])  # Close last-day
    # block_info_price.append(prices.max())
    # block_info_price.append(prices.min())
    block_info_price.append(info_prices[2])
    block_info_price.append(info_prices[3])
    block_info_price.append(info_prices[4])
    block_info_price.append(info_prices[5])

    decimal = gvar.get('decimal', 2)
    if info_prices[5] >= 1000:
        gvar['decimal'] = 0

    for bi_pos in range(len(block_info_text)):
            lin = bi_pos %  2
            col = bi_pos // 2
            
            if TEMPLATE not in ["SBT", 'SBT_LOWER']:
                text_info_label = [block_info_lbl_x[col] - block_info_lbl_dx[col] - px_rel(GT_BLOCK_DX),
                    block_info_lbl_y[lin], GT_BLOCK_FONT_COLOR, GT_BLOCK_LBL_FS]

                price_info_label = [block_info_lbl_x[col] + px_rel(GT_BLOCK_DX),
                    block_info_lbl_y[lin], GT_BLOCK_FONT_COLOR, GT_BLOCK_NUM_FS]

                annotations.append(label_to_dict(text_info_label,
                    f'<b>{block_info_text[bi_pos]}</b>'))

                annotations.append(label_to_dict(price_info_label,
                    f'{get_value_txt(block_info_price[bi_pos])}'))
                    # f'{get_value_txt(block_info_price[bi_pos], bold=True)}'))
            else:
                if bi_pos < 2:
                    
                    if TEMPLATE == 'SBT': 
                        price_info_label = [block_info_lbl_x[lin],
                            block_info_lbl_y[0] + 0.01, GT_BLOCK_FONT_COLOR, 45]

                        annotations.append(label_to_dict(price_info_label,
                        f'{get_value_txt(block_info_price[bi_pos])}', xanchor='right'))
                    
                        annotations.append(label_to_dict([block_info_lbl_x[lin]+0.01, block_info_lbl_y[lin] + 0.03, GT_BLOCK_FONT_COLOR, 23],
                            f'{get_value_txt(int(block_info_price[bi_pos]*100 % 100))}', xanchor='left'))
                    else:
                        price_info_label = [block_info_lbl_x[lin],
                            block_info_lbl_y[lin], GT_BLOCK_FONT_COLOR, 45]

                        annotations.append(label_to_dict(price_info_label,
                            f'{get_value_txt(block_info_price[bi_pos])}', xanchor='right'))
                        
                        annotations.append(label_to_dict([block_info_lbl_x[lin]+0.01, block_info_lbl_y[lin] + 0.015, GT_BLOCK_FONT_COLOR, 23],
                            f'{get_value_txt(int(block_info_price[bi_pos]*100 % 100))}', xanchor='left'))

    gvar['decimal'] = decimal


def update_labels(fig, period, prices, info_prices, market_time_ts, symbol, currency):

    price = prices.iloc[-1]
    #price = info_prices[0]
    #price_previous_close = info_prices[1]
    price_open = prices.iloc[0]

    #if period == 0:
    #    price_first = price_previous_close
    #else:
    price_first = price_open

    diff  = price - price_first

    price_txt = set_price(price, diff)
    diff_txt  = set_diff(diff, price_first)
    
    annotations = []
    if TEMPLATE == 'SBT':
        if diff > 0:
            add_image(fig, 'images/sbt/bg_001_arrowup.png', 43, 130,
                890, 380, xanchor='left', yanchor='top', layer='below')
            annotations.append(label_to_dict([subdiff_x-0.02+0.002, diff_y+0.013, '#65E0FF', 30], f'<b>,{int(diff*100 % 100)}</b>', xanchor='left'))
            annotations.append(label_to_dict([subdiff_x-0.02, diff_y, '#65E0FF', 60], price_txt, xanchor='right'))
            annotations.append(label_to_dict([pp_x+0.06,   pp_y,   '#65E0FF', 60], diff_txt))
        else:
            add_image(fig, 'images/sbt/bg_001_arrowdown.png', 43, 130,
                890, 380, xanchor='left', yanchor='top', layer='below')
            annotations.append(label_to_dict([subdiff_x+0.001, diff_y+0.013, '#FF657F', 30], f'<b>,{int(diff*100 % 100)}</b>', xanchor='left'))
            annotations.append(label_to_dict([subdiff_x, diff_y, '#FF657F', 60], price_txt, xanchor='right'))
            annotations.append(label_to_dict([pp_x+0.05,   pp_y,   '#FF657F', 60], diff_txt))
    elif TEMPLATE == 'SBT_LOWER':
        if diff > 0:
            add_image(fig, 'images/sbt/bg_lower_001_arrowup.png', 0, 0,
                978, 600, xanchor='left', yanchor='top', layer='below')
            annotations.append(label_to_dict([subdiff_x-0.02+0.001, diff_y+0.013, '#65E0FF', 30], f'<b>,{int(diff*100 % 100)}</b>', xanchor='left'))
            annotations.append(label_to_dict([subdiff_x-0.02, diff_y, '#65E0FF', 60], price_txt, xanchor='right'))
            annotations.append(label_to_dict([pp_x+0.06,   pp_y,   '#65E0FF', 60], diff_txt))
        else:
            add_image(fig, 'images/sbt/bg_lower_001_arrowdown.png', 0, 0,
                600, 1080, xanchor='left', yanchor='top', layer='below')
            annotations.append(label_to_dict([subdiff_x+0.001, diff_y+0.013, '#FF657F', 30], f'<b>,{int(diff*100 % 100)}</b>', xanchor='left'))
            annotations.append(label_to_dict([subdiff_x, diff_y, '#FF657F', 60], price_txt, xanchor='right'))
            annotations.append(label_to_dict([pp_x+0.05,   pp_y,   '#FF657F', 60], diff_txt))
    else:
        annotations.append(label_to_dict(pres_price_label, price_txt))
        annotations.append(label_to_dict(diff_price_label, diff_txt))
    
    #annotations.append(label_to_dict(title_label, 'RESUMO DO MERCADO | <b>Ibovespa</b>'))

    symbol_name = asset_code_to_name(symbol)
    if  symbol_name == symbol:
        symbol_name = ''

    if TEMPLATE not in ['SBT', 'SBT_LOWER']:
        symbol_text = f'{symbol_name}<b> ({symbol})</b>'
    else:
        symbol_text = symbol_name.upper()

    if TEMPLATE in ['SBT', 'SBT_LOWER']:
        txt = f'<span style="fill-opacity: 0; stroke: #50B7F8; stroke-opacity: 1; clip-path: inset(48px 0px 33px 0px)">{symbol_text}</span>'
        if TEMPLATE == 'SBT':
            annotations.append(label_to_dict([0.58, 1.13, '#FF657F', 180], txt, xanchor='right'))
        else:
            annotations.append(label_to_dict([0.02, 0.832, '#FF657F', 180], txt, xanchor='left'))

    annotations.append(label_to_dict(asset_label, symbol_text, xanchor='right'))

    if TEMPLATE not in ['SBT', 'SBT_LOWER']:
        annotations.append(label_to_dict(dfont_label, 'FONTE: YAHOO FINANCE', xanchor='right'))
    else:
        ts = pd.Timestamp(str(date.today())) 
        offset = pd.tseries.offsets.BusinessDay(n=1)
        res = date.today() - offset
        if TEMPLATE == 'SBT':
            annotations.append(label_to_dict([0.95, 1.12, '#0A2038', 50], f'{str(res.day).zfill(2)}|{str(res.month).zfill(2)}|{str(res.year).zfill(2)}', xanchor='right'))
        else:
            annotations.append(label_to_dict([0.05, 0.75, '#fff', 35], f'{str(res.day).zfill(2)}|{str(res.month).zfill(2)}|{str(res.year).zfill(2)}', xanchor='left'))
    
    if market_time_ts == 0:
        market_time = 'Feriado'
    else:
        ts = market_time_ts['time']
        if market_time_ts["timezone"] != 'BRST':
            ts += market_time_ts['gmtoffset'] + 3*3600  # 3h Brasil
        dt_obj = datetime.fromtimestamp(ts)
        market_time = dt_obj.strftime('%d de %b. %H:%M')
        market_time +=  ' ' + market_time_ts["timezone"]
    
    if TEMPLATE not in ['SBT', 'SBT_LOWER']:
        annotations.append(label_to_dict(time_label,
                f'{market_time}'
                f'\xa0\xa0 (Moeda: {currency})'))
    
    # value of last close at line
    if period == 0 and TEMPLATE not in ['SBT', 'SBT_LOWER']:
        close_txt = f'FECHAM.<br>{get_value_txt(info_prices[1])}'
        close_price_label[1] = info_prices[1]
        annotations.append(label_to_dict(close_price_label, close_txt,
        yref='y', xanchor='right'))
    else:
        
        close_price_label = [None, None]
        close_txt = ''
    
    
    block_annotation_labels(annotations, prices, info_prices)
    
    fig.update_layout(
        annotations=annotations
    )

# Por enquanto é o jeito de ligar/desligar uma linha
# sempre na posicao selector = 3
def init_close_line(fig):
    fig.add_shape(type='line',
        xref='paper', yref='paper',
        x0=0, y0=0, x1=0, y1=0,
        line=dict(color=color_text_5, width=0, dash='dot'))

def show_close_line(fig, price_close):
    widh = 3
    if template_num == 1:
        width = 4
    fig.update_shapes(selector=3, yref='y',
        x0=0, y0=price_close, x1=1, y1=price_close,
        line=dict(width=width*GS))

def hide_close_line(fig):
    fig.update_shapes(selector=3, yref='paper',
        x0=0, y0=0, x1=0, y1=0,
        line=dict(width=0))
