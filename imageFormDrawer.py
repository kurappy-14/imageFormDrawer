from PIL import Image, ImageDraw, ImageFont

class FormDrawer:
    def __init__(self, font_path):
        """
        フォントパスのみを初期化時に受け取る
        """
        self.font_path = font_path
        self._font_cache = {} # フォント読み込みのオーバーヘッドを減らすためのキャッシュ

    def _get_font(self, size):
        """指定サイズのフォントオブジェクトを返す（キャッシュ機能付き）"""
        if size not in self._font_cache:
            try:
                self._font_cache[size] = ImageFont.truetype(self.font_path, size)
            except IOError:
                self._font_cache[size] = ImageFont.load_default()
        return self._font_cache[size]

    def draw(self, image: Image.Image, data: dict, positions: dict, circles: dict):
        """
        引数で受け取った image オブジェクトに直接書き込みを行う
        """
        draw = ImageDraw.Draw(image) # 画像からDrawオブジェクトを生成

        # デフォルトの区分を取得
        iki_type = data.get("行き_区分", "b")
        kaeri_type = data.get("帰り_区分", "b")

        # --- 1. 文字の描画 ---
        for key, value in data.items():
            draw_key = key
            
            # キーの動的変換ロジック
            if key in ["行き_時間", "行き_分"]:
                draw_key = key.replace("行き_", f"行き{iki_type}_")
            elif key in ["帰り_時間", "帰り_分"]:
                draw_key = key.replace("帰り_", f"帰り{kaeri_type}_")
            elif key in ["行き_区分", "帰り_区分"]:
                continue

            # 描画実行
            if draw_key in positions:
                x, y, size = positions[draw_key]
                draw.text((x, y), str(value), font=self._get_font(size), fill=(0, 0, 0))

        # --- 2. チェックマークの描画 ---
        for key, coords in circles.items():
            if len(coords) != 3:
                continue
            cx, cy, r = coords
            
            is_valid = False
            
            # チェックマーク判定ロジック
            if key.startswith("行き") and len(key) == 3:
                if key[-1] == iki_type: is_valid = True
            elif key.startswith("帰り") and len(key) == 3:
                if key[-1] == kaeri_type: is_valid = True
            elif key.startswith("科目"):
                subject_key = key + "_科目名"
                if data.get(subject_key, "").strip(): is_valid = True
                
            if is_valid:
                draw.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(0, 0, 0), fill=None)
        
        # 変更された画像オブジェクトを返す（メソッドチェーン用）
        return image
