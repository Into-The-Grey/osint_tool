# Medusa Tool Documentation

## Overview

The Medusa Tool tests web applications for vulnerabilities. This is an active tool and should only be used on authorized targets.

## Configuration

- **File**: `configs/medusa_tool.json`
- **Example Content**:

  ```json
  {
    "medusa_path": "/usr/bin/medusa",
    "options": "--force",
    "required": false
  }
  ```

- **medusa_path**: Path to the Medusa executable.
- **options**: Additional options to pass to Medusa.
- **required**: Set to `false` by default.

## Usage

Run the Medusa tool on a target URL by invoking its `run()` method.

## Logging

Scan output is logged in `logs/medusa_tool.log`.

## EXTRA DOCUMENTATION

```HTML
    Display all modules currently installed:

    % medusa -d
     
    Medusa v1.0-rc1 [http://www.foofus.net] (C) JoMo-Kun / Foofus Networks

      Available modules in "." :
      Available modules in "/usr/local/lib/medusa/modules" :
        + mssql.mod :
          Brute force module for M$-SQL sessions : version 0.1.0
        + http.mod :
          Brute force module for HTTP : version 0.1.1
        + ssh.mod :
          Brute force module for SSH v2 sessions : version 0.1.1
        + smbnt.mod :
          Brute force module for SMB/NTLMv1 sessions : version 0.1.1
        + telnet.mod :
          Brute force module for telnet sessions : version 0.1.4

    Display specific options for a given module:

    % medusa -M smbnt -q 
    Medusa v1.0-rc1 [http://www.foofus.net] (C) JoMo-Kun / Foofus Networks

    smbnt.mod (0.1.1) JoMo-Kun :: Brute force module for SMB/NTLMv1 sessions

    Available module options:
      GROUP:? (DOMAIN, LOCAL*, BOTH)
        Option sets NetBIOS workgroup field.
        DOMAIN: Check credentials against this hosts primary domain controller via this host.
        LOCAL:  Check local account.
        BOTH:   Check both. This leaves the workgroup field set blank and then attempts to check
                the credentials against the host. If the account does not exist locally on the
                host being tested, that host then queries its domain controller.
      GROUP_OTHER:?
        Option allows manual setting of domain to check against. Use instead of GROUP.
      PASS:?  (PASSWORD*, HASH, MACHINE)
        PASSWORD: Use normal password.
        HASH:     Use a NTLM hash rather than a password.
        MACHINE:  Use the machine's NetBIOS name as the password.
      NETBIOS
        Force NetBIOS Mode (Disable Native Win2000 Mode). Win2000 mode is the default.
        Default mode is to test TCP/445 using Native Win2000. If this fails, module will
        fall back to TCP/139 using NetBIOS mode. To test only TCP/139, use the following:
        medusa -M smbnt -m NETBIOS -n 139

    (*) Default value
    Usage example: "-M smbnt -m GROUP:DOMAIN -m PASS:HASH"

    The following command instructs Medusa to test all passwords listed in passwords.txt against a single user (administrator) on the host 192.168.0.20 via the SMB service. The "-e ns" instructs Medusa to additionally check if the administrator account has either a blank password or has its password set to match its username (administrator).


    % medusa -h 192.168.0.20 -u administrator -P passwords.txt -e ns -M smbnt

    Medusa v1.0-rc1 [http://www.foofus.net] (C) JoMo-Kun / Foofus Networks

    ACCOUNT CHECK: [smbnt] Host: 192.168.0.20 (1/1) User: administrator (1/1) Password:  (1/7)
    ACCOUNT CHECK: [smbnt] Host: 192.168.0.20 (1/1) User: administrator (1/1) Password: administrator (2/7)
    ACCOUNT CHECK: [smbnt] Host: 192.168.0.20 (1/1) User: administrator (1/1) Password: password (3/7)
    ACCOUNT CHECK: [smbnt] Host: 192.168.0.20 (1/1) User: administrator (1/1) Password: pass1 (4/7)
    ACCOUNT CHECK: [smbnt] Host: 192.168.0.20 (1/1) User: administrator (1/1) Password: pass2 (5/7)
    ACCOUNT CHECK: [smbnt] Host: 192.168.0.20 (1/1) User: administrator (1/1) Password: pass3 (6/7)
    ACCOUNT CHECK: [smbnt] Host: 192.168.0.20 (1/1) User: administrator (1/1) Password: pass4 (7/7)

    The below command-line demonstrates how to execute some of the parallel features of Medusa. Here at least 20 hosts and 10 users are tested concurrently. The "-L" options instructs Medusa to parallelize by user. This means each of the 10 threads targeting a host checks a unique user.


    % medusa -H hosts.txt -U users.txt -P passwords.txt -T 20 -t 10 -L -F -M smbnt

    Medusa allows host/username/password data to also be set using a "combo" file. The combo file can be specified using the "-C" option. The file should contain one entry per line and have the values colon separated in the format host:user:password. If any of the three fields are left empty, the respective information should be provided either as a global value or as a list in a file. Medusa will perform a basic parameter check based on the contents of the first line in the file.

    The following combinations are possible in the combo file:
        host:username:password
        host:username:
        host::
        :username:password
        :username:
        ::password
        host::password 

    The following example will check each entry in the file combo.txt
    % medusa -M smbnt -C combo.txt

    The combo.txt file:
    192.168.0.20:administrator:password
    192.168.0.20:testuser:pass
    192.168.0.30:administrator:blah
    192.168.0.40:user1:foopass

    The following example will check each entry in the file combo.txt against the targets listed in hosts.txt
    % medusa -M smbnt -C combo.txt -H hosts.txt

    The combo.txt file:
    :administrator:password
    :testuser:pass
    :administrator:blah
    :user1:foopass

    Medusa also supports using PwDump files as a combo file. The format of these files should be user:id:lm:ntlm:::. We look for ':::' at the end of the first line to determine if the file contains PwDump output.
    Resume a Medusa scan. Medusa has the ability to resume a scan which was interrupted with a SIGINT signal (e.g. CTRL-C). For example:

    Test interrupted with SIGINT
    % ../medusa -M ssh -H host.txt -U users.txt -p password
    Medusa v2.0 [http://www.foofus.net] (C) JoMo-Kun / Foofus Networks

    ACCOUNT CHECK: [ssh] Host: 192.168.0.1 (1 of 11, 0 complete) User: foo (1 of 4, 0 complete) Password: password (1 of 1 complete)
    ACCOUNT CHECK: [ssh] Host: 192.168.0.1 (1 of 11, 0 complete) User: administrator (2 of 4, 1 complete) Password: password (1 of 1 complete)
    ACCOUNT CHECK: [ssh] Host: 192.168.0.1 (1 of 11, 0 complete) User: jmk (3 of 4, 2 complete) Password: password (1 of 1 complete)
    ACCOUNT CHECK: [ssh] Host: 192.168.0.1 (1 of 11, 0 complete) User: bar (4 of 4, 3 complete) Password: password (1 of 1 complete)
    ACCOUNT CHECK: [ssh] Host: 192.168.0.11 (2 of 11, 1 complete) User: foo (1 of 4, 0 complete) Password: password (1 of 1 complete)
    ACCOUNT CHECK: [ssh] Host: 192.168.0.11 (2 of 11, 1 complete) User: administrator (2 of 4, 1 complete) Password: password (1 of 1 complete)
    ALERT: Medusa received SIGINT - Sending notification to login threads that we are are aborting.
    ACCOUNT CHECK: [ssh] Host: 192.168.0.11 (2 of 11, 1 complete) User: jmk (3 of 4, 2 complete) Password: password (1 of 1 complete)
    ALERT: To resume scan, add the following to your original command: "-Z h2u3u4h3."

    Interrupted scan being resumed
    % ../medusa -M ssh -H host.txt -U users.txt -p password -Z h2u3u4h3.
    Medusa v2.0 [http://www.foofus.net] (C) JoMo-Kun / Foofus Networks

    ACCOUNT CHECK: [ssh] Host: 192.168.0.11 (2 of 11, 0 complete) User: jmk (3 of 4, 0 complete) Password: password (1 of 1 complete)
    ACCOUNT CHECK: [ssh] Host: 192.168.0.11 (2 of 11, 0 complete) User: bar (4 of 4, 1 complete) Password: password (1 of 1 complete)
    ACCOUNT CHECK: [ssh] Host: 192.168.0.15 (3 of 11, 1 complete) User: foo (1 of 4, 0 complete) Password: password (1 of 1 complete)

    The following is a brief discription of the resume map:

    h2u3u4h3.
    +--------- First host which was not 100% completed
      +------- First user for host which was not 100% completed
        +----- First user for host which was not started
          +--- First host which was not started
            +- Map ending mark

Module specific details:

    AFP
    CVS
    FTP
    HTTP
    IMAP
    MS-SQL
    MySQL
    NetWare NCP
    NNTP
    PcAnywhere
    POP3
    PostgreSQL
    REXEC
    RDP
    RLOGIN
    RSH
    SMBNT (SMBv1-3, SMB signing)
    SMTP-AUTH
    SMTP-VRFY
    SNMP
    SSHv2
    Subversion (SVN)
    Telnet
    VMware Authentication Daemon (vmauthd)
    VNC
    Generic Wrapper
    Web Form 
```

---
