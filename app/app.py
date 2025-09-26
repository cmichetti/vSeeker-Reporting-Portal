import reflex as rx
from app.states.state import State
import re

def result_item_with_description(item: rx.Var[tuple[str, str]]) -> rx.Component:
    key = item[0]
    value = item[1]
    return (
        rx.cond(
            value == "",
            None,
            rx.el.li(
                rx.cond(
                    key == "os",
                    rx.cond(
                        value.contains("2012")
                        | value.contains("2008")
                        | value.contains("2003")
                        | value.contains("2000"),
                        rx.el.div(
                            rx.el.span("!", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(" - Operating System: ", class_name="font-normal border-none"),
                            rx.el.span(value, class_name="font-semibold text-red-300 border-none"),
                        ),
                        rx.el.div(
                            rx.el.span("* - Operating System: ", class_name="font-normal border-none"),
                            rx.el.span(value, class_name="font-semibold border-none"),
                        ),
                    ),
                    None,
                ),
                rx.cond(
                    key == "virtual",
                    rx.cond(
                        value == "1",
                        rx.el.div(
                            rx.el.span(
                                "*- Server is a Virtual Machine.",
                                class_name="font-normal border-none",
                            ),
                        ),
                        rx.el.div(
                            rx.el.span(
                                "* - Server is not a Virtual Machine.",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "serialnumber",
                    rx.cond(
                        value != None,
                        rx.el.div(
                            rx.el.span(
                                "* - Serial Number: ", value, 
                                class_name="font-normal border-none",
                            ),
                        ),
                        None,
                    ),
                ),
                rx.cond(
                    key == "windowsfullypatched",
                    rx.cond(
                        value == "1",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(
                                " - Windows is fully patched with Windows Updates.",
                                class_name="font-normal border-none",
                            ),
                        ),
                        rx.el.div(
                            rx.el.span("X", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - Windows is not fully patched with Windows Updates.",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "firewallstatus",
                    rx.cond(
                        value == "1",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(
                                " - The Windows Firewall is fully enabled.",
                                class_name="font-normal border-none",
                            ),
                        ),
                        rx.el.div(
                            rx.el.span("X", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - The Windows Firewall is not fully enabled.",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "avinstalled",
                    rx.cond(
                        value == "1",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(
                                " - There is a Talix/Microsoft-recognized Anti-Virus installed.",
                                class_name="font-normal border-none",
                            ),
                        ),
                        rx.el.div(
                            rx.el.span("X", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - There is no Talix/Microsoft-recognized Anti-Virus installed.",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "everyoneShares",
                    rx.cond(
                        value == "1",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(
                                " - There are no file shares with Everyone access granted.",
                                class_name="font-normal border-none",
                            ),
                        ),
                        rx.el.div(
                            rx.el.span("X", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - There are file shares with Everyone access granted.",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "DriveSpaceAll",
                    rx.cond(
                        value == "1",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(
                                " - All drives have over 10% free space.",
                                class_name="font-normal border-none",
                            ),
                        ),
                        rx.el.div(
                            rx.el.span("!", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - There are some drives with less than 10% free space!",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "printspooler",
                    rx.cond(
                        value == "0",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(
                                " - The Print Spooler service is disabled.",
                                class_name="font-normal border-none",
                            ),
                        ),
                        rx.el.div(
                            rx.el.span("X", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - The Print Spooler service is enabled and should be disabled if possible.",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "smbv1Disabled",
                    rx.cond(
                        value == "1",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(" - SMBv1 is disabled.", class_name="font-normal border-none"),
                        ),
                        rx.el.div(
                            rx.el.span("X", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - SMBv1 is enabled and should be disabled, as it is a vulnerable file transfer protocol.",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "netbiosDisabled",
                    rx.cond(
                        value == "1",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(" - NetBIOS is disabled.", class_name="font-normal border-none"),
                        ),
                        rx.el.div(
                            rx.el.span("X", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - NetBIOS is enabled and should be disabled, as it is an extremely vulnerable network protocol.",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "lmhostsDisabled",
                    rx.cond(
                        value == "1",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(
                                " - LMHosts Lookup is disabled.", class_name="font-normal border-none"
                            ),
                        ),
                        rx.el.div(
                            rx.el.span("X", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - LMHosts Lookup is enabled and should be disabled.",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "tls10Disabled",
                    rx.cond(
                        value == "1",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(
                                " - TLS v1.0 is disabled.", class_name="font-normal border-none"
                            ),
                        ),
                        rx.el.div(
                            rx.el.span("X", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - TLS v1.0 is enabled and should be disabled, as it is a vulnerable network protocol.",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "tls11Disabled",
                    rx.cond(
                        value == "1",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(
                                " - TLS v1.1 is disabled.", class_name="font-normal border-none"
                            ),
                        ),
                        rx.el.div(
                            rx.el.span("X", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - TLS v1.1 is enabled and should be disabled, as it is a vulnerable network protocol.",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "llmnrDisabled",
                    rx.cond(
                        value == "1",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(" - LLMNR is disabled.", class_name="font-normal border-none"),
                        ),
                        rx.el.div(
                            rx.el.span("X", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - LLMNR is enabled and should be disabled, as it is a vulnerable to man in the middle attacks.",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "ntlmv1Level",
                    rx.cond(
                        value == "5",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(
                                " - NTLMv1 is fully disabled.", class_name="font-normal border-none"
                            ),
                        ),
                        rx.el.div(
                            rx.el.span("X", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - NTLMv1 is not fully disabled, and should be as it is a vulnerable network authentication protocol.",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "autorunDisabled",
                    rx.cond(
                        value == "1",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(
                                " - AutoRun is fully disabled.", class_name="font-normal border-none"
                            ),
                        ),
                        rx.el.div(
                            rx.el.span("!", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - AutoRun is enabled and should be turned off to prevent automatically running software from mounted drives.",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "wdigestDisabled",
                    rx.cond(
                        value == "1",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(
                                " - wDigest is fully disabled.", class_name="font-normal border-none"
                            ),
                        ),
                        rx.el.div(
                            rx.el.span("!", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - wDigest is enabled and should be as it is a vulnerable authentication protocol.",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "smbsigningEnabled",
                    rx.cond(
                        value == "1",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(
                                " - SMBv2 Signing is fully enabled.",
                                class_name="font-normal border-none",
                            ),
                        ),
                        rx.el.div(
                            rx.el.span("X", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - SMBv2 Signing is not fully enabled, and should be to help protect against file interception.",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "anonSIDTransDisabled",
                    rx.cond(
                        value == "1",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(
                                " - Anonymous SID translation is fully disabled.",
                                class_name="font-normal border-none",
                            ),
                        ),
                        rx.el.div(
                            rx.el.span("X", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - Anonymous SID translation is not fully disabled.",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "uacEnabledPW",
                    rx.cond(
                        value == "1",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(
                                " - UAC is enabled to prevent elevation with a password requirement.",
                                class_name="font-normal border-none",
                            ),
                        ),
                        rx.el.div(
                            rx.el.span("X", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - UAC needs to be enabled to protect elevation requests with a password requirement.",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "browserpwDisabled",
                    rx.cond(
                        value == "1",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(
                                " - Browser password saving is disabled.",
                                class_name="font-normal border-none",
                            ),
                        ),
                        rx.el.div(
                            rx.el.span("X", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - Browser password saving should be disabled to protect user passwords from being easily obtained.",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "ipv6Disabled",
                    rx.cond(
                        value == "1",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(" - IPv6 is disabled.", class_name="font-normal border-none"),
                        ),
                        rx.el.div(
                            rx.el.span("X", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - IPv6 networking protocol should be disabled if not needed/used.",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "winrmDisabled",
                    rx.cond(
                        value == "1",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(" - WinRM is disabled.", class_name="font-normal border-none"),
                        ),
                        rx.el.div(
                            rx.el.span("!", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - WinRM should be disabled if not needed/used, as it provides an attacker connectivity across the network.",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "smbencryptEnabled",
                    rx.cond(
                        value == "1",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(
                                " - SMBv3 Encryption is enabled.", class_name="font-normal border-none"
                            ),
                        ),
                        rx.el.div(
                            rx.el.span("X", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - SMBv3 Encryption should be enabled if possible to provide the best file protection possible on the network.",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "lsaProtEnabled",
                    rx.cond(
                        value == "1",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(
                                " - LSA Protection is fully enabled.",
                                class_name="font-normal border-none",
                            ),
                        ),
                        rx.el.div(
                            rx.el.span("!", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - LSA Protection should be enabled to protect against malicious apps being able to execute.",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "lastusershownatlogon",
                    rx.cond(
                        value == "0",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(
                                " - Information about the previous user account that logged in is hidden.",
                                class_name="font-normal border-none",
                            ),
                        ),
                        rx.el.div(
                            rx.el.span("!", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - Information about the previous user account that logged in should be hidden.",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "ldapSigning",
                    rx.cond(
                        value == "1",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(
                                " - LDAP Signing is enabled.", class_name="font-normal border-none"
                            ),
                        ),
                        rx.el.div(
                            rx.el.span("!", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - LDAP Signing should be enabled to secure the use of LDAP on the domain.",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "ldapChBinding",
                    rx.cond(
                        value == "1",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(
                                " - LDAP Channel Binding is enabled.",
                                class_name="font-normal border-none",
                            ),
                        ),
                        rx.el.div(
                            rx.el.span("!", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - LDAP Channel Binding should be enabled to secure the use of LDAP on the domain.",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "credmgrDisabled",
                    rx.cond(
                        value == "1",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(
                                " - Windows Credential Manager is disabled.",
                                class_name="font-normal border-none",
                            ),
                        ),
                        rx.el.div(
                            rx.el.span("!", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - Windows Credential Manager should be disabled, as passwords should not be stored on the server.",
                                class_name="font-normal border-none border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "EvtVwrAuditPolicy",
                    rx.cond(
                        value == "1",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(
                                " - The Event Viewer Audit Policy is correctly configured.",
                                class_name="font-normal border-none",
                            ),
                        ),
                        rx.el.div(
                            rx.el.span("X", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - The Event Viewer Audit Policy is not configured correctly to gather all events.",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "DHCPScopeOver80",
                    rx.cond(
                        value == "0",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(
                                " - The DHCP server has leased out less than 80% of its IP available addresses.",
                                class_name="font-normal border-none",
                            ),
                        ),
                        rx.el.div(
                            rx.el.span("!", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - The DHCP server has leased out more than 80% of its available IP addresses.",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "IISDefPAgesExist",
                    rx.cond(
                        value == "0",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(
                                " - The default IIS pages have been removed.",
                                class_name="font-normal border-none",
                            ),
                        ),
                        rx.el.div(
                            rx.el.span("!", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - The default IIS pages should be removed from the web server.",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "cachedlogoncount",
                    rx.cond(
                        value == "0",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(
                                " - The cached logon count on the domain is set to 4 or less.",
                                class_name="font-normal border-none",
                            ),
                        ),
                        rx.el.div(
                            rx.el.span("!", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - The cached logon count on the domain should be set to 4 logins or less.",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "LATFPDisabled",
                    rx.cond(
                        value == "1",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(
                                " - The Local Admin account cannot be used to log on remotely.",
                                class_name="font-normal border-none",
                            ),
                        ),
                        rx.el.div(
                            rx.el.span("X", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - The Local Admin account should be restricted from logging on remotely.",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "RemoteRegDisabled",
                    rx.cond(
                        value == "1",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(
                                " - The Remote Registry service is disabled.",
                                class_name="font-normal border-none",
                            ),
                        ),
                        rx.el.div(
                            rx.el.span("X", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - The Remote Registry service is not disabled (this is OK on Domain Controllers).",
                                class_name="font-normal border-none",
                            ),
                        ),
                    ),
                ),
                rx.cond(
                    key == "BitLockerEnabled",
                    rx.cond(
                        value == "1",
                        rx.el.div(
                            rx.el.span("√", class_name="font-bold bg-none text-green-500 border-none"),
                            rx.el.span(
                                " - BitLocker is enabled.", class_name="font-normal border-none"
                            ),
                        ),
                        rx.el.div(
                            rx.el.span("X", class_name="font-bold bg-none text-red-500 border-none"),
                            rx.el.span(
                                " - BitLocker is not enabled.", class_name="font-normal border-none"
                            ),
                        ),
                    ),
                ), class_name="font-normal border-none"
            ),
        ), 
    )

# Filter the list ahead of the foreach loop
# @rx.cached_property
#def filtered_items(self) -> list[str]:
 #   # Filter out the items we don't want in the list for each server
 #   return [item for item in self.items if (item[0] != "id" | item[0] != "hostname" | item[0] != "company" | item[0] != "ipaddress" | item[1] != "-1")]


def scan_results_list() -> rx.Component:
    return rx.el.div(
        rx.el.ul(
            rx.foreach(
                State.scan_data,
                lambda result: rx.cond(
                    State.scan_data.length() > 0,
                    rx.el.li(
                        rx.el.span(
                            result["hostname"],
                            " (",
                            result["ipaddress"],
                            ")",
                            class_name="text-xl font-semibold text-gray-700 border-none",
                        ),

                        rx.foreach(
                            # result.items(),
                            result.items(),
                            lambda item: rx.cond(
                                (item[0] != "id")
                                & (item[0] != "hostname")
                                & (item[0] != "company")
                                & (item[0] != "ipaddress")
                                & (item[1] != "-1") # Ignore items that have -1 value in the db
                                & (item[1] != "NULL"),  
                                rx.el.ul(result_item_with_description(item)),
                                None,
                            ),
                        ), class_name="list-none p-0 mt-2 mb-4 border-none rounded-md overflow-hidden shadow-sm",
                                              
#                        rx.el.ul(
#                            rx.foreach(
#                                result.items(),
#                                lambda item: rx.cond(
#                                    (item[0] != "id")
#                                    & (item[0] != "hostname")
#                                    & (item[0] != "company")
#                                    & (item[0] != "ipaddress")
#                                    & (item[1] != "-1"),  # Ignore items that have -1 value in the db
#                                    result_item_with_description(item),
#                                    rx.fragment(),
#                                ),
#                            ),
#                            class_name="list-none p-0 mt-2 mb-4 border-none rounded-md overflow-hidden shadow-sm",
#                        ),
                  
                    ),
                    rx.el.ul(
                        rx.foreach(
                            result.items(),
                            lambda item: rx.cond(
                                (item[0] != "id")
                                & (item[1] != "-1"),  # Ignore items that have -1 value in the db
                                result_item_with_description(item),
                                None,
                            ),
                        ),
                        class_name="border-none",
                    ),
                ),
            ),
            class_name="w-full max-w-4xl list-none p-0 border-none",
        ),
        class_name="w-full flex flex-col items-center mt-8 items-center border-none",
    )


def index() -> rx.Component:
    return rx.el.main(
        rx.el.div(
            rx.el.h1(
                "vSeeker Reporting Portal",
                class_name="text-xl font-bold text-gray-800",
            ),
            rx.el.div(
                rx.el.select(
                    rx.el.option("Select Company", value="", disabled=True),
                    rx.foreach(
                        State.companies,
                        lambda company: rx.el.option(company, value=company),
                    ),
                    value=State.selected_company,
                    on_change=State.on_company_change,
                    class_name="bg-white border-2 rounded",
                ),
                rx.el.select(
                    rx.el.option("Select Hostname", value="", disabled=True),
                    rx.foreach(
                        State.hostnames,
                        lambda hostname: rx.el.option(hostname, value=hostname),
                    ),
                    value=State.selected_hostname,
                    on_change=State.on_hostname_change,
                    class_name="bg-white border-2 rounded",
                    is_disabled=~State.selected_company.to(bool),
                ),
                rx.el.select(
                    rx.el.option("Select Scan Date", value="", disabled=True),
                    rx.foreach(
                        State.scan_dates,
                        lambda scan_date: rx.el.option(scan_date, value=scan_date),
                    ),
                    value=State.selected_scan_date,
                    on_change=State.on_scan_date_change,
                    class_name="bg-white border-2 rounded",
                    is_disabled=~State.selected_hostname.to(bool)
                    | (State.selected_hostname == "All Servers"),
                ),
                class_name="border-none",
            ),
            rx.cond(State.scan_data, scan_results_list(), rx.el.div()),
            class_name="w-full flex flex-col items-center pt-10 px-4 border-none",
        ),
        class_name="font-['Arial'] text-11 bg-white min-h-screen border-none",
    )


app = rx.App(
    theme=rx.theme(appearance="light", panel_background="translucent"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, on_load=State.on_load)