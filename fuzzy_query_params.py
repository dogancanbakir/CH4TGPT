import requests
import random
import sys
from urllib.parse import urlparse, parse_qs, urlencode


# check if the user provided the -h or --help parameter
if "-h" in sys.argv or "--help" in sys.argv:
    print(" ____________________________ ")
    print("< Fuzzy Query Params           >")
    print(" ---------------------------- ")
    print("        \\   ^__^")
    print("         \\  (oo)\\_______")
    print("            (__)\\       )\\/\\")
    print("                ||----w |")
    print("                ||     ||")
    print()

    # print the usage document
    print("Usage: python3 fuzzy_query_params.py <url> <payload1> <payload2> ... <payloadN>")
    print()
else:
    url = sys.argv[1]
    payloads = sys.argv[2:]

    def fuzz_query_params(url, payloads):
        parsed_url = urlparse(url)
        params = parse_qs(parsed_url.query)
        payload = random.choice(payloads)
        for key in params:
            params[key] = payload
        new_url = parsed_url._replace(query=urlencode(params, doseq=True)).geturl()
        return new_url

    # generate new payloads by adding random suffixes, prefixes, and values to each user-provided payload
    new_payloads = []
    for payload in payloads:
        # change the casing of the payload
        new_payload = payload.upper() if random.random() > 0.5 else payload.lower()

        # add a random suffix to the payload
        suffix = random.randint(1, 1000)
        new_payload = new_payload + str(suffix)

        # add a random prefix to the payload
        prefix = random.randint(1, 1000)
        new_payload = str(prefix) + new_payload

        # add a random value based on the input type
        if isinstance(payload, int):
            new_payload = int(new_payload)
        elif isinstance(payload, float):
            new_payload = float(new_payload)

        # add the new payload to the list
        new_payloads.append(new_payload)

    # add the new payloads to the list of payloads
    payloads += new_payloads

    # create a list of URLs to test
    urls = []
    for i in range(0, random.randint(10, 100)):
        # generate a random URL
        url = fuzz_query_params(url, payloads)

        # add the URL to the list
        urls.append(url)

    # test each URL
    for url in urls:
        try:
            # make a request to the URL
            response = requests.get(url)

            # print the URL and the response headers
            print("URL:", url)
            print("Headers:", response.headers)
            print()
        except:
            print("Error: Unable to connect to", url)
            print()
