import pandas as pd
import magic


class FileReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_type = magic.from_file(file_path, mime=True)
        self.pd_dataframe = None
        self.pd_columns = None
      
    # supported file formats: csv, txt, xlsx, xls
    # file should contain first row with column names
    def read_file(self) -> None:
        if self.file_type == 'text/csv':
            self.pd_dataframe = self.read_csv()
        elif self.file_type == 'text/plain':
            self.pd_dataframe = self.read_txt()
        elif self.file_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':  # noqa: E501
            self.pd_dataframe = self.read_xlsx()
        elif self.file_type == 'application/vnd.ms-excel':
            self.pd_dataframe = self.read_xls()

    def read_csv(self) -> pd.DataFrame:
        return pd.read_csv(self.file_path)

    def read_txt(self) -> pd.DataFrame:
        return pd.read_csv(self.file_path, sep='\t')

    def read_xlsx(self) -> pd.DataFrame:
        return pd.read_excel(self.file_path)

    def read_xls(self) -> pd.DataFrame:
        return pd.read_excel(self.file_path)

    def read_columns(self) -> None:
        if self.pd_dataframe is not None:
            self.pd_columns = list(self.pd_dataframe.columns)
        else:
            return None

    def get_columns(self) -> list:
        return self.pd_columns

    def df_to_list(self, column: str) -> list:
        if self.pd_dataframe is not None:
            return self.pd_dataframe[column].values.tolist()
        else:
            return None
