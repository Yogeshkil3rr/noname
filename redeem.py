<?php
error_reporting(0);
// Read user input for Mobile Number and Coupon Code
echo"Gift Code Claim Script by 404\n";
echo"__________________________\n\n";
echo "Enter your Mobile Number: ";
$mobile = trim(fgets(STDIN));


echo "Enter your Coupon Code: ";
$coupon_code = trim(fgets(STDIN));
echo"__________________________\n\n";

// STEP 1: Initialize cURL to get cookies and token
$ch = curl_init();
$url = "https://hookstepchallenge.woohoo.in/claimReward";

// Set headers for the first request
$headers = [
    "upgrade-insecure-requests: 1",
    "user-agent: Mozilla/5.0 (Linux; Android 14; RMX3870) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.200 Mobile Safari/537.36",
    "accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "accept-encoding: gzip, deflate, br, zstd",
    "accept-language: en-GB,en-US;q=0.9,en;q=0.8"
];

curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
curl_setopt($ch, CURLOPT_ENCODING, "gzip, deflate, br, zstd");
curl_setopt($ch, CURLOPT_HEADER, true);

$response = curl_exec($ch);
if (curl_errno($ch)) {
    echo 'Error: ' . curl_error($ch);
    curl_close($ch);
    exit;
}

// Extract cookies and token
$header_size = curl_getinfo($ch, CURLINFO_HEADER_SIZE);
$headers = substr($response, 0, $header_size);
$body = substr($response, $header_size);

preg_match('/AWSALB=([^;]+)/', $headers, $awsalb_match);
$awsalb = $awsalb_match[1] ?? '';

preg_match('/AWSALBCORS=([^;]+)/', $headers, $awsalbcors_match);
$awsalbcors = $awsalbcors_match[1] ?? '';

preg_match('/\.AspNetCore\.Session=([^;]+)/', $headers, $session_match);
$session = $session_match[1] ?? '';

preg_match('/\.AspNetCore\.Antiforgery\.[^=]+=([^;]+)/', $headers, $antiforgery_match);
$antiforgery = $antiforgery_match[1] ?? '';

preg_match('/<input name="__RequestVerificationToken" type="hidden" value="([^"]+)"/', $body, $token_match);
$request_verification_token = $token_match[1] ?? '';

curl_close($ch);

// STEP 2: First POST request to send OTP
$ch = curl_init();
$post_url = "https://hookstepchallenge.woohoo.in/ClaimReward/SaveData";

$post_data = http_build_query([
    "FIRSTNAME" => "Abhinav",
    "MOBILE" => $mobile,
    "COUPONCODE" => $coupon_code,
    "CHECKBOX1" => "on",
    "OTP" => "",
    "REDEMPTIONTYPE" => "",
    "curPage" => "1",
    "maxPage" => "3",
    "__RequestVerificationToken" => $request_verification_token
]);

$cookies = ".AspNetCore.Session={$session}; .AspNetCore.Antiforgery.nrapuvI9APs={$antiforgery}; AWSALB={$awsalb}; AWSALBCORS={$awsalbcors}";

$post_headers = [
    "user-agent: Mozilla/5.0 (Linux; Android 14; RMX3870) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.200 Mobile Safari/537.36",
    "accept: */*",
    "content-type: application/x-www-form-urlencoded; charset=UTF-8",
    "origin: https://hookstepchallenge.woohoo.in",
    "cookie: $cookies"
];

curl_setopt($ch, CURLOPT_URL, $post_url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_POSTFIELDS, $post_data);
curl_setopt($ch, CURLOPT_HTTPHEADER, $post_headers);
curl_setopt($ch, CURLOPT_ENCODING, "gzip, deflate, br, zstd");

$post_response = curl_exec($ch);
$response_data = json_decode($post_response, true);

if ($response_data['error'] === false && $response_data['sendOTPCount'] > 0) {
    echo "OTP sent successfully.\n";

    echo "Enter the OTP: ";
    $otp = trim(fgets(STDIN));

    // STEP 3: Verify OTP
    $third_post_data = http_build_query([
        "FIRSTNAME" => "Abhinav",
        "MOBILE" => $mobile,
        "COUPONCODE" => $coupon_code,
        "CHECKBOX1" => "on",
        "OTP" => $otp,
        "curPage" => "2",
        "maxPage" => "3",
        "__RequestVerificationToken" => $request_verification_token
    ]);

    curl_setopt($ch, CURLOPT_POSTFIELDS, $third_post_data);
    $third_post_response = curl_exec($ch);
    $third_response_data = json_decode($third_post_response, true);

    if ($third_response_data['error'] === false && $third_response_data['pagno'] === "#Step3") {
        echo "OTP Verified. Proceeding with reward claim...\n";

        // STEP 4: Final request to claim reward
        $fourth_post_data = http_build_query([
            "FIRSTNAME" => "Abhinav",
            "MOBILE" => $mobile,
            "COUPONCODE" => $coupon_code,
            "CHECKBOX1" => "on",
            "OTP" => $otp,
            "REDEMPTIONTYPE" => "57",
            "curPage" => "3",
            "maxPage" => "3",
            "__RequestVerificationToken" => $request_verification_token
        ]);

        curl_setopt($ch, CURLOPT_POSTFIELDS, $fourth_post_data);
        $fourth_post_response = curl_exec($ch);
        $fourth_response_data = json_decode($fourth_post_response, true);

        if ($fourth_response_data['error'] === false) {
            echo "Reward claimed successfully.\n";
        } else {
            echo "Error in claiming reward: " . ($fourth_response_data['messageBody'] ?? "Unknown error.") . "\n";
        }
    } else {
        echo "Error in verify OTP: " . ($third_response_data['messageBody'] ?? "Please try again.") . "\n";
    }
} else {
    echo "Failed to send OTP: " . ($response_data['messageBody'] ?? "Please check your details.") . "\n";
}

curl_close($ch);
?>
