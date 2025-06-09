import pandas as pd
from vnstock import Vnstock
import sys

if len(sys.argv) < 2:
    sys.stderr.write("Lỗi: Vui lòng cung cấp mã chứng khoán làm đối số dòng lệnh.\n")
    sys.stderr.write("Ví dụ: python Data.py FPT\n")
    sys.exit(1)

symbol = sys.argv[1].upper()

print(f"Đang tiến hành lấy dữ liệu cho mã chứng khoán: {symbol}")

try:
    stock_object = Vnstock().stock(symbol=symbol, source='VCI')

    company_overview_df = stock_object.company.overview()
    if company_overview_df is not None and not company_overview_df.empty:
        info_filename = f'{symbol}_info.csv'
        company_overview_df.to_csv(info_filename, index=False, encoding='utf-8-sig')
        print(f"Đã lưu thông tin tổng quan của {symbol} vào file: {info_filename}")
    else:
        sys.stderr.write(f"Không tìm thấy thông tin tổng quan cho mã: {symbol}.\n")

    df_history = stock_object.quote.history(symbol=symbol, start='2016-01-01', end='2025-05-24', interval='1D')

    if df_history is not None and not df_history.empty:
        output_filename = f'{symbol}.csv'
        df_history.to_csv(output_filename, index=False)
        print(f"Đã lưu dữ liệu giá của {symbol} vào file: {output_filename}")
    else:
        sys.stderr.write(f"Không tìm thấy dữ liệu lịch sử cho mã: {symbol} với các tham số đã cho.\n")
        sys.exit(1)

except Exception as e:
    sys.stderr.write(f"Đã xảy ra lỗi trong quá trình xử lý mã {symbol}: {e}\n")
    sys.exit(1)