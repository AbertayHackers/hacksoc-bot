from libs.db import Conn
from time import time
from libs.loadconf import config

class SignupConn(Conn):
    def manualInvite(self, code: str, role: str) -> bool:
        sql = """INSERT INTO signups (perms, inviteCode, genType) VALUES (%s, %s, "MANUAL")"""
        if not self.curs.execute(sql, (role, code)):
            return False
        self.dbh.commit()
        return True

    def autoInvite(self, studentID: str, perms: str, verificationCode: str) -> bool:
        sql = """INSERT INTO signups (studentID, perms, verificationCode, verificationExpiry) VALUES (%s, %s, %s, %s)"""
        expires = int(time()) + config["inviteExpireTime"]
        if not self.curs.execute(sql, (studentID, perms, verificationCode, expires)):
            return False
        self.dbh.commit()
        return self.curs.lastrowid

    def checkValidInvites(self, studentID: str):
        sql = """SELECT verificationExpiry FROM signups WHERE inviteUsed = 0 AND studentID = %s"""
        if not self.curs.execute(sql, (studentID,)):
            return False
        invites = self.curs.fetchall()
        for i in invites:
            if i[0] > int(time()):
                return True
        return False

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

    def checkRoleFromID(self, discordID: int):
        sql = """SELECT perms FROM signups WHERE discordID = %s"""
        self.curs.execute(sql, (discordID,))
        if self.curs.rowcount < 1:
            return False
        return self.curs.fetchall()[-1][0]

    def setDiscordID(self, discordID: int, code: str) -> bool:
        sql = """UPDATE signups SET discordID = %s, joinTime = NOW() WHERE inviteCode = %s"""
        if not self.curs.execute(sql, (discordID, code)):
            return False
        self.dbh.commit()
        return True
    
    def updateUserRole(self, discordID: int, newRole: str) -> bool:
        sql = f"""UPDATE signups SET perms = %s WHERE discordID = %s"""
        self.curs.execute(sql, (newRole, discordID))
        self.dbh.commit()

    def ganualUserInsert(self, discordID: int, role: str) -> bool:
        sql = """INSERT INTO signups (discordID, perms, genType) VALUES (%s, %s, "MANUAL")"""
        if not self.curs.execute(sql, (discordID, role)):
            return False
        self.dbh.commit()
        return True