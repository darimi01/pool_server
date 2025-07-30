from flask import Flask, request, jsonify
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 이미지 저장 폴더
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    # 1. 파일과 json 파라미터 받기
    image = request.files.get('image')
    json_data = request.form.get('json')  # 문자열로 온 JSON

    if not image or not json_data:
        return jsonify({'error': 'Image or JSON missing'}), 400

    try:
        # 2. JSON 파싱
        parsed_json = json.loads(json_data)
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON format'}), 400

    # 3. 이미지 저장
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = secure_filename(f"{timestamp}.jpg")
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    image.save(filepath)

    # 4. 로그 출력
    print("\n[📸 이미지 저장 완료]")
    print(f" → 경로: {filepath}")

    print("\n[⚠️ 위험 데이터 수신]")
    print(f" → 내용: {json.dumps(parsed_json, indent=2)}")

    # 5. 응답
    return jsonify({'status': 'received', 'filename': filename}), 200

if __name__ == '__main__':
    # 외부 접속 가능하도록 0.0.0.0 사용
    app.run(host='0.0.0.0', port=5000, debug=True)
