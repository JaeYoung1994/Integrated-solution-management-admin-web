from common.db.mariaDB import MariaDB

class UserSql():
    _mariaDB = None;
    _dbConn = None;

    def __init__(self):
        self._mariaDB = MariaDB()
        self._dbConn = self._mariaDB.connect()

    '''
        SQL: 계정 정보
        SQL: Account Information
        author: 이재영 (Jae Young Lee)
    '''
    def getAccountInfo(self, d):
        rv = { 'result':False }
        try:
            curs = self._dbConn.cursor()
            sql = '''
                SELECT u.email, u.nickName, u.password, u.authority, u.group 
                FROM user AS u
                WHERE u.email = "%s"
                ''' % (d["email"])
            curs.execute(sql)
            rv['result'] = True
            rv['data'] = curs.fetchone()
        except Exception as ex:
            rv['msg'] = ex
        finally:
            if curs:
                curs.close()
            return rv
    '''
        SQL: 이메일 존재 유무 확인
        SQL: Check for existence of email
        author: 이재영 (Jae Young Lee)
    '''
    def isEmail(self, d):
        rv = {'result': False, 'msg': 'Email already registered'}
        try:
            curs = self._dbConn.cursor()
            sql = '''
                SELECT u.email 
                FROM user AS u
                WHERE u.email = "%s"
            ''' % (d["email"])
            curs.execute(sql)
            if curs.fetchone() is None:
                rv['result'] = True
        except Exception as ex:
            rv['msg'] = str(ex)
        finally:
            if curs:
                curs.close()
            return rv

    '''
        SQL: 닉네임 존재 유무 확인
        SQL: Check whether a nickname exists
        author: 이재영 (Jae Young Lee)
    '''
    def isNickName(self, d):
        rv = {'result': False, 'msg': None}
        try:
            curs = self._dbConn.cursor()
            sql = '''
                    SELECT u.nickName 
                    FROM user AS u
                    WHERE u.nickName = "%s"
                ''' % (d["nickName"])
            curs.execute(sql)
            if curs.fetchone() is None:
                rv['result'] = True
            else:
                rv['msg'] = 'NickName already registered'
        except Exception as ex:
            rv['msg'] = str(ex)
        finally:
            if curs:
                curs.close()
            return rv

    def setAccountRegist(self, d):
        rv = { 'result': True, 'msg': '' }
        try:
            curs = self._dbConn.cursor()
            sql = '''
                INSERT INTO user(email, nickName, password, first_name, last_name, authority)
                VALUES( "%s", "%s", "%s", "%s", "%s", "%s" ) 
            ''' % (d["email"], d["nickName"], d["password"], d["firstName"], d["lastName"], d["authority"])
            curs.execute(sql)
            rv['data'] = curs.fetchall()
        except Exception as ex:
            rv['result'] = False
            rv['msg'] = str(ex)
        finally:
            if curs:
                curs.close()
            return rv

    def getAuthorityList(self):
        rv = {'result': False}
        try:
            curs = self._dbConn.cursor()
            sql = '''
                SELECT `code`, `name` FROM set_authority
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
