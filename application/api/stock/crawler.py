import requests
import json
from application.api.stock.StockSchema import StockSchema
from application.api.stock.StockPrice import StockPrice
from application.api.stock.Stock import Stock

####### region Crawler
def get_stock_index(symbol):
    pass
    # url = f'https://svr4.fireant.vn/api/Data/Companies/CompanyInfo?symbol={symbol}'
    # response = requests.get(url=url)
    # if response.ok:
    #     print('ok')
    #     result = json.loads(response.content)
    new_item = {
        'symbol': symbol
        # 'symbol': result.get('Symbol', None),
        # 'company_name': result.get('CompanyName', None)
    }
    Stock.create(**new_item)
    # else:
    #     print('not ok')


def get_all_stock_indices():
    url = 'https://svr4.fireant.vn/api/Data/Finance/AllLastestFinancialInfo'
    response = requests.get(url=url)
    if response.ok:
        print('ok')
        # sql = f"delete from public.stock where 1=1;"
        # Stock.execute(sql)
        data = json.loads(response.content)
        result = []
        for item in data:
            result.append(item['Symbol'])
            # get_stock_index(item['Symbol'])
        return result
    else:
        print('get_all_stock_indices not ok')

def get_crawl_url(stock_index, start_date, end_date):
    return f'https://svr1.fireant.vn/api/Data/Companies/HistoricalQuotes?symbol={stock_index}&startDate={start_date}&endDate={end_date}';

def crawl(stock_index):
    url = get_crawl_url(stock_index=stock_index, start_date='2014-07-10', end_date='2021-1-29')
    response = requests.get(url=url)
    if response.ok:
        print('ok')
        result = json.loads(response.content)
        sql = f"delete from public.stock where symbol = '{stock_index}';"
        StockPrice.execute(sql)
        for item in result:
            new_item = {
                'symbol': item.get('Symbol', None),
                'stock_date': item.get('Date', None),
                'currency_unit': 'VND',
                'open_price': item.get('PriceOpen', None),
                'high_price': item.get('PriceHigh', None),
                'low_price': item.get('PriceLow', None),
                'close_price': item.get('PriceClose', None),
                'volume': item.get('Volume', None),
                'market_cap': item.get('MarketCap', None)
            }
            StockPrice.create(**new_item)
    else:
        print('not ok')

