import json
from PIL import Image
from imageFormDrawer import FormDrawer # 作成したモジュール

# --- 設定 ---
IMAGE_PATH = 'image/A4.jpg'
OUTPUT_PATH = 'image/記入済_完全版.jpg'
FONT_PATH = "fonts/ipaexg.ttf"

# データファイルのパス設定
JSON_FILES = {
    'data': 'json/data_dual-out.json',
    'image_positions': 'json/image_positions-out.json',
    'circ_positions': 'json/circles_positions-out.json',
}

def load_json(path):
    """JSON読み込みヘルパー"""
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    try:
        # 1. 必要なデータをすべて辞書としてメモリにロード
        print("設定データを読み込み中...")
        dual_data = load_json(JSON_FILES['data'])
        image_positions = load_json(JSON_FILES['image_positions'])
        circ_positions = load_json(JSON_FILES['circ_positions'])

        # 2. 画像を開く (Imageオブジェクトの生成)
        print(f"画像 '{IMAGE_PATH}' を開いています...")
        img = Image.open(IMAGE_PATH)

        # 3. 描画処理 (モジュールの使用)
        # インスタンス化
        drawer = FormDrawer(FONT_PATH)

        # 画像オブジェクトを渡して描画させる
        # 左側のフォームを描画
        drawer.draw(img, dual_data["data_left"], image_positions["left"], circ_positions["left"])
        
        # 同じ画像オブジェクトを引き続き渡して、右側のフォームを描画
        drawer.draw(img, dual_data["data_right"], image_positions["right"], circ_positions["right"])

        # 4. 保存
        img.save(OUTPUT_PATH)
        print(f"完了: '{OUTPUT_PATH}' に保存しました。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()
