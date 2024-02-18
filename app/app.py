from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

from flask import jsonify

@app.route('/email/<user_email>', methods=['GET'])
def get_user_id_by_email(user_email):
    api_url = "https://b-graph.facebook.com/recover_accounts"
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': '[FBAN/FB4A;FBAV/417.0.0.33.65;FBBV/480086274;FBDM/{density=1.5,width=1280,height=720};FBLC/vi_VN;FBRV/0;FBCR/Vinaphone;FBMF/Asus;FBBD/Asus;FBPN/com.facebook.katana;FBDV/ASUS_Z01QD;FBSV/9;FBOP/1;FBCA/x86:armeabi-v7a;]'
    }
    data = {
        'q': user_email,
        'friend_name': '',
        'qs': '',
        'summary': 'true',
        'device_id': '2d38ee8f-44eb-4aff-bf3c-a1c725538cce',
        'src': 'fb4a_account_recovery',
        'machine_id': '',
        'sfdid': '7cc4e1e3-3f4e-46a8-9e24-80d46f24d334',
        'fdid': '2d38ee8f-44eb-4aff-bf3c-a1c725538cce',
        'sim_serials': '%5B%5D',
        'sms_retriever': 'false',
        'cds_experiment_group': '-1',
        'oe_aa_experiment_group': '-1',
        'oe_aa_experiment_group_immediate_exposure': '-1',
        'shared_phone_test_group': '',
        'allowlist_email_exp_name': '',
        'shared_phone_exp_name': '',
        'shared_phone_cp_nonce_code': '',
        'shared_phone_number': '',
        'is_auto_search': 'false',
        'is_feo2_api_level_enabled': 'false',
        'is_sso_like_oauth_search': 'false',
        'encrypted_msisdn': '',
        'locale': 'vi_VN',
        'client_country_code': 'VN',
        'method': 'GET',
        'fb_api_req_friendly_name': 'accountRecoverySearch',
        'fb_api_caller_class': 'AccountSearchHelper',
        'access_token': '350685531728%7C62f8ce9f74b12f84c123cc23437a4a32',
    }
    response = requests.get(api_url, headers=headers, params=data)
    user_data = response.json()
    
    # Lấy danh sách các tài khoản có thể phục hồi
    accounts = user_data.get("data", [])

    # Kiểm tra nếu danh sách tài khoản rỗng
    if not accounts:
        return jsonify({
            "data": [],
            "status": "Email không liên kết với bất kỳ tài khoản Facebook nào",
            "summary": {
                "is_shared_phone_no_signal": False,
                "total_count": 0
            }
        })

    # Lưu trữ thông tin tài khoản mà bạn muốn giữ lại
    transformed_accounts = []

    # Lặp qua từng tài khoản và thực hiện biến đổi
    for account in accounts:
        transformed_account = {}
        transformed_account["code"] = account.get("shared_phone_nonce_length", 8)
        transformed_account["name"] = account.get("first_name", "")
        transformed_account["profile_pic_url"] = account.get("profile_pic_uri", "")
        
        # Lấy thông tin liên hệ (email hoặc số điện thoại)
        contactpoints = account.get("contactpoints", {}).get("data", [])
        for contactpoint in contactpoints:
            if contactpoint["type"] == "EMAIL":
                transformed_account["email"] = contactpoint["display"]
            elif contactpoint["type"] == "PHONE":
                transformed_account["phone"] = contactpoint["display"]
        
        transformed_accounts.append(transformed_account)
    
    return jsonify({
        "data": transformed_accounts,
        "status": "Email có liên kết với một tài khoản Facebook",
    })


@app.route('/email/<email>', methods=['GET'])
def get_user_id_by_email_api(email):
    try:
        user_id_data = get_user_id_by_email(email)
        return jsonify(user_id_data)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'User information not found.'}), 404

if __name__ == '__main__':
    app.run(debug=True)
