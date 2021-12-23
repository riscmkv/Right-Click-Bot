import argparse
import requests
import time
import urllib
import hashlib

def openseas_request(page=0, pagesize=50):
    url = f"https://api.opensea.io/api/v1/assets?order_direction=desc&offset={page}&limit={pagesize}"
    # Wait to prevent API timeout
    time.sleep(1.0)
    return requests.request("GET", url).json()

def main():
    # Grab user arguments
    parser = argparse.ArgumentParser(description="Automatically scrape NFT's from OpenSea",
                                    add_help=True)
    parser.add_argument('--limit', dest='limit', type=int, help="Max number of NFT's to scrape, in multiples of 50. Default unlimited.", default=0)
    parser.add_argument('--savedir', dest='savedir', type=str, help="Destination directory where to save NFT's", default=".")
    args = parser.parse_args()

    run_forever = (args.limit == 0)
    limit = args.limit
    page = 0

    # Iterate over all pages
    while run_forever or (limit > 0):
        limit -= 1

        # Grab NFT's
        response = openseas_request(page=page)
        
        for nft in response['assets']:
            if nft['image_url'] == '':
                continue
            imname = nft['image_url'].split("/")[-1]

            # Save the png's, handle any exceptions
            try:
                urllib.request.urlretrieve(nft['image_url'], args.savedir + "/" + imname + ".png") 
            except urllib.error.HTTPError as e:
                print("HTTPError: ", e.code)
            except urllib.error.URLError as e:
                print("URLError: ", e.reason)
        
        page += 1

if __name__ == '__main__':
    main()