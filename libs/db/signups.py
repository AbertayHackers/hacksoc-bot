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

    def checkVerificationCode(self, rowID: int):
        sql = """SELECT studentID, verificationCode, verificationExpiry FROM signups WHERE id = %s AND verificationUsed = 0"""
        if not self.dictcurs.execute(sql, (rowID,)):
            return False
        return self.dictcurs.fetchall()[-1]

    def checkPreviousSignup(self, studentID: str) -> bool:
        sql = """SELECT studentID FROM signups WHERE studentID = %s AND inviteUsed = 1"""
        if self.curs.execute(sql, (studentID,)):
            return True
        return False

    def insertInvite(self, registerID: int, code: str) -> bool:
        sql = """UPDATE signups SET inviteCode = %s WHERE id = %s"""
        if not self.curs.execute(sql, (code, registerID)):
            return False
        self.dbh.commit()
        return True

    def insertPermaJoin(self, discordID, perms, inviteCode):
        sql = """INSERT INTO signups (discordID, perms, inviteCode, joinTime, genType, inviteUsed) VALUES (%s, %s, %s, NOW(), "PERMA", 1)"""
        if not self.curs.execute(sql, (discordID, perms, inviteCode)):
            return False
        self.dbh.commit()
        return True


    def setUsed(self, code: str) -> bool:
        sql = """UPDATE signups SET inviteUsed = 1 WHERE inviteCode = %s"""
        if not self.curs.execute(sql, (code,)):
            return False
        self.dbh.commit()
        return True

    def setVerificationUsed(self, rowID: int) -> bool:
        sql = """UPDATE signups SET verificationUsed = 1 WHERE id = %s"""
        if not self.curs.execute(sql, (rowID,)):
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

    def manualUserInsert(self, discordID: int, role: str) -> bool:
        sql = """INSERT INTO signups (discordID, perms, genType) VALUES (%s, %s, "INSERT")"""
        if not self.curs.execute(sql, (discordID, role)):
            return False
        self.dbh.commit()
        return True

    def storePerma(self, code: str, perms: str) -> bool:
        sql = """INSERT INTO permaInvites (inviteCode, perms) VALUES (%s, %s)"""
        if not self.curs.execute(sql, (code,perms)):
            return False
        self.dbh.commit()
        return True

    def delPerma(self, code: str) -> bool:
        sql = """DELETE FROM permaInvites WHERE inviteCode = %s"""
        self.curs.execute(sql, (code,))
        if self.curs.rowcount < 1:
            return False
        self.dbh.commit()
        return True
        
    def getPermaInvites(self, withPerms=False) -> list:
        sql = f"""SELECT inviteCode{", perms" if withPerms else ""} FROM permaInvites"""
        self.curs.execute(sql)
        if self.curs.rowcount == 0:
            return []
        res = []
        for i in self.curs.fetchall():
            if withPerms:
                res.append(list(i))
            else:
                res.append(i[0])
        return res

    def getPermaInviteRole(self, code: str) -> str:
        sql = """SELECT perms FROM permaInvites WHERE inviteCode = %s"""
        if not self.curs.execute(sql, (code,)):
            return False
        elif self.curs.rowcount != 1:
            return False

        return self.curs.fetchone()[0]

    def getPermaUses(self, code: str):
        sql = """SELECT uses FROM permaInvites WHERE inviteCode = %s"""
        if not self.curs.execute(sql, (code,)) or self.curs.rowcount != 1:
            return False
        return self.curs.fetchone()[0]

    def incrementPermaUses(self, code: str) -> bool:
        sql = """UPDATE permaInvites SET uses = uses + 1 WHERE inviteCode = %s"""
        if not self.curs.execute(sql, (code,)):
            return False
        elif self.curs.rowcount != 1:
            return False
        return True