list_done = [
    'HPX','HPW','HPU','HPT','HPS','HPP','HPM','HPI','HPH','HPG','HPD','HPB','HOT',
    'HOM','HNT','HNR','HNP','HNM','HNI','HNG','HNF','HNE','HND','HNB','HNA','HMS',
    'HMH','HMG','HMC','HLY','HLT','HLS','HLR','HLG','HLE','HLD','HLC','HLB','HLA',
    'HKT','HKP','HKC','HKB','HJS','HJC','HIZ','HII','HIG','HID','HHV','HHS','HHR',
    'HHP','HHN','HHG','HHC','HHA','HGW','HGR','HGM','HGC','HGA','HFX','HFT','HFS',
    'HFC','HFB','HEV','HES','HEP','HEM','HEJ','HEC','HDW','HDP','HDO','HDM','HDG',
    'HDC','HDB','HDA','HD8','HD6','HD3','HD2','HCT','HCS','HCM','HCI','HCD','HCC',
    'HCB','HC3','HC1','HBW','HBS','HBI','HBH','HBE','HBD','HBC','HAX','HAW','HAV',
    'HAT','HAS','HAR','HAP','HAN','HAM','HAI','HAH','HAG','HAF','HAD','HAC','HAB',
    'H11','GVT','GVR','GTT','GTS','GTN','GTK','GTH','GTD','GTC','GTA','GSP','GSM',
    'GQN','GND','GMX','GMD','GMC','GLW','GLT','GLC','GKM','GIL','GIC','GHC','GGS',
    'GGG','GEX','GER','GEG','GDW','GDT','GCB','GAS','GAB','G36','G20','FUEVN100',
    'FUEVFVND','FUESSVFL','FUESSV50','FUESSV30','FUEMAV30','FUCVREIT','FUCTVGF2',
    'FUCTVGF1','FTS','FTM','FTI','FT1','FSO','FSC','FRT','FRM','FRC','FPT','FOX',
    'FOC','FMC','FLC','FIT','FIR','FID','FIC','FHS','FHN','FGL','FDT','FDG','FDC',
    'FCS','FCN','FCM','FCC','FBC','FBA','EVS','EVG','EVF','EVE','EPH','EPC','EMS',
    'EMG','EME','EMC','ELC','EIN','EID','EIC','EIB','EFI','ECI','EBS','EBA','EAD',
    'E29','E1VFVN30','E12','DZM','DXV','DXP','DXL','DXG','DXD','DX2','DWS','DVW',
    'DVP','DVN','DVH','DVC','DUS','DTV','DTT','DTP','DTN','DTL','DTK','DTI','DTG',
    'DTD','DTC','DTB','DTA','DT4','DSV','DST','DSS','DSP','DSN','DSG','DSC','DS3',
    'DRL','DRI','DRH','DRG','DRC','DQC','DPS','DPR','DPP','DPM','DPH','DPG','DPC',
    'DP3','DP2','DP1','DOP','DOC','DNY','DNW','DNT','DNS','DNR','DNP','DNN','DNM',
    'DNL','DNH','DNF','DNE','DND','DNC','DNB','DNA','DMC','DM7','DLT','DLR','DLG',
    'DLD','DLC','DL1','DKP','DKH','DKC','DIH','DIG','DID','DIC','DHT','DHP','DHN',
    'DHM','DHG','DHD','DHC','DHB','DHA','DGW','DGT','DGL','DGC','DFS','DFC','DDV',
    'DDN','DDM','DDH','DDG','DCT','DCS','DCR','DCM','DCL','DCI','DCH','DCG','DCF',
    'DCD','DC4','DC2','DC1','DBW','DBT','DBM','DBH','DBF','DBD','DBC','DAT','DAS',
    'DAR','DAP','DAH','DAG','DAE','DAD','DAC','D2D','D26','D11','CZC','CYC','CXH',
    'CX8','CVT','CVN','CVH','CVC','CTX','CTW','CTT','CTS','CTR','CTP','CTN','CTM',
    'CTI','CTG','CTF','CTD','CTC','CTB','CTA','CT6','CT5','CT3','CSV','CSM','CSI',
    'CSC','CRE','CRC','CQT','CQN','CPW','CPI','CPH','CPC','CPA','COM','CNT','CNN',
    'CNH','CNG','CNC','CMX','CMW','CMV','CMT','CMS','CMP','CMN','CMK','CMI','CMG',
    'CMF','CMD','CMC','CLX','CLW','CLM','CLL','CLH','CLG','CLC','CKV','CKH','CKG',
    'CKD','CKA','CJC','CIP','CII','CIG','CID','CIA','CI5','CHS','CHP','CHC','CH5',
    'CGV','CGP','CFV','CFC','CET','CER','CEO','CEN','CEG','CEE','CEC','CE1','CDR',
    'CDP','CDO','CDN','CDH','CDG','CDC','CCV','CCT','CCR','CCP','CCM','CCL','CCI',
    'CCH','CCA','CC4','CC1','CBS','CBI','CBC','CAV','CAT','CAP','CAN','CAM','CAG',
    'CAD','CAB','C92','C71','C69','C4G','C47','C36','C32','C22','C21','C12','BXT',
    'BXH','BWS','BWE','BWA','BVS','BVN','BVH','BVG','BVB','BUD','BTW','BTV','BTU',
    'BTT','BTS','BTR','BTP','BTN','BTH','BTG','BTD','BTC','BTB','BT6','BT1','BST',
    'BSR','BSQ','BSP','BSL','BSI','BSH','BSG','BSD','BSC','BSA','BRS','BRR','BRC',
    'BQB','BPW','BPC','BOT','BNW','BNA','BMV','BMS','BMP','BMN','BMJ','BMI','BMG',
    'BMF','BMD','BMC','BM9','BLW','BLU','BLT','BLN','BLI','BLF','BKH','BKC','BIO',
    'BII','BID','BIC','BHV','BHT','BHS','BHP','BHN','BHK','BHG','BHC','BHA','BGW',
    'BGM','BFC','BEL','BED','BDW','BDT','BDP','BDG','BDF','BDC','BDB','BCP','BCM',
    'BCI','BCG','BCF','BCE','BCC','BCB','BBT','BBS','BBM','BBH','BBC','BAX','BAM',
    'BAL','BAB','B82','AVF','AVC','AUM','ATS','ATG','ATD','ATB','ATA','AST','ASP',
    'ASM','ASIAGF','ASG','ASD','ASA','ART','ARM','AQN','APT','APS','APP','APL','API',
    'APH','APG','APF','APC','ANV','ANT','AMV','AMS','AMP','AME','AMD','AMC','ALV',
    'ALT','ALP','AIC','AGX','AGR','AGP','AGM','AGG','AGF','AG1','AFX','AFC','ADS',
    'ADP','ADG','ADC','ACV','ACS','ACM','ACL','ACE','ACC','ACB','AC4','ABT','ABS',
    'ABR','ABI','ABC','ABB','AAV','AAS','AAM','AAA'
]
def crawl_all_list():
    # list_stock = Stock.get_all()
    list_stock = get_all_stock_indices()
    result = []
    list_stock.sort()
    for item in list_stock:
        if item not in list_done:
            result.append(item)
            crawl(item)
    return result

####### endregion Crawler

####### region insert all to table

####### endregion insert all to table

####### endregion calculate and insert ema200, sma200, ema50, ema20, rsi14, macd to table stock

####### endregion event observer schedualing crawl and insert ema, rsi to table stock

####### endregion backtest: entry when, exit when, stop loss when

####### endregion pip or % calculator
