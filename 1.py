import requests
from bs4 import BeautifulSoup
import random
import string

def num():
    first = random.choice(["7", "8", "9"])
    remain = ''.join(random.choices("0123456789", k=9))
    return first + remain

def generate_coupon_code():
    # Generate a random pattern with alternating digits and letters
    return ''.join(random.choices(string.ascii_uppercase + "0123456789", k=5))



session = requests.Session()

headers = {
    'User-Agent': "Mozilla/5.0 (Linux; Android 8.1.0; CPH1909 Build/O11019) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.106 Mobile Safari/537.36",
    'Accept-Encoding': "gzip, deflate, br, zstd",
    'sec-ch-ua': "\"Not)A;Brand\";v=\"99\", \"Android WebView\";v=\"127\", \"Chromium\";v=\"127\"",
    'sec-ch-ua-platform': "\"Android\"",
    'x-requested-with': "XMLHttpRequest",
    'sec-ch-ua-mobile': "?1",
    'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
    'origin': "https://hookstepchallenge.woohoo.in",
    'sec-fetch-site': "same-origin",
    'sec-fetch-mode': "cors",
    'sec-fetch-dest': "empty",
    'accept-language': "en-US,en;q=0.9",
    'cookie': ".AspNetCore.Antiforgery.nrapuvI9APs=CfDJ8NhaIHCuKdZPoqW86_ftR-7_0ifr95xhASrKVjga5iDRERJ84Yz1AWEnaOvDayeQn_x9_2pJobk9pXJ1ck8EPY8sadETVo4db640-gp1LwitnMotndryM1BfhETQWJTsgkbLg4AlxFLIpqzpXiIt7_o; .AspNetCore.Session=CfDJ8NhaIHCuKdZPoqW86%2FftR%2B6PLrWSS8LM4nrw%2BiDgToItCMpYlOOtjY4Y7QIZ8yc3DXo7nMFkQrYetEa9RdoQKQaQ7VXPNjqx8dtuhleKEGLUb1plhGQQIULMeZy%2FmEo4iFwSO4SyTxkkRLQ%2Fxaujj9ncmAAdrTS80Ojvy6EpeYDq; AWSALB=6ZR+nUMEn58/G2dwU4AOK7JP9CqBaLrDYs9whd4l69E8YTDVZ7otAy/4EmDthO/z/szWGY5JxUMIX59KG9soPgjSHcYu12imA/KaFMY+XvrV4go8tnIkg5/ni38x; AWSALBCORS=6ZR+nUMEn58/G2dwU4AOK7JP9CqBaLrDYs9whd4l69E8YTDVZ7otAy/4EmDthO/z/szWGY5JxUMIX59KG9soPgjSHcYu12imA/KaFMY+XvrV4go8tnIkg5/ni38x",
    'priority': "u=1, i"
}


# Loop to fetch the token and send POST requests
while True:
    try:
        # Fetch a new verification token
        url = "https://hookstepchallenge.woohoo.in/claimReward"
        response = session.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for HTTP errors
        cookies = session.cookies.get_dict()
        cookie_header = '; '.join([f"{key}={value}" for key, value in cookies.items()])
        headers['Cookie'] = cookie_header
        token = BeautifulSoup(response.text, 'html.parser').find('input', {'name': '__RequestVerificationToken'}).get('value')
        print(f"Verification Token: {token}")

        # Generate mobile number and coupon code
        mobile_number = num()
        coupon_code = generate_coupon_code()

        # Prepare payload for the claim reward request
        payload = {
            "longi": "",
            "lat": "",
            "FIRSTNAME": "Abhinav",
            "MOBILE": mobile_number,
            "COUPONCODE": f"T8{coupon_code}",
            "CHECKBOX1": "on",
            "OTP": "",
            "REDEMPTIONTYPE": "",
            "curPage": "1",
            "stateDropdown": "0",
            "cityDropdown": "0",
            "branchDropdown": "0",
            "retailerDropdown": "0",
            "couponCodeData": "",
            "parametersOccurance": "0",
            "__RequestVerificationToken": token
        }

        # Send POST request to claim reward
        post_url = "https://hookstepchallenge.woohoo.in/ClaimReward/SaveData"
        response = session.post(post_url, headers=headers, data=payload)
        response.raise_for_status()  # Raise exception for HTTP errors

        # Print the raw response from the server
        print(f"Response Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        print(coupon_code)

        # Debug raw response if JSON decoding fails
        try:
            response_data = response.json()
            error = response_data.get('error')
            if not error:
                with open("code.txt", "a") as file:
                    file.write(f"T8{coupon_code}\n")
                print(f"Coupon code saved: T8{coupon_code}")
            else:
                msg = response_data.get("messageBody", "Unknown error")
                print(f"Error: {msg}")
        except ValueError:
            print("Non-JSON response received:")
            print(response.text)  # Debug raw response
            continue

    except requests.exceptions.RequestException as e:
        print(f"HTTP error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
