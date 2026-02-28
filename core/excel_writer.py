import pandas as pd
import io

def dataframe_to_xlsx_bytes(df: pd.DataFrame) -> bytes:
    """
    Converte DataFrame para bytes de um arquivo Excel (.xlsx).
    Aplica formatação:
    - Aba: "Lançamentos"
    - Datas: dd/mm/yyyy
    - Moeda: R$ #,##0.00
    """
    output = io.BytesIO()
    
    # Usar XlsxWriter como engine para formatação rica
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Lançamentos')
        
        workbook = writer.book
        worksheet = writer.sheets['Lançamentos']
        
        # Formatos
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#FF6B00',
            'font_color': 'white',
            'border': 1
        })
        
        money_format = workbook.add_format({'num_format': 'R$ #,##0.00', 'border': 1})
        date_format = workbook.add_format({'num_format': 'dd/mm/yyyy', 'align': 'center', 'border': 1})
        text_format = workbook.add_format({'border': 1})
        
        # Aplicar formatos às colunas
        # Colunas: 0:Data, 1:Histórico, 2:Valor, 3:Tipo, 4:Saldo
        
        # Cabeçalhos
        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
            
        # Largura das colunas e formatos
        worksheet.set_column(0, 0, 12, date_format)   # Data
        worksheet.set_column(1, 1, 50, text_format)   # Histórico
        worksheet.set_column(2, 2, 15, money_format)  # Valor
        worksheet.set_column(3, 3, 10, text_format)   # Tipo
        worksheet.set_column(4, 4, 15, money_format)  # Saldo
        
    return output.getvalue()
