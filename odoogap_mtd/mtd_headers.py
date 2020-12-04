from requests import get
from datetime import datetime, timezone
import socket

def get_local_ip():
    return ([l for l in ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2]
                              if not ip.startswith("127.")][:1], [[(s.connect(('8.8.8.8', 53)),
                                                                    s.getsockname()[0], s.close()) for s in
                                                                   [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][
                                                                      0][1]]) if l][0][0])

def create_headers_dic(public_port, device_id, user_id, screens, window_size, browser_plugin, js_user_agent, login_date_format, unique_reference, module_version, licence_ids):
    
    public_ip = get('https://api.ipify.org').text
    public_vendor_ip = socket.gethostbyname('odoomtd.co.uk')

    timestamp = login_date_format.replace("/", "-").replace(", ", "T").replace(":", "%3A") + "Z"

    date_string = str(datetime.now(timezone.utc).astimezone().isoformat())
    
    if '+' in date_string:
        data = date_string.rsplit('+', 1)
        utc_time = "UTC+%s" % str(data[1])
    else:
        data = date_string.rsplit('-', 1)
        utc_time = "UTC-%s" % str(data[1])

    return {
        'Gov-Client-Connection-Method': 'WEB_APP_VIA_SERVER',
        'Gov-Client-Public-IP': public_ip,
        'Gov-Client-Public-Port': public_port,
        'Gov-Client-Device-ID': device_id,
        'Gov-Client-User-IDs': 'My_Webapp_Software=' + str(user_id),
        'Gov-Client-Timezone': utc_time,
        'Gov-Client-Local-IPs': get_local_ip(),
        'Gov-Client-Screens': screens if screens else "width=1920&height=1080&scaling-factor=1.7777777777777777&colour-depth=24",
        'Gov-Client-Window-Size': window_size if window_size else "width=1920&height=1080",
        'Gov-Client-Browser-Plugins': browser_plugin if browser_plugin else 'Native%20Client',
        'Gov-Client-Browser-JS-User-Agent': js_user_agent if js_user_agent else "",
        'Gov-Client-Browser-Do-Not-Track': "false",
        'Gov-Client-Multi-Factor': "type=OTHER&timestamp=" + timestamp + "&unique-reference=" + str(hash(unique_reference)),
        'Gov-Vendor-Version': "hmrc_mtd_client" + "=" + str(module_version) + "&hmrc_mtd_server" + "=" + "0.1",
        'Gov-Vendor-License-IDs': "hmrc_mtd_server" + "=" + str(hash(licence_ids)),
        'Gov-Vendor-Public-IP': public_vendor_ip,
        'Gov-Vendor-Forwarded': "by=" + public_vendor_ip + "&for=" + public_ip
    }