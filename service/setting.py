'''
配置可確保應用程式在不同的環境（如開發、測試和生產環境）中正常工作。 為了避免在項目原始程式碼中暴露位址和訪問憑據等敏感資訊，建議通過環境變數定義配置。
儘管有此建議，但通常使用名為 .env 的檔來存儲開發和測試環境的本地環境配置。 此檔避免了在每個終端、IDE中或重新啟動計算機後手動重置環境變數的需要。 有一些庫可以自動識別 .env 檔，並在專案執行開始時載入其中定義的環境變數。 但是，重要的是要配置版本控制，以便不跟蹤 .env 檔。

'''

import uuid

from starlette.config import Config

# 載入.env文件
config = Config("data/.env")


class Settings:
    # 項目版本
    VERSION: str = config("VERSION", default="1.6")
    # 是否開啟Debug模式
    DEBUG = config('DEBUG', cast=bool, default=True)
    # Port number
    PORT = config('PORT', cast=int, default=5000)
    # DB文件
    DATABASE_FILE = config('DATABASE_FILE', cast=str, default='data/database.db')
    # DB URL
    DATABASE_URL = config('DATABASE_URL', cast=str, default=f"sqlite+aiosqlite:///{DATABASE_FILE}")
    # Data文件夾
    DATA_ROOT = './data/' + config('DATA_ROOT', cast=str, default=f"static")
    # 靜態文件夾
    STATIC_URL = config('STATIC_URL', cast=str, default="/static")
    # 是否允許上傳
    ENABLE_UPLOAD = config('ENABLE_UPLOAD', cast=bool, default=True)
    # 最長保存天數
    MAX_DAYS = config('MAX_DAYS', cast=int, default=7)
    # 錯誤次數
    ERROR_COUNT = config('ERROR_COUNT', cast=int, default=5)
    # 錯誤間隔（分鐘）
    ERROR_MINUTE = config('ERROR_MINUTE', cast=int, default=10)
    # 上傳次數
    UPLOAD_COUNT = config('UPLOAD_COUNT', cast=int, default=60)
    # 是否允許永久保存
    ENABLE_PERMANENT = config('ENABLE_PERMANENT', cast=bool, default=True)
    # 上傳限制時間（分鐘）
    UPLOAD_MINUTE = config('UPLOAD_MINUTE', cast=int, default=1)
    # 刪除過期文件間隔（分鐘）
    DELETE_EXPIRE_FILES_INTERVAL = config('DELETE_EXPIRE_FILES_INTERVAL', cast=int, default=10)
    # 管理地址
    ADMIN_ADDRESS = config('ADMIN_ADDRESS', cast=str, default=uuid.uuid4().hex)
    # 管理密碼
    ADMIN_PASSWORD = config('ADMIN_PASSWORD', cast=str, default=uuid.uuid4().hex)
    # 文件大小限制（MB）
    FILE_SIZE_LIMIT = config('FILE_SIZE_LIMIT', cast=int, default=10) * 1024 * 1024
    # 網站標題
    TITLE = config('TITLE', cast=str, default="TextCodeBox")
    # 網站描述
    DESCRIPTION = config('DESCRIPTION', cast=str, default="匿名口令分享文本，文件")
    # 網站關鍵字
    KEYWORDS = config('KEYWORDS', cast=str, default="匿名,分享,文本,文件")
    # 儲存系統：['aliyunsystem','filesystem']
    STORAGE_ENGINE = config('STORAGE_ENGINE', cast=str, default="filesystem")
    # 儲存系統配置
    STORAGE_CONFIG = {}
    # Banners
    BANNERS = [{
        'text': 'FileCodeBox',
        'url': 'https://github.com/vastsa/FileCodeBox',
        'src': '/static/banners/img_1.png'
    }, {
        'text': 'LanBlog',
        'url': 'https://www.lanol.cn',
        'src': '/static/banners/img_2.png'
    }]
    int_dict = {'PORT', 'MAX_DAYS', 'ERROR_COUNT', 'ERROR_MINUTE', 'UPLOAD_COUNT', 'UPLOAD_MINUTE',
                'DELETE_EXPIRE_FILES_INTERVAL', 'FILE_SIZE_LIMIT'}
    bool_dict = {'DEBUG', 'ENABLE_UPLOAD'}

    async def update(self, key, value) -> None:
        if hasattr(self, key):
            if key in self.int_dict:
                value = int(value)
            elif key in self.bool_dict:
                value = bool(value)
            setattr(self, key, value)

    async def updates(self, options) -> None:
        with open('data/.env', 'w', encoding='utf-8') as f:
            for i, key, value in options:
                # 更新env文件
                f.write(f"{key}={value}\n")
                # 更新配置
                await self.update(key, value)
            f.flush()


settings = Settings()