from libs.db import Conn

class SignupConn(Conn):
    def manualInvite(self, code: str, role: str) -> bool:
        sql = """INSERT INTO signups (perms, inviteCode, genType) VALUES (%s, %s, "MANUAL")"""
        if not self.curs.execute(sql, (role, code)):
            return False
        self.dbh.commit()
        return True

    def setUsed(self, code: str) -> bool:
        sql = """UPDATE signups SET inviteUsed = 1 WHERE inviteCode = %s"""
        if not self.curs.execute(sql, (code,)):
            return False
        self.dbh.commit()
        return True

    def checkRoleFromInvite(self, code: str):
        sql = """SELECT perms FROM signups WHERE inviteCode = %s"""
        self.curs.execute(sql, (code,))
        if self.curs.rowcount != 1:
            return False
        return self.curs.fetchone()[0]

    def setDiscordID(self, discordID: int, code: str) -> bool:
        sql = f"""UPDATE signups SET discordID = %s, joinTime = NOW() WHERE inviteCode = %s"""
        if not self.curs.execute(sql, (discordID, code)):
            return False
        self.dbh.commit()
        return True
    
     
