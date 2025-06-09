from flask import Flask, request, jsonify, send_file, send_from_directory
import pandas as pd
from vnstock import Vnstock
import os
from datetime import datetime, timedelta

app = Flask(__name__)

DATA_OUTPUT_DIR = 'Data'
if not os.path.exists(DATA_OUTPUT_DIR):
    os.makedirs(DATA_OUTPUT_DIR)

SUPPORTED_INTERVALS_CONFIG = {
    '1h': {'days_back': 7, 'time_format': 'unix_timestamp'}, 
    '1D': {'start_date_fixed': '2016-01-01', 'time_format': 'YYYY-MM-DD'},
    '1W': {'start_date_fixed': '2016-01-01', 'time_format': 'YYYY-MM-DD'},
    '1M': {'start_date_fixed': '2016-01-01', 'time_format': 'YYYY-MM-DD'},
}
DEFAULT_INTERVAL = '1D'

def get_stock_data_and_save(symbol, interval=DEFAULT_INTERVAL):
    print(f"app.py: Đang tiến hành lấy dữ liệu cho mã: {symbol}, interval: {interval}")

    if interval not in SUPPORTED_INTERVALS_CONFIG:
        print(f"app.py: Interval '{interval}' không được hỗ trợ.")
        return None

    config = SUPPORTED_INTERVALS_CONFIG[interval]
    current_date = datetime.now()
    end_date_str = current_date.strftime('%Y-%m-%d')

    if 'start_date_fixed' in config:
        start_date_str = config['start_date_fixed']
    elif 'days_back' in config:
        start_date_obj = current_date - timedelta(days=config['days_back'])
        start_date_str = start_date_obj.strftime('%Y-%m-%d')
    else:
        start_date_str = (current_date - timedelta(days=365)).strftime('%Y-%m-%d') 
    
    print(f"app.py: Khoảng thời gian lấy dữ liệu: từ {start_date_str} đến {end_date_str} cho interval {interval}")

    try:
        stock_loader = Vnstock().stock(symbol=symbol, source='VCI') 
        
        company_overview_df = stock_loader.company.overview()
        if company_overview_df is not None and not company_overview_df.empty:
            filename = os.path.join(DATA_OUTPUT_DIR, f'{symbol}_info.csv')
            company_overview_df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"app.py: Đã lưu thông tin tổng quan của {symbol} vào file: {filename}")

        shareholders_df = stock_loader.company.shareholders()
        if shareholders_df is not None and not shareholders_df.empty:
            filename = os.path.join(DATA_OUTPUT_DIR, f'{symbol}_shareholders.csv')
            shareholders_df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"app.py: Đã lưu thông tin cổ đông của {symbol} vào file: {filename}")

        officers_df = stock_loader.company.officers(filter_by='working')
        if officers_df is not None and not officers_df.empty:
            filename = os.path.join(DATA_OUTPUT_DIR, f'{symbol}_BLD.csv')
            officers_df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"app.py: Đã lưu thông tin ban lãnh đạo của {symbol} vào file: {filename}")

        subsidiaries_df = stock_loader.company.subsidiaries()
        if subsidiaries_df is not None and not subsidiaries_df.empty:
            filename = os.path.join(DATA_OUTPUT_DIR, f'{symbol}_con.csv')
            subsidiaries_df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"app.py: Đã lưu thông tin công ty con của {symbol} vào file: {filename}")

        news_df = stock_loader.company.news().head(10)
        if news_df is not None and not news_df.empty:
            filename = os.path.join(DATA_OUTPUT_DIR, f'{symbol}_news10.csv')
            news_df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"app.py: Đã lưu 10 tin tức mới nhất của {symbol} vào file: {filename}")
        
        income_statement_year_df = stock_loader.finance.income_statement(period='year', lang='vi')
        if income_statement_year_df is not None and not income_statement_year_df.empty:
            filename = os.path.join(DATA_OUTPUT_DIR, f'{symbol}_kqkd_year.csv')
            income_statement_year_df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"app.py: Đã lưu báo cáo KQKD (năm) của {symbol} vào file: {filename}")

        income_statement_quarter_df = stock_loader.finance.income_statement(period='quarter', lang='vi')
        if income_statement_quarter_df is not None and not income_statement_quarter_df.empty:
            filename = os.path.join(DATA_OUTPUT_DIR, f'{symbol}_kqkd_quarter.csv')
            income_statement_quarter_df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"app.py: Đã lưu báo cáo KQKD (quý) của {symbol} vào file: {filename}")
        
        financial_ratios_year_df = stock_loader.finance.ratio(period='year', lang='vi')
        if financial_ratios_year_df is not None and not financial_ratios_year_df.empty:
            filename = os.path.join(DATA_OUTPUT_DIR, f'{symbol}_cstc_year.csv')
            financial_ratios_year_df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"app.py: Đã lưu chỉ số tài chính (năm) của {symbol} vào file: {filename}")

        financial_ratios_quarter_df = stock_loader.finance.ratio(period='quarter', lang='vi')
        if financial_ratios_quarter_df is not None and not financial_ratios_quarter_df.empty:
            filename = os.path.join(DATA_OUTPUT_DIR, f'{symbol}_cstc_quarter.csv')
            financial_ratios_quarter_df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"app.py: Đã lưu chỉ số tài chính (quý) của {symbol} vào file: {filename}")

        cash_flow_year_df = stock_loader.finance.cash_flow(period='year', lang='vi')
        if cash_flow_year_df is not None and not cash_flow_year_df.empty:
            filename = os.path.join(DATA_OUTPUT_DIR, f'{symbol}_lctt_year.csv')
            cash_flow_year_df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"app.py: Đã lưu lưu chuyển tiền tệ (năm) của {symbol} vào file: {filename}")
        
        cash_flow_quarter_df = stock_loader.finance.cash_flow(period='quarter', lang='vi')
        if cash_flow_quarter_df is not None and not cash_flow_quarter_df.empty:
            filename = os.path.join(DATA_OUTPUT_DIR, f'{symbol}_lctt_quarter.csv')
            cash_flow_quarter_df.to_csv(filename, index=False, encoding='utf-8-sig')
            print(f"app.py: Đã lưu lưu chuyển tiền tệ (quý) của {symbol} vào file: {filename}")
            
        df_history = stock_loader.quote.history(
            symbol=symbol, 
            start=start_date_str, 
            end=end_date_str,
            interval=interval
        )

        if df_history is not None and not df_history.empty:
            time_col_name = 'time'
            if 'TradingDate' in df_history.columns and 'time' not in df_history.columns:
                df_history.rename(columns={'TradingDate': 'time'}, inplace=True)
            
            df_history.rename(columns={'Open': 'open', 'High': 'high', 'Low': 'low', 'Close': 'close', 'Volume': 'volume'}, inplace=True)
            
            if time_col_name not in df_history.columns:
                print(f"app.py: Cột '{time_col_name}' không tìm thấy trong dữ liệu trả về.")
                return None

            df_history[time_col_name] = pd.to_datetime(df_history[time_col_name])

            if config['time_format'] == 'YYYY-MM-DD':
                df_history[time_col_name] = df_history[time_col_name].dt.strftime('%Y-%m-%d')
            elif config['time_format'] == 'unix_timestamp':
                df_history[time_col_name] = (df_history[time_col_name].astype(int) // 10**9)
            
            output_filename = os.path.join(DATA_OUTPUT_DIR, f'{symbol}_{interval}.csv')
            df_history.to_csv(output_filename, index=False)
            print(f"app.py: Đã lưu dữ liệu của {symbol} (interval {interval}) vào file: {output_filename}")
            return output_filename
        else:
            print(f"app.py: Không tìm thấy dữ liệu lịch sử cho mã: {symbol} với interval {interval}")
            return None
    except Exception as e:
        print(f"app.py: Đã xảy ra lỗi khi xử lý mã {symbol} với interval {interval}: {e}")
        return None

@app.route('/')
def index():
    return send_from_directory('.', 'chart2.0.html')

@app.route('/api/get_stock_csv', methods=['GET'])
def api_get_stock_csv():
    stock_code = request.args.get('symbol', '').upper()
    interval_req = request.args.get('interval', DEFAULT_INTERVAL)

    if not stock_code:
        return jsonify({"error": "Mã chứng khoán không được cung cấp"}), 400
    
    if interval_req not in SUPPORTED_INTERVALS_CONFIG:
        valid_intervals_str = ", ".join(SUPPORTED_INTERVALS_CONFIG.keys())
        return jsonify({"error": f"Interval '{interval_req}' không được hỗ trợ. Các interval hợp lệ: {valid_intervals_str}"}), 400

    csv_filepath = get_stock_data_and_save(stock_code, interval_req)

    if csv_filepath and os.path.exists(csv_filepath):
        try:
            return send_file(csv_filepath, mimetype='text/csv', as_attachment=False, download_name=f'{stock_code}_{interval_req}.csv')
        except Exception as e:
            return jsonify({"error": f"Lỗi khi gửi file: {str(e)}"}), 500
    else:
        return jsonify({"error": f"Không thể lấy hoặc tạo file dữ liệu cho {stock_code} với interval {interval_req}"}), 404

@app.route('/Data/<path:filename>')
def serve_data_file(filename):
    return send_from_directory('Data', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)