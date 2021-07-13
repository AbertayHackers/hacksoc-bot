CREATE DATABASE discord;
CREATE TABLE discord.signups (
    id INT AUTO_INCREMENT PRIMARY KEY,
    discordID VARCHAR(25) UNIQUE,
    studentID VARCHAR(10) UNIQUE,
    perms VARCHAR(20),
    inviteCode VARCHAR(20) UNIQUE,
    verificationCode VARCHAR(35) UNIQUE,
    verificationExpiry DATETIME,
    genType VARCHAR(10) DEFAULT "AUTO",
    inviteUsed BOOL DEFAULT 0
);
CREATE USER 'discord'@'localhost' IDENTIFIED BY 'PUT_A_SECURE_PASSWORD_HERE';
GRANT ALL ON discord.* TO 'discord'@'localhost';
