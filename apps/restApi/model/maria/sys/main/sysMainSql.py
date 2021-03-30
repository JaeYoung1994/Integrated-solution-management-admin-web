from common.db.mariaDB import MariaDB

class SysMainSql():
    _mariaDB = None;
    _dbConn = None;
    def __init__(self):
        self._mariaDB = MariaDB()
        self._dbConn = self._mariaDB.connect()
    '''
        SQL: 메인 메뉴 정보
        SQL: Main Menu Information
        author: 이재영 (Jae Young Lee)
    '''
    def getMainMenuList(self):
        rv = { 'result':False }
        try:
            curs = self._dbConn.cursor()
            sql = '''
                SELECT `id`, `name`, `url`, `depth`, `pid`, `order` FROM sys_menu
                ORDER BY `depth`, `pid`, `order`
                '''
            curs.execute(sql)
            print(sql)
            rv['result'] = True
            rv['data'] = curs.fetchall()
        except Exception as ex:
            rv['msg'] = ex
        finally:
            if curs:
                curs.close()
            return rv