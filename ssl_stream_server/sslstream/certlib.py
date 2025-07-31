import base64
import datetime
import logging
import time

from collections import OrderedDict

from OpenSSL import crypto
from construct import Struct, Byte, Int16ub, Int64ub, Enum, Bytes, \
    Int24ub, this, GreedyBytes, GreedyRange, Terminated

MerkleTreeHeader = Struct(
    "Version"         / Byte,
    "MerkleLeafType"  / Byte,
    "Timestamp"       / Int64ub,
    "LogEntryType"    / Enum(Int16ub, X509LogEntryType=0, PrecertLogEntryType=1),
    "Entry"           / GreedyBytes
)

Certificate = Struct(
    "Length" / Int24ub,
    "CertData" / Bytes(this.Length)
)

CertificateChain = Struct(
    "ChainLength" / Int24ub,
    "Chain" / GreedyRange(Certificate),
)

PreCertEntry = Struct(
    "LeafCert" / Certificate,
    "Chain" / CertificateChain,
    Terminated
)

def dump_extensions(certificate):
    extensions = {}
    for x in range(certificate.get_extension_count()):
        extension_name = ""
        try:
            extension_name = certificate.get_extension(x).get_short_name()

            if extension_name == b'UNDEF':
                continue

            extensions[extension_name.decode('latin-1')] = certificate.get_extension(x).__str__()
        except:
            try:
                extensions[extension_name.decode('latin-1')] = "NULL"
            except Exception as e:
                logging.debug("Extension parsing error -> {}".format(e))
    return extensions

def serialize_certificate(certificate):
    subject = certificate.get_subject()
    not_before_datetime = datetime.datetime.strptime(certificate.get_notBefore().decode('ascii'), "%Y%m%d%H%M%SZ")
    not_after_datetime = datetime.datetime.strptime(certificate.get_notAfter().decode('ascii'), "%Y%m%d%H%M%SZ")
    return {
        "subject": {
            "aggregated": repr(certificate.get_subject())[18:-2],
            "C": subject.C,
            "ST": subject.ST,
            "L": subject.L,
            "O": subject.O,
            "OU": subject.OU,
            "CN": subject.CN
        },
        "extensions": dump_extensions(certificate),
        "not_before": not_before_datetime.timestamp(),
        "not_after": not_after_datetime.timestamp(),
        "serial_number": '{0:x}'.format(int(certificate.get_serial_number())),
        "fingerprint": str(certificate.digest("sha1"),'utf-8'),
        "as_der": base64.b64encode(
            crypto.dump_certificate(
                crypto.FILETYPE_ASN1, certificate
            )
        ).decode('utf-8')
    }

def add_all_domains(cert_data):
    all_domains = []
    if cert_data['leaf_cert']['subject']['CN']:
        all_domains.append(cert_data['leaf_cert']['subject']['CN'])

    subject_alternative_name = cert_data['leaf_cert']['extensions'].get('subjectAltName')
    if subject_alternative_name:
        for entry in subject_alternative_name.split(', '):
            if entry.startswith('DNS:'):
                all_domains.append(entry.replace('DNS:', ''))

    cert_data['leaf_cert']['all_domains'] = list(OrderedDict.fromkeys(all_domains))
    return cert_data

def parse_ctl_entry(entry, operator_information):
    try:
        mtl = MerkleTreeHeader.parse(base64.b64decode(entry['leaf_input']))
    except Exception as e:
        logging.error(f"Error parsing MerkleTreeHeader: {e}")
        return None

    cert_data = {}
    try:
        if mtl.LogEntryType == "X509LogEntryType":
            cert_data['update_type'] = "X509LogEntry"
            try:
                if isinstance(mtl.Entry, bytes):
                    parsed_cert = Certificate.parse(mtl.Entry)
                    if hasattr(parsed_cert, 'CertData'):
                        cert_bytes = parsed_cert.CertData
                    else:
                        cert_bytes = mtl.Entry
                else:
                    cert_bytes = base64.b64decode(mtl.Entry) if isinstance(mtl.Entry, str) else mtl.Entry
                    
                chain = [crypto.load_certificate(crypto.FILETYPE_ASN1, cert_bytes)]
                
                if 'extra_data' in entry and entry['extra_data']:
                    extra_data = CertificateChain.parse(base64.b64decode(entry['extra_data']))
                    for cert in extra_data.Chain:
                        if hasattr(cert, 'CertData'):
                            chain.append(crypto.load_certificate(crypto.FILETYPE_ASN1, cert.CertData))
                        
            except Exception as cert_parse_error:
                logging.error(f"Error parsing X509 certificate: {cert_parse_error}")
                try:
                    chain = [crypto.load_certificate(crypto.FILETYPE_ASN1, mtl.Entry)]
                except Exception as fallback_error:
                    logging.error(f"Fallback parsing also failed: {fallback_error}")
                    return None
                    
        else:
            cert_data['update_type'] = "PreCertEntry"
            try:
                if 'extra_data' in entry and entry['extra_data']:
                    extra_data = PreCertEntry.parse(base64.b64decode(entry['extra_data']))
                    if hasattr(extra_data.LeafCert, 'CertData'):
                        chain = [crypto.load_certificate(crypto.FILETYPE_ASN1, extra_data.LeafCert.CertData)]
                    else:
                        chain = [crypto.load_certificate(crypto.FILETYPE_ASN1, mtl.Entry)]

                    for cert in extra_data.Chain:
                        if hasattr(cert, 'CertData'):
                            chain.append(crypto.load_certificate(crypto.FILETYPE_ASN1, cert.CertData))
                else:
                    chain = [crypto.load_certificate(crypto.FILETYPE_ASN1, mtl.Entry)]
                    
            except Exception as precert_parse_error:
                logging.error(f"Error parsing PreCert entry: {precert_parse_error}")
                try:
                    chain = [crypto.load_certificate(crypto.FILETYPE_ASN1, mtl.Entry)]
                except Exception as fallback_error:
                    logging.error(f"PreCert fallback parsing also failed: {fallback_error}")
                    return None

        cert_data.update({
            "leaf_cert": serialize_certificate(chain[0]),
            "chain": [serialize_certificate(x) for x in chain[1:]] if len(chain) > 1 else [],
            "cert_index": entry.get('index', 0),
            "seen": time.time()
        })

        add_all_domains(cert_data)
        cert_data['source'] = {
            "url": operator_information['url'],
            "name": operator_information['description']
        }
        return cert_data
        
    except Exception as e:
        logging.error(f"General error parsing CT entry: {e}")
        return None
